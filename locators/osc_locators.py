"""
OSC Application Locators - Clean, DOM-inspected selectors only.
"""

from typing import Literal, Tuple

LocatorStrategy = Literal["id", "name", "css", "xpath", "text", "role"]
Locator = Tuple[LocatorStrategy, str] | str


class CommonLocators:
    """Common locators used across the application"""
    
    # Success/Error Toast Notifications
    SUCCESS_ALERT = "//div[@id='myAlert' and contains(@class,'alert-success')]"
    ERROR_ALERT = "//div[@id='myAlert' and contains(@class,'alert-danger')]"
    WARNING_ALERT = "//div[@id='myAlert' and contains(@class,'alert-warning')]"
    INFO_ALERT = "//div[@id='myAlert' and contains(@class,'alert-info')]"


class LoginPageLocators:
    FORM = "#form1"
    USERNAME_FIELD = "#txtUsername"
    PASSWORD_FIELD = "#txtPassword"
    LOGIN_BUTTON = "#btnLogin"
    PAGE_HEADING = "h1"
    FORGOT_PASSWORD_LINK = "//a[contains(text(), 'Forgot your password?')]"
    LOGIN_URL_PATTERN = "/SalesCenter/"

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
    """Locators for the OSC Dashboard/Home page"""

    # ============================
    # HEADER SECTION
    # ============================
    USER_INFO_TEXT = "//span[@id='ctl00_txtUserInfo']"
    LOGOUT_LINK = "//a[text()='Logout']"

    # ============================
    # PAGE TITLE & HEADERS
    # ============================
    PAGE_MAIN_HEADING = "//h1[text()='Sales Center']"
    HOME_SECTION_HEADING = "//h1[text()='Home']"
    APPLICATION_SUMMARY_HEADING = "//h2[contains(text(),'Application Summary')] | //h3[contains(text(),'Application Summary')]"
    CONTRACTOR_NAME = "#ctl00_ContentPlaceHolder2_lblContractorName"
    LEVEL_VALUE = "#ctl00_ContentPlaceHolder2_txtLevel"
    TEMPLATE_VALUE = "#ctl00_ContentPlaceHolder2_txtTemplate"

    # ============================
    # TOP MENU NAVIGATION
    # ============================
    MENU_HOME = "//ul[@class='nav']//a[text()='Home']"
    MENU_APPLICATIONS = "//ul[@class='nav']//a[text()='Applications']"
    MENU_LIBRARY = "//ul[@class='nav']//a[text()='Library']"
    MENU_REPORTING = "//ul[@class='nav']//a[text()='Reporting']"
    MENU_ACCOUNTING = "//ul[@class='nav']//a[text()='Accounting']"
    MENU_LINKS = "//ul[@class='nav']//a[text()='Links']"
    MENU_CONFIGURATION = "//ul[@class='nav']//a[text()='Configuration']"

    # Applications → Dropdown Items
    APPLICATIONS_WORK_IN_PROGRESS = "//a[text()='Work In Progress']"
    APPLICATIONS_NEW_APPLICATION = "//a[text()='New Application']"

    # Reporting → Dropdown Items
    REPORTING_MERCHANT_SEARCH = "//a[text()='Merchant Search']"
    REPORTING_T_E = "//a[text()='T&E']"
    REPORTING_PENDING = "//a[text()='Pending Merchants']"
    REPORTING_EQUIPMENT = "//a[text()='Equipment']"
    REPORTING_GATEWAY_LOAD = "//a[text()='Gateway Load']"
    REPORTING_LEAD_SOURCE = "//a[text()='Lead Source']"
    REPORTING_CHANGE_LOGS = "//a[text()='Merchant Change Logs']"
    REPORTING_ACH = "//a[text()='Commission ACH']"

    # Links → Dropdown Items
    LINKS_MY_VIRTUAL_REPORTS = "//a[text()='My Virtual Reports']"
    LINKS_CORPORATE = "//a[text()='Corporate']"

    # Configuration → Dropdown Items
    CONFIG_CHANGE_PASSWORD = "//a[text()='Change Password']"
    CONFIG_TEMPLATES = "//a[text()='Templates']"
    CONFIG_MFA_SETTINGS = "//a[text()='MFA Settings']"

    # ========================================
    # Home Page – Application Summary Section
    # ========================================
    
    # FILTER DROPDOWNS - Contractor and Product Filters
    FILTER_CONTRACTOR = "//select[contains(@id,'ddlAgent')]"
    FILTER_PRODUCT = "//select[contains(@id,'ddlProduct')]"

    # ============================
    # APPLICATION SUMMARY TABLE
    # ============================
    SUMMARY_TABLE = "//table[contains(@class,'table')]"
    SUMMARY_ROWS = "//table[contains(@class,'table')]//tr"
    SUMMARY_STATUS_CELL = "//table[contains(@class,'table')]//tr/td[1]"

    # ================================================================================
    # Dynamic locator for application summary links based on status name and timeframe
    # Example: xpath = get_app_summary_link("Declined", "Lifetime")
    # ================================================================================

    def GET_APP_SUMMARY_LINK(status_name: str, timeframe: str):
        return (
            f"//table[contains(@id,'GridView1')]//tr[td[1][normalize-space()='{status_name}']]"
            f"//td[count(//table[contains(@id,'GridView1')]//th"
            f"[normalize-space()='{timeframe}']/preceding-sibling::th)+1]//a"
        )

    # ============================
    # FOOTER LINKS
    # ============================

    # ----- HOME -----
    FOOTER_HOME = "//div[@class='row-fluid']//a[text()='Home']"

    # ----- APPLICATIONS -----
    FOOTER_WORK_IN_PROGRESS = "//div[@class='row-fluid']//a[text()='Work In Progress']"
    FOOTER_NEW_APPLICATION = "//div[@class='row-fluid']//a[text()='New Application']"

    # ----- LIBRARY -----
    FOOTER_LIBRARY = "//div[@class='row-fluid']//a[text()='Library']"

    # ----- REPORTING -----
    FOOTER_MERCHANT_SEARCH = "//div[@class='row-fluid']//a[text()='Merchant Search']"
    FOOTER_T_E = "//div[@class='row-fluid']//a[text()='T&E']"
    FOOTER_PENDING_MERCHANTS = "//div[@class='row-fluid']//a[text()='Pending Merchants']"
    FOOTER_EQUIPMENT = "//div[@class='row-fluid']//a[text()='Equipment']"
    FOOTER_GATEWAY_LOAD = "//div[@class='row-fluid']//a[text()='Gateway Load']"
    FOOTER_LEAD_SOURCE = "//div[@class='row-fluid']//a[text()='Lead Source']"
    FOOTER_MERCHANT_CHANGE_LOG = "//div[@class='row-fluid']//a[text()='Merchant Change Log']"
    FOOTER_COMMISSION_ACH = "//div[@class='row-fluid']//a[text()='Commission ACH']"

    # ----- ACCOUNTING -----
    FOOTER_ACCOUNTING = "//div[@class='row-fluid']//a[text()='Accounting']"

    # ----- LINKS -----
    FOOTER_MY_VIRTUAL_REPORTS = "//div[@class='row-fluid']//a[text()='My Virtual Reports']"
    FOOTER_CORPORATE = "//div[@class='row-fluid']//a[text()='Corporate']"

    # ----- CONFIGURATION -----
    FOOTER_CHANGE_PASSWORD = "//div[@class='row-fluid']//a[text()='Change Password']"
    FOOTER_TEMPLATES = "//div[@class='row-fluid']//a[text()='Templates']"


