from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from sports_betting.ui.pages.base_page import BasePage


class BetSlipPage(BasePage):
    """Page object for the fixed bet slip and receipt modal."""

    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        super().__init__(driver, timeout)

    def enter_stake(self, stake: str) -> None:
        """Enter a stake value into the bet slip."""
        self.fill((By.ID, "bet-slip-stake-input"), stake)

    def place_bet(self) -> None:
        """Click the place bet button."""
        self.click((By.ID, "bet-slip-place-bet"))

    def potential_payout_text(self) -> str:
        """Return the displayed potential payout text."""
        return self.text((By.ID, "bet-slip-potential-payout"))

    def wait_for_success_receipt(self) -> None:
        """Wait until the success receipt modal is visible."""
        self.visible_element((By.ID, "modal-success"))

    def receipt_match_text(self) -> str:
        """Return the match text from the success receipt."""
        return self.text((By.ID, "modal-success-match"))

    def receipt_bet_id_text(self) -> str:
        """Return the bet id text from the success receipt."""
        return self.text((By.ID, "modal-success-bet-id"))

    def receipt_stake_text(self) -> str:
        """Return the stake text from the success receipt."""
        return self.text((By.ID, "modal-success-stake"))

    def receipt_odds_text(self) -> str:
        """Return the odds text from the success receipt."""
        return self.text((By.ID, "modal-success-odds"))

    def receipt_payout_text(self) -> str:
        """Return the payout text from the success receipt."""
        return self.text((By.ID, "modal-success-payout"))

    def receipt_placed_at_text(self) -> str:
        """Return the placement timestamp text from the success receipt."""
        return self.text((By.ID, "modal-success-placed-at"))
