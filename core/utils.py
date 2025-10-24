"""Utility functions for common operations."""

import os
from datetime import datetime
from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    """Create directory if it doesn't exist, return Path object.

    Args:
        path: Directory path to ensure exists

    Returns:
        Path object of the created/existing directory
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def now_ts() -> str:
    """Return current timestamp as formatted string.

    Returns:
        Timestamp in format: YYYY-MM-DD_HH-MM-SS
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def get_env(key: str, default: str = "") -> str:
    """Get environment variable with optional default.

    Args:
        key: Environment variable name
        default: Default value if not found

    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get environment variable as boolean.

    Args:
        key: Environment variable name
        default: Default boolean value

    Returns:
        True if env var is '1', 'true', 'yes' (case-insensitive), else False
    """
    value = os.getenv(key, "").lower()
    if not value:
        return default
    return value in ("1", "true", "yes")


def get_env_int(key: str, default: int) -> int:
    """Get environment variable as integer.

    Args:
        key: Environment variable name
        default: Default integer value

    Returns:
        Integer value from environment or default
    """
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
