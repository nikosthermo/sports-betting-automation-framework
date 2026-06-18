from __future__ import annotations

from decimal import Decimal

import allure
import pytest

from sports_betting.ui.services.betting_ui_service import BettingUiService


@allure.epic("Sports Betting")
@allure.feature("Single Bet Placement")
@allure.story("Success receipt")
@allure.title("Single HOME bet receipt matches selected bet and balance")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_single_home_bet_receipt_matches_selected_bet(
    driver, sporty_settings, api_service, reset_balance
):
    """Chosen because it covers the critical revenue journey from selection to receipt."""
    stake = Decimal("10.00")

    with allure.step("Get a match from the catalog"):
        match = api_service.first_match()

    with allure.step("Place a valid HOME bet through the browser"):
        ui = BettingUiService(driver, timeout=sporty_settings.timeout_seconds)
        receipt = ui.place_home_bet(
            app_url=sporty_settings.app_url,
            match=match,
            stake=stake,
            starting_balance=reset_balance,
        )

    with allure.step("Verify receipt, displayed balance, and persisted balance"):
        failures = []
        expected_pairs = {
            "bet slip payout": ("bet_slip_payout", "expected_payout"),
            "receipt match": ("receipt_match", "expected_match"),
            "receipt stake": ("receipt_stake", "expected_stake"),
            "receipt odds": ("receipt_odds", "expected_odds"),
            "receipt payout": ("receipt_payout", "expected_payout"),
        }

        for label, (actual_key, expected_key) in expected_pairs.items():
            if receipt[actual_key] != receipt[expected_key]:
                failures.append(
                    f"{label}: expected {receipt[expected_key]!r}, got {receipt[actual_key]!r}"
                )

        if receipt["expected_balance"] not in receipt["header_balance_after"]:
            failures.append(
                "header balance after placement: "
                f"expected to contain {receipt['expected_balance']!r}, "
                f"got {receipt['header_balance_after']!r}"
            )

        persisted_balance = api_service.current_balance()
        expected_persisted_balance = reset_balance - stake
        if persisted_balance != expected_persisted_balance:
            failures.append(
                "persisted balance after placement: "
                f"expected {expected_persisted_balance}, got {persisted_balance}"
            )

        if not receipt["receipt_bet_id"].strip():
            failures.append("receipt bet id should be present")

        if not receipt["receipt_placed_at"].strip():
            failures.append("receipt placement timestamp should be present")

        assert not failures, "\n".join(failures)
