from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

from domain.value_objects.action import Action
from domain.value_objects.wfg_state import WFGState


@dataclass
class Session:
    id: str = field(default_factory=lambda: str(uuid4()))
    prompt: str = ""
    selected_actions: list[Action] = field(default_factory=list)
    selected_agent_id: Optional[str] = None
    wfg: WFGState = field(default_factory=WFGState)
    expanded: bool = False

    # Locked domain rule: one user objective → one top-level History entry
    history: list[dict] = field(default_factory=list)

    def set_prompt(self, text: str) -> None:
        self.prompt = text

    def toggle_action(self, action: Action) -> None:
        if action in self.selected_actions:
            self.selected_actions.remove(action)
        else:
            self.selected_actions.append(action)

    def set_selected_actions(self, actions: list[Action]) -> None:
        self.selected_actions = list(actions)

    def select_agent(self, agent_id: str) -> None:
        self.selected_agent_id = agent_id

    def deselect_agent(self) -> None:
        # Locked domain rule: clicking Selected unselects and returns control to ForgeMaster
        self.selected_agent_id = None

    def toggle_wfg(self) -> None:
        self.wfg = self.wfg.toggle()

    def release_wfg(self) -> None:
        # Locked domain rule: GO automatically turns WFG off
        self.wfg = self.wfg.release()

    def reset(self) -> None:
        self.prompt = ""
        self.selected_actions = []
        self.selected_agent_id = None
        self.wfg = WFGState(active=False)
        self.expanded = False
