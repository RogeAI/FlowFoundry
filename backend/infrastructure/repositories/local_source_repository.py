from pathlib import Path
from shutil import rmtree

from domain.entities.source import SessionSource
from domain.repositories.source_repository import SourceRepository


class LocalSourceRepository(SourceRepository):
    """Metadata index for files stored below the FlowFoundry runtime root."""

    def __init__(self, storage_root: Path) -> None:
        self.storage_root = storage_root.resolve()
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self._sources: dict[tuple[str, str], SessionSource] = {}

    def save(self, source: SessionSource) -> None:
        location = Path(source.location).resolve()
        if not location.is_relative_to(self.storage_root):
            raise ValueError("Source location is outside the controlled storage root")
        self._sources[(source.session_id, source.source_id)] = source

    def get_for_session(self, session_id: str, source_id: str) -> SessionSource | None:
        return self._sources.get((session_id, source_id))

    def list_for_session(self, session_id: str) -> list[SessionSource]:
        return [
            source
            for (stored_session_id, _), source in self._sources.items()
            if stored_session_id == session_id
        ]

    def delete_for_session(self, session_id: str) -> None:
        self._sources = {
            key: source
            for key, source in self._sources.items()
            if key[0] != session_id
        }
        session_root = (self.storage_root / session_id).resolve()
        if not session_root.is_relative_to(self.storage_root):
            raise ValueError("Invalid session storage location")
        if session_root.exists():
            rmtree(session_root)

    def delete(self, session_id: str, source_id: str) -> bool:
        source = self._sources.pop((session_id, source_id), None)
        if source is None:
            return False
        location = Path(source.location).resolve()
        session_root = (self.storage_root / session_id).resolve()
        if not location.is_relative_to(session_root):
            raise ValueError("Source location is outside its session storage root")
        location.unlink(missing_ok=True)
        return True
