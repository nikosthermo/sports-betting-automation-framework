from __future__ import annotations

from decimal import Decimal
from typing import Any

from sports_betting.api.clients.betting_api_client import BettingApiClient


class BettingApiService:
    """API workflows used by tests and setup fixtures."""

    def __init__(self, client: BettingApiClient) -> None:
        self.client = client

    def reset_balance(self) -> dict[str, Any]:
        """Reset balance and return the API response body."""
        response = self.client.reset_balance()
        response.raise_for_status()
        return response.json()

    def current_balance(self) -> Decimal:
        """Return the persisted balance as a Decimal."""
        response = self.client.get_balance()
        response.raise_for_status()
        return Decimal(str(response.json()["balance"]))

    def first_match(self) -> dict[str, Any]:
        """Return the first upcoming match from the catalog."""
        response = self.client.get_matches()
        response.raise_for_status()
        matches = response.json()
        if not matches:
            raise AssertionError("Expected at least one upcoming match from /api/matches")
        return matches[0]

    def place_home_bet(self, match_id: str, stake: Decimal) -> dict[str, Any]:
        """Place a HOME selection bet for the provided match."""
        response = self.client.place_bet(
            {"matchId": match_id, "selection": "HOME", "stake": float(stake)}
        )
        response.raise_for_status()
        return response.json()
