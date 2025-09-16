"""Factory to create Selenium WebDriver instances based on framework config."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from .config import get_config

def create_driver():
    cfg = get_config()
    browser = cfg.browser.name.lower()

    if browser == "chrome":
        options = ChromeOptions()
        if cfg.browser.headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--remote-allow-origins=*")
        driver = webdriver.Chrome(options=options, service=ChromeService())
    elif browser == "firefox":
        options = FirefoxOptions()
        if cfg.browser.headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options, service=FirefoxService())
    else:
        raise ValueError(f"Unsupported browser: {cfg.browser.name}")

    # Timeouts
    driver.implicitly_wait(cfg.browser.implicit_wait)
    driver.set_page_load_timeout(cfg.browser.page_load_timeout)
    driver.set_script_timeout(cfg.browser.script_timeout)
    return driver
