"""Base page object for OSC application with common functionality."""

from logging import Logger

from playwright.sync_api import Page

from apps.osc.config import osc_settings
from core.logger import Logger as LoggerFactory
from core.ui import Ui


class OSCBasePage:
    """Base page object for all OSC pages.

    Provides shared navigation, common elements, and utilities
    that all OSC page objects inherit.

    Attributes:
        ui: UI interaction wrapper
        logger: Logger instance
        settings: OSC application settings
    """

    def __init__(self, page: Page) -> None:
        """Initialize base page.

        Args:
            page: Playwright Page instance
        """
        self.ui = Ui(page)
        self.logger: Logger = LoggerFactory.get("osc")
        self.settings = osc_settings
        self._page = page

    def open(self) -> None:
        """Navigate to OSC base URL.

        Should be overridden by subclasses to navigate to specific pages.
        """
        self.logger.info(f"Opening OSC base URL | url={self.settings.base_url}")
        self.ui.goto(self.settings.base_url)

    def get_page_title(self) -> str:
        """Get current page title.

        Returns:
            Page title string
        """
        title = self._page.title()
        self.logger.debug(f"Page title | title={title}")
        return title

    def get_current_url(self) -> str:
        """Get current page URL.

        Returns:
            Current URL string
        """
        url = self._page.url
        self.logger.debug(f"Current URL | url={url}")
        return url

    def wait_for_url_contains(self, substring: str, timeout_ms: int = 10000) -> None:
        """Wait for URL to contain substring.

        Args:
            substring: Expected URL substring
            timeout_ms: Timeout in milliseconds

        Raises:
            Error: If URL doesn't match within timeout
        """
        self.logger.debug(f"Waiting for URL to contain | substring={substring}")
        try:
            self._page.wait_for_url(f"**/*{substring}*", timeout=timeout_ms)
        except Exception as e:
            current = self._page.url
            self.logger.error(
                f"URL condition not met | expected_contains={substring}, actual={current}"
            )
            raise RuntimeError(f"URL did not contain '{substring}': {e}") from e
