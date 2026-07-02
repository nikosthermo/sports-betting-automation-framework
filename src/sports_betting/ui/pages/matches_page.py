from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from sports_betting.ui.pages.base_page import BasePage


class MatchesPage(BasePage):
    """Page object for the upcoming matches list."""

    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        super().__init__(driver, timeout)

    def open(self, app_url: str) -> None:
        """Open the application and wait for the match list to render."""
        self.open_url(app_url)
        self.visible_element((By.ID, "match-list-title"))

    def select_home_outcome(self, match_id: str) -> None:
        """Select the HOME outcome odds for a match."""
        self.click((By.ID, f"odds-{match_id}-home"))

    def header_balance_text(self) -> str:
        """Return the header balance text."""
        return self.text((By.ID, "header-balance"))
