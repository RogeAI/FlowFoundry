from dataclasses import dataclass


@dataclass(frozen=True)
class WFGReleased:
    session_id: str
