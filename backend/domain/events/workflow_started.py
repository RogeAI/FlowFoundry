from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowStarted:
    session_id: str
    workflow_plan_id: str
    workflow_type: str
