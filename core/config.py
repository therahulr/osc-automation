"""Global configuration management for automation framework.

Enhanced configuration system with advanced parameterization.
All settings can be controlled via environment variables or programmatically.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

from core.utils import get_env, get_env_bool, get_env_int


@dataclass
class Settings:
    """Global automation settings loaded from environment variables.

    All settings support:
    - Environment variable configuration
    - Programmatic override
    - Sensible defaults

    Attributes:
        # Browser Settings
        headless: Run browser in headless mode
        incognito: Use incognito/private browsing mode
        slow_mo_ms: Slow down operations by specified milliseconds
        browser_type: Browser to use (chromium, firefox, webkit)

        # Timeout Settings
        default_timeout_ms: Default timeout for UI operations
        nav_timeout_ms: Timeout for page navigation
        action_timeout_ms: Timeout for actions like click, fill

        # Viewport Settings
        viewport_width: Browser viewport width
        viewport_height: Browser viewport height

        # Path Settings
        downloads_dir: Directory for downloaded files
        screenshots_dir: Directory for screenshots
        logs_dir: Directory for log files
        data_dir: Directory for test data

        # Performance Settings
        trace_enabled: Enable Playwright trace collection
        performance_tracking: Enable performance tracking
        video_recording: Enable video recording

        # Logging Settings
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        colored_output: Enable colored terminal output

        # Retry Settings
        max_retries: Maximum number of retries for failed actions
        retry_delay_ms: Delay between retries in milliseconds

        # Environment
        env: Environment name (dev, qa, prod)
    """

    # Browser Settings
    headless: bool
    incognito: bool
    slow_mo_ms: int
    browser_type: str

    # Timeout Settings
    default_timeout_ms: int
    nav_timeout_ms: int
    action_timeout_ms: int

    # Viewport Settings
    viewport_width: int
    viewport_height: int

    # Path Settings
    downloads_dir: str
    screenshots_dir: str
    logs_dir: str
    data_dir: str

    # Performance Settings
    trace_enabled: bool
    performance_tracking: bool
    video_recording: bool

    # Logging Settings
    log_level: str
    colored_output: bool

    # Retry Settings
    max_retries: int
    retry_delay_ms: int

    # Environment
    env: str

    def __init__(self) -> None:
        """Initialize settings from environment variables with sensible defaults."""
        # Browser Settings
        self.headless = get_env_bool("HEADLESS", default=False)
        self.incognito = get_env_bool("INCOGNITO", default=True)
        self.slow_mo_ms = get_env_int("SLOW_MO_MS", default=0)
        self.browser_type = get_env("BROWSER_TYPE", default="chromium")

        # Timeout Settings
        self.default_timeout_ms = get_env_int("DEFAULT_TIMEOUT_MS", default=30000)
        self.nav_timeout_ms = get_env_int("NAV_TIMEOUT_MS", default=60000)
        self.action_timeout_ms = get_env_int("ACTION_TIMEOUT_MS", default=10000)

        # Viewport Settings
        self.viewport_width = get_env_int("VIEWPORT_WIDTH", default=1920)
        self.viewport_height = get_env_int("VIEWPORT_HEIGHT", default=1080)

        # Path Settings
        base_dir = Path.cwd()
        self.downloads_dir = get_env("DOWNLOADS_DIR", default=str(base_dir / "downloads"))
        self.screenshots_dir = get_env("SCREENSHOTS_DIR", default=str(base_dir / "screenshots"))
        self.logs_dir = get_env("LOGS_DIR", default=str(base_dir / "logs"))
        self.data_dir = get_env("DATA_DIR", default=str(base_dir / "data"))

        # Performance Settings
        self.trace_enabled = get_env_bool("TRACE_ENABLED", default=False)
        self.performance_tracking = get_env_bool("PERFORMANCE_TRACKING", default=True)
        self.video_recording = get_env_bool("VIDEO_RECORDING", default=False)

        # Logging Settings
        self.log_level = get_env("LOG_LEVEL", default="INFO")
        self.colored_output = get_env_bool("COLORED_OUTPUT", default=True)

        # Retry Settings
        self.max_retries = get_env_int("MAX_RETRIES", default=3)
        self.retry_delay_ms = get_env_int("RETRY_DELAY_MS", default=1000)

        # Environment
        self.env = get_env("ENV", default="dev")

    def override(self, **kwargs) -> None:
        """Override settings programmatically.

        Usage:
            settings.override(headless=True, slow_mo_ms=500)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown setting: {key}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary.

        Returns:
            Dictionary of all settings
        """
        return {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }

    def print_settings(self):
        """Print all current settings."""
        print("\n" + "="*80)
        print("AUTOMATION FRAMEWORK SETTINGS")
        print("="*80)

        categories = {
            "Browser Settings": ["headless", "incognito", "slow_mo_ms", "browser_type"],
            "Timeout Settings": ["default_timeout_ms", "nav_timeout_ms", "action_timeout_ms"],
            "Viewport Settings": ["viewport_width", "viewport_height"],
            "Path Settings": ["downloads_dir", "screenshots_dir", "logs_dir", "data_dir"],
            "Performance Settings": ["trace_enabled", "performance_tracking", "video_recording"],
            "Logging Settings": ["log_level", "colored_output"],
            "Retry Settings": ["max_retries", "retry_delay_ms"],
            "Environment": ["env"]
        }

        for category, attrs in categories.items():
            print(f"\n{category}:")
            for attr in attrs:
                value = getattr(self, attr, "N/A")
                print(f"  {attr}: {value}")

        print("\n" + "="*80 + "\n")


# Singleton instance
settings = Settings()
