from dataclasses import dataclass
from enum import Enum


class AgentStatus(str, Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    UNAVAILABLE = "Unavailable"


@dataclass
class Agent:
    id: str
    name: str
    role: str
    description: str
    status: AgentStatus
    portrait_index: int  # 0-5, maps to sprite position in agent-portraits.png

    def can_be_selected(self) -> bool:
        return self.status == AgentStatus.AVAILABLE

    def is_available(self) -> bool:
        return self.status == AgentStatus.AVAILABLE
