from dataclasses import dataclass
import os
import yaml


@dataclass
class AppSettings:
    base_url: str


@dataclass
class BrowserSettings:
    name: str
    headless: bool
    implicit_wait: int
    page_load_timeout: int
    script_timeout: int


@dataclass
class TimeoutSettings:
    short: int
    medium: int
    long: int


@dataclass
class FrameworkConfig:
    app: AppSettings
    browser: BrowserSettings
    timeouts: TimeoutSettings


_config_cache: FrameworkConfig | None = None


def load_yaml_config(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_config() -> FrameworkConfig:
    global _config_cache
    if _config_cache:
        return _config_cache

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
    _config_cache = FrameworkConfig(
        app=app, browser=browser, timeouts=timeouts)
    return _config_cache
