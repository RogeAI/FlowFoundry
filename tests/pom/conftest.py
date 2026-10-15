import pytest
from playwright.sync_api import Page, Browser

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": BASE_URL}


@pytest.fixture
def page(page: Page) -> Page:
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    return page
