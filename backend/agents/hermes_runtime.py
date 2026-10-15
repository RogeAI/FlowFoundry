"""Hermes runtime adapter from AgentTask to validated AgentResult."""

from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Protocol
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from pydantic import BaseModel, ConfigDict, Field

from agent_sdk.contracts import (
    AgentResult,
    AgentTask,
    CriterionResult,
    CriterionStatus,
    PermissionOperation,
    ResultStatus,
    SourceReference,
)
from agents.hermes import build_hermes_manifest


class HermesRuntimeError(RuntimeError):
    """Safe runtime failure that should return to ForgeMaster."""


class HermesSource(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_id: str
    source_type: str
    content: str = Field(min_length=1)


class HermesModelRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    objective: str
    requested_actions: tuple[str, ...]
    system_instructions: str
    skill_instructions: tuple[str, ...]
    sources: tuple[HermesSource, ...]
    acceptance_criteria: tuple[str, ...]


class HermesModelOutput(BaseModel):
    """Structured specialist output returned by a configured model gateway."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    summary: str = Field(min_length=1)
    findings: tuple[dict[str, Any], ...] = ()
    evidence_references: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    unresolved_questions: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    recommended_follow_up: tuple[str, ...] = ()
    supported_acceptance_criteria: tuple[str, ...] = ()


class HermesModelGateway(Protocol):
    def analyze(self, request: HermesModelRequest) -> HermesModelOutput:
        """Analyze authorized task data and return structured Hermes output."""


class LocalSourceReader:
    """Read authorized local text and DOCX sources with optional SHA-256 verification."""

    _DOCX_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    def read(self, reference: SourceReference) -> HermesSource:
        if not reference.location:
            raise HermesRuntimeError(f"Source {reference.source_id} has no readable location")

        path = Path(reference.location).resolve(strict=True)
        raw = path.read_bytes()
        self._verify_hash(reference.source_id, raw)

        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".csv", ".json", ".xml", ".html"}:
            content = raw.decode("utf-8-sig")
        elif suffix == ".docx":
            content = self._read_docx(path)
        else:
            raise HermesRuntimeError(f"Unsupported source type: {suffix or 'unknown'}")

        if not content.strip():
            raise HermesRuntimeError(f"Source {reference.source_id} contains no readable text")
        return HermesSource(
            source_id=reference.source_id,
            source_type=reference.source_type,
            content=content.strip(),
        )

    def _verify_hash(self, source_id: str, raw: bytes) -> None:
        prefix = "sha256:"
        if not source_id.lower().startswith(prefix):
            return
        expected = source_id[len(prefix):].lower()
        actual = sha256(raw).hexdigest()
        if actual != expected:
            raise HermesRuntimeError("Source hash does not match the authorized reference")

    def _read_docx(self, path: Path) -> str:
        try:
            with ZipFile(path) as archive:
                root = ElementTree.fromstring(archive.read("word/document.xml"))
        except (BadZipFile, KeyError, ElementTree.ParseError) as exc:
            raise HermesRuntimeError("DOCX source could not be parsed safely") from exc

        namespace = {"w": self._DOCX_NAMESPACE}
        paragraphs: list[str] = []
        for paragraph in root.findall(".//w:body//w:p", namespace):
            text = "".join(
                node.text or "" for node in paragraph.findall(".//w:t", namespace)
            ).strip()
            if text:
                paragraphs.append(text)
        return "\n".join(paragraphs)


class HermesInstructionLoader:
    """Load persistent Hermes governance and only the selected skills."""

    _SKILL_PATHS = {
        "information_intelligence": "information-intelligence/SKILL.md",
        "source_analysis": "source-analysis/SKILL.md",
        "quality_assessment": "quality-assessment/SKILL.md",
        "recommendations_actions": "recommendations-actions/SKILL.md",
        "testability_analysis": "testability-analysis/SKILL.md",
        "test_design_handover": "test-design-handover/SKILL.md",
    }

    def __init__(self, agent_root: Path | None = None) -> None:
        repository_root = Path(__file__).resolve().parents[2]
        self._agent_root = agent_root or repository_root / "Solutions" / "Hermes" / "Agent"

    def load(self, capability_ids: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
        primary = self._read(self._agent_root / "AGENT.md")
        governance = [
            self._read(path)
            for path in sorted((self._agent_root / "Instructions").glob("*.md"))
        ]
        system_instructions = "\n\n".join((primary, *governance))

        skills = tuple(
            self._read(self._agent_root / "Skills" / self._SKILL_PATHS[capability_id])
            for capability_id in capability_ids
        )
        return system_instructions, skills

    def _read(self, path: Path) -> str:
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise HermesRuntimeError(f"Required Hermes instruction is unavailable: {path.name}") from exc
        if not content.strip():
            raise HermesRuntimeError(f"Required Hermes instruction is empty: {path.name}")
        return content.strip()


class HermesRuntime:
    """Validate, execute, and translate one bounded Hermes assignment."""

    def __init__(
        self,
        model_gateway: HermesModelGateway,
        source_reader: LocalSourceReader | None = None,
        instruction_loader: HermesInstructionLoader | None = None,
    ) -> None:
        self._model_gateway = model_gateway
        self._source_reader = source_reader or LocalSourceReader()
        self._instruction_loader = instruction_loader or HermesInstructionLoader()
        self._manifest = build_hermes_manifest()

    def execute(self, task: AgentTask) -> AgentResult:
        capabilities = self._resolve_capabilities(task)
        self._validate_identity(task)
        self._validate_source_permissions(task)

        system_instructions, skill_instructions = self._instruction_loader.load(capabilities)
        sources = tuple(self._source_reader.read(reference) for reference in task.source_references)
        if not sources:
            raise HermesRuntimeError("Hermes requires at least one authorized source")

        model_request = HermesModelRequest(
            objective=task.objective,
            requested_actions=task.requested_actions,
            system_instructions=system_instructions,
            skill_instructions=skill_instructions,
            sources=sources,
            acceptance_criteria=task.acceptance_criteria,
        )
        output = self._model_gateway.analyze(model_request)
        return self._build_result(task, output)

    def _validate_identity(self, task: AgentTask) -> None:
        if task.agent_id != self._manifest.agent_id:
            raise HermesRuntimeError("Assignment identity does not target Hermes")
        if task.agent_version != self._manifest.agent_version:
            raise HermesRuntimeError("Assignment requires an incompatible Hermes version")
        if task.contract_version not in self._manifest.supported_contract_versions:
            raise HermesRuntimeError("Assignment contract version is not supported by Hermes")

    def _resolve_capabilities(self, task: AgentTask) -> tuple[str, ...]:
        by_id = {capability.capability_id: capability for capability in self._manifest.capabilities}
        by_action = {
            action: capability
            for capability in self._manifest.capabilities
            for action in capability.supported_actions
        }
        selected = []
        for action in task.requested_actions:
            capability = by_id.get(action) or by_action.get(action)
            if capability is None:
                raise HermesRuntimeError(f"Hermes does not support requested action: {action}")
            if capability.capability_id not in selected:
                selected.append(capability.capability_id)

        explicit = set(task.context.get("explicit_capability_activations", ()))
        for capability_id in selected:
            capability = by_id[capability_id]
            if capability.explicit_user_activation_required and capability_id not in explicit:
                raise HermesRuntimeError(
                    f"Capability requires explicit user activation: {capability_id}"
                )
        return tuple(selected)

    def _validate_source_permissions(self, task: AgentTask) -> None:
        readable_targets = {
            grant.target
            for grant in task.permissions
            if grant.operation == PermissionOperation.READ
            and (grant.expires_at is None or grant.expires_at > datetime.now(UTC))
        }
        for source in task.source_references:
            if source.source_id not in readable_targets:
                raise HermesRuntimeError(
                    f"No active read permission for source {source.source_id}"
                )

    def _build_result(self, task: AgentTask, output: HermesModelOutput) -> AgentResult:
        supported = set(output.supported_acceptance_criteria)
        criteria = tuple(
            CriterionResult(
                criterion=criterion,
                status=(
                    CriterionStatus.PASS
                    if criterion in supported and output.evidence_references
                    else CriterionStatus.UNVERIFIED
                ),
                evidence_references=output.evidence_references,
            )
            for criterion in task.acceptance_criteria
        )
        all_verified = bool(criteria) and all(
            item.status == CriterionStatus.PASS for item in criteria
        )
        status = (
            ResultStatus.COMPLETED_VERIFIED
            if all_verified
            else ResultStatus.COMPLETED_UNVERIFIED
        )

        return AgentResult(
            request_id=task.request_id,
            session_id=task.session_id,
            workflow_id=task.workflow_id,
            plan_version=task.plan_version,
            assignment_id=task.assignment_id,
            correlation_id=task.correlation_id,
            agent_id=task.agent_id,
            agent_version=task.agent_version,
            status=status,
            summary=output.summary,
            findings=output.findings,
            evidence_references=output.evidence_references,
            validation_performed=(
                "Hermes model output matched the structured runtime schema.",
                "Acceptance-criterion evidence references were checked by the runtime.",
            ),
            acceptance_criteria_status=criteria,
            assumptions=output.assumptions,
            limitations=output.limitations,
            unresolved_questions=output.unresolved_questions,
            risks=output.risks,
            recommended_follow_up=output.recommended_follow_up,
            completed_at=datetime.now(UTC),
        )
