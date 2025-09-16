"""Pytest fixtures for WebDriver lifecycle and test setup."""
from typing import Generator

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from src.core.webdriver_factory import create_driver


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    """Provide a fresh WebDriver per test and quit afterwards."""
    web_driver = create_driver()
    try:
        yield web_driver
    finally:
        web_driver.quit()
