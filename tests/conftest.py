from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.common import WebDriverException

from sports_betting.api.clients.betting_api_client import BettingApiClient
from sports_betting.api.services.betting_api_service import BettingApiService
from sports_betting.config import settings
from sports_betting.ui.driver_factory import create_chrome_driver


@pytest.fixture(scope="session")
def sporty_settings():
    """Return shared runtime settings."""
    return settings


@pytest.fixture
def api_client(sporty_settings):
    """Create an authenticated API client or skip when config is missing."""
    try:
        base_url, user_id = sporty_settings.require_runtime_config()
    except RuntimeError as exc:
        pytest.skip(str(exc))
    client = BettingApiClient(
        base_url=base_url,
        user_id=user_id,
        timeout=sporty_settings.timeout_seconds,
    )
    yield client
    client.close()


@pytest.fixture
def api_service(api_client):
    """Create the API service used by tests."""
    return BettingApiService(api_client)


@pytest.fixture
def reset_balance(api_service):
    """Reset balance before tests that mutate wallet state."""
    api_service.reset_balance()
    return api_service.current_balance()


@pytest.fixture
def driver(sporty_settings):
    """Create a Chrome browser or skip when browser prerequisites are missing."""
    try:
        sporty_settings.require_runtime_config()
    except RuntimeError as exc:
        pytest.skip(str(exc))
    try:
        driver = create_chrome_driver(headless=sporty_settings.headless)
    except WebDriverException as exc:
        pytest.skip(f"Chrome/WebDriver is not available in this environment: {exc.msg}")
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot path to failed UI test reports."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    screenshot_dir = Path("evidence/screenshots")
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    screenshot_path = screenshot_dir / f"{item.name}-{timestamp}.png"
    screenshot = driver.get_screenshot_as_png()
    screenshot_path.write_bytes(screenshot)
    allure.attach(
        screenshot,
        name="failure-screenshot",
        attachment_type=AttachmentType.PNG,
    )
    report.sections.append(("screenshot", str(screenshot_path)))
