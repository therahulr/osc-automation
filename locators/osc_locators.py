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


class NewApplicationPageLocators:
    """Locators for the New Application page - Application Information section"""
    
    # Application Information Section
    APPLICATION_INFO_SECTION = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_lblTitle"
    
    # Office (display only - dynamic xpath)
    OFFICE_DISPLAY = "//span[normalize-space(.)='{office_name}']"
    
    # Phone (display only)
    PHONE_DISPLAY = "//span[contains(text(), '{phone}')]"
    
    # Contractor (display only - dynamic xpath)
    CONTRACTOR_DISPLAY = "//span[normalize-space(text())='{contractor_name}']"
    
    # Association dropdown
    ASSOCIATION_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlAssociation"
    ASSOCIATION_DROPDOWN_ALT = "//select[@name='ctl00$ContentPlaceHolder1$ctrlApplicationInfo1$FormView1$ddlAssociation']"
    ASSOCIATION_OPTION = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlAssociation']/option[normalize-space(.)='{association_name}']"
    
    # Lead Source dropdown
    LEAD_SOURCE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlLeadSource"
    LEAD_SOURCE_DROPDOWN_ALT = "//select[@name='ctl00$ContentPlaceHolder1$ctrlApplicationInfo1$FormView1$ddlLeadSource']"
    LEAD_SOURCE_OPTION = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlLeadSource']/option[normalize-space(.)='{lead_source_name}']"
    
    # Referral Partner dropdown
    REFERRAL_PARTNER_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlReferralPartner"
    REFERRAL_PARTNER_DROPDOWN_ALT = "//select[@name='ctl00$ContentPlaceHolder1$ctrlApplicationInfo1$FormView1$ddlReferralPartner']"
    REFERRAL_PARTNER_OPTION = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlReferralPartner']/option[normalize-space(.)='{referral_partner_name}']"
    
    # Promo Code input
    PROMO_CODE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtPromoCode"
    PROMO_CODE_INPUT_ALT = "//input[@name='ctl00$ContentPlaceHolder1$ctrlApplicationInfo1$FormView1$txtPromoCode']"
    
    # Corporate Atlas ID input
    CORPORATE_ATLAS_ID_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtCorpAtlasID"
    CORPORATE_ATLAS_ID_INPUT_ALT = "//input[@name='ctl00$ContentPlaceHolder1$ctrlApplicationInfo1$FormView1$txtCorpAtlasID']"