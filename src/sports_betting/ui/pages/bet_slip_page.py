from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BetSlipPage:
    """Page object for the fixed bet slip and receipt modal."""

    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def enter_stake(self, stake: str) -> None:
        """Enter a stake value into the bet slip."""
        field = self.wait.until(EC.element_to_be_clickable((By.ID, "bet-slip-stake-input")))
        field.clear()
        field.send_keys(stake)

    def place_bet(self) -> None:
        """Click the place bet button."""
        self.wait.until(EC.element_to_be_clickable((By.ID, "bet-slip-place-bet"))).click()

    def potential_payout_text(self) -> str:
        """Return the displayed potential payout text."""
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "bet-slip-potential-payout"))
        ).text

    def wait_for_success_receipt(self) -> None:
        """Wait until the success receipt modal is visible."""
        self.wait.until(EC.visibility_of_element_located((By.ID, "modal-success")))

    def receipt_match_text(self) -> str:
        """Return the match text from the success receipt."""
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "modal-success-match"))
        ).text

    def receipt_bet_id_text(self) -> str:
        """Return the bet id text from the success receipt."""
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "modal-success-bet-id"))
        ).text

    def receipt_stake_text(self) -> str:
        """Return the stake text from the success receipt."""
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "modal-success-stake"))
        ).text

    def receipt_odds_text(self) -> str:
        """Return the odds text from the success receipt."""
        return self.wait.until(EC.visibility_of_element_located((By.ID, "modal-success-odds"))).text

    def receipt_payout_text(self) -> str:
        """Return the payout text from the success receipt."""
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "modal-success-payout"))
        ).text

    def receipt_placed_at_text(self) -> str:
        """Return the placement timestamp text from the success receipt."""
        return self.wait.until(
            EC.visibility_of_element_located((By.ID, "modal-success-placed-at"))
        ).text
