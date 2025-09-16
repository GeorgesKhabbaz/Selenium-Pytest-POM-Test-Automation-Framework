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


@lru_cache(maxsize=1)
def get_config() -> FrameworkConfig:
    """Return the parsed and validated framework configuration (cached)."""
    cfg = load_yaml_config(os.path.join("config", "config.yaml"))

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
