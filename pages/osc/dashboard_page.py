"""Dashboard page object for OSC application."""

from playwright.sync_api import Page

from locators.osc.dashboard_locators import (
    CREATE_QUOTE_BUTTON,
    DASHBOARD_SUMMARY,
    NAV_QUOTES,
)
from pages.osc.base_page import OSCBasePage


class DashboardPage(OSCBasePage):
    """Dashboard page object for OSC application.

    Handles navigation and dashboard interactions.
    """

    def __init__(self, page: Page) -> None:
        """Initialize dashboard page.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)

    def open(self) -> None:
        """Navigate to OSC dashboard page."""
        self.logger.info(f"Opening dashboard page | url={self.settings.dashboard_url}")
        self.ui.goto(self.settings.dashboard_url)

    def wait_for_dashboard_loaded(self) -> None:
        """Wait for dashboard to fully load.

        Raises:
            RuntimeError: If dashboard doesn't load within timeout
        """
        self.logger.debug("Waiting for dashboard to load")
        try:
            self.ui.wait_visible(DASHBOARD_SUMMARY, timeout_ms=10000)
            self.logger.info("Dashboard loaded successfully")
        except Exception as e:
            self.logger.error(f"Dashboard load timeout | error={e}")
            raise RuntimeError(f"Dashboard failed to load: {e}") from e

    def navigate_to_quotes(self) -> None:
        """Navigate to quotes section from dashboard.

        Raises:
            RuntimeError: If navigation fails
        """
        self.logger.info("Navigating to quotes section")
        try:
            self.ui.click(NAV_QUOTES, name="Quotes navigation")
            self.wait_for_url_contains("quote")
            self.logger.info("Navigation to quotes successful")
        except Exception as e:
            self.logger.error(f"Failed to navigate to quotes | error={e}")
            raise RuntimeError(f"Navigation to quotes failed: {e}") from e

    def click_create_quote(self) -> None:
        """Click create quote button.

        Raises:
            RuntimeError: If button click fails
        """
        self.logger.info("Clicking create quote button")
        try:
            self.ui.click(CREATE_QUOTE_BUTTON, name="Create Quote button")
            self.logger.info("Create quote button clicked")
        except Exception as e:
            self.logger.error(f"Failed to click create quote | error={e}")
            raise RuntimeError(f"Failed to click create quote button: {e}") from e
