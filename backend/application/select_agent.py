from typing import Optional

from domain.repositories.agent_repository import AgentRepository
from domain.repositories.session_repository import SessionRepository
from domain.entities.session import Session


class SelectAgent:
    def __init__(
        self,
        session_repo: SessionRepository,
        agent_repo: AgentRepository,
    ) -> None:
        self._sessions = session_repo
        self._agents = agent_repo

    def execute(self, session_id: str, agent_id: Optional[str]) -> Session:
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        if agent_id is None:
            session.deselect_agent()
        else:
            agent = self._agents.get_by_id(agent_id)
            if agent is None:
                raise ValueError(f"Agent {agent_id} not found")
            if not agent.can_be_selected():
                raise ValueError(f"Agent {agent_id} is {agent.status} and cannot be selected")
            session.select_agent(agent_id)

        self._sessions.save(session)
        return session
