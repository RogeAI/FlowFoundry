from playwright.sync_api import Page
from .base_page import BasePage


class ComposerPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.textarea = page.locator("#workflow-prompt")
        self.expand_button = page.locator(".composer-title button")
        self.attach_button = page.locator("button:has-text('Attach context')")
        self.panel = page.locator(".orchestration-panel")

    def type_prompt(self, text: str) -> None:
        self.textarea.fill(text)

    def get_prompt(self) -> str:
        return self.textarea.input_value()

    def is_expanded(self) -> bool:
        return "expanded" in (self.panel.get_attribute("class") or "")

    def toggle_expand(self) -> None:
        self.expand_button.click()
