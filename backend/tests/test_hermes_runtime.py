from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from agent_sdk.contracts import (
    AgentTask,
    AuthorizationContext,
    ExpectedOutput,
    PermissionGrant,
    PermissionOperation,
    ResultStatus,
    SourceReference,
)
from agents.hermes_runtime import (
    HermesInstructionLoader,
    HermesModelOutput,
    HermesRuntime,
    HermesRuntimeError,
)


class FakeModelGateway:
    def __init__(self, supported_criteria: tuple[str, ...]) -> None:
        self.supported_criteria = supported_criteria
        self.last_request = None

    def analyze(self, request):
        self.last_request = request
        return HermesModelOutput(
            summary="Hermes analyzed the authorized source.",
            findings=({"classification": "verified", "finding": "Login is required."},),
            evidence_references=(request.sources[0].source_id,),
            supported_acceptance_criteria=self.supported_criteria,
        )


class StubInstructionLoader(HermesInstructionLoader):
    def load(self, capability_ids):
        return "Hermes system instructions", tuple(
            f"Skill: {capability_id}" for capability_id in capability_ids
        )


class HermesRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.source_path = Path(self.temp_dir.name) / "requirements.txt"
        self.source_path.write_text("The website requires a login page.", encoding="utf-8")
        digest = sha256(self.source_path.read_bytes()).hexdigest()
        self.source_id = f"sha256:{digest}"
        self.criterion = "Material findings reference the supplied source."

    def make_task(self, **overrides) -> AgentTask:
        now = datetime.now(UTC)
        data = {
            "request_id": "request-1",
            "session_id": "session-1",
            "workflow_id": "workflow-1",
            "plan_version": 1,
            "assignment_id": "assignment-1",
            "correlation_id": "correlation-1",
            "agent_id": "hermes",
            "agent_version": "1.0.0",
            "objective": "Analyze the requirements.",
            "reason_for_selection": "Hermes provides information intelligence.",
            "requested_actions": ("information_intelligence",),
            "source_references": (
                SourceReference(
                    source_id=self.source_id,
                    source_type="text",
                    location=str(self.source_path),
                ),
            ),
            "authorization": AuthorizationContext(
                wfg_active=False,
                released_request_id="request-1",
                authorized_at=now,
            ),
            "permissions": (
                PermissionGrant(
                    operation=PermissionOperation.READ,
                    target=self.source_id,
                    purpose="Analyze the supplied source.",
                ),
            ),
            "expected_output": ExpectedOutput(output_type="analysis"),
            "acceptance_criteria": (self.criterion,),
            "termination_conditions": ("Stop if source authorization is invalid.",),
            "issued_at": now,
        }
        data.update(overrides)
        return AgentTask.model_validate(data)

    def make_runtime(self, supported_criteria=None):
        gateway = FakeModelGateway(supported_criteria or (self.criterion,))
        runtime = HermesRuntime(
            model_gateway=gateway,
            instruction_loader=StubInstructionLoader(),
        )
        return runtime, gateway

    def test_executes_authorized_source_and_returns_verified_result(self) -> None:
        runtime, gateway = self.make_runtime()

        result = runtime.execute(self.make_task())

        self.assertEqual(result.status, ResultStatus.COMPLETED_VERIFIED)
        self.assertEqual(result.evidence_references, (self.source_id,))
        self.assertEqual(gateway.last_request.sources[0].content, "The website requires a login page.")

    def test_rejects_missing_read_permission(self) -> None:
        runtime, _ = self.make_runtime()

        with self.assertRaisesRegex(HermesRuntimeError, "No active read permission"):
            runtime.execute(self.make_task(permissions=()))

    def test_rejects_hash_mismatch(self) -> None:
        runtime, _ = self.make_runtime()
        bad_source = SourceReference(
            source_id="sha256:" + "0" * 64,
            source_type="text",
            location=str(self.source_path),
        )
        permission = PermissionGrant(
            operation=PermissionOperation.READ,
            target=bad_source.source_id,
            purpose="Analyze the supplied source.",
        )

        with self.assertRaisesRegex(HermesRuntimeError, "hash does not match"):
            runtime.execute(
                self.make_task(source_references=(bad_source,), permissions=(permission,))
            )

    def test_testability_requires_explicit_activation(self) -> None:
        runtime, _ = self.make_runtime()

        with self.assertRaisesRegex(HermesRuntimeError, "explicit user activation"):
            runtime.execute(self.make_task(requested_actions=("testability_analysis",)))

    def test_unverified_criteria_cannot_claim_verified_completion(self) -> None:
        runtime, _ = self.make_runtime(supported_criteria=("Different criterion",))

        result = runtime.execute(self.make_task())

        self.assertEqual(result.status, ResultStatus.COMPLETED_UNVERIFIED)


if __name__ == "__main__":
    unittest.main()
