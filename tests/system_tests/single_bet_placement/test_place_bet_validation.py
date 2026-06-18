from __future__ import annotations

import allure
import pytest


@allure.epic("Sports Betting")
@allure.feature("Single Bet Placement")
@allure.story("Stake validation")
@allure.title("API rejects stake precision above two decimal places")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
def test_place_bet_rejects_stake_with_more_than_two_decimal_places(api_client, api_service):
    """Chosen because stake precision protects money movement and must be enforced by the API."""
    with allure.step("Get a valid match id"):
        match = api_service.first_match()
        balance_before = api_service.current_balance()

    with allure.step("Submit a bet with invalid stake precision"):
        response = api_client.place_bet(
            {"matchId": match["id"], "selection": "HOME", "stake": 10.999}
        )

    with allure.step("Verify API rejects the request"):
        assert response.status_code == 422
        body = response.json()
        assert body["error"] == "invalid_stake_precision"
        assert "2 decimal" in body["message"] or "two decimal" in body["message"].lower()

    with allure.step("Verify rejected bet did not mutate balance"):
        assert api_service.current_balance() == balance_before
