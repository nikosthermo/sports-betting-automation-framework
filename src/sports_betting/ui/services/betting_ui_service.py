from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.remote.webdriver import WebDriver

from sports_betting.ui.pages.bet_slip_page import BetSlipPage
from sports_betting.ui.pages.matches_page import MatchesPage


class BettingUiService:
    """User-level workflows composed from page objects."""

    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        self.matches_page = MatchesPage(driver, timeout)
        self.bet_slip_page = BetSlipPage(driver, timeout)

    def place_home_bet(self, app_url: str, match: dict, stake: Decimal) -> dict[str, str]:
        """Place a HOME bet through the browser and return expected and actual receipt values."""
        self.matches_page.open(app_url)
        self.matches_page.select_home_outcome(match["id"])
        self.bet_slip_page.enter_stake(f"{stake:.2f}")
        expected_payout = self.bet_slip_page.potential_payout_text()
        self.bet_slip_page.place_bet()
        self.bet_slip_page.wait_for_success_receipt()
        return {
            "expected_match": f"{match['homeTeam']} vs {match['awayTeam']}",
            "expected_stake": f"€{stake:.2f}",
            "expected_odds": f"{Decimal(str(match['odds']['home'])):.2f}",
            "expected_payout": expected_payout,
            "receipt_match": self.bet_slip_page.receipt_match_text(),
            "receipt_stake": self.bet_slip_page.receipt_stake_text(),
            "receipt_odds": self.bet_slip_page.receipt_odds_text(),
            "receipt_payout": self.bet_slip_page.receipt_payout_text(),
        }
