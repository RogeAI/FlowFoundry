import pytest
from playwright.sync_api import Page
from tests.pom.pages.agent_selector_page import AgentSelectorPage
from tests.pom.pages.reset_dialog_page import ResetDialogPage


AVAILABLE_AGENTS = ["Axiom", "Verity", "Loom", "Scribe"]
BUSY_AGENTS = ["Atlas"]
UNAVAILABLE_AGENTS = ["Sentinel"]


def test_all_six_agents_visible(page: Page) -> None:
    selector = AgentSelectorPage(page)
    names = selector.all_agent_names()
    assert len(names) == 6


def test_select_available_agent(page: Page) -> None:
    selector = AgentSelectorPage(page)
    selector.click_select("Axiom")
    assert selector.is_selected("Axiom")


def test_click_selected_agent_unselects(page: Page) -> None:
    selector = AgentSelectorPage(page)
    selector.click_select("Axiom")
    assert selector.is_selected("Axiom")
    selector.click_select("Axiom")
    assert not selector.is_selected("Axiom")


def test_only_one_agent_selected_at_a_time(page: Page) -> None:
    selector = AgentSelectorPage(page)
    selector.click_select("Axiom")
    selector.click_select("Verity")
    assert selector.is_selected("Verity")
    assert not selector.is_selected("Axiom")


def test_busy_agent_button_disabled(page: Page) -> None:
    selector = AgentSelectorPage(page)
    assert selector.is_button_disabled("Atlas")


def test_unavailable_agent_button_disabled(page: Page) -> None:
    selector = AgentSelectorPage(page)
    assert selector.is_button_disabled("Sentinel")


@pytest.mark.parametrize("agent", AVAILABLE_AGENTS)
def test_available_agents_selectable(page: Page, agent: str) -> None:
    selector = AgentSelectorPage(page)
    assert not selector.is_button_disabled(agent)


def test_reset_clears_agent_selection(page: Page) -> None:
    selector = AgentSelectorPage(page)
    reset = ResetDialogPage(page)
    selector.click_select("Axiom")
    assert selector.is_selected("Axiom")
    reset.reset_and_confirm()
    assert not selector.is_selected("Axiom")
