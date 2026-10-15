from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.agent import Agent
from agent_sdk.contracts import AgentManifest


class AgentRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Agent]:
        ...

    @abstractmethod
    def get_by_id(self, agent_id: str) -> Optional[Agent]:
        ...

    @abstractmethod
    def get_manifest(self, agent_id: str) -> Optional[AgentManifest]:
        ...

    @abstractmethod
    def get_all_manifests(self) -> list[AgentManifest]:
        ...