class Step1SalesRepLocators:
    STEP1_HEADING = "//h3[normalize-space()='Step 1: Sales Representative']"
    STEP1_INFO_TEXT = "//p[contains(@class, 'text-info')]"

    # Filters
    FILTER_ALL = "//ul[@id='ulLetters']//a[normalize-space()='All']"
    FILTER_BY_LETTER = lambda letter: f"//ul[@id='ulLetters']//a[normalize-space()='{letter.upper()}']"
    # Example - locator = FILTER_BY_LETTER('J')

    # Contractor table
    CONTRACTOR_TABLE = "//table[@id='ctl00_ContentPlaceHolder2_NewAppWizard_ContractorGrid']"
    CONTRACTOR_ROWS = "//table[@id='ctl00_ContentPlaceHolder2_NewAppWizard_ContractorGrid']//tr[td]"

    # Pagination
    PAGINATION_PAGE_1 = "//table[@id='ctl00_ContentPlaceHolder2_NewAppWizard_ContractorGrid']//span[normalize-space()='1']"
    PAGINATION_PAGE_2 = "//table[@id='ctl00_ContentPlaceHolder2_NewAppWizard_ContractorGrid']//a[normalize-space()='2']"

    # Dynamic sales rep selection
    SELECT_REP_CHECKBOX = lambda rep_name: (
        f"//table[@id='ctl00_ContentPlaceHolder2_NewAppWizard_ContractorGrid']"
        f"//tr[td[1][normalize-space()='{rep_name}']]//input[@type='checkbox']"
    )
    # Example - locator = SELECT_REP_CHECKBOX("DEMONET1")


    # Next button
    STEP1_NEXT_BUTTON = "//input[@id='ctl00_ContentPlaceHolder2_NewAppWizard_StartNavigationTemplateContainerID_StartNextButton']"

    # OPTIONAL ALTERNATIVE FOR PAGINATION
    def GET_PAGINATION_LINK(page_no: int):
        return (
            f"//table[@id='ctl00_ContentPlaceHolder2_NewAppWizard_ContractorGrid']"
            f"//td[@colspan='4']//table//tr/td//*[self::a or self::span][normalize-space()='{page_no}']"
        )
    # Example - locator = GET_PAGINATION_LINK(2)

class Step2ExistingMerchantLocators:
    # Page heading and description
    STEP2_HEADING = "//h3[normalize-space()='Step 2: Existing Merchant']"
    STEP2_DESCRIPTION = "//p[contains(@class,'text-info')]"

    # Radio options
    EXISTING_MERCHANT_YES = "#ctl00_ContentPlaceHolder2_NewAppWizard_rdExistingMechList_0"
    EXISTING_MERCHANT_NO = "#ctl00_ContentPlaceHolder2_NewAppWizard_rdExistingMechList_1"

    # Navigation buttons
    STEP2_PREVIOUS_BUTTON = "#ctl00_ContentPlaceHolder2_NewAppWizard_StepNavigationTemplateContainerID_StepPreviousButton"
    STEP2_NEXT_BUTTON = "#ctl00_ContentPlaceHolder2_NewAppWizard_StepNavigationTemplateContainerID_StepNextButton"

class NewApplicationPageLocators:

    PAGE_TITLE = "//span[@id='ctl00_ContentPlaceHolder1_lblTitle' and contains(text(),'Sales Center - Application')]"
    APPLICATION_INFO_SECTION = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_lblTitle"

    # ============================================
    # APPLICATION FORM - HEADER ACTION MENU
    # ============================================
    BTN_SAVE = "//a[@id='ctl00_ContentPlaceHolder1_btnSave']"
    BTN_VALIDATE = "//a[@id='ctl00_ContentPlaceHolder1_btnValidate']"
    BTN_SUBMIT = "//a[@id='ctl00_ContentPlaceHolder1_btnSubmit']"
    BTN_ADD_DOCUMENTS = "//a[@id='ctl00_ContentPlaceHolder1_btnAddDocument']"
    BTN_SEND_FOR_SIGNATURE = "//a[@id='ctl00_ContentPlaceHolder1_btnSendForSignature']"

    BTN_ORDERS = "//a[@id='ctl00_ContentPlaceHolder1_btnOrders']"
    BTN_PRINT_CREDIT = "//a[@id='ctl00_ContentPlaceHolder1_btnPrintCredit']"
    BTN_PRINT_ACH = "//a[@id='ctl00_ContentPlaceHolder1_btnPrintACH']"

    # ============================================
    # PRODUCT BUTTONS
    # ============================================
    PRODUCT_BTN_CREDIT_CARD = "//input[@id='ctl00_ContentPlaceHolder1_rptrProducts_ctl00_btnProduct']"
    PRODUCT_BTN_EFT = "//input[@id='ctl00_ContentPlaceHolder1_rptrProducts_ctl01_btnProduct']"
    PRODUCT_BTN_DEBIT_CARD = "//input[@id='ctl00_ContentPlaceHolder1_rptrProducts_ctl02_btnProduct']"
    PRODUCT_BTN_EBT = "//input[@id='ctl00_ContentPlaceHolder1_rptrProducts_ctl03_btnProduct']"
    PRODUCT_BTN_ACH = "//input[@id='ctl00_ContentPlaceHolder1_rptrProducts_ctl04_btnProduct']"

    # ============================================
    # VALIDATION ERRORS
    # ============================================
    VALIDATION_ERRORS_CONTAINER = "//div[@id='divErrors' and contains(@class,'alert-error')]"
    VALIDATION_ERROR_ITEMS = "//div[@id='divErrors']//ul/li"
    ERROR_CLOSE_BTN = "//div[@id='divErrors']//button[@class='close']"
    ERROR_HEADER = "//div[@id='divErrors']//h4[contains(text(),'Did you forget something?')]"
    
    # ============================================
    # SUCCESS TOAST NOTIFICATIONS
    # ============================================
    SUCCESS_TOAST = "//div[@id='myAlert' and contains(@class,'alert-success')]"
    SUCCESS_TOAST_MESSAGE = "//div[@id='myAlert' and contains(@class,'alert-success')]/div"
    
    # Legacy alias for backward compatibility
    ERROR_CONTAINER = "//div[@id='divErrors' and contains(@class,'alert-error')]"


class ApplicationInformationLocators:
    # -------- Section Header --------
    SECTION_TITLE = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_lblTitle' and text()='Application Information']"

    # -------- Static Display Fields (get text) --------
    OFFICE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_lblOffice']"
    OFFICE_VALUE = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtOffice']"

    PHONE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_lblPhone']"
    PHONE_VALUE = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtPhone']"

    CONTRACTOR_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_lblContractor']"
    CONTRACTOR_VALUE = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtContractor']"

    # -------- Dropdowns (select elements) --------
    ASSOCIATION_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlAssociation"
    LEAD_SOURCE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlLeadSource"
    REFERRAL_PARTNER_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlReferralPartner"

    # Individual dropdown option locators (optional but useful)
    ASSOCIATION_OPTION = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlAssociation']/option"
    LEAD_SOURCE_OPTION = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlLeadSource']/option"
    REFERRAL_PARTNER_OPTION = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_ddlReferralPartner']/option"

    # -------- Input fields --------
    PROMO_CODE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtPromoCode"
    CORP_ATLAS_ID_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationInfo1_FormView1_txtCorpAtlasID"


