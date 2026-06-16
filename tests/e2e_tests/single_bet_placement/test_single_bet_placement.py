from __future__ import annotations

from decimal import Decimal

import allure
import pytest

from sports_betting.ui.services.betting_ui_service import BettingUiService


@allure.epic("Sports Betting")
@allure.feature("Single Bet Placement")
@allure.story("Success receipt")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_single_home_bet_receipt_matches_selected_bet(
    driver, sporty_settings, api_service, reset_balance
):
    """Chosen because it covers the critical revenue journey from selection to receipt."""
    with allure.step("Get a match from the catalog"):
        match = api_service.first_match()

    with allure.step("Place a valid HOME bet through the browser"):
        ui = BettingUiService(driver, timeout=sporty_settings.timeout_seconds)
        receipt = ui.place_home_bet(
            app_url=sporty_settings.app_url,
            match=match,
            stake=Decimal("10.00"),
        )

    with allure.step("Verify the receipt matches the selected bet"):
        assert receipt["receipt_match"] == receipt["expected_match"]
        assert receipt["receipt_stake"] == receipt["expected_stake"]
        assert receipt["receipt_odds"] == receipt["expected_odds"]
        assert receipt["receipt_payout"] == receipt["expected_payout"]
