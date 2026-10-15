import pytest
from playwright.sync_api import Page
from tests.pom.pages.action_selector_page import ActionSelectorPage, ACTIONS
from tests.pom.pages.reset_dialog_page import ResetDialogPage


def test_all_actions_visible(page: Page) -> None:
    selector = ActionSelectorPage(page)
    for action in ACTIONS:
        assert selector.action_button(action).is_visible()


def test_select_single_action(page: Page) -> None:
    selector = ActionSelectorPage(page)
    selector.toggle_action("Summarize")
    assert selector.is_selected("Summarize")
    assert selector.selected_count() == 1


def test_deselect_action(page: Page) -> None:
    selector = ActionSelectorPage(page)
    selector.toggle_action("Summarize")
    assert selector.is_selected("Summarize")
    selector.toggle_action("Summarize")
    assert not selector.is_selected("Summarize")
    assert selector.selected_count() == 0


def test_multi_select(page: Page) -> None:
    selector = ActionSelectorPage(page)
    selector.toggle_action("Summarize")
    selector.toggle_action("Identify gaps")
    selector.toggle_action("Design test cases")
    assert selector.selected_count() == 3


def test_chips_appear_when_selected(page: Page) -> None:
    selector = ActionSelectorPage(page)
    selector.toggle_action("Summarize")
    chips = selector.chip_buttons()
    assert any("Summarize" in c.inner_text() for c in chips)


def test_chip_remove_deselects(page: Page) -> None:
    selector = ActionSelectorPage(page)
    selector.toggle_action("Summarize")
    selector.remove_chip("Summarize")
    assert not selector.is_selected("Summarize")
    assert selector.selected_count() == 0


def test_reset_clears_actions(page: Page) -> None:
    selector = ActionSelectorPage(page)
    reset = ResetDialogPage(page)
    selector.toggle_action("Summarize")
    selector.toggle_action("Identify gaps")
    reset.reset_and_confirm()
    assert selector.selected_count() == 0
