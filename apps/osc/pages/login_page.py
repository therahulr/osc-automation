"""Login page object for OSC application."""

from playwright.sync_api import Page

from apps.osc.locators.login_locators import (
    LOGIN_BUTTON,
    PASSWORD_INPUT,
    USERNAME_INPUT,
    WELCOME_MESSAGE,
)
from apps.osc.pages.base_page import OSCBasePage


class LoginPage(OSCBasePage):
    """Login page object for OSC application.

    Handles authentication and login verification.
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
        """Perform login with credentials.

        Args:
            username: Username or email
            password: User password

        Raises:
            RuntimeError: If login fails
        """
        self.logger.info(f"Attempting login | username={username}")

        try:
            # Input credentials
            self.ui.input_text(USERNAME_INPUT, username)
            self.ui.input_text(PASSWORD_INPUT, password)

            # Submit login
            self.ui.click(LOGIN_BUTTON, name="Login button")

            # Wait for successful login indicator
            self.ui.wait_visible(WELCOME_MESSAGE, timeout_ms=10000)

            self.logger.info(f"Login successful | username={username}")

        except Exception as e:
            self.logger.error(f"Login failed | username={username}, error={e}")
            raise RuntimeError(f"Login failed for user '{username}': {e}") from e

    def is_logged_in(self) -> bool:
        """Check if user is currently logged in.

        Returns:
            True if welcome message is visible, False otherwise
        """
        try:
            self.ui.wait_visible(WELCOME_MESSAGE, timeout_ms=3000)
            return True
        except Exception:
            return False
