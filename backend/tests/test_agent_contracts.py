from datetime import UTC, datetime, timedelta
import unittest

from pydantic import ValidationError

from agent_sdk.contracts import (
    AgentCapability,
    AgentManifest,
    AgentResult,
    AgentTask,
    AuthorizationContext,
    CriterionResult,
    CriterionStatus,
    ExpectedOutput,
    ResultStatus,
    RuntimeStatus,
)


NOW = datetime.now(UTC)


def make_task(**overrides: object) -> AgentTask:
    data = {
        "request_id": "request-1",
        "session_id": "session-1",
        "workflow_id": "workflow-1",
        "plan_version": 1,
        "assignment_id": "assignment-1",
        "correlation_id": "correlation-1",
        "agent_id": "hermes",
        "agent_version": "1.0.0",
        "objective": "Analyze the supplied sources.",
        "reason_for_selection": "Hermes provides source analysis.",
        "requested_actions": ("source_analysis",),
        "authorization": AuthorizationContext(
            wfg_active=False,
            released_request_id="request-1",
            authorized_at=NOW,
        ),
        "expected_output": ExpectedOutput(output_type="analysis"),
        "acceptance_criteria": ("Material claims reference evidence.",),
        "termination_conditions": ("Stop if authorization becomes invalid.",),
        "issued_at": NOW,
    }
    data.update(overrides)
    return AgentTask.model_validate(data)


class AgentContractTests(unittest.TestCase):
    def test_manifest_requires_current_contract(self) -> None:
        manifest = AgentManifest(
            agent_id="hermes",
            agent_version="1.0.0",
            display_name="Hermes",
            role="Information Intelligence Agent",
            description="Transforms mixed information into structured intelligence.",
            capabilities=(
                AgentCapability(
                    capability_id="source_analysis",
                    purpose="Compare and synthesize sources.",
                    output_type="analysis",
                ),
            ),
            boundaries=("Must not bypass ForgeMaster.",),
            supported_contract_versions=("1.00",),
            runtime_status=RuntimeStatus.OPERATIONAL,
        )
        self.assertEqual(manifest.agent_id, "hermes")

    def test_task_rejects_active_wfg(self) -> None:
        with self.assertRaisesRegex(ValidationError, "WFG is active"):
            make_task(
                authorization=AuthorizationContext(
                    wfg_active=True,
                    released_request_id="request-1",
                    authorized_at=NOW,
                )
            )

    def test_task_rejects_go_for_another_request(self) -> None:
        with self.assertRaisesRegex(ValidationError, "does not match"):
            make_task(
                authorization=AuthorizationContext(
                    wfg_active=False,
                    released_request_id="request-2",
                    authorized_at=NOW,
                )
            )

    def test_task_rejects_past_deadline(self) -> None:
        with self.assertRaisesRegex(ValidationError, "later than issued_at"):
            make_task(deadline=NOW - timedelta(seconds=1))

    def test_verified_result_requires_validation(self) -> None:
        with self.assertRaisesRegex(ValidationError, "requires validation evidence"):
            AgentResult(
                request_id="request-1",
                session_id="session-1",
                workflow_id="workflow-1",
                plan_version=1,
                assignment_id="assignment-1",
                correlation_id="correlation-1",
                agent_id="hermes",
                agent_version="1.0.0",
                status=ResultStatus.COMPLETED_VERIFIED,
                summary="Analysis completed.",
                acceptance_criteria_status=(
                    CriterionResult(
                        criterion="Material claims reference evidence.",
                        status=CriterionStatus.PASS,
                    ),
                ),
                completed_at=NOW,
            )

    def test_valid_verified_result(self) -> None:
        result = AgentResult(
            request_id="request-1",
            session_id="session-1",
            workflow_id="workflow-1",
            plan_version=1,
            assignment_id="assignment-1",
            correlation_id="correlation-1",
            agent_id="hermes",
            agent_version="1.0.0",
            status=ResultStatus.COMPLETED_VERIFIED,
            summary="Analysis completed.",
            validation_performed=("Evidence references checked.",),
            acceptance_criteria_status=(
                CriterionResult(
                    criterion="Material claims reference evidence.",
                    status=CriterionStatus.PASS,
                    evidence_references=("source-1",),
                ),
            ),
            completed_at=NOW,
        )
        self.assertEqual(result.status, ResultStatus.COMPLETED_VERIFIED)


if __name__ == "__main__":
    unittest.main()
