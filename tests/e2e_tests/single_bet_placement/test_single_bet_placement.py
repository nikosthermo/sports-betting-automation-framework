from __future__ import annotations

from decimal import Decimal

import pytest

from sports_betting.ui.services.betting_ui_service import BettingUiService


@pytest.mark.e2e
def test_single_home_bet_receipt_matches_selected_bet(driver, sporty_settings, api_service, reset_balance):
    """Chosen because it covers the critical revenue journey from selection to receipt."""
    match = api_service.first_match()
    ui = BettingUiService(driver, timeout=sporty_settings.timeout_seconds)

    receipt = ui.place_home_bet(
        app_url=sporty_settings.app_url,
        match=match,
        stake=Decimal("10.00"),
    )

    assert receipt["receipt_match"] == receipt["expected_match"]
    assert receipt["receipt_stake"] == receipt["expected_stake"]
    assert receipt["receipt_odds"] == receipt["expected_odds"]
    assert receipt["receipt_payout"] == receipt["expected_payout"]
