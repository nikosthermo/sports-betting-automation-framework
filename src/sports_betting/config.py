from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str | None = os.getenv("SPORTY_BASE_URL")
    user_id: str | None = os.getenv("SPORTY_USER_ID")
    headless: bool = os.getenv("SPORTY_HEADLESS", "true").lower() in {"1", "true", "yes"}
    timeout_seconds: int = int(os.getenv("SPORTY_TIMEOUT_SECONDS", "12"))

    @property
    def app_url(self) -> str:
        base_url = self.require_base_url()
        user_id = self.require_user_id()
        return f"{base_url}/?user-id={user_id}"

    def require_base_url(self) -> str:
        if not self.base_url:
            raise RuntimeError(
                "SPORTY_BASE_URL is required. "
                "Pass the target application URL as an environment variable."
            )
        return self.base_url.rstrip("/")

    def require_user_id(self) -> str:
        if not self.user_id:
            raise RuntimeError(
                "SPORTY_USER_ID is required for authenticated API/UI flows. "
                "Pass the assignment user id as an environment variable."
            )
        return self.user_id

    def require_runtime_config(self) -> tuple[str, str]:
        return self.require_base_url(), self.require_user_id()


settings = Settings()
