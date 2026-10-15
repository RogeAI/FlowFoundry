from domain.entities.session import Session
from domain.repositories.session_repository import SessionRepository
from domain.repositories.source_repository import SourceRepository


class ResetSession:
    def __init__(
        self,
        session_repo: SessionRepository,
        source_repo: SourceRepository,
    ) -> None:
        self._sessions = session_repo
        self._sources = source_repo

    def execute(self, session_id: str) -> Session:
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        session.reset()
        self._sources.delete_for_session(session_id)
        self._sessions.save(session)
        return session
