from __future__ import annotations

from typing import Any

import requests


class BettingApiClient:
    """Thin HTTP wrapper around the betting API."""

    def __init__(self, base_url: str, user_id: str, timeout: int = 12) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "x-user-id": user_id,
            }
        )

    def get_matches(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/matches", timeout=self.timeout)

    def get_balance(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/balance", timeout=self.timeout)

    def reset_balance(self) -> requests.Response:
        return self.session.post(f"{self.base_url}/api/reset-balance", timeout=self.timeout)

    def place_bet(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/place-bet",
            json=payload,
            timeout=self.timeout,
        )

    def close(self) -> None:
        self.session.close()
