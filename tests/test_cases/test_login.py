import pytest

from src.pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_page_loads(driver):
    page = LoginPage(driver)
    page.open("/login")
    assert page.is_loaded(), "Login page did not load"
