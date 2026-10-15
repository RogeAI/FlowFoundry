from domain.entities.session import Session
from domain.repositories.session_repository import SessionRepository


class StartSession:
    def __init__(self, session_repo: SessionRepository) -> None:
        self._sessions = session_repo

    def execute(self) -> Session:
        session = Session()
        self._sessions.save(session)
        return session
