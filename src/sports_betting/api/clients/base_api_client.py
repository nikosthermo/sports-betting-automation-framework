from __future__ import annotations

from typing import Any

import requests


class BaseApiClient:
    """Shared HTTP transport behavior for API clients."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 12,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        if headers:
            self.session.headers.update(headers)

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a GET request to a path relative to the base URL."""
        request_kwargs = {"timeout": self.timeout, **kwargs}
        return self.session.get(self.url_for(path), **request_kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a POST request to a path relative to the base URL."""
        request_kwargs = {"timeout": self.timeout, **kwargs}
        return self.session.post(self.url_for(path), **request_kwargs)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

    def url_for(self, path: str) -> str:
        """Build an absolute URL for a path relative to the base URL."""
        return f"{self.base_url}/{path.lstrip('/')}"
