"""Pydantic models for the FlowFoundry specialist Agent contract v1.00."""

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


CONTRACT_VERSION = "1.00"


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class RuntimeStatus(str, Enum):
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"


class AssignmentState(str, Enum):
    ACCEPTED = "accepted"
    WORKING = "working"
    WAITING_DEPENDENCY = "waiting_dependency"
    CLARIFICATION_REQUIRED = "clarification_required"
    APPROVAL_REQUIRED = "approval_required"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class ResultStatus(str, Enum):
    COMPLETED_VERIFIED = "completed_verified"
    COMPLETED_UNVERIFIED = "completed_unverified"
    PARTIAL = "partial"
    BLOCKED = "blocked"
    FAILED = "failed"
    NOT_ATTEMPTED = "not_attempted"
    STOPPED = "stopped"


class CriterionStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    UNVERIFIED = "unverified"


class PermissionOperation(str, Enum):
    DISCOVER = "discover"
    READ = "read"
    SEARCH = "search"
    CREATE = "create"
    UPDATE = "update"
    EXECUTE = "execute"
    APPROVE = "approve"
    PUBLISH = "publish"
    SHARE = "share"
    MOVE = "move"
    DELETE = "delete"
    ADMINISTER = "administer"


class EscalationType(str, Enum):
    CAPABILITY_MISMATCH = "capability_mismatch"
    MISSING_INFORMATION = "missing_information"
    PERMISSION_REQUIRED = "permission_required"
    TOOL_UNAVAILABLE = "tool_unavailable"
    DEPENDENCY_FAILURE = "dependency_failure"
    SOURCE_CONFLICT = "source_conflict"
    SCOPE_CHANGE = "scope_change"
    SECURITY_OR_PRIVACY_RISK = "security_or_privacy_risk"
    QUALITY_GATE_FAILURE = "quality_gate_failure"
    ADDITIONAL_AGENT_RECOMMENDED = "additional_agent_recommended"
    RUNTIME_FAILURE = "runtime_failure"
    UNCERTAIN_EXTERNAL_OUTCOME = "uncertain_external_outcome"


class AgentErrorCategory(str, Enum):
    CONTRACT_VERSION_UNSUPPORTED = "contract_version_unsupported"
    SCHEMA_VALIDATION_FAILED = "schema_validation_failed"
    IDENTITY_MISMATCH = "identity_mismatch"
    AUTHORIZATION_INVALID = "authorization_invalid"
    PERMISSION_DENIED = "permission_denied"
    INVALID_STATE_TRANSITION = "invalid_state_transition"
    CONTEXT_UNAVAILABLE = "context_unavailable"
    TOOL_ERROR = "tool_error"
    TIMEOUT = "timeout"
    RUNTIME_ERROR = "runtime_error"
    SAFE_FAILURE = "safe_failure"


class AgentCapability(ContractModel):
    capability_id: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    supported_actions: tuple[str, ...] = ()
    required_inputs: tuple[str, ...] = ()
    output_type: str = Field(min_length=1)
    prerequisites: tuple[str, ...] = ()
    required_tools: tuple[str, ...] = ()
    required_permissions: tuple[PermissionOperation, ...] = ()
    limitations: tuple[str, ...] = ()
    explicit_user_activation_required: bool = False


class AgentManifest(ContractModel):
    agent_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    agent_version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    display_name: str = Field(min_length=1)
    role: str = Field(min_length=1)
    agent_class: Literal["specialist"] = "specialist"
    description: str = Field(min_length=1)
    capabilities: tuple[AgentCapability, ...] = Field(min_length=1)
    boundaries: tuple[str, ...] = Field(min_length=1)
    supported_contract_versions: tuple[str, ...] = Field(min_length=1)
    required_tools: tuple[str, ...] = ()
    optional_tools: tuple[str, ...] = ()
    required_permissions: tuple[PermissionOperation, ...] = ()
    escalation_types: tuple[EscalationType, ...] = ()
    runtime_status: RuntimeStatus

    @model_validator(mode="after")
    def validate_manifest(self) -> "AgentManifest":
        if CONTRACT_VERSION not in self.supported_contract_versions:
            raise ValueError(f"Agent must support contract version {CONTRACT_VERSION}")
        ids = [capability.capability_id for capability in self.capabilities]
        if len(ids) != len(set(ids)):
            raise ValueError("Capability IDs must be unique")
        return self


class AuthorizationContext(ContractModel):
    wfg_active: bool
    released_request_id: str = Field(min_length=1)
    authorized_at: datetime


