"""Base page providing robust wait-based interactions."""
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import get_config

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.cfg = get_config()

    def open(self, path: str) -> None:
        url = self.cfg.app.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    def wait_for_visible(self, locator: Tuple[By, str], timeout: int | None = None) -> WebElement:
        t = timeout if timeout is not None else self.cfg.timeouts.medium
        return WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Tuple[By, str], timeout: int | None = None) -> WebElement:
        t = timeout if timeout is not None else self.cfg.timeouts.medium
        return WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(locator))

    def find(self, locator: Tuple[By, str], timeout: int | None = None) -> WebElement:
        return self.wait_for_visible(locator, timeout)

    def click(self, locator: Tuple[By, str], timeout: int | None = None) -> None:
        self.wait_for_clickable(locator, timeout).click()

    def type(self, locator: Tuple[By, str], text: str, timeout: int | None = None) -> None:
        el = self.wait_for_visible(locator, timeout)
        el.clear()
        el.send_keys(text)
