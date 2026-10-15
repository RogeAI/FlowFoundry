from playwright.sync_api import Page
from .base_page import BasePage


class AgentSelectorPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.grid = page.locator(".agent-grid")

    def agent_card(self, name: str):
        return self.grid.locator(f"article:has(h3:text('{name}'))")

    def select_button(self, name: str):
        return self.agent_card(name).locator("button")

    def click_select(self, name: str) -> None:
        self.select_button(name).click()

    def is_selected(self, name: str) -> bool:
        card = self.agent_card(name)
        return "selected" in (card.get_attribute("class") or "")

    def is_button_disabled(self, name: str) -> bool:
        return self.select_button(name).is_disabled()

    def agent_status(self, name: str) -> str:
        return self.agent_card(name).locator(".agent-status").inner_text().strip()

    def all_agent_names(self) -> list[str]:
        return [h.inner_text() for h in self.grid.locator("h3").all()]
