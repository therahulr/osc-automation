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
    # Top Menu Navigation
    APPLICATIONS_MENU = "//a[text()='Applications']"
    NEW_APPLICATION_LINK = "//a[text()='New Application']"
    
    # Step 1 - Sales Representative Selection
    TABLE_ROWS = "//table//tr[td]"
    STEP1_NEXT_BUTTON = "#ctl00_ContentPlaceHolder2_NewAppWizard_StartNavigationTemplateContainerID_StartNextButton"
    
    # Step 2 - Existing Merchant Selection
    NEW_CORPORATION_RADIO = "#ctl00_ContentPlaceHolder2_NewAppWizard_rdExistingMechList_1"
    STEP2_NEXT_BUTTON = "#ctl00_ContentPlaceHolder2_NewAppWizard_StepNavigationTemplateContainerID_StepNextButton"
    
    # Step 3 - New Application Page
    APPLICATION_INFORMATION_HEADER = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_lblTitle"


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