class CorporateInformationLocators:

    # ---- Section Header ----
    CORPORATE_INFORMATION_SECTION = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_lblTitle' "
        "and text()='Corporate Information']"
    )

    # ---- Input Fields ----
    LEGAL_BUSINESS_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpName"
    ADDRESS_LINE_1_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpAddress1"
    CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpCity"
    ZIP_CODE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpZip"
    PHONE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpPhone"
    FAX_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpFax"
    EMAIL_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpEmail"
    DUNNS_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtDunnBradNum"
    CONTACT_TITLE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpContactTitle"
    CONTACT_FIRST_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpContactFirstName"
    CONTACT_LAST_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpContactLastName"

    # ---- Dropdowns ----
    STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_ddlCorpState"
    COUNTRY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_ddlCorpCountry"
    
    STATE_DROPDOWN_OPTIONS = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_ddlCorpState']/option"
    COUNTRY_DROPDOWN_OPTIONS = "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_ddlCorpCountry']/option"

    LOCATION_SAME_ADDRESS_RADIO = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_rblAddress_0"
    LOCATION_DIFFERENT_ADDRESS_RADIO = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_rblAddress_1"



class LocationInformationLocators:

    SECTION_LOCATION_INFORMATION = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_lblTitle' "
        "and text()='Location Information']"
    )

    DBA_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBA']"
    DBA_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtDBA"

    ADDRESS_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBAAddress1']"
    ADDRESS_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtDBAAddress1"

    CITY_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBACity']"
    CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtDBACity"

    STATE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBAState']"
    STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_ddlDBAState"
    STATE_DROPDOWN_OPTIONS = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_ddlDBAState']/option"
    )

    ZIP_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBAZip']"
    ZIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtDBAZip"

    COUNTRY_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBACountry']"
    COUNTRY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_ddlDBACountry"
    COUNTRY_DROPDOWN_OPTIONS = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_ddlDBACountry']/option"
    )

    PHONE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBAPhone']"
    PHONE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtDBAPhone"

    FAX_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblDBAFax']"
    FAX_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtDBAFax"

    CUSTOMER_SERVICE_PHONE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblCustomerServicePhone']"
    CUSTOMER_SERVICE_PHONE_INPUT = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtCustomerServicePhone"
    )

    WEBSITE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblLocURL']"
    WEBSITE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtLocURL"

    EMAIL_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblLocEmail']"
    EMAIL_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtLocEmail"

    CHARGEBACK_EMAIL_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblChaEmail']"
    CHARGEBACK_EMAIL_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtChaEmail"

    BUSINESS_OPEN_DATE_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblBusOpenDate']"
    
    BUSINESS_OPEN_DATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtBusOpenDate"

    EXISTING_MID_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblMerchID']"
    EXISTING_MID_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtMerchID"

    GENERAL_COMMENTS_LABEL = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_lblGeneralComment']"
    GENERAL_COMMENTS_TEXTAREA = "#ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_txtGeneralComment"

    # ---- Dynamic Locators ----
    SELECT_STATE_BY_NAME = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_ddlDBAState']"
        "/option[text()='{}']"
    )

    SELECT_COUNTRY_BY_NAME = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationLocation1_FormView1_ddlDBACountry']"
        "/option[text()='{}']"
    )


class TaxInformationLocators:
    """Tax Information section locators"""
    
    # Section Header
    SECTION_TITLE = "//span[contains(text(), 'Tax Information')]"
    
    # Federal Tax ID (masked input)
    FEDERAL_TAX_ID_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_txtFedTaxID"
    
    # Tax Filing Corporation Name
    TAX_FILING_CORP_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_txtTaxFilCorp"
    
    # Ownership Type dropdown
    OWNERSHIP_TYPE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_ddlCorpType"
    
    # Tax Filing State dropdown
    TAX_FILING_STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_ddlTaxFilState"
    
    # Checkboxes
    LOCATION_IS_CORP_HQ_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_ckbCorpHead"
    FOREIGN_ENTITY_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_ckbCertForeign"
    AUTHORIZE_1099_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationTaxInfo1_FormView1_ckbAuth"


class Owner1Locators:
    TITLE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerTitle"
    FIRST_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerFName"
    LAST_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerLName"
    ADDRESS1_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerAddress1"
    ADDRESS2_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerAddress2"
    CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerCity"
    STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_ddlOwnerState"
    ZIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerZip"
    COUNTRY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_ddlOwnerCountry"
    PHONE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerPhoneNumber"
    FAX_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerFaxNumber"
    EMAIL_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerEmail"
    DOB_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerDOB"
    SSN_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerSSN"
    DATE_OF_OWNERSHIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerLength"
    EQUITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner1_FormView1_txtOwnerEquity"


class Owner2Locators:
    TITLE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerTitle"
    FIRST_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerFName"
    LAST_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerLName"
    ADDRESS1_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerAddress1"
    ADDRESS2_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerAddress2"
    CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerCity"
    STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_ddlOwnerState"
    ZIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerZip"
    COUNTRY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_ddlOwnerCountry"
    PHONE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerPhoneNumber"
    FAX_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerFaxNumber"
    EMAIL_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerEmail"
    DOB_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerDOB"
    SSN_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerSSN"
    DATE_OF_OWNERSHIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerLength"
    EQUITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationOwner2_FormView1_txtOwnerEquity"


class TradeReferenceLocators:
    TITLE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferenceTitle"
    NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferenceName"
    ADDRESS_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferenceAddress"
    CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferenceCity"
    STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_ddlReferenceState"
    ZIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferenceZip"
    COUNTRY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_ddlReferenceCountry"
    PHONE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferencePhone"
    EMAIL_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationTradeReference1_FormView1_txtReferenceEmail"

