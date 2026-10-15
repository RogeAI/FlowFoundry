from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def wait_for_ready(self) -> None:
        self.page.wait_for_load_state("networkidle")
