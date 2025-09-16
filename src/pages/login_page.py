"""Page Object for the Login page."""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.base_page import BasePage
from src.core.locator_manager import LocatorManager


class LoginPage(BasePage):
    """Encapsulates actions on the Login page."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.locators = LocatorManager()
        self._login_path = "/login"

    def open(self, path: str = "/login") -> None:
        """Open the login page. Parameter kept for signature compatibility."""
        super().open(path)

    def is_loaded(self) -> bool:
        """Return True if the login banner is visible within timeout."""
        banner = self.locators.get("login_page", "banner")
        try:
            self.find(banner, timeout=self.cfg.timeouts.medium)
            return True
        except TimeoutException:
            return False

    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        user = self.locators.get("login_page", "username_input")
        pwd = self.locators.get("login_page", "password_input")
        submit = self.locators.get("login_page", "submit_button")

        self.type(user, username)
        self.type(pwd, password)
        self.click(submit)
