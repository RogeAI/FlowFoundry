"""In-process specialist runtime registry for the current FlowFoundry baseline."""

from __future__ import annotations

from typing import Callable

from agent_sdk.contracts import AgentResult, AgentTask
from application.dispatch_specialist import SpecialistRuntime


class LazyHermesRuntime:
    """Create the live provider gateway only when ForgeMaster dispatches Hermes."""

    def __init__(self, factory: Callable[[], SpecialistRuntime] | None = None) -> None:
        self._factory = factory or self._default_factory
        self._runtime: SpecialistRuntime | None = None

    def execute(self, task: AgentTask) -> AgentResult:
        if self._runtime is None:
            self._runtime = self._factory()
        return self._runtime.execute(task)

    def _default_factory(self) -> SpecialistRuntime:
        from agents.hermes_runtime import HermesRuntime
        from infrastructure.model_gateways.anthropic_hermes import AnthropicHermesGateway

        return HermesRuntime(model_gateway=AnthropicHermesGateway.from_environment())


class MemorySpecialistRuntimeRegistry:
    def __init__(self, runtimes: dict[str, SpecialistRuntime] | None = None) -> None:
        self._runtimes = (
            runtimes if runtimes is not None else {"hermes": LazyHermesRuntime()}
        )

    def get(self, agent_id: str) -> SpecialistRuntime | None:
        return self._runtimes.get(agent_id)
