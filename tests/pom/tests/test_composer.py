import pytest
from playwright.sync_api import Page
from tests.pom.pages.composer_page import ComposerPage
from tests.pom.pages.reset_dialog_page import ResetDialogPage


def test_prompt_entry(page: Page) -> None:
    composer = ComposerPage(page)
    composer.type_prompt("Analyse the checkout requirements document")
    assert composer.get_prompt() == "Analyse the checkout requirements document"


def test_prompt_textarea_is_focusable(page: Page) -> None:
    composer = ComposerPage(page)
    composer.textarea.click()
    assert composer.textarea.is_focused()


def test_expand_toggle(page: Page) -> None:
    composer = ComposerPage(page)
    assert not composer.is_expanded()
    composer.toggle_expand()
    assert composer.is_expanded()
    composer.toggle_expand()
    assert not composer.is_expanded()


def test_reset_clears_prompt(page: Page) -> None:
    composer = ComposerPage(page)
    reset = ResetDialogPage(page)
    composer.type_prompt("Some workflow goal")
    assert composer.get_prompt() == "Some workflow goal"
    reset.reset_and_confirm()
    assert composer.get_prompt() == ""


def test_expanded_textarea_is_taller(page: Page) -> None:
    composer = ComposerPage(page)
    normal_height = composer.textarea.bounding_box()["height"]
    composer.toggle_expand()
    expanded_height = composer.textarea.bounding_box()["height"]
    assert expanded_height > normal_height
