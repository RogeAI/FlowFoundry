from dataclasses import dataclass


@dataclass(frozen=True)
class SessionSource:
    source_id: str
    session_id: str
    original_filename: str
    source_type: str
    location: str
    size_bytes: int
    sha256: str

