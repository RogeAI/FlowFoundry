from playwright.sync_api import Page
from .base_page import BasePage


ACTIONS = [
    "Summarize",
    "Review requirements",
    "Create testable scenarios",
    "Design test cases",
    "Identify gaps",
    "Compare documents",
]


class ActionSelectorPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.grid = page.locator(".shortcut-grid")
        self.chips = page.locator(".selected-action-chips")
        self.count_badge = page.locator(".action-heading > span")

    def action_button(self, action: str):
        return self.grid.locator(f"button:has-text('{action}')")

    def toggle_action(self, action: str) -> None:
        self.action_button(action).click()

    def is_selected(self, action: str) -> bool:
        btn = self.action_button(action)
        return "selected" in (btn.get_attribute("class") or "")

    def selected_count(self) -> int:
        text = self.count_badge.inner_text()
        return int(text.split()[0]) if text and text[0].isdigit() else 0

    def chip_buttons(self):
        return self.chips.locator("button").all()

    def remove_chip(self, action: str) -> None:
        self.chips.locator(f"button:has-text('{action}')").click()
