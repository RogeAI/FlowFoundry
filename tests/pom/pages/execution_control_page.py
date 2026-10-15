from playwright.sync_api import Page
from .base_page import BasePage


class ExecutionControlPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.wfg_button = page.locator("button[aria-pressed]")
        self.begin_button = page.locator(".begin-control")
        self.wfg_indicator = page.locator(".wfg-indicator")

    def toggle_wfg(self) -> None:
        self.wfg_button.click()

    def is_wfg_active(self) -> bool:
        return self.wfg_button.get_attribute("aria-pressed") == "true"

    def is_wfg_indicator_visible(self) -> bool:
        return self.wfg_indicator.is_visible()

    def begin_label(self) -> str:
        return self.begin_button.inner_text().strip()

    def click_begin(self) -> None:
        self.begin_button.click()
