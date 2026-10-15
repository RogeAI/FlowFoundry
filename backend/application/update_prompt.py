from domain.entities.session import Session
from domain.repositories.session_repository import SessionRepository


class UpdatePrompt:
    def __init__(self, session_repo: SessionRepository) -> None:
        self._sessions = session_repo

    def execute(self, session_id: str, prompt: str) -> Session:
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        if not prompt.strip():
            raise ValueError("Workflow objective cannot be empty")
        session.set_prompt(prompt.strip())
        self._sessions.save(session)
        return session

