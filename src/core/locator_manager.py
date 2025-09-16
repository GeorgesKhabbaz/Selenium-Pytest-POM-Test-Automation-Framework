"""Locator manager that reads data/locators.yaml and resolves logical names to (By, value)."""
import os
import yaml
from selenium.webdriver.common.by import By

_BY_MAP = {
    "id": By.ID,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "link_text": By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT,
    "tag": By.TAG_NAME,
    "class": By.CLASS_NAME,
}

class LocatorManager:
    def __init__(self, yaml_path: str = os.path.join("data", "locators.yaml")) -> None:
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Locators file not found: {yaml_path}")
        with open(yaml_path, "r", encoding="utf-8") as f:
            self._locators = yaml.safe_load(f) or {}

    def get(self, *path: str):
        """Resolve a path like ('login_page', 'username_input') to (By, value)."""
        node = self._locators
        for key in path:
            if key not in node:
                raise KeyError(f"Locator path not found: {'/'.join(path)}")
            node = node[key]
        if isinstance(node, dict) and "by" in node and "value" in node:
            by_key = node["by"].lower()
            if by_key not in _BY_MAP:
                raise ValueError(f"Unknown locator strategy: {by_key}")
            return _BY_MAP[by_key], node["value"]
        raise ValueError(f"Invalid locator entry at: {'/'.join(path)}")
