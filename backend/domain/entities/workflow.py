from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4


class WorkflowType(str, Enum):
    FORGEMASTER_ONLY = "ForgeMasterOnly"
    SINGLE_AGENT = "SingleAgent"
    CHAINED = "Chained"
    PARALLEL = "Parallel"
    MIXED = "Mixed"


class WorkflowStatus(str, Enum):
    PLANNING = "Planning"
    READY = "Ready"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"


@dataclass
class WorkflowStep:
    agent_id: Optional[str]
    description: str
    depends_on: list[str] = field(default_factory=list)


@dataclass
class WorkflowPlan:
    id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    workflow_type: WorkflowType = WorkflowType.FORGEMASTER_ONLY
    status: WorkflowStatus = WorkflowStatus.PLANNING
    steps: list[WorkflowStep] = field(default_factory=list)
    forgemaster_summary: str = ""
    clarification_needed: bool = False
    clarification_question: Optional[str] = None
