"""Configuration loader for the framework. Reads config/config.yaml and exposes a typed object."""
from dataclasses import dataclass
from functools import lru_cache
import os
import yaml


@dataclass
class AppSettings:
    """Application-level settings."""
    base_url: str


@dataclass
class BrowserSettings:
    """Browser and WebDriver settings."""
    name: str
    headless: bool
    implicit_wait: int
    page_load_timeout: int
    script_timeout: int


@dataclass
class TimeoutSettings:
    """Common wait durations to standardize explicit waits."""
    short: int
    medium: int
    long: int


@dataclass
class FrameworkConfig:
    """Top-level configuration composed of app, browser, and timeouts."""
    app: AppSettings
    browser: BrowserSettings
    timeouts: TimeoutSettings


def load_yaml_config(path: str) -> dict:
    """Load a YAML file and return a dict."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _apply_env_overrides(cfg: dict) -> dict:
    """Override config values from environment variables if present.

    Supported variables:
      - FW_APP_BASE_URL
      - FW_BROWSER_NAME
      - FW_BROWSER_HEADLESS ("true"/"false"/"1"/"0")
      - FW_BROWSER_IMPLICIT_WAIT
      - FW_BROWSER_PAGE_LOAD_TIMEOUT
      - FW_BROWSER_SCRIPT_TIMEOUT
      - FW_TIMEOUT_SHORT
      - FW_TIMEOUT_MEDIUM
      - FW_TIMEOUT_LONG
    """
    def get_bool(name: str, default: bool) -> bool:
        val = os.getenv(name)
        if val is None:
            return default
        return str(val).strip().lower() in {"1", "true", "yes", "on"}

    def get_int(name: str, default: int) -> int:
        val = os.getenv(name)
        if val is None or str(val).strip() == "":
            return default
        try:
            return int(val)
        except ValueError:
            return default

    app = cfg.get("app", {})
    browser = cfg.get("browser", {})
    timeouts = cfg.get("timeouts", {})

    app["base_url"] = os.getenv("FW_APP_BASE_URL", app.get("base_url"))
    browser["name"] = os.getenv("FW_BROWSER_NAME", browser.get("name"))
    browser["headless"] = get_bool("FW_BROWSER_HEADLESS", bool(browser.get("headless", False)))
    browser["implicit_wait"] = get_int("FW_BROWSER_IMPLICIT_WAIT", int(browser.get("implicit_wait", 0)))
    browser["page_load_timeout"] = get_int("FW_BROWSER_PAGE_LOAD_TIMEOUT", int(browser.get("page_load_timeout", 60)))
    browser["script_timeout"] = get_int("FW_BROWSER_SCRIPT_TIMEOUT", int(browser.get("script_timeout", 30)))

    timeouts["short"] = get_int("FW_TIMEOUT_SHORT", int(timeouts.get("short", 3)))
    timeouts["medium"] = get_int("FW_TIMEOUT_MEDIUM", int(timeouts.get("medium", 10)))
    timeouts["long"] = get_int("FW_TIMEOUT_LONG", int(timeouts.get("long", 20)))

    cfg["app"] = app
    cfg["browser"] = browser
    cfg["timeouts"] = timeouts
    return cfg


@lru_cache(maxsize=1)
def get_config() -> FrameworkConfig:
    """Return the parsed and validated framework configuration (cached)."""
    cfg = load_yaml_config(os.path.join("config", "config.yaml"))
    cfg = _apply_env_overrides(cfg)

    app = AppSettings(base_url=cfg["app"]["base_url"])
    browser = BrowserSettings(
        name=cfg["browser"]["name"],
        headless=bool(cfg["browser"]["headless"]),
        implicit_wait=int(cfg["browser"]["implicit_wait"]),
        page_load_timeout=int(cfg["browser"]["page_load_timeout"]),
        script_timeout=int(cfg["browser"]["script_timeout"]),
    )
    timeouts = TimeoutSettings(
        short=int(cfg["timeouts"]["short"]),
        medium=int(cfg["timeouts"]["medium"]),
        long=int(cfg["timeouts"]["long"]),
    )
    return FrameworkConfig(app=app, browser=browser, timeouts=timeouts)


def reload_config() -> None:
    """Clear the cached configuration so changes/env overrides take effect."""
    get_config.cache_clear()  # type: ignore[attr-defined]
