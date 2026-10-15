from typing import Any, Optional
from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: str
    prompt: str
    selected_actions: list[str]
    selected_agent_id: Optional[str]
    wfg_active: bool
    expanded: bool


class SourceResponse(BaseModel):
    source_id: str
    original_filename: str
    source_type: str
    size_bytes: int


class UpdateActionsRequest(BaseModel):
    actions: list[str]


class UpdatePromptRequest(BaseModel):
    prompt: str


class SetWFGRequest(BaseModel):
    active: bool


class SelectAgentRequest(BaseModel):
    agent_id: Optional[str] = None


class WorkflowStepResponse(BaseModel):
    agent_id: Optional[str]
    description: str
    depends_on: list[str]


class WorkflowPlanResponse(BaseModel):
    id: str
    session_id: str
    workflow_type: str
    status: str
    steps: list[WorkflowStepResponse]
    forgemaster_summary: str
    clarification_needed: bool
    clarification_question: Optional[str]
    specialist_result: Optional[dict[str, Any]] = None
    specialist_error: Optional[dict[str, Any]] = None
