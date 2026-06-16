from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from selenium.common import WebDriverException

from sports_betting.api.clients.betting_api_client import BettingApiClient
from sports_betting.api.services.betting_api_service import BettingApiService
from sports_betting.config import settings
from sports_betting.ui.driver_factory import create_chrome_driver


@pytest.fixture(scope="session")
def sporty_settings():
    return settings


@pytest.fixture
def api_client(sporty_settings):
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
    return BettingApiService(api_client)


@pytest.fixture
def reset_balance(api_service):
    api_service.reset_balance()
    return api_service.current_balance()


@pytest.fixture
def driver(sporty_settings):
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
    driver.save_screenshot(str(screenshot_path))
    report.sections.append(("screenshot", str(screenshot_path)))
