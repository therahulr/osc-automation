"""
OSC Application Locators - Clean, DOM-inspected selectors only.
"""

from typing import Literal, Tuple

LocatorStrategy = Literal["id", "name", "css", "xpath", "text", "role"]
Locator = Tuple[LocatorStrategy, str] | str


class LoginPageLocators:
    FORM = "#form1"
    USERNAME_FIELD = "#txtUsername"
    PASSWORD_FIELD = "#txtPassword"
    LOGIN_BUTTON = "#btnLogin"
    PAGE_HEADING = "h1"
    FORGOT_PASSWORD_LINK = "//a[contains(text(), 'Forgot your password?')]"
    LOGIN_URL_PATTERN = "/SalesCenter/"


class NavigationLocators:
    TABLE_ROWS = "//table//tr[td]"
    NEXT_BUTTON_TEXT = "Next"
    NEW_CORPORATION_TEXT = "new corporation"


class MFAPageLocators:
    FORM = "#form1"
    HEADING = "//h2[text()='One-time Passcode']"
    MOBILE_OPTION = "//div[@class='mfa-card-new'][.//img[@alt='SMS']]"
    EMAIL_OPTION = "//div[@class='mfa-card-new'][.//img[@alt='EMAIL']]"
    MOBILE_SPAN = "#spanMobile"
    CANCEL_BUTTON = "#btnCancel"
    NEXT_BUTTON = "#btnNext"
    MFA_TYPE_FIELD = "#hdmfaType"
    MFA_URL_PATTERN = "/SalesCenter/mfa/frmMFAMenuOptionPage.aspx"


class DashboardPageLocators:
    pass