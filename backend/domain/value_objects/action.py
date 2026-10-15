from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    label: str

    def __post_init__(self) -> None:
        if not self.label or not self.label.strip():
            raise ValueError("Action label cannot be empty")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Action):
            return False
        return self.label == other.label

    def __hash__(self) -> int:
        return hash(self.label)
