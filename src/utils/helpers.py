"""Utility helpers for the AI Study Assistant project."""

import logging
from typing import Iterable


def setup_logging(level: int = logging.INFO) -> None:
    """Configure basic logging for local development and production."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def validate_required_fields(fields: Iterable[str]) -> None:
    """Validate that required configuration values are present."""
    missing = [field for field in fields if not field]
    if missing:
        raise ValueError(f"Missing required configuration fields: {', '.join(missing)}")
