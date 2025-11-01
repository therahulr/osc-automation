"""OSC Application Locators - Organized by page classes with optimized selectors."""

from typing import Literal, Tuple

# Type alias for locator strategies
LocatorStrategy = Literal["id", "name", "css", "xpath", "text", "role"]
Locator = Tuple[LocatorStrategy, str] | str


class LoginPageLocators:
    """Locators for OSC Login page elements."""
    
    # Main form elements
    USERNAME_FIELD = ("id", "txtUsername")
    PASSWORD_FIELD = ("id", "txtPassword")  
    LOGIN_BUTTON = ("id", "btnLogin")
    
    # Alternative selectors for redundancy
    USERNAME_FIELD_ALT = ("name", "txtUsername")
    PASSWORD_FIELD_ALT = ("name", "txtPassword") 
    LOGIN_BUTTON_ALT = ("name", "btnLogin")
    
    # Page indicators
    PAGE_TITLE = "Sales Center"
    LOGIN_FORM_HEADING = "text=Login"
    
    # Error handling
    ERROR_MESSAGE = ".error-message, .validation-summary-errors, [id*='error']"


class MFAPageLocators:
    """Locators for MFA/One-time Passcode page elements."""
    
    # Page indicators
    MFA_HEADING = "text=One-time Passcode"
    MFA_DESCRIPTION = "text=Please select how you want us to deliver your one-time passcode"
    
    # MFA options
    MOBILE_OPTION_TEXT = "text=Mobile : ********4415"
    EMAIL_OPTION_TEXT = "text=Email : r********@nuvei.com"
    
    # Buttons
    CANCEL_BUTTON = "button:has-text('Cancel')"
    NEXT_BUTTON = "button:has-text('Next')"
    
    # URL pattern for detection
    MFA_URL_PATTERN = "/SalesCenter/mfa/"


class DashboardPageLocators:
    """Locators for OSC Dashboard/Home page elements."""
    
    # Main page indicators
    HOME_HEADING = "text=Home"
    APPLICATION_SUMMARY_HEADING = "text=Application Summary"
    
    # Navigation menu
    HOME_LINK = "link=Home"
    APPLICATIONS_LINK = "link=Applications"
    LIBRARY_LINK = "link=Library"
    REPORTING_LINK = "link=Reporting"
    
    # User info
    OFFICE_INFO = "text=[Office 907861-DEMO NET1]"
    LOGOUT_LINK = "text=Logout"
    
    # Dashboard content
    CONTRACTOR_DROPDOWN = "combobox"
    USER_LEVEL_TEXT = "text=Level: 3 - Admin"
    
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