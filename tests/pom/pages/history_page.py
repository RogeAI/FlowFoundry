from playwright.sync_api import Page
from .base_page import BasePage


class HistoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.history_links = page.locator(".recent-link")

    def history_count(self) -> int:
        return self.history_links.count()

    def first_entry_label(self) -> str:
        return self.history_links.first.locator("span").first.inner_text().strip()

    def has_running_entry(self) -> bool:
        return self.page.locator(".recent-dot.running").count() > 0