class GeneralUnderwritingLocators:
    BUSINESS_TYPE_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_ddlBusinessLevel"
    )

    SIC_CODE_INPUT = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_txtSICCode"
    )
    
    # SIC Code autocomplete dropdown (jQuery UI autocomplete)
    SIC_CODE_AUTOCOMPLETE_DROPDOWN = "ul.ui-autocomplete"
    SIC_CODE_AUTOCOMPLETE_ITEM = "ul.ui-autocomplete li.ui-menu-item div.ui-menu-item-wrapper"

    PRODUCTS_SOLD_TEXTAREA = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_txtProduct"
    )

    RETURN_POLICY_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_ddlReturnPolicy"
    )

    DAYS_UNTIL_PRODUCT_DELIVERY_INPUT = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_txtDaysUntilProductDelivery"
    )

    # ------- Seasonal Months Checkboxes (January – December) -------
    SEASONAL_MONTH_JANUARY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl02_ckbMonth"
    )
    SEASONAL_MONTH_FEBRUARY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl03_ckbMonth"
    )
    SEASONAL_MONTH_MARCH_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl04_ckbMonth"
    )
    SEASONAL_MONTH_APRIL_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl05_ckbMonth"
    )
    SEASONAL_MONTH_MAY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl06_ckbMonth"
    )
    SEASONAL_MONTH_JUNE_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl07_ckbMonth"
    )
    SEASONAL_MONTH_JULY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl08_ckbMonth"
    )
    SEASONAL_MONTH_AUGUST_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl09_ckbMonth"
    )
    SEASONAL_MONTH_SEPTEMBER_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl10_ckbMonth"
    )
    SEASONAL_MONTH_OCTOBER_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl11_ckbMonth"
    )
    SEASONAL_MONTH_NOVEMBER_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl12_ckbMonth"
    )
    SEASONAL_MONTH_DECEMBER_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationUnderwriting1_FormView1_gvSeasonalMonths_ctl13_ckbMonth"
    )


class BillingQuestionnaireLocators:

    # ---- Type of Merchant (Radio Buttons) ----
    MERCHANT_TYPE_INTERNET_RADIO = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_rbtnInternet"
    )
    MERCHANT_TYPE_MOTO_RADIO = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_rbtnMoto"
    )
    MERCHANT_TYPE_RETAIL_RADIO = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_rbtnRetail"
    )

    # ---- Full Payment Upfront ----
    FULL_PAYMENT_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkFullPayment"
    )
    FULL_PAYMENT_DAYS_INPUT = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_txtFullPaymentDays"
    )

    # ---- Partial Payment Upfront ----
    PARTIAL_PAYMENT_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkPartialPayment"
    )
    PARTIAL_PAYMENT_PERCENTAGE_INPUT = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_txtPartialPaymentPercentage"
    )
    PARTIAL_PAYMENT_DAYS_INPUT = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_txtPartialPaymentDays"
    )

    # ---- Payment Received After Delivery ----
    PAYMENT_RECEIVED_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkPaymentReceived"
    )

    # ---- Recurring Billing Options ----
    BILLING_MONTHLY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkMonthly"
    )
    BILLING_QUARTERLY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkQuarterly"
    )
    BILLING_SEMI_ANNUALLY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkSemiAnnually"
    )
    BILLING_ANNUALLY_CHECKBOX = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_chkAnnually"
    )

    # ---- Outsourced to Third Party ----
    OUTSOURCED_YES_RADIO = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_rbtnYes"
    )
    OUTSOURCED_NO_RADIO = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_rbtnNo"
    )

    # ---- Explanation Text ----
    OUTSOURCED_EXPLANATION_TEXTAREA = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationBillingQuestionnaire1_FormView1_txtExplain"
    )

class BankInformationLocators:

    # ---- Bank Basic Details ----
    BANK_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtBankName"
    BANK_ADDRESS1_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtAddress1"
    BANK_ADDRESS2_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtAddress2"
    BANK_CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtCity"
    BANK_STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_ddlState"
    BANK_ZIP_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtZip"
    BANK_COUNTRY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_ddlCountry"
    BANK_PHONE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtPhoneNumber"

    # ---- Depository Account (Credit) ----
    DEPOSITORY_ROUTING_NUMBER_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtCreditRoutingNumber"
    DEPOSITORY_ACCOUNT_NUMBER_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtCreditAccountNumber"
    DEPOSITORY_ROUTING_VERIFY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtVerifyCreditRouting"
    DEPOSITORY_ACCOUNT_VERIFY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtVerifyCreditAccount"

    # ---- Fee Account (Debit) ----     
    FEE_ROUTING_NUMBER_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtDebitRoutingNumber"
    FEE_NUMBER_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtDebitAccountNumber"
    FEE_ROUTING_VERIFY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtVerifyDebitRouting"
    FEE_VERIFY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationBank1_FormView1_txtVerifyDebitAccount"

class CreditCardInformationLocators:

    AUTHORIZATION_NETWORK_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_FormView1_ddlFrontEnd"
    )

    SETTLEMENT_BANK_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_FormView1_ddlSettlementBank"
    )

    SETTLEMENT_NETWORK_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_FormView1_ddlBackEnd"
    )

    DISCOUNT_PAID_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_FormView1_ddlDiscountPaid"
    )

    USER_BANK_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_FormView1_ddlUserBank"
    )

class ServiceSelectionLocators:
    """
    Locators for the Service Selection section of the application.
    Pass in the service name to get the corresponding checkbox locator.
    """

    CREDIT_CARD_SERVICES_HEADER_TEXT = "ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_Label3"
    def SERVICE_CHECKBOX_LOCATOR(service_name: str) -> str:
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_GridView1']"
            f"//tr[td//span[normalize-space(text())='{service_name}']]"
            f"//input[@type='checkbox']"
        )

class CreditCardUnderwritingLocators:

    # ===== Section Heading =====
    SECTION_CREDIT_CARD_UNDERWRITING = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_Label1' and text()='Credit Card Underwriting']"

    # ===== Row 1 =====
    MONTHLY_VOLUME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtMonthlyVolume"
    CARD_PRESENT_SWIPED_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlCardPresentSwiped"
    SALES_TO_CONSUMER_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlSalesToConsumer"

    # ===== Row 2 =====
    AVERAGE_TICKET_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtAverageTicket"
    CARD_PRESENT_KEYED_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlCardPresentImprint"
    BUSINESS_SALES_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlBusToBus"

    # ===== Row 3 =====
    HIGHEST_TICKET_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtMaxSalesAmt"
    CARD_NOT_PRESENT_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlCardNotPresent"
    GOVERNMENT_SALES_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlSalesToGov"

    # ===== Totals =====
    CREDIT_TOTAL_1_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtCreditTotal1"
    CREDIT_TOTAL_2_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtCreditTotal2"

    # ===== Processor Info =====
    CURRENT_PROCESSOR_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtCurrentProcessor"

    # ===== Credit Card Interchange Sub-section =====
    SECTION_CREDIT_CARD_INTERCHANGE = "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_lblInterchangeTitle' and text()='Credit Card Interchange']"

    INTERCHANGE_TYPE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlBETInterchangeType"
    CHARGEBACK_BET_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlChargebackBET"
    FANF_TYPE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ddlFANFTypes"


    # ===== Visa Section =====
    VISA_BET_VALUE = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_lblVisaBET"
    VISA_BET_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_btnVisaBET"
    BET_MODAL = "//div[@id='divBetInterchange' and contains(@class,'in')]"

    def BET_CHECKBOX_BY_NUMBER(bet_no: str) -> str:
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_BETGridView']"
            f"//tr[td[2][normalize-space(text())='{bet_no}']]"
            "//input[contains(@id,'ckbSelected')]"
        )

    VISA_MATCH_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_btnVisaMatch"

    VISA_QUALIFIED_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtVisaDiscountQualifiedRate"
    VISA_DISCOUNT_PER_ITEM_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtVisaQualDiscount"

    VISA_SIGNATURE_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtVisaDiscountCheckcardRate"
    VISA_SIGNATURE_DISCOUNT_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtVisaCheckDiscount"

    # ===== MasterCard Section =====
    MC_BET_VALUE = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_lblMasterCardBET"
    MC_BET_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_btnMasterCardBET"
    MC_MATCH_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_btnMasterCardMatch"

    MC_QUALIFIED_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtMasterCardDiscountQualifiedRate"
    MC_DISCOUNT_PER_ITEM_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtMasterCardQualDiscount"

    MC_SIGNATURE_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtMasterCardDiscountCheckcardRate"
    MC_SIGNATURE_DISCOUNT_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtMasterCardCheckDiscount"


    # ===== Discover Section =====
    DISCOVER_BET_VALUE = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_lblDiscoverBET"
    DISCOVER_BET_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_btnDiscoverBET"

    DISCOVER_QUALIFIED_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtDiscoverDiscountQualifiedRate"
    DISCOVER_DISCOUNT_PER_ITEM_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtDiscoverQualDiscount"

    DISCOVER_SIGNATURE_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtDiscoverDiscountCheckcardRate"
    DISCOVER_SIGNATURE_DISCOUNT_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtDiscoverCheckDiscount"


    # ===== AMEX Section =====
    AMEX_BET_VALUE = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_lblBusinessLevel"
    AMEX_BET_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_btnAmexBusinessLevel"

    AMEX_QUALIFIED_RATE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtAmexDiscountQualifiedRate"
    AMEX_DISCOUNT_PER_ITEM_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtAmexQualDiscount"

    AMEX_NOT_ACCEPT_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ckbNotAcceptAmex"
    AMEX_OPTOUT_MARKETING_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_ckbOptOutMarket"
    AMEX_ANNUAL_VOLUME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_fvCreditUnderwriting_txtAmexAnnualVolume"


