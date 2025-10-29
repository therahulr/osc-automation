"""Login page object for OSC application."""

from playwright.sync_api import Page

from apps.osc.locators.login_locators import (
    APPLICATION_SUMMARY,
    DASHBOARD_LOADED,
    HOME_HEADING,
    LOGIN_BUTTON,
    MFA_PAGE_INDICATOR,
    PASSWORD_INPUT,
    USERNAME_INPUT,
)
from apps.osc.pages.base_page import OSCBasePage


class LoginPage(OSCBasePage):
    """Login page object for OSC application.

    Handles authentication, MFA bypass, and login verification.
    """

    def __init__(self, page: Page) -> None:
        """Initialize login page.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)

    def open(self) -> None:
        """Navigate to OSC login page."""
        self.logger.info(f"Opening login page | url={self.settings.login_url}")
        self.ui.goto(self.settings.login_url)

    def login(self, username: str, password: str) -> None:
        """Perform login with credentials and bypass MFA.

        This method:
        1. Enters username and password
        2. Clicks login button
        3. Detects if MFA page appears
        4. Bypasses MFA by navigating directly to dashboard
        5. Verifies dashboard is loaded

        Args:
            username: Username (e.g., contractordemo)
            password: User password

        Raises:
            RuntimeError: If login fails or dashboard doesn't load
        """
        self.logger.info(f"Attempting login | username={username}")

        try:
            # Step 1: Input credentials
            self.logger.debug("Entering username")
            self.ui.input_text(USERNAME_INPUT, username)

            self.logger.debug("Entering password")
            self.ui.input_text(PASSWORD_INPUT, password)

            # Step 2: Submit login
            self.logger.info("Clicking login button")
            self.ui.click(LOGIN_BUTTON, name="Login button")

            # Step 3: Handle MFA bypass
            self._bypass_mfa_if_present()

            # Step 4: Verify dashboard loaded
            self._verify_dashboard_loaded()

            self.logger.info(f"Login successful | username={username}")

        except Exception as e:
            self.logger.error(f"Login failed | username={username}, error={e}")
            raise RuntimeError(f"Login failed for user '{username}': {e}") from e

    def _bypass_mfa_if_present(self) -> None:
        """Bypass MFA screen by navigating directly to dashboard.

        If the MFA page appears, we skip it by directly navigating to
        the dashboard URL instead of selecting email/mobile options.
        """
        try:
            # Wait briefly to see if MFA page appears
            self.logger.debug("Checking if MFA page appears")
            self.ui.wait_visible(MFA_PAGE_INDICATOR, timeout_ms=5000)

            self.logger.info("MFA page detected - bypassing by navigating to dashboard")
            self.ui.goto(self.settings.dashboard_url)
            self.logger.info("MFA bypassed successfully")

        except Exception:
            # MFA page didn't appear, likely already on dashboard
            self.logger.debug("MFA page not detected - continuing")

    def _verify_dashboard_loaded(self) -> None:
        """Verify that dashboard/home page has loaded successfully.

        Checks for either "Home" heading or "Application Summary" text.

        Raises:
            RuntimeError: If dashboard indicators not found
        """
        self.logger.debug("Verifying dashboard loaded")

        try:
            # Wait for either Home heading or Application Summary text
            self._page.wait_for_selector(
                DASHBOARD_LOADED, state="visible", timeout=15000
            )
            self.logger.info("Dashboard loaded successfully")

        except Exception as e:
            current_url = self.get_current_url()
            self.logger.error(
                f"Dashboard verification failed | current_url={current_url}, error={e}"
            )
            raise RuntimeError(f"Dashboard did not load properly: {e}") from e

    def is_logged_in(self) -> bool:
        """Check if user is currently logged in.

        Returns:
            True if dashboard is visible, False otherwise
        """
        try:
            self.ui.wait_visible(HOME_HEADING, timeout_ms=3000)
            return True
        except Exception:
            return False

    def verify_home_page(self) -> None:
        """Verify we are on the home/dashboard page.

        Raises:
            RuntimeError: If home page indicators not found
        """
        self.logger.info("Verifying home page")

        try:
            # Check for Home heading
            self.ui.wait_visible(HOME_HEADING, timeout_ms=10000)
            self.logger.info("Home page verified - 'Home' heading found")

        except Exception:
            # Fallback: check for Application Summary text
            try:
                self.ui.wait_visible(APPLICATION_SUMMARY, timeout_ms=5000)
                self.logger.info(
                    "Home page verified - 'Application Summary' text found"
                )
            except Exception as e:
                self.logger.error(f"Home page verification failed | error={e}")
                raise RuntimeError(f"Home page verification failed: {e}") from e
