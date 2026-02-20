import logging
import sys
from typing import Any

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structured logging for the application."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def log_extra(message: str, **kwargs: Any) -> None:
    """Log with extra key=value pairs for structured output."""
    extra = " | ".join(f"{k}={v}" for k, v in kwargs.items())
    logging.getLogger(__name__).info("%s | %s", message, extra if extra else "")
