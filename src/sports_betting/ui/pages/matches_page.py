from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MatchesPage:
    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, app_url: str) -> None:
        self.driver.get(app_url)
        self.wait.until(EC.visibility_of_element_located((By.ID, "match-list-title")))

    def select_home_outcome(self, match_id: str) -> None:
        selector = (By.ID, f"odds-{match_id}-home")
        self.wait.until(EC.element_to_be_clickable(selector)).click()

    def header_balance_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located((By.ID, "header-balance"))).text