class PinDebitInterchangeLocators:

    PIN_DEBIT_INTERCHANGE_TYPE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlDebitCard1_FormView1_ddlDebitCard"


class TerminalWizardLocators:
    TERMINAL_WIZARD_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_aTerminalWizard"
    MODAL = "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard']"
    PROCESSING_BANNER = "//div[contains(@class,'alert-success') and normalize-space(text())='Processing...']"

    # ==================================================================
    # STEP 1 : MODAL
    # ==================================================================

    STEP_1_HEADER = (
        "//h4[contains(text(),'Step 1 of 6') and contains(text(),'Select Type')]"
    )
    STEP_1_PART_TYPE_DROPDOWN = "//select[contains(@id,'ddlPartType')]"
    STEP_1_PROVIDER_DROPDOWN = "//select[contains(@id,'ddlProvider')]"
    STEP_1_PART_CONDITION_DROPDOWN = "//select[contains(@id,'ddlPartCondition')]"

    @staticmethod
    def STEP_1_PART_TYPE_OPTION(option_text: str) -> str:
        """Select option only inside Part Type dropdown."""
        return (
            "//select[contains(@id,'ddlPartType')]"
            f"/option[normalize-space(text())='{option_text}']"
        )

    @staticmethod
    def STEP_1_PROVIDER_OPTION(option_text: str) -> str:
        """Select option only inside Provider dropdown."""
        return (
            "//select[contains(@id,'ddlProvider')]"
            f"/option[normalize-space(text())='{option_text}']"
        )

    @staticmethod
    def STEP_2_PART_CONDITION_OPTION(option_text: str) -> str:
        """Select option only inside Part Condition dropdown."""
        return (
            "//select[contains(@id,'ddlPartCondition')]"
            f"/option[normalize-space(text())='{option_text}']"
        )
    STEP_1_NEXT_BUTTON = (
        "//input[contains(@id,'StartNavigationTemplateContainerID_StartNextButton')]"
    )

    STEP_1_CANCEL_BUTTON = (
        "//input[contains(@id,'StartNavigationTemplateContainerID_CancelButton')]"
    )

    # ==================================================================
    # STEP 2 : MODAL
    # ==================================================================

    STEP_2_HEADING = "//h4[contains(text(), 'Step 2 of 6')]"

    # ===== Terminal Grid Table =====
    TERMINAL_GRID = "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_TerminalGrid']"
    TERMINAL_GRID_ROWS = TERMINAL_GRID + "//tr[td]"

    # ===== Dynamic Part ID Checkbox =====
    # Pass PartID as exact visible text (e.g., "PAX S300", "Commerce Suite")
    @staticmethod
    def STEP_2_PART_ID_CHECKBOX(part_id: str):
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_TerminalGrid']"
            f"//tr[td[2][normalize-space(text())='{part_id}']]"
            f"//input[contains(@id,'ckbSelectedPart')]"
        )

    # ===== Navigation Buttons =====
    STEP_2_PREVIOUS_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton"
    )

    STEP_2_NEXT_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_StepNextButton"
    )

    STEP_2_CANCEL_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_CancelButton"
    )

    # ==================================================================
    # STEP 3: MODAL
    # ==================================================================

    # ===== STEP 3 HEADING =====
    STEP_3_HEADING = "//h4[contains(text(), 'Step 3 of 6')]"

    # ===== INPUT FIELDS =====
    SERIAL_NUMBER_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtSerialNumber"
    MERCHANT_SALE_PRICE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtMerchantSalePrice"

    # ===== FILE BUILT BY (Dropdown) =====
    FILE_BUILT_BY_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlFileBuiltBy"

    # ===== SALES GROUP COST / MERCHANT COST CHECKBOX + INPUT PAIRS =====
    REPROGRAM_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ckbReProgram"
    REPROGRAM_FEE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtReprogramFee"

    WELCOME_KIT_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ckbWelcomeKitFee"
    WELCOME_KIT_FEE_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtWelcomeKitFee"

    # ===== NAVIGATION BUTTONS =====
    STEP_3_PREVIOUS_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton"
    )

    STEP_3_NEXT_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_StepNextButton"
    )

    STEP_3_CANCEL_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_CancelButton"
    )

    # ==================================================================
    # STEP 4: MODAL
    # ==================================================================

    STEP_4_HEADING = "//h4[contains(text(), 'Step 4 of 6')]"
    FRONT_END_PROCESSOR_DROPDOWN = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlFrontEndProcessor"
    )

    def STEP_4_SELECT_TERMINAL_PROGRAM_CHECKBOX(program_name: str):


        # ROW matching the Program Name
        row_xpath = (
            "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_TerminalApplicationGrid']"
            f"//tr[td[normalize-space(text())='{program_name}']]"
        )
        # Checkbox inside that row
        checkbox_xpath = row_xpath + "//input[contains(@id,'ckbSelectedProgram')]"

        return checkbox_xpath
    

    # ===== NAVIGATION BUTTONS =====
    STEP_4_PREVIOUS_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton"
    )

    STEP_4_NEXT_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_StepNextButton"
    )

    STEP_4_CANCEL_BUTTON = (
        "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_"
        "StepNavigationTemplateContainerID_CancelButton"
    )

    # ==================================================================
    # STEP 5: MODAL
    # ==================================================================
    
    STEP_5_HEADING = "//h4[normalize-space(text())='Step 5 of 6 : Enter Billing / Shipping Information']"
    
    # ============================
    # BILLING INFORMATION
    # ============================
    STEP_5_BILL_TO = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlBillTo"
    STEP_5_BILL = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtBill"
    STEP_5_BILL_CONTACT = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtContact"
    STEP_5_BILL_ADDRESS = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtAddress"
    STEP_5_BILL_ADDRESS2 = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtAddress2"
    STEP_5_BILL_CITY = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtCity"
    STEP_5_BILL_STATE = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtState"
    STEP_5_BILL_ZIP = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtZip"
    STEP_5_BILL_COUNTRY = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlCountryBillTo"
    STEP_5_BILL_PHONE = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtPhone"

    # ============================
    # SHIPPING INFORMATION
    # ============================
    STEP_5_SHIP_TO = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlShipTo"
    STEP_5_SHIP_METHOD = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlShipMethod"
    STEP_5_SHIP = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtShip"
    STEP_5_SHIP_CONTACT = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtContactShipTo"
    STEP_5_SHIP_ADDRESS = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtAddressShipTo"
    STEP_5_SHIP_ADDRESS2 = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtAddress2ShipTo"
    STEP_5_SHIP_CITY = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtCityShipTo"
    STEP_5_SHIP_STATE = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtStateShipTo"
    STEP_5_SHIP_ZIP = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtZipShipTo"
    STEP_5_SHIP_COUNTRY = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_ddlCountryShipTo"
    STEP_5_SHIP_PHONE = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_txtPhoneShipTo"

    # ============================
    # NAVIGATION
    # ============================
    STEP_5_PREVIOUS = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_StepNavigationTemplateContainerID_StepPreviousButton"
    STEP_5_NEXT = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_StepNavigationTemplateContainerID_StepNextButton"
    STEP_5_CANCEL = "ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_StepNavigationTemplateContainerID_CancelButton"

    # ==================================================================
    # STEP 6: FINAL STEP
    # ==================================================================
    
    STEP_6_HEADING = "//h4[normalize-space(text())='Step 6 of 6 : Review']"

    STEP_6_TERMINAL_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblTerminalReview']"
    )

    STEP_6_SERIAL_NUMBER_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblSN']"
    )

    STEP_6_TOTAL_SALES_PRICE_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblSalesPriceReview']"
    )

    STEP_6_SHIP_METHOD_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblShipMethodReview']"
    )

    STEP_6_BILL_TO_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblBillToReview']"
    )

    STEP_6_SHIP_TO_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblShipToReview']"
    )

    STEP_6_CONTACT_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_lblBilltoContactReview']"
    )

    # Navigation buttons
    STEP_6_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_FinishNavigationTemplateContainerID_FinishPreviousButton']"
    )

    STEP_6_FINISH_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_FinishNavigationTemplateContainerID_FinishButton']"
    )

    STEP_6_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_FinishNavigationTemplateContainerID_CancelButton']"
    )


