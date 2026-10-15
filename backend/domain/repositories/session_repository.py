from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.session import Session


class SessionRepository(ABC):
    @abstractmethod
    def save(self, session: Session) -> None:
        ...

    @abstractmethod
    def get_by_id(self, session_id: str) -> Optional[Session]:
        ...

    @abstractmethod
    def delete(self, session_id: str) -> None:
        ...
