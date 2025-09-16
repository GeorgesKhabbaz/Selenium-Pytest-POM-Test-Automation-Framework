import logging
import os
from datetime import datetime

_LOGGERS = {}

def get_logger(name: str = "framework") -> logging.Logger:
    if name in _LOGGERS:
        return _LOGGERS[name]

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    log_path = os.path.join("logs", f"{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    _LOGGERS[name] = logger
    return logger
