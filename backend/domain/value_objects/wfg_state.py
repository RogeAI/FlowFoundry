from dataclasses import dataclass


@dataclass(frozen=True)
class WFGState:
    active: bool = False

    def activate(self) -> "WFGState":
        return WFGState(active=True)

    def release(self) -> "WFGState":
        return WFGState(active=False)

    def toggle(self) -> "WFGState":
        return WFGState(active=not self.active)
