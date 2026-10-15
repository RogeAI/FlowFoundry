from datetime import UTC, datetime
import unittest

from agent_sdk.contracts import (
    AgentErrorCategory,
    AgentResult,
    AgentTask,
    AuthorizationContext,
    CriterionResult,
    CriterionStatus,
    ExpectedOutput,
    ResultStatus,
)
from application.dispatch_specialist import DispatchSpecialist
from infrastructure.repositories.memory_agent_repository import MemoryAgentRepository
from infrastructure.runtime_registry import MemorySpecialistRuntimeRegistry


class FakeRuntime:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def execute(self, task):
        self.calls.append(task)
        if self.error:
            raise self.error
        return self.result


class SpecialistDispatchTests(unittest.TestCase):
    def make_task(self, **overrides):
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
            "objective": "Analyze the source.",
            "reason_for_selection": "Hermes owns information intelligence.",
            "requested_actions": ("information_intelligence",),
            "authorization": AuthorizationContext(
                wfg_active=False,
                released_request_id="request-1",
                authorized_at=now,
            ),
            "expected_output": ExpectedOutput(output_type="analysis"),
            "acceptance_criteria": ("Return a grounded analysis.",),
            "termination_conditions": ("Stop on invalid authority.",),
            "issued_at": now,
        }
        data.update(overrides)
        return AgentTask.model_validate(data)

    def make_result(self, task, **overrides):
        data = {
            "request_id": task.request_id,
            "session_id": task.session_id,
            "workflow_id": task.workflow_id,
            "plan_version": task.plan_version,
            "assignment_id": task.assignment_id,
            "correlation_id": task.correlation_id,
            "agent_id": task.agent_id,
            "agent_version": task.agent_version,
            "status": ResultStatus.COMPLETED_VERIFIED,
            "summary": "Analysis completed.",
            "validation_performed": ("Evidence checked.",),
            "acceptance_criteria_status": (
                CriterionResult(
                    criterion="Return a grounded analysis.",
                    status=CriterionStatus.PASS,
                    evidence_references=("source-1",),
                ),
            ),
            "completed_at": datetime.now(UTC),
        }
        data.update(overrides)
        return AgentResult.model_validate(data)

    def test_dispatches_registered_available_hermes_runtime(self):
        task = self.make_task()
        runtime = FakeRuntime(result=self.make_result(task))
        dispatcher = DispatchSpecialist(
            MemoryAgentRepository(),
            MemorySpecialistRuntimeRegistry({"hermes": runtime}),
        )

        outcome = dispatcher.execute(task)

        self.assertTrue(outcome.succeeded)
        self.assertEqual(outcome.result.assignment_id, task.assignment_id)
        self.assertEqual(runtime.calls, [task])

    def test_rejects_unregistered_agent(self):
        task = self.make_task(agent_id="unknown")
        dispatcher = DispatchSpecialist(
            MemoryAgentRepository(), MemorySpecialistRuntimeRegistry({})
        )

        outcome = dispatcher.execute(task)

        self.assertEqual(outcome.error.category, AgentErrorCategory.IDENTITY_MISMATCH)

    def test_rejects_missing_runtime(self):
        task = self.make_task()
        dispatcher = DispatchSpecialist(
            MemoryAgentRepository(), MemorySpecialistRuntimeRegistry({"other": FakeRuntime()})
        )

        outcome = dispatcher.execute(task)

        self.assertEqual(outcome.error.category, AgentErrorCategory.RUNTIME_ERROR)

    def test_runtime_failure_is_returned_as_safe_error(self):
        task = self.make_task()
        runtime = FakeRuntime(error=RuntimeError("secret provider detail"))
        dispatcher = DispatchSpecialist(
            MemoryAgentRepository(),
            MemorySpecialistRuntimeRegistry({"hermes": runtime}),
        )

        outcome = dispatcher.execute(task)

        self.assertEqual(outcome.error.category, AgentErrorCategory.SAFE_FAILURE)
        self.assertNotIn("secret provider detail", outcome.error.summary)

    def test_rejects_mismatched_result_identity(self):
        task = self.make_task()
        runtime = FakeRuntime(
            result=self.make_result(task, assignment_id="different-assignment")
        )
        dispatcher = DispatchSpecialist(
            MemoryAgentRepository(),
            MemorySpecialistRuntimeRegistry({"hermes": runtime}),
        )

        outcome = dispatcher.execute(task)

        self.assertEqual(outcome.error.category, AgentErrorCategory.IDENTITY_MISMATCH)


if __name__ == "__main__":
    unittest.main()
