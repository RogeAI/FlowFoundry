from typing import Optional

from domain.entities.session import Session
from domain.repositories.session_repository import SessionRepository


class MemorySessionRepository(SessionRepository):
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def save(self, session: Session) -> None:
        self._sessions[session.id] = session

    def get_by_id(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