class AddonWizardLocators:
    ADDON_WIZARD_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_aAddOnWizard"

    # ==========================================================
    # STEP 1: SELECT EXISTING TERMINAL
    # ==========================================================

    STEP_1_EXISTING_TERMINAL_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlExistingTerminal']"
    )

    STEP_1_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StartNavigationTemplateContainerID_StartNextButton']"
    )

    STEP_1_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StartNavigationTemplateContainerID_CancelButton']"
    )

    # Dynamic locator: select existing terminal by name text
    @staticmethod
    def STEP_1_SELECT_EXISTING_TERMINAL_OPTION(terminal_name: str) -> str:
        return (
            f"//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlExistingTerminal']"
            f"/option[normalize-space(text())='{terminal_name}']"
        )
    

    # ==========================================================
    # STEP 2: SELECT THE PROVIDER
    # ==========================================================

    STEP_2_HEADER = (
        "//h4[contains(normalize-space(),'Step 2 of 8')]"
    )

    # -----------------------
    # DROPDOWNS
    # -----------------------

    STEP_2_ADDON_TYPE_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnPartType']"
    )

    STEP_2_PROVIDER_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnProvider']"
    )

    STEP_2_PART_CONDITION_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnPartConditionID']"
    )

    # -----------------------
    # Dynamic option selectors
    # -----------------------

    @staticmethod
    def STEP_2_SELECT_ADDON_TYPE(option_text: str) -> str:
        return (
            f"//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnPartType']"
            f"/option[normalize-space(text())='{option_text}']"
        )

    @staticmethod
    def STEP_2_SELECT_PROVIDER(option_text: str) -> str:
        return (
            f"//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnProvider']"
            f"/option[normalize-space(text())='{option_text}']"
        )

    @staticmethod
    def STEP_2_SELECT_PART_CONDITION(option_text: str) -> str:
        return (
            f"//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnPartConditionID']"
            f"/option[normalize-space(text())='{option_text}']"
        )

    # -----------------------
    # NAVIGATION BUTTONS
    # -----------------------

    STEP_2_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StepNavigationTemplateContainerID_StepPreviousButton']"
    )

    STEP_2_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StepNavigationTemplateContainerID_StepNextButton']"
    )

    STEP_2_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StepNavigationTemplateContainerID_CancelButton']"
    )


    # ==========================================================
    # Add On Wizard Step 3
    # ==========================================================

    STEP_3_HEADER = (
        "//h4[contains(normalize-space(),'Step 3 of 8')]"
    )

    STEP_3_CURRENT_TERMINAL_PROGRAM_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblTerminalProgramSelected']"
    )

    # Checkbox - Change Terminal Program
    STEP_3_CHANGE_TERMINAL_PROGRAM_CHECKBOX = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_chkChangeTerminalProgram']"
    )

    @staticmethod
    def STEP_3_SELECT_PROGRAM_CHECKBOX(program_name: str) -> str:
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ReviewAddOnGrid']"
            f"//tr[td[normalize-space(text())='{program_name}']]"
            f"//input[contains(@id,'ckbReviewProgram')]"
        )

    # Navigation buttons
    STEP_3_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StepNavigationTemplateContainerID_StepPreviousButton']"
    )

    STEP_3_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StepNavigationTemplateContainerID_StepNextButton']"
    )

    STEP_3_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_StepNavigationTemplateContainerID_CancelButton']"
    )

    # ==========================================================
    # Add On Wizard Step 4
    # ==========================================================

    @staticmethod
    def STEP_4_FEATURE_CHECKBOX(feature_name: str) -> str:
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ReviewAddOnFeaturesGrid']"
            f"//tr[td[2][normalize-space(text())='{feature_name}']]"
            f"//input[contains(@id,'ckbTerminalProgramFeature')]"
        )

        STEP_4_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton']"
    )

    STEP_4_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepNextButton']"
    )

    STEP_4_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_CancelButton']"
    )

    # ==============================================================
    # STEP 5: SELECT ADD ONS
    # ==============================================================

    @staticmethod
    def STEP_5_SELECT_ADDON_CHECKBOX(addon_name: str) -> str:
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_SelectAddOnsGrid']"
            f"//tr[td[2][normalize-space(text())='{addon_name}']]"
            f"//input[contains(@id,'ckbSelectAddOn')]"
        )
    
        STEP_5_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton']"
    )

    STEP_5_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepNextButton']"
    )

    STEP_5_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_CancelButton']"
    )

    # ==================================================================
    # STEP 6: ADD ON EQUIPMENT COST
    # ==================================================================

    # --- Input Fields ---
    STEP_6_SERIAL_NUMBER_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnSerialNumber']"
    )

    STEP_6_SALE_PRICE_PER_UNIT_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtSalesPricePerUnit']"
    )

    # --- Sales Group Cost / Merchant Cost (Reprogram) ---
    STEP_6_REPROGRAM_CHECKBOX = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ckbAddOnReProgram']"
    )

    STEP_6_REPROGRAM_FEE_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnReProgramFee']"
    )

    # --- Navigation Buttons ---
    STEP_6_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton']"
    )

    STEP_6_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepNextButton']"
    )

    STEP_6_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_CancelButton']"
    )


    # ==================================================================
    # STEP 7: ADD-ON BILLING & SHIPPING INFORMATION
    # ==================================================================

    # -------------------------
    # Billing Information
    # -------------------------

    STEP_7_BILL_TO_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnBillTo']"
    )

    STEP_7_BILL_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnBill']"
    )

    STEP_7_CONTACT_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnContact']"
    )

    STEP_7_ADDRESS_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnAddress']"
    )

    STEP_7_ADDRESS2_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnAddress2']"
    )

    STEP_7_CITY_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnCity']"
    )

    STEP_7_STATE_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnState']"
    )

    STEP_7_COUNTRY_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnCountryBillTo']"
    )

    STEP_7_ZIP_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnZip']"
    )

    STEP_7_PHONE_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnPhone']"
    )

    # -------------------------
    # Shipping Information
    # -------------------------

    STEP_7_SHIP_TO_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnShipTo']"
    )

    STEP_7_SHIP_METHOD_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnShipMethod']"
    )

    STEP_7_SHIP_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnShip']"
    )

    STEP_7_CONTACT_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnContactShipTo']"
    )

    STEP_7_ADDRESS_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnAddressShipTo']"
    )

    STEP_7_ADDRESS2_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnAddress2ShipTo']"
    )

    STEP_7_CITY_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnCityShipTo']"
    )

    STEP_7_STATE_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnStateShipTo']"
    )

    STEP_7_COUNTRY_SHIP_TO_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_ddlAddOnCountryShipTo']"
    )

    STEP_7_ZIP_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnZipShipTo']"
    )

    STEP_7_PHONE_SHIP_TO_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_txtAddOnPhoneShipTo']"
    )

    # -------------------------
    # Navigation Buttons
    # -------------------------

    STEP_7_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepPreviousButton']"
    )

    STEP_7_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_StepNextButton']"
    )

    STEP_7_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "StepNavigationTemplateContainerID_CancelButton']"
    )

    # ==================================================================
    # STEP 8: FINAL REVIEW — VALUE LOCATORS
    # ==================================================================

    STEP_8_TERMINAL_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddOnTerminalReview']"
    )

    STEP_8_NEW_ADDON_EQUIPMENT_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblNewAddOnEquipmentReview']"
    )

    STEP_8_SERIAL_NUMBER_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddOnSN']"
    )

    STEP_8_TOTAL_SALES_PRICE_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddOnTotalSalesPriceReview']"
    )

    STEP_8_SHIP_METHOD_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddOnShipMethodReview']"
    )

    STEP_8_BILL_TO_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddonBillToReview']"
    )

    STEP_8_SHIP_TO_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddOnShipToReview']"
    )

    STEP_8_CONTACT_VALUE = (
        "//span[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_lblAddOnBilltoContactReview']"
    )

    # ==================================================================
    # STEP 8: BUTTONS
    # ==================================================================

    STEP_8_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "FinishNavigationTemplateContainerID_FinishPreviousButton']"
    )

    STEP_8_FINISH_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "FinishNavigationTemplateContainerID_FinishButton']"
    )

    STEP_8_CANCEL_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_AddOnWizard_"
        "FinishNavigationTemplateContainerID_CancelButton']"
    )


