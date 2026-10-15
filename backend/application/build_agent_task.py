from datetime import UTC, datetime
from uuid import uuid4

from agent_sdk.contracts import (
    AgentTask,
    AuthorizationContext,
    ExpectedOutput,
    PermissionGrant,
    PermissionOperation,
    SourceReference,
)
from domain.entities.session import Session
from domain.entities.workflow import WorkflowPlan, WorkflowStatus, WorkflowStep
from domain.repositories.agent_repository import AgentRepository
from domain.repositories.source_repository import SourceRepository


class BuildAgentTask:
    """ForgeMaster boundary that turns one approved plan step into Agent contract v1.00."""

    _ACTION_MAP = {
        "summarize": "summarize",
        "review_requirements": "assess_information_quality",
        "identify_gaps": "assess_information_quality",
        "compare_documents": "compare_sources",
    }

    def __init__(
        self,
        agent_repo: AgentRepository,
        source_repo: SourceRepository,
    ) -> None:
        self._agents = agent_repo
        self._sources = source_repo

    def execute(
        self,
        session: Session,
        plan: WorkflowPlan,
        step: WorkflowStep,
    ) -> AgentTask:
        if session.wfg.active:
            raise ValueError("Cannot build an Agent task while WFG is active")
        if plan.session_id != session.id or plan.status != WorkflowStatus.READY:
            raise ValueError("Workflow plan is not ready for this session")
        if plan.clarification_needed:
            raise ValueError("Workflow requires clarification before specialist dispatch")
        if not step.agent_id:
            raise ValueError("Workflow step does not assign a specialist")

        manifest = self._agents.get_manifest(step.agent_id)
        if manifest is None:
            raise ValueError("Workflow step does not reference a registered specialist")
        sources = self._sources.list_for_session(session.id)
        if not sources:
            raise ValueError("Specialist assignment requires at least one session source")

        supported = {
            action
            for capability in manifest.capabilities
            for action in (capability.capability_id, *capability.supported_actions)
        }
        requested = []
        for action in session.selected_actions:
            normalized = action.label.strip().lower().replace(" ", "_")
            candidate = self._ACTION_MAP.get(normalized, normalized)
            if candidate in supported and candidate not in requested:
                requested.append(candidate)
        if not requested:
            requested.append(manifest.capabilities[0].capability_id)

        selected_capabilities = tuple(
            capability
            for capability in manifest.capabilities
            if capability.capability_id in requested
            or any(action in requested for action in capability.supported_actions)
        )
        explicit_activations = tuple(
            capability.capability_id
            for capability in selected_capabilities
            if capability.explicit_user_activation_required
        )

        now = datetime.now(UTC)
        request_id = plan.id
        source_references = tuple(
            SourceReference(
                source_id=source.source_id,
                source_type=source.source_type,
                location=source.location,
            )
            for source in sources
        )
        permissions = tuple(
            PermissionGrant(
                operation=PermissionOperation.READ,
                target=source.source_id,
                purpose="Read this session-isolated source for the assigned workflow step.",
            )
            for source in sources
        )
        return AgentTask(
            request_id=request_id,
            session_id=session.id,
            workflow_id=plan.id,
            plan_version=1,
            assignment_id=str(uuid4()),
            correlation_id=str(uuid4()),
            agent_id=manifest.agent_id,
            agent_version=manifest.agent_version,
            objective=session.prompt or step.description,
            reason_for_selection=step.description,
            requested_actions=tuple(requested),
            context={
                "source_filenames": tuple(source.original_filename for source in sources),
                "explicit_capability_activations": explicit_activations,
            },
            source_references=source_references,
            authorization=AuthorizationContext(
                wfg_active=False,
                released_request_id=request_id,
                authorized_at=now,
            ),
            permissions=permissions,
            prohibited_actions=(
                "Access sources outside this session assignment.",
                "Delegate directly to another Agent.",
                "Change WFG, approval, or workflow state.",
            ),
            expected_output=ExpectedOutput(output_type=selected_capabilities[0].output_type),
            acceptance_criteria=(
                "Material findings reference the supplied source.",
                "Unknowns and unsupported assumptions are identified explicitly.",
            ),
            escalation_triggers=manifest.escalation_types,
            termination_conditions=(
                "Stop if source authorization or assignment identity is invalid.",
                "Return safely to ForgeMaster if required evidence cannot be read.",
            ),
            issued_at=now,
        )