class PermissionGrant(ContractModel):
    operation: PermissionOperation
    target: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    expires_at: datetime | None = None


class SourceReference(ContractModel):
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    location: str | None = None
    version: str | None = None
    partial: bool = False
    stale: bool = False
    unreadable: bool = False


class ExpectedOutput(ContractModel):
    output_type: str = Field(min_length=1)
    schema_name: str | None = None
    format: str | None = None


class MessageIdentity(ContractModel):
    request_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    workflow_id: str = Field(min_length=1)
    plan_version: int = Field(ge=1)
    assignment_id: str = Field(min_length=1)
    correlation_id: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    agent_version: str = Field(pattern=r"^\d+\.\d+\.\d+$")


class AgentTask(MessageIdentity):
    contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    objective: str = Field(min_length=1)
    reason_for_selection: str = Field(min_length=1)
    requested_actions: tuple[str, ...] = Field(min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)
    source_references: tuple[SourceReference, ...] = ()
    authorization: AuthorizationContext
    permissions: tuple[PermissionGrant, ...] = ()
    prohibited_actions: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    expected_output: ExpectedOutput
    acceptance_criteria: tuple[str, ...] = Field(min_length=1)
    escalation_triggers: tuple[EscalationType, ...] = ()
    termination_conditions: tuple[str, ...] = Field(min_length=1)
    issued_at: datetime
    deadline: datetime | None = None

    @model_validator(mode="after")
    def validate_authorization(self) -> "AgentTask":
        if self.authorization.wfg_active:
            raise ValueError("AgentTask cannot be dispatched while WFG is active")
        if self.authorization.released_request_id != self.request_id:
            raise ValueError("GO authorization does not match the dispatched request")
        if self.deadline is not None and self.deadline <= self.issued_at:
            raise ValueError("Deadline must be later than issued_at")
        return self


class AgentProgress(MessageIdentity):
    contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    previous_state: AssignmentState
    current_state: AssignmentState
    summary: str = Field(min_length=1)
    completed_milestone: str | None = None
    blocker_or_dependency: str | None = None
    next_expected_transition: AssignmentState | None = None
    occurred_at: datetime


class AgentClarification(MessageIdentity):
    contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    question: str = Field(min_length=1)
    why_it_matters: str = Field(min_length=1)
    affected_criterion: str | None = None
    safe_work_that_may_continue: tuple[str, ...] = ()
    suggested_answer_format: str | None = None
    occurred_at: datetime


class AgentEscalation(MessageIdentity):
    contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    escalation_type: EscalationType
    urgency: Literal["low", "medium", "high", "critical"]
    description: str = Field(min_length=1)
    evidence_references: tuple[str, ...] = ()
    work_attempted: tuple[str, ...] = ()
    workflow_impact: str = Field(min_length=1)
    safe_state_reached: str = Field(min_length=1)
    available_options: tuple[str, ...] = ()
    recommended_option: str | None = None
    assistance_required: str = Field(min_length=1)
    occurred_at: datetime


class CriterionResult(ContractModel):
    criterion: str = Field(min_length=1)
    status: CriterionStatus
    evidence_references: tuple[str, ...] = ()
    note: str | None = None


class AgentResult(MessageIdentity):
    contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    status: ResultStatus
    summary: str = Field(min_length=1)
    findings: tuple[dict[str, Any], ...] = ()
    deliverables: tuple[str, ...] = ()
    evidence_references: tuple[str, ...] = ()
    actions_performed: tuple[str, ...] = ()
    validation_performed: tuple[str, ...] = ()
    acceptance_criteria_status: tuple[CriterionResult, ...]
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    unresolved_questions: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    unmet_criteria: tuple[str, ...] = ()
    recommended_follow_up: tuple[str, ...] = ()
    completed_at: datetime

    @model_validator(mode="after")
    def protect_completion_claims(self) -> "AgentResult":
        if self.status == ResultStatus.COMPLETED_VERIFIED:
            if not self.validation_performed:
                raise ValueError("Verified completion requires validation evidence")
            if any(item.status != CriterionStatus.PASS for item in self.acceptance_criteria_status):
                raise ValueError("Verified completion requires every criterion to pass")
        if self.status in {ResultStatus.BLOCKED, ResultStatus.FAILED} and not self.limitations:
            raise ValueError("Blocked or failed results must describe their limitations")
        return self


class AgentError(ContractModel):
    contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    category: AgentErrorCategory
    summary: str = Field(min_length=1)
    technical_reference_id: str = Field(min_length=1)
    retryable: bool
    state_impact: str = Field(min_length=1)
    occurred_at: datetime
