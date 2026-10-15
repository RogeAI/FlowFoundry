from domain.entities.session import Session
from domain.repositories.session_repository import SessionRepository
from domain.value_objects.action import Action


class UpdateActions:
    def __init__(self, session_repo: SessionRepository) -> None:
        self._sessions = session_repo

    def execute(self, session_id: str, action_labels: list[str]) -> Session:
        session = self._sessions.get_by_id(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        session.set_selected_actions([Action(label=label) for label in action_labels])
        self._sessions.save(session)
        return session