class ClearEquipmentLocators:
    CLEAR_EQUIPMENT_BUTTON = "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_btnClear"


class EquipmentTableLocators:
    # ================
    # MAIN TABLE
    # ================
    TABLE = "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_gvEquipment']"
    
    # No configured equipment message
    NO_CONFIGURED_TERMINAL_TEXT = (
        "//div[@class='alert' and contains(normalize-space(),'You currently have no configured Equipment.')]"
    )

    # ================
    # STATIC ROW LOCATORS
    # ================
    # All terminal rows (= top-level equipment)
    ALL_TERMINALS = (
        "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_gvEquipment']//tr[@datakeys]"
    )

    # AddOns under a terminal row
    ADDONS_UNDER_TERMINAL = ".//ul/li"

    # ================
    # NAME LOCATORS
    # ================
    TERMINAL_NAME = ".//span[contains(@id,'lblPart')]"
    ADDON_NAME = ".//span[contains(@id,'lblAddOn')]"

    # ================
    # ACTION BUTTONS
    # ================
    ACTION_BUTTON = ".//a[contains(@class,'dropdown-toggle') and contains(text(),'Action')]"
    ACTION_EDIT = ".//a[contains(@class,'my-edit-Terminal') and text()='Edit']"

    # ================
    # DYNAMIC LOCATORS
    # ================

    @staticmethod
    def TERMINAL_ROW_BY_NAME(name: str) -> str:
        """Returns the equipment/terminal row by exact name."""
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_gvEquipment']"
            f"//tr[@datakeys='{name}']"
        )

    @staticmethod
    def ADDONS_OF_TERMINAL(name: str) -> str:
        """Returns all addon rows under a specific terminal."""
        return (
            f"//tr[@datakeys='{name}']//ul/li"
        )

    @staticmethod
    def ADDON_OF_TERMINAL(name: str, addon_name: str) -> str:
        """Returns a specific addon under a specific terminal."""
        return (
            f"//tr[@datakeys='{name}']//span[contains(@id,'lblAddOn') "
            f"and normalize-space(text())='{addon_name}']"
        )

    @staticmethod
    def EDIT_BUTTON_FOR_TERMINAL(name: str) -> str:
        """Returns locator for Edit button for a specific terminal row."""
        return (
            f"//tr[@datakeys='{name}']//a[contains(@class,'my-edit-Terminal') and text()='Edit']"
        )
    

class GeneralFeesLocators:
    """
    EXAMPLE USAGE:
    chk = fee_checkbox("MC Infrastructure Fee")
    amt = fee_amount_input("MC Infrastructure Fee")
    """

    def FEE_CHECKBOX(description: str) -> str:
        return (
            f"//span[normalize-space(text())='{description}']"
            f"/ancestor::tr//input[contains(@id,'ckbInclude')]"
        )

    def FEE_AMOUNT_INPUT(description: str) -> str:
        return (
            f"//span[normalize-space(text())='{description}']"
            f"/ancestor::tr//input[contains(@id,'txtAmount')]"
        )


