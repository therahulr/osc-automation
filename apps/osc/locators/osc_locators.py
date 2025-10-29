"""OSC Application Locators - Organized by page classes with optimized selectors."""

from typing import Literal, Tuple

# Type alias for locator strategies
LocatorStrategy = Literal["id", "name", "css", "xpath", "text", "role"]
Locator = Tuple[LocatorStrategy, str] | str


class LoginPageLocators:
    """Locators for OSC Login page elements."""
    
    # Main form elements
    USERNAME_FIELD = ("name", "txtUsername")
    PASSWORD_FIELD = ("name", "txtPassword") 
    LOGIN_BUTTON = ("name", "btnLogin")
    
    # Page indicators
    LOGIN_FORM = "form[name='frmHome']"
    PAGE_TITLE = "title"
    
    # Error messages
    ERROR_MESSAGE = ".error-message, .validation-summary-errors, [id*='error']"
    VALIDATION_SUMMARY = "#ValidationSummary1"
    
    # Loading indicators
    LOADING_INDICATOR = ".loading, #loading"


class MFAPageLocators:
    """Locators for MFA/One-time Passcode page elements."""
    
    # Page indicators
    MFA_HEADING = "h2:has-text('One‑time Passcode')"
    MFA_OPTIONS_FORM = "form[name='frmMFAMenuOptionPage']"
    
    # MFA options (to identify but not interact with)
    MOBILE_OPTION = "input[value='Mobile']"
    EMAIL_OPTION = "input[value='Email']"
    
    # Skip indicators
    MFA_URL_PATTERN = "/SalesCenter/mfa/frmMFAMenuOptionPage.aspx"


class DashboardPageLocators:
    """Locators for OSC Dashboard/Home page elements."""
    
    # Main page indicators
    HOME_HEADING = "h2:has-text('Home')"
    APPLICATION_SUMMARY_TEXT = "text=Application Summary"
    
    # Dashboard sections
    DASHBOARD_CONTAINER = "#content, .dashboard, .main-content"
    NAVIGATION_MENU = ".nav, #navigation, .menu"
    
    # Common dashboard elements
    USER_INFO = ".user-info, #userinfo"
    LOGOUT_LINK = "a:has-text('Logout'), a[href*='logout']"
    
    # Work sections
    WORK_IN_PROGRESS = "text=Work In Progress"
    APPLICATIONS_SECTION = "[id*='application'], .applications"


class NavigationLocators:
    """Common navigation elements across OSC pages."""
    
    # Top navigation
    HOME_LINK = "a[href*='frmHome']"
    LOGOUT_LINK = "a[href*='logout'], a:has-text('Logout')"
    
    # Menu items
    MENU_CONTAINER = ".menu, #menu, .navigation"
    
    # Breadcrumbs
    BREADCRUMB = ".breadcrumb, #breadcrumb"