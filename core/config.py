"""Global configuration management for automation framework."""

from dataclasses import dataclass
from pathlib import Path

from core.utils import get_env, get_env_bool, get_env_int


@dataclass
class Settings:
    """Global automation settings loaded from environment variables.

    Attributes:
        headless: Run browser in headless mode
        incognito: Use incognito/private browsing mode
        slow_mo_ms: Slow down operations by specified milliseconds
        default_timeout_ms: Default timeout for UI operations
        nav_timeout_ms: Timeout for page navigation
        downloads_dir: Directory for downloaded files
        trace_enabled: Enable Playwright trace collection
    """

    headless: bool
    incognito: bool
    slow_mo_ms: int
    default_timeout_ms: int
    nav_timeout_ms: int
    downloads_dir: str
    trace_enabled: bool

    def __init__(self) -> None:
        """Initialize settings from environment variables with sensible defaults."""
        self.headless = get_env_bool("HEADLESS", default=True)
        self.incognito = get_env_bool("INCOGNITO", default=True)
        self.slow_mo_ms = get_env_int("SLOW_MO_MS", default=0)
        self.default_timeout_ms = get_env_int("DEFAULT_TIMEOUT_MS", default=30000)
        self.nav_timeout_ms = get_env_int("NAV_TIMEOUT_MS", default=60000)
        self.downloads_dir = get_env("DOWNLOADS_DIR", default=str(Path.cwd() / "downloads"))
        self.trace_enabled = get_env_bool("TRACE_ENABLED", default=False)


# Singleton instance
settings = Settings()
