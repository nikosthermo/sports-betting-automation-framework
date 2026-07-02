from __future__ import annotations

from typing import Any

import requests

from sports_betting.api.clients.base_api_client import BaseApiClient


class BettingApiClient(BaseApiClient):
    """Thin HTTP wrapper around the betting API."""

    def __init__(self, base_url: str, user_id: str, timeout: int = 12) -> None:
        super().__init__(base_url=base_url, timeout=timeout, headers={"x-user-id": user_id})

    def get_matches(self) -> requests.Response:
        """Get the upcoming match catalog."""
        return self.get("/api/matches")

    def get_balance(self) -> requests.Response:
        """Get the current user balance."""
        return self.get("/api/balance")

    def reset_balance(self) -> requests.Response:
        """Reset the current user's balance to the configured initial state."""
        return self.post("/api/reset-balance")

    def place_bet(self, payload: dict[str, Any]) -> requests.Response:
        """Submit a single bet placement request."""
        return self.post("/api/place-bet", json=payload)
