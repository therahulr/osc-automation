"""OSC Application Locators - Organized by page classes with optimized selectors."""

from typing import Literal, Tuple

# Type alias for locator strategies
LocatorStrategy = Literal["id", "name", "css", "xpath", "text", "role"]
Locator = Tuple[LocatorStrategy, str] | str


class LoginPageLocators:
    """Locators for OSC Login page elements - VERIFIED with real browser inspection."""
    
    # Main form elements - VERIFIED: Real selectors from live application
    USERNAME_FIELD = ("id", "txtUsername")  # Verified: input#txtUsername
    PASSWORD_FIELD = ("id", "txtPassword")  # Verified: input#txtPassword  
    LOGIN_BUTTON = ("id", "btnLogin")       # Verified: input#btnLogin[type="submit"]
    
    # Alternative selectors for redundancy
    USERNAME_FIELD_ALT = ("name", "txtUsername")
    PASSWORD_FIELD_ALT = ("name", "txtPassword") 
    LOGIN_BUTTON_ALT = ("name", "btnLogin")
    
    # Page indicators - VERIFIED
    PAGE_TITLE = "Sales Center"  # Verified: Page title
    LOGIN_FORM_HEADING = "text=Login"  # Verified: Login text on page
    
    # Error handling
    ERROR_MESSAGE = ".error-message, .validation-summary-errors, [id*='error']"


class MFAPageLocators:
    """Locators for MFA/One-time Passcode page elements - VERIFIED with real browser inspection."""
    
    # Page indicators - VERIFIED
    MFA_HEADING = "text=One-time Passcode"  # Verified: h2 with text "One-time Passcode"
    MFA_DESCRIPTION = "text=Please select how you want us to deliver your one-time passcode"
    
    # MFA options - VERIFIED from browser inspection
    MOBILE_OPTION_TEXT = "text=Mobile : ********4415"  # Verified in snapshot
    EMAIL_OPTION_TEXT = "text=Email : r********@nuvei.com"  # Verified in snapshot
    
    # Buttons - VERIFIED
    CANCEL_BUTTON = "button:has-text('Cancel')"  # Verified in snapshot
    NEXT_BUTTON = "button:has-text('Next')"      # Verified in snapshot (disabled)
    
    # URL pattern for detection
    MFA_URL_PATTERN = "/SalesCenter/mfa/"


class DashboardPageLocators:
    """Locators for OSC Dashboard/Home page elements - VERIFIED with real browser inspection."""
    
    # Main page indicators - VERIFIED from live application
    HOME_HEADING = "text=Home"  # Verified: h2 with text "Home"
    APPLICATION_SUMMARY_HEADING = "text=Application Summary"  # Verified: h4 heading
    
    # Navigation menu - VERIFIED
    HOME_LINK = "link=Home"          # Verified in nav
    APPLICATIONS_LINK = "link=Applications"  # Verified in nav
    LIBRARY_LINK = "link=Library"    # Verified in nav
    REPORTING_LINK = "link=Reporting"  # Verified in nav
    
    # User info - VERIFIED
    OFFICE_INFO = "text=[Office 907861-DEMO NET1]"  # Verified text
    LOGOUT_LINK = "text=Logout"      # Verified link text (use text= instead of link=)
    
    # Dashboard content - VERIFIED
    CONTRACTOR_DROPDOWN = "combobox"  # Verified: Contractor selection dropdown
    USER_LEVEL_TEXT = "text=Level: 3 - Admin"  # Verified user level text
    
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