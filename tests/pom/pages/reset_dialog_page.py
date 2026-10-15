from playwright.sync_api import Page
from .base_page import BasePage


class ResetDialogPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.reset_button = page.locator(".reset-control")

    def reset_and_confirm(self) -> None:
        self.page.on("dialog", lambda d: d.accept())
        self.reset_button.click()

    def reset_and_cancel(self) -> None:
        self.page.on("dialog", lambda d: d.dismiss())
        self.reset_button.click()
