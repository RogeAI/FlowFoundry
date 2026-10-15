from typing import Optional

from domain.entities.agent import Agent, AgentStatus
from domain.repositories.agent_repository import AgentRepository
from agent_sdk.contracts import AgentManifest
from agents.hermes import build_hermes_manifest

# Python-owned canonical Agent Registry. The frontend consumes its safe projection.
_DEFAULT_AGENTS: list[Agent] = [
    Agent(id="athena", name="Athena", role="The Testing Mentor",
          description="Teaches you how to create test scenarios and manual test cases step by step. Covers requirements analysis, test approaches, coverage, and test data — aligned with ISTQB concepts.",
          status=AgentStatus.AVAILABLE, portrait_index=0),
    Agent(id="hermes", name="Hermes", role="Information Intelligence Agent",
          description="Transforms fragmented or mixed information into structured, evidence-aware intelligence. Surfaces meaningful insights, decisions, actions, risks, gaps, contradictions, and unresolved questions.",
          status=AgentStatus.AVAILABLE, portrait_index=1),
    Agent(id="themis", name="Themis", role="Test Cases Creator",
          description="Designs high-quality test assets from requirements, user stories, and handoff materials. Produces clear scenarios, test data, and manual test cases with atomic steps and measurable expected results.",
          status=AgentStatus.AVAILABLE, portrait_index=2),
    Agent(id="minerva", name="Minerva", role="Test Strategy Advisor",
          description="Guides you through creating and finalizing your Test Strategy — what's being tested, what could go wrong, how testing builds confidence, and what dependencies apply.",
          status=AgentStatus.AVAILABLE, portrait_index=3),
    Agent(id="apolo", name="Apolo", role="Coming Soon",
          description="This specialist is under development and not yet available.",
          status=AgentStatus.UNAVAILABLE, portrait_index=4),
    Agent(id="agent6", name="Agent 6", role="Coming Soon",
          description="This specialist is under development and not yet available.",
          status=AgentStatus.UNAVAILABLE, portrait_index=5),
]

_DEFAULT_MANIFESTS: tuple[AgentManifest, ...] = (build_hermes_manifest(),)


class MemoryAgentRepository(AgentRepository):
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {a.id: a for a in _DEFAULT_AGENTS}
        self._manifests: dict[str, AgentManifest] = {
            manifest.agent_id: manifest for manifest in _DEFAULT_MANIFESTS
        }

    def get_all(self) -> list[Agent]:
        return list(self._agents.values())

    def get_by_id(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    def get_manifest(self, agent_id: str) -> Optional[AgentManifest]:
        return self._manifests.get(agent_id)

    def get_all_manifests(self) -> list[AgentManifest]:
        return list(self._manifests.values())
