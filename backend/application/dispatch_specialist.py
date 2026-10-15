"""ForgeMaster-controlled dispatch of validated tasks to specialist runtimes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from agent_sdk.contracts import (
    AgentError,
    AgentErrorCategory,
    AgentResult,
    AgentTask,
)
from domain.repositories.agent_repository import AgentRepository


class SpecialistRuntime(Protocol):
    def execute(self, task: AgentTask) -> AgentResult:
        """Execute one validated, bounded specialist assignment."""


class SpecialistRuntimeRegistry(Protocol):
    def get(self, agent_id: str) -> SpecialistRuntime | None:
        """Return the registered runtime for an Agent ID."""


@dataclass(frozen=True)
class DispatchOutcome:
    result: AgentResult | None = None
    error: AgentError | None = None

    def __post_init__(self) -> None:
        if (self.result is None) == (self.error is None):
            raise ValueError("DispatchOutcome requires exactly one result or error")

    @property
    def succeeded(self) -> bool:
        return self.result is not None


class DispatchSpecialist:
    """Internal dispatch boundary used by ForgeMaster, never a direct user route."""

    def __init__(
        self,
        agent_repository: AgentRepository,
        runtime_registry: SpecialistRuntimeRegistry,
    ) -> None:
        self._agents = agent_repository
        self._runtimes = runtime_registry

    def execute(self, task: AgentTask) -> DispatchOutcome:
        agent = self._agents.get_by_id(task.agent_id)
        manifest = self._agents.get_manifest(task.agent_id)
        if agent is None or manifest is None:
            return self._error(
                AgentErrorCategory.IDENTITY_MISMATCH,
                "The assigned specialist is not registered.",
                retryable=False,
                state_impact="Assignment was not started.",
            )
        if not agent.is_available():
            return self._error(
                AgentErrorCategory.AUTHORIZATION_INVALID,
                "The assigned specialist is not currently available.",
                retryable=True,
                state_impact="Assignment remains pending for ForgeMaster replanning.",
            )
        if task.agent_version != manifest.agent_version:
            return self._error(
                AgentErrorCategory.IDENTITY_MISMATCH,
                "The assignment requires an incompatible specialist version.",
                retryable=False,
                state_impact="Assignment was not started.",
            )
        if task.contract_version not in manifest.supported_contract_versions:
            return self._error(
                AgentErrorCategory.CONTRACT_VERSION_UNSUPPORTED,
                "The specialist does not support the assignment contract version.",
                retryable=False,
                state_impact="Assignment was not started.",
            )

        runtime = self._runtimes.get(task.agent_id)
        if runtime is None:
            return self._error(
                AgentErrorCategory.RUNTIME_ERROR,
                "No operational runtime is registered for the specialist.",
                retryable=False,
                state_impact="Assignment was not started.",
            )

        try:
            result = runtime.execute(task)
        except Exception:
            return self._error(
                AgentErrorCategory.SAFE_FAILURE,
                "The specialist runtime failed safely.",
                retryable=False,
                state_impact="Assignment requires ForgeMaster review or replanning.",
            )

        if result.assignment_id != task.assignment_id or result.agent_id != task.agent_id:
            return self._error(
                AgentErrorCategory.IDENTITY_MISMATCH,
                "The specialist result identity did not match the assignment.",
                retryable=False,
                state_impact="Result was rejected and requires ForgeMaster review.",
            )
        return DispatchOutcome(result=result)

    def _error(
        self,
        category: AgentErrorCategory,
        summary: str,
        *,
        retryable: bool,
        state_impact: str,
    ) -> DispatchOutcome:
        return DispatchOutcome(
            error=AgentError(
                category=category,
                summary=summary,
                technical_reference_id=str(uuid4()),
                retryable=retryable,
                state_impact=state_impact,
                occurred_at=datetime.now(UTC),
            )
        )
