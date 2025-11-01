"""Login page object for OSC application."""

from playwright.sync_api import Page

from locators.osc.osc_locators import DashboardPageLocators, LoginPageLocators, MFAPageLocators
from pages.osc.base_page import OSCBasePage


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

    def enter_username(self, username: str) -> None:
        """Enter username in the login form.
        
        Args:
            username: Username to enter
        """
        self.logger.info(f"Entering username | username={username}")
        self.ui.input_text(LoginPageLocators.USERNAME_FIELD, username)

    def enter_password(self, password: str) -> None:
        """Enter password in the login form.
        
        Args:
            password: Password to enter (will be masked in logs)
        """
        self.logger.info("Entering password")
        self.ui.input_text(LoginPageLocators.PASSWORD_FIELD, password)

    def click_login_button(self) -> None:
        """Click the login button to submit credentials."""
        self.logger.info("Clicking login button")
        self.ui.click(LoginPageLocators.LOGIN_BUTTON, name="Login Button")

    def bypass_mfa_to_dashboard(self) -> None:
        """Bypass MFA by directly navigating to dashboard.
        
        This method handles the MFA redirect by immediately going to the 
        dashboard URL instead of interacting with MFA options.
        """
        self.logger.info("Bypassing MFA - navigating directly to dashboard")
        
        # Wait a moment for the MFA redirect to potentially occur
        self._page.wait_for_timeout(2000)
        
        # Check if we're on MFA page
        current_url = self._page.url
        if MFAPageLocators.MFA_URL_PATTERN in current_url:
            self.logger.info("MFA page detected - bypassing to dashboard")
            # Direct navigation to bypass MFA
            self.ui.goto(self.settings.dashboard_url)
        else:
            self.logger.info("No MFA redirect detected")

    def verify_dashboard_loaded(self) -> None:
        """Verify that dashboard has loaded successfully.
        
        Raises:
            RuntimeError: If dashboard indicators are not found
        """
        self.logger.info("Verifying dashboard is loaded")
        
        try:
            # Try to find the Home heading first
            try:
                self.ui.wait_visible(DashboardPageLocators.HOME_HEADING, timeout_ms=5000)
                self.logger.info("✓ Dashboard loaded - Home heading found")
                return
            except Exception:
                pass
            
            # Fallback to Application Summary text
            try:
                self.ui.wait_visible(DashboardPageLocators.APPLICATION_SUMMARY_TEXT, timeout_ms=5000)
                self.logger.info("✓ Dashboard loaded - Application Summary found")
                return
            except Exception:
                pass
            
            # If neither found, raise error
            raise RuntimeError("Dashboard verification failed - no expected elements found")
            
        except Exception as e:
            self.logger.error(f"Dashboard verification failed | error={e}")
            current_url = self._page.url
            self.logger.error(f"Current URL: {current_url}")
            raise RuntimeError(f"Failed to verify dashboard loaded: {e}") from e

    def login(self, username: str, password: str) -> None:
        """Perform complete login workflow with MFA bypass.

        Args:
            username: Username or email
            password: User password

        Raises:
            RuntimeError: If login fails
        """
        self.logger.info(f"Starting login workflow | username={username}")

        try:
            # Step 1: Enter credentials
            self.enter_username(username)
            self.enter_password(password)
            
            # Step 2: Submit login
            self.click_login_button()
            
            # Step 3: Handle MFA bypass
            self.bypass_mfa_to_dashboard()
            
            # Step 4: Verify dashboard
            self.verify_dashboard_loaded()

            self.logger.info(f"✓ Login workflow completed successfully | username={username}")

        except Exception as e:
            self.logger.error(f"❌ Login workflow failed | username={username}, error={e}")
            raise RuntimeError(f"Login failed for user '{username}': {e}") from e

    def is_logged_in(self) -> bool:
        """Check if user is currently logged in.

        Returns:
            True if dashboard indicators are visible, False otherwise
        """
        try:
            # Check for either dashboard indicator
            try:
                self.ui.wait_visible(DashboardPageLocators.HOME_HEADING, timeout_ms=3000)
                return True
            except Exception:
                pass
                
            try:
                self.ui.wait_visible(DashboardPageLocators.APPLICATION_SUMMARY_TEXT, timeout_ms=3000)
                return True
            except Exception:
                pass
                
            return False
        except Exception:
            return False