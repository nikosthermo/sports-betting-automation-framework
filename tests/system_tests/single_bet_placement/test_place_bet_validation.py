from __future__ import annotations

import pytest


@pytest.mark.api
def test_place_bet_rejects_stake_with_more_than_two_decimal_places(api_client, api_service):
    """Chosen because stake precision protects money movement and must be enforced by the API."""
    match = api_service.first_match()

    response = api_client.place_bet({"matchId": match["id"], "selection": "HOME", "stake": 10.999})

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "invalid_stake_precision"
    assert "2 decimal" in body["message"] or "two decimal" in body["message"].lower()