class ACHSectionLocators:
    """
    ACH Section (Enabled when Product ACH is selected)
    Contains:
    - Service enable checkboxes (Dynamic)
    - Underwriting Profile fields
    - Reporting checkboxes
    """

    # =============================================================
    # STEP_ACH - HEADER
    # =============================================================
    STEP_ACH_HEADER = "//span[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_lblTitle' and normalize-space()='ACH']"

    # =============================================================
    # STEP_ACH - SERVICES TABLE (DYNAMIC)
    # =============================================================
    @staticmethod
    def STEP_ACH_SERVICE_CHECKBOX(service_name: str) -> str:
        """
        Returns checkbox locator for ACH Service by service name.
        """
        return (
            f"//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView2']"
            f"//tr[td[normalize-space()='{service_name}']]"
            f"//input[contains(@id, 'ckbService')]"
        )

    # =============================================================
    # STEP_ACH - UNDERWRITING PROFILE FIELDS
    # =============================================================

    # Annual Volume
    STEP_ACH_ANNUAL_VOLUME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_txtAnnualVol"

    # Written %
    STEP_ACH_WRITTEN_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_ddlWritten"

    # Merchant %
    STEP_ACH_MERCHANT_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_ddlMerchant"

    # Average Ticket
    STEP_ACH_AVG_TICKET_INPUT = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_txtAvgTkt"

    # Non-Written %
    STEP_ACH_NON_WRITTEN_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_ddlNonWritten"

    # Consumer %
    STEP_ACH_CONSUMER_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_ddlConsumer"

    # Highest Ticket
    STEP_ACH_HIGHEST_TICKET_INPUT = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_txtMaxSalesAmount"

    # =============================================================
    # STEP_ACH - REPORTING SECTION
    # =============================================================
    STEP_ACH_SEND_EMAIL_CHECKBOX = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_ckbSendEmail"
    STEP_ACH_SEND_FAX_CHECKBOX   = "#ctl00_ContentPlaceHolder1_ctrlEFT1_fvEFT_ckbSendFax"


    @staticmethod
    def ach_rate_input(label_text: str) -> str:
        """
        Returns the RATE input box xpath under ACH Fees.
        Example label: "CCD Written", "PPD Written", "WEB", etc.
        """
        return (
            f"//span[normalize-space()='{label_text}']"
            "/parent::div/following-sibling::div[1]//input"
        )

    @staticmethod
    def ach_fee_input(label_text: str) -> str:
        """
        Returns the FEE input box xpath under ACH Fees.
        Example label: 'CCD Written', 'PPD Non-Written', 'ARC', etc.
        """
        return (
            f"//span[normalize-space()='{label_text}']"
            "/parent::div/following-sibling::div[2]//input"
        )

    @staticmethod
    def misc_fee_input(fee_name: str) -> str:
        return (
            f"//span[normalize-space()='{fee_name}']"
            "/parent::td/following-sibling::td//input"
        )


class ACHOriginatorLocators:

    # ================================
    # ORIGINATOR MAIN SECTION
    # ================================
    ORIGINATOR_HEADER = "//span[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_Label2']"

    ADD_ORIGINATOR_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_btnAddOriginator']"
    )

    NO_ORIGINATOR_ALERT = (
        "//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']//div[contains(@class,'alert')]"
    )

    # ================================
    # ADD ORIGINATOR MODAL
    # ================================
    MODAL_CONTAINER = "//div[@id='divAddOriginator' and contains(@class,'modal')]"
    MODAL_CLOSE_BUTTON = "//div[@id='divAddOriginator']//button[@class='close']"
    MODAL_TITLE = "//div[@id='divAddOriginator']//h3[contains(text(),'Add Originator')]"

    # ================================
    # STEP 1 HEADER
    # ================================
    STEP_1_HEADER = (
        "//div[@id='divAddOriginator']//h4[contains(normalize-space(),'Step 1')]"
    )

    # ================================
    # STEP 1 — ORIGINATOR DETAILS
    # ================================
    STEP_1_DESCRIPTION_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtOriginatorDescription']"
    )

    STEP_1_TRANSACTION_TYPE_DROPDOWN = (
        "//select[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_ddlEFTTransactionTypes']"
    )

    STEP_1_CHECKBOX_WRITTEN = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_ckbWritten']"
    )

    STEP_1_CHECKBOX_RESUBMIT_R01 = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_ckbResubmitR01']"
    )

    # ================================
    # STEP 1 — BANK INFORMATION
    # ================================
    STEP_1_DISBURSE_ROUTING_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtDisbursementABANumber']"
    )
    STEP_1_DISBURSE_ACCOUNT_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtDisbursementDDANumber']"
    )

    STEP_1_FEES_ROUTING_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtFeeABANumber']"
    )
    STEP_1_FEES_ACCOUNT_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtFeeDDANumber']"
    )

    STEP_1_FEES_COPY_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_btnCopy']"
    )

    STEP_1_REJECT_ROUTING_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtRejectABANumber']"
    )
    STEP_1_REJECT_ACCOUNT_INPUT = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_txtRejectDDANumber']"
    )

    # ================================
    # STEP 1 — NAVIGATION
    # ================================
    STEP_1_NEXT_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_StartNavigationTemplateContainerID_StartNextButton']"
    )


    # ================================
    # STEP 2 HEADER & MESSAGE
    # ================================
    STEP_2_HEADER = (
        "//div[@id='divAddOriginator']//h4[contains(text(),'Step 2')]"
    )

    STEP_2_MESSAGE = (
        "//div[@id='divAddOriginator']//div[@class='modal-body']"
        "[contains(.,'Originator with same Transaction') and contains(.,'Do you want to continue')]"
    )

    # ================================
    # STEP 2 NAVIGATION BUTTONS
    # ================================
    STEP_2_PREVIOUS_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_FinishNavigationTemplateContainerID_FinishPreviousButton']"
    )

    STEP_2_FINISH_BUTTON = (
        "//input[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_AddOriginatorWizard_FinishNavigationTemplateContainerID_FinishButton']"
    )

    # FULL TABLE
    ORIGINATOR_TABLE = "//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']"

    # ============================
    # ALL ORIGINATOR NAMES (column-1)
    # ============================
    ORIGINATOR_NAMES = (
        "//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']"
        "//tr[@datakeys]/td[1][normalize-space(text())!='']"
    )

    # ============================
    # ORIGINATOR COUNT
    # ============================
    ORIGINATOR_COUNT = (
        "count(//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']//tr[@datakeys])"
    )

    # ============================
    # ACTION BUTTON DROPDOWN (for each row)
    # ============================
    ACTION_BUTTON_BY_NAME = (
        "//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']//tr[@datakeys]"
        "[td[1][normalize-space(text())='{name}']]"
        "//div[@class='btn-group']/a[contains(@class,'dropdown-toggle')]"
    )

    # ============================
    # ACTION → EDIT (Menu Item)
    # ============================
    ACTION_EDIT_BY_NAME = (
        "//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']//tr[@datakeys]"
        "[td[1][normalize-space(text())='{name}']]"
        "//a[contains(@id,'btnGridView1Edit')]"
    )

    # ============================
    # ACTION → DELETE (Menu Item)
    # ============================
    ACTION_DELETE_BY_NAME = (
        "//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']//tr[@datakeys]"
        "[td[1][normalize-space(text())='{name}']]"
        "//a[contains(@id,'btnGridView1Delete')]"
    )

