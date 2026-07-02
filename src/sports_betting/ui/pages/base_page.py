from __future__ import annotations

from typing import TypeAlias

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator: TypeAlias = tuple[str, str]


class BasePage:
    """Shared Selenium interactions for page objects."""

    def __init__(self, driver: WebDriver, timeout: int = 12) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, url: str) -> None:
        """Open a URL in the active browser session."""
        self.driver.get(url)

    def visible_element(self, locator: Locator) -> WebElement:
        """Wait for an element to be visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable_element(self, locator: Locator) -> WebElement:
        """Wait for an element to be clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Locator) -> None:
        """Click an element once it is ready for interaction."""
        self.clickable_element(locator).click()

    def text(self, locator: Locator) -> str:
        """Return visible text for an element."""
        return self.visible_element(locator).text

    def fill(self, locator: Locator, value: str) -> None:
        """Clear an input and type a value into it."""
        field = self.clickable_element(locator)
        field.clear()
        field.send_keys(value)
