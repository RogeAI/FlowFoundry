import pytest
from playwright.sync_api import Page
from tests.pom.pages.execution_control_page import ExecutionControlPage
from tests.pom.pages.composer_page import ComposerPage


def test_begin_button_default_label(page: Page) -> None:
    ctrl = ExecutionControlPage(page)
    assert "Begin workflow" in ctrl.begin_label()


def test_wfg_activates(page: Page) -> None:
    ctrl = ExecutionControlPage(page)
    ctrl.toggle_wfg()
    assert ctrl.is_wfg_active()


def test_wfg_indicator_appears_when_active(page: Page) -> None:
    ctrl = ExecutionControlPage(page)
    ctrl.toggle_wfg()
    assert ctrl.is_wfg_indicator_visible()


def test_begin_button_becomes_go_when_wfg_active(page: Page) -> None:
    ctrl = ExecutionControlPage(page)
    ctrl.toggle_wfg()
    assert "GO" in ctrl.begin_label()


def test_wfg_toggle_off(page: Page) -> None:
    ctrl = ExecutionControlPage(page)
    ctrl.toggle_wfg()
    assert ctrl.is_wfg_active()
    ctrl.toggle_wfg()
    assert not ctrl.is_wfg_active()


def test_go_clears_wfg(page: Page) -> None:
    """Pressing GO should release WFG (backend call, or fallback no-op)."""
    ctrl = ExecutionControlPage(page)
    ctrl.toggle_wfg()
    assert ctrl.is_wfg_active()
    ctrl.click_begin()
    # After GO, WFG should be off — the page handles this in beginWorkflow()
    page.wait_for_timeout(500)
    assert not ctrl.is_wfg_active()
