from domain.entities.session import Session
from domain.repositories.session_repository import SessionRepository


class ToggleWFG:
    def __init__(self, session_repo: SessionRepository) -> None:
        self._sessions = session_repo

    def execute(self, session_id: str) -> Session:
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        session.toggle_wfg()
        self._sessions.save(session)
        return session
