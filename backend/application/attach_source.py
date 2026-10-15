from hashlib import sha256
from io import BytesIO
from pathlib import Path
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

from domain.entities.source import SessionSource
from domain.repositories.session_repository import SessionRepository
from domain.repositories.source_repository import SourceRepository


class AttachSource:
    MAX_FILE_SIZE = 10 * 1024 * 1024
    ALLOWED_TYPES = {
        ".csv": "text/csv",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".html": "text/html",
        ".json": "application/json",
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".xml": "application/xml",
    }

    def __init__(
        self,
        session_repo: SessionRepository,
        source_repo: SourceRepository,
        storage_root: Path,
    ) -> None:
        self._sessions = session_repo
        self._sources = source_repo
        self._storage_root = storage_root.resolve()
        self._storage_root.mkdir(parents=True, exist_ok=True)

    def execute(self, session_id: str, filename: str, content: bytes) -> SessionSource:
        if self._sessions.get_by_id(session_id) is None:
            raise ValueError("Session not found")
        safe_name = Path(filename).name
        suffix = Path(safe_name).suffix.lower()
        if not safe_name or safe_name in {".", ".."} or suffix not in self.ALLOWED_TYPES:
            raise ValueError("Unsupported source file type")
        if not content:
            raise ValueError("Source file is empty")
        if len(content) > self.MAX_FILE_SIZE:
            raise ValueError("Source file exceeds the 10 MB limit")
        if suffix == ".docx":
            try:
                with ZipFile(BytesIO(content)) as archive:
                    if "word/document.xml" not in archive.namelist() or archive.testzip():
                        raise ValueError("DOCX source is not a valid Office package")
            except BadZipFile as exc:
                raise ValueError("DOCX source is not a valid Office package") from exc

        digest = sha256(content).hexdigest()
        source_id = f"sha256:{digest}"
        existing = self._sources.get_for_session(session_id, source_id)
        if existing is not None:
            return existing

        session_root = (self._storage_root / session_id).resolve()
        if not session_root.is_relative_to(self._storage_root):
            raise ValueError("Invalid session storage location")
        session_root.mkdir(parents=True, exist_ok=True)
        location = session_root / f"{uuid4()}{suffix}"
        location.write_bytes(content)
        source = SessionSource(
            source_id=source_id,
            session_id=session_id,
            original_filename=safe_name,
            source_type=self.ALLOWED_TYPES[suffix],
            location=str(location),
            size_bytes=len(content),
            sha256=digest,
        )
        self._sources.save(source)
        return source
