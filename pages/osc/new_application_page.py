"""
New Application Page - OSC Application automation

Sections:
- Application Information
- Corporate Information  
- Location Information
- Tax Information
- Owner/Officer 1 & 2
- Trade Reference
- General Underwriting
- Product Selection (Credit Card, Debit Card, ACH)
"""

from playwright.sync_api import Page, TimeoutError
from typing import Dict, Any, Optional
import time

from pages.osc.base_page import BasePage
from locators.osc_locators import (
    ApplicationInformationLocators,
    CorporateInformationLocators,
    LocationInformationLocators,
    TaxInformationLocators,
    Owner1Locators,
    Owner2Locators,
    TradeReferenceLocators,
    GeneralUnderwritingLocators,
    NewApplicationPageLocators,
    ServiceSelectionLocators,
    PinDebitInterchangeLocators,
    ACHSectionLocators,
    ACHOriginatorLocators,
    BillingQuestionnaireLocators,
    BankInformationLocators,
    CreditCardInformationLocators,
    CreditCardUnderwritingLocators,
    GeneralFeesLocators,
    CommonLocators,
)
# Dynamic data loading based on OSC_DATA_ENV environment variable
from config.osc.config import get_osc_data
_data = get_osc_data()

# Import all data from the dynamically loaded module
APPLICATION_INFO = _data.APPLICATION_INFO
CORPORATE_INFO = _data.CORPORATE_INFO
LOCATION_INFO = _data.LOCATION_INFO
TAX_INFO = _data.TAX_INFO
OWNER1_INFO = _data.OWNER1_INFO
OWNER2_INFO = _data.OWNER2_INFO
TRADE_REFERENCE_INFO = _data.TRADE_REFERENCE_INFO
GENERAL_UNDERWRITING_INFO = _data.GENERAL_UNDERWRITING_INFO
BILLING_QUESTIONNAIRE_INFO = _data.BILLING_QUESTIONNAIRE_INFO
BANK_INFORMATION = _data.BANK_INFORMATION
CREDIT_CARD_INFORMATION = _data.CREDIT_CARD_INFORMATION
CREDIT_CARD_SERVICES = _data.CREDIT_CARD_SERVICES
CREDIT_CARD_UNDERWRITING = _data.CREDIT_CARD_UNDERWRITING
generate_credit_card_underwriting_data = _data.generate_credit_card_underwriting_data
CREDIT_CARD_INTERCHANGE = _data.CREDIT_CARD_INTERCHANGE

from data.osc.add_terminal_data import TERMINALS_TO_ADD
from pages.osc.add_terminal_page import AddTerminalPage
from utils.decorators import log_step, timeit
from core.performance_decorators import performance_step


class NewApplicationPage(BasePage):
    """Page object for handling New Application form"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = ApplicationInformationLocators

    
    # =========================================================================
    # PRODUCT SELECTION SECTION
    # =========================================================================

    @performance_step("scroll_to_application_info")
    @log_step
    def scroll_to_application_info(self) -> bool:
        """
        Scroll to the Application Information section header.
        
        Returns:
            bool: True if scroll successful, False otherwise
        """
        try:
            section_header = ApplicationInformationLocators.SECTION_TITLE
            self.page.locator(section_header).scroll_into_view_if_needed()
            time.sleep(0.3)
            self.logger.info("Scrolled to Application Information section")
            return True
        except Exception as e:
            self.logger.error(f"Failed to scroll to Application Information: {e}")
            return False

    @performance_step("select_credit_card_product")
    @log_step
    def select_credit_card_product(self) -> bool:
        """
        Select the Credit Card product and verify the section loads.
        
        Clicks the Credit Card product button, waits for page reload,
        and verifies the Credit Card Services header is visible.
        
        Returns:
            bool: True if product selected and verified, False otherwise
        """
        loc = NewApplicationPageLocators
        
        self.logger.info("Selecting Credit Card product...")
        
        try:
            # Step 1: Click the Credit Card product button
            self.logger.info("Step 1: Clicking Credit Card product button")
            self.page.click(loc.PRODUCT_BTN_CREDIT_CARD)
            
            # Step 2: Wait for page reload (dynamic wait, max 5 seconds)
            self.logger.info("Step 2: Waiting for page to reload...")
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Step 3: Verify Credit Card Services section header is visible
            self.logger.info("Step 3: Verifying Credit Card Services section is visible")
            verification_selector = f"#{ServiceSelectionLocators.CREDIT_CARD_SERVICES_HEADER_TEXT}"
            
            try:
                self.page.wait_for_selector(verification_selector, state="visible", timeout=5000)
                self.logger.info("✅ Credit Card product selected successfully - Credit Card Services section visible")
                
                # Step 4: Scroll back to Application Information section
                self.scroll_to_application_info()
                
                return True
            except TimeoutError:
                self.logger.error("Credit Card Services section not visible after selection")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to select Credit Card product: {e}")
            return False

    @performance_step("select_debit_card_product")
    @log_step
    def select_debit_card_product(self) -> bool:
        """
        Select the Debit Card product and verify the section loads.
        
        Clicks the Debit Card product button, waits for page reload,
        and verifies the PIN Debit Interchange dropdown is visible.
        
        Returns:
            bool: True if product selected and verified, False otherwise
        """
        loc = NewApplicationPageLocators
        
        self.logger.info("Selecting Debit Card product...")
        
        try:
            # Step 1: Click the Debit Card product button
            self.logger.info("Step 1: Clicking Debit Card product button")
            self.page.click(loc.PRODUCT_BTN_DEBIT_CARD)
            
            # Step 2: Wait for page reload (dynamic wait, max 5 seconds)
            self.logger.info("Step 2: Waiting for page to reload...")
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Step 3: Verify PIN Debit Interchange dropdown is visible
            self.logger.info("Step 3: Verifying PIN Debit Interchange section is visible")
            verification_selector = PinDebitInterchangeLocators.PIN_DEBIT_INTERCHANGE_TYPE_DROPDOWN
            
            try:
                # Scroll to the dropdown to verify it exists
                dropdown = self.page.locator(verification_selector)
                dropdown.scroll_into_view_if_needed()
                self.page.wait_for_selector(verification_selector, state="visible", timeout=5000)
                self.logger.info("✅ Debit Card product selected successfully - PIN Debit Interchange section visible")
                
                # Step 4: Scroll back to Application Information section
                self.scroll_to_application_info()
                
                return True
            except TimeoutError:
                self.logger.error("PIN Debit Interchange section not visible after selection")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to select Debit Card product: {e}")
            return False

    @performance_step("select_ach_product")
    @log_step
    def select_ach_product(self) -> bool:
        """
        Select the ACH product and verify the section loads.
        
        Clicks the ACH product button, waits for page reload,
        and verifies the ACH section header is visible.
        
        Returns:
            bool: True if product selected and verified, False otherwise
        """
        loc = NewApplicationPageLocators
        
        self.logger.info("Selecting ACH product...")
        
        try:
            # Step 1: Click the ACH product button
            self.logger.info("Step 1: Clicking ACH product button")
            self.page.click(loc.PRODUCT_BTN_ACH)
            
            # Step 2: Wait for page reload (dynamic wait, max 5 seconds)
            self.logger.info("Step 2: Waiting for page to reload...")
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Step 3: Verify ACH section header is visible
            self.logger.info("Step 3: Verifying ACH section header is visible")
            verification_selector = ACHSectionLocators.STEP_ACH_HEADER
            
            try:
                self.page.wait_for_selector(verification_selector, state="visible", timeout=5000)
                self.logger.info("✅ ACH product selected successfully - ACH section visible")
                
                # Step 4: Scroll back to Application Information section
                self.scroll_to_application_info()
                
                return True
            except TimeoutError:
                self.logger.error("ACH section header not visible after selection")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to select ACH product: {e}")
            return False

    @performance_step("deselect_credit_card_product")
    @log_step
    def deselect_credit_card_product(self) -> bool:
        """
        Deselect the Credit Card product and verify the section is removed from DOM.
        
        Clicks the Credit Card product button again to deselect, waits for page reload,
        and verifies the Credit Card Services header is NOT present in DOM.
        
        Returns:
            bool: True if product deselected and verified, False otherwise
        """
        loc = NewApplicationPageLocators
        
        self.logger.info("Deselecting Credit Card product...")
        
        try:
            # Step 1: Click the Credit Card product button to deselect
            self.logger.info("Step 1: Clicking Credit Card product button to deselect")
            self.page.click(loc.PRODUCT_BTN_CREDIT_CARD)
            
            # Step 2: Wait for page reload (dynamic wait, max 5 seconds)
            self.logger.info("Step 2: Waiting for page to reload...")
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Step 3: Verify Credit Card Services section is NOT in DOM
            self.logger.info("Step 3: Verifying Credit Card Services section is removed from DOM")
            verification_selector = f"#{ServiceSelectionLocators.CREDIT_CARD_SERVICES_HEADER_TEXT}"
            
            # Check element count is 0 (not present in DOM)
            element_count = self.page.locator(verification_selector).count()
            
            if element_count == 0:
                self.logger.info("✅ Credit Card product deselected successfully - section removed from DOM")
                
                # Step 4: Scroll back to Application Information section
                self.scroll_to_application_info()
                
                return True
            else:
                self.logger.error("Credit Card Services section still present in DOM after deselection")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to deselect Credit Card product: {e}")
            return False

    @performance_step("deselect_debit_card_product")
    @log_step
    def deselect_debit_card_product(self) -> bool:
        """
        Deselect the Debit Card product and verify the section is removed from DOM.
        
        Clicks the Debit Card product button again to deselect, waits for page reload,
        and verifies the PIN Debit Interchange dropdown is NOT present in DOM.
        
        Returns:
            bool: True if product deselected and verified, False otherwise
        """
        loc = NewApplicationPageLocators
        
        self.logger.info("Deselecting Debit Card product...")
        
        try:
            # Step 1: Click the Debit Card product button to deselect
            self.logger.info("Step 1: Clicking Debit Card product button to deselect")
            self.page.click(loc.PRODUCT_BTN_DEBIT_CARD)
            
            # Step 2: Wait for page reload (dynamic wait, max 5 seconds)
            self.logger.info("Step 2: Waiting for page to reload...")
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Step 3: Verify PIN Debit Interchange section is NOT in DOM
            self.logger.info("Step 3: Verifying PIN Debit Interchange section is removed from DOM")
            verification_selector = PinDebitInterchangeLocators.PIN_DEBIT_INTERCHANGE_TYPE_DROPDOWN
            
            # Check element count is 0 (not present in DOM)
            element_count = self.page.locator(verification_selector).count()
            
            if element_count == 0:
                self.logger.info("✅ Debit Card product deselected successfully - section removed from DOM")
                
                # Step 4: Scroll back to Application Information section
                self.scroll_to_application_info()
                
                return True
            else:
                self.logger.error("PIN Debit Interchange section still present in DOM after deselection")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to deselect Debit Card product: {e}")
            return False

    @performance_step("deselect_ach_product")
    @log_step
    def deselect_ach_product(self) -> bool:
        """
        Deselect the ACH product and verify the section is removed from DOM.
        
        Clicks the ACH product button again to deselect, waits for page reload,
        and verifies the ACH section header is NOT present in DOM.
        
        Returns:
            bool: True if product deselected and verified, False otherwise
        """
        loc = NewApplicationPageLocators
        
        self.logger.info("Deselecting ACH product...")
        
        try:
            # Step 1: Click the ACH product button to deselect
            self.logger.info("Step 1: Clicking ACH product button to deselect")
            self.page.click(loc.PRODUCT_BTN_ACH)
            
            # Step 2: Wait for page reload (dynamic wait, max 5 seconds)
            self.logger.info("Step 2: Waiting for page to reload...")
            self.page.wait_for_load_state("networkidle", timeout=5000)
            
            # Step 3: Verify ACH section header is NOT in DOM
            self.logger.info("Step 3: Verifying ACH section header is removed from DOM")
            verification_selector = ACHSectionLocators.STEP_ACH_HEADER
            
            # Check element count is 0 (not present in DOM)
            element_count = self.page.locator(verification_selector).count()
            
            if element_count == 0:
                self.logger.info("✅ ACH product deselected successfully - section removed from DOM")
                
                # Step 4: Scroll back to Application Information section
                self.scroll_to_application_info()
                
                return True
            else:
                self.logger.error("ACH section header still present in DOM after deselection")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to deselect ACH product: {e}")
            return False
        
    @performance_step("verify_application_info_section")
    @log_step
    def verify_application_info_section(self, timeout: int = 10000) -> bool:
        """
        Verify that the Application Information section is visible and loaded
        
        Args:
            timeout: Maximum time to wait for the section to be visible
            
        Returns:
            bool: True if section is visible, False otherwise
        """
        try:
            self.page.wait_for_selector(
                self.locators.SECTION_TITLE, 
                timeout=timeout,
                state="visible"
            )
            self.logger.info("Application Information section verified successfully")
            return True
        except TimeoutError:
            self.logger.error(f"Application Information section not found within {timeout}ms")
            return False
    
    @performance_step("verify_display_fields")
    @log_step
    def verify_display_fields(self, app_data: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """
        Verify that display-only fields show correct values
        
        Args:
            app_data: Application data to verify against (defaults to APPLICATION_INFO)
            
        Returns:
            Dict[str, bool]: Verification results for each field
        """
        if app_data is None:
            app_data = APPLICATION_INFO
            
        results = {}
        
        # Verify Office display
        try:
            office_locator = self.locators.OFFICE_DISPLAY.format(office_name=app_data["office"])
            office_element = self.page.locator(office_locator)
            if office_element.is_visible():
                results["office"] = True
                self.logger.info(f"Office field verified: {app_data['office']}")
            else:
                results["office"] = False
                self.logger.warning(f"Office field not visible or incorrect: {app_data['office']}")
        except Exception as e:
            results["office"] = False
            self.logger.error(f"Error verifying office field: {e}")
        
        # Verify Phone display
        try:
            phone_locator = self.locators.PHONE_DISPLAY.format(phone=app_data["phone"])
            phone_element = self.page.locator(phone_locator)
            if phone_element.is_visible():
                results["phone"] = True
                self.logger.info(f"Phone field verified: {app_data['phone']}")
            else:
                results["phone"] = False
                self.logger.warning(f"Phone field not visible or incorrect: {app_data['phone']}")
        except Exception as e:
            results["phone"] = False
            self.logger.error(f"Error verifying phone field: {e}")
        
        # Verify Contractor display
        try:
            contractor_locator = self.locators.CONTRACTOR_DISPLAY.format(contractor_name=app_data["contractor"])
            contractor_element = self.page.locator(contractor_locator)
            if contractor_element.is_visible():
                results["contractor"] = True
                self.logger.info(f"Contractor field verified: {app_data['contractor']}")
            else:
                results["contractor"] = False
                self.logger.warning(f"Contractor field not visible or incorrect: {app_data['contractor']}")
        except Exception as e:
            results["contractor"] = False
            self.logger.error(f"Error verifying contractor field: {e}")
        
        return results
    
    @performance_step("fill_application_information")
    @log_step
    def fill_application_information(self, app_data: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """
        Fill out the complete Application Information section
        
        Args:
            app_data: Application data to use (defaults to APPLICATION_INFO)
            
        Returns:
            Dict[str, bool]: Results for each field operation
        """
        if app_data is None:
            app_data = APPLICATION_INFO
            
        results = {}
        
        # First verify the section is loaded
        if not self.verify_application_info_section():
            self.logger.error("Application Information section not available")
            return {"section_verification": False}
        
        results["section_verification"] = True
        
        # Verify display-only fields
        display_results = self.verify_display_fields(app_data)
        results.update(display_results)
        
        # Fill Association dropdown (using base class method)
        results["association"] = self.select_dropdown_by_text(
            self.locators.ASSOCIATION_DROPDOWN,
            app_data["association"],
            "Association"
        )
        
        # Fill Lead Source dropdown (using base class method)
        results["lead_source"] = self.select_dropdown_by_text(
            self.locators.LEAD_SOURCE_DROPDOWN,
            app_data["lead_source"],
            "Lead Source"
        )
        
        # Fill Referral Partner dropdown (using base class method)
        results["referral_partner"] = self.select_dropdown_by_text(
            self.locators.REFERRAL_PARTNER_DROPDOWN,
            app_data["referral_partner"],
            "Referral Partner"
        )
        
        # Fill Promo Code (using base class method)
        results["promo_code"] = self.fill_text(
            self.locators.PROMO_CODE_INPUT,
            app_data.get("promo_code", ""),
            "Promo Code"
        )
        
        # Fill Corporate Atlas ID (using base class method)
        results["corporate_atlas_id"] = self.fill_text(
            self.locators.CORP_ATLAS_ID_INPUT,
            app_data.get("corporate_atlas_id", ""),
            "Corporate Atlas ID"
        )
        
        # Summary logging
        successful_operations = sum(1 for result in results.values() if result)
        total_operations = len(results)
        
        self.logger.info(f"Application Information section completed: {successful_operations}/{total_operations} operations successful")
        
        if successful_operations == total_operations:
            self.logger.info("✅ All Application Information fields processed successfully")
        else:
            failed_fields = [field for field, result in results.items() if not result]
            self.logger.warning(f"⚠️ Some fields failed: {failed_fields}")
        
        return results
    
    @performance_step("get_all_available_options")
    @log_step
    def get_all_available_options(self) -> Dict[str, list]:
        """
        Get all available options from all dropdowns for analysis.
        Uses base class get_dropdown_options method.
        
        Returns:
            Dict[str, list]: Dictionary mapping field names to their available options
        """
        options = {}
        
        # Using base class get_dropdown_options method
        options["association"] = self.get_dropdown_options(self.locators.ASSOCIATION_DROPDOWN)
        options["lead_source"] = self.get_dropdown_options(self.locators.LEAD_SOURCE_DROPDOWN)
        options["referral_partner"] = self.get_dropdown_options(self.locators.REFERRAL_PARTNER_DROPDOWN)
        
        return options

    # =========================================================================
    # CORPORATE INFORMATION SECTION
    # =========================================================================
    
    @performance_step("fill_corporate_information_section")
    @log_step
    def fill_corporate_information_section(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the Corporate Information section.
        
        Args:
            data: Optional dictionary with corporate data. Uses CORPORATE_INFO if not provided.
            
        Returns:
            Dict with success status for each field
        """
        data = data or CORPORATE_INFO
        results = {}
        loc = CorporateInformationLocators
        
        # Scroll to section
        self.scroll_to_section(loc.CORPORATE_INFORMATION_SECTION)
        
        # Legal Business Name
        results["legal_business_name"] = self.fill_text(
            loc.LEGAL_BUSINESS_NAME_INPUT,
            data.get("legal_business_name", ""),
            "Legal Business Name"
        )
        
        # Address
        results["address"] = self.fill_text(
            loc.ADDRESS_LINE_1_INPUT,
            data.get("address", ""),
            "Corporate Address"
        )
        
        # City
        results["city"] = self.fill_text(
            loc.CITY_INPUT,
            data.get("city", ""),
            "Corporate City"
        )
        
        # State dropdown
        results["state"] = self.select_dropdown_by_text(
            loc.STATE_DROPDOWN,
            data.get("state", "California"),
            "Corporate State"
        )
        
        # Zip Code
        results["zip_code"] = self.fill_text(
            loc.ZIP_CODE_INPUT,
            data.get("zip_code", ""),
            "Corporate Zip Code"
        )
        
        # Country dropdown
        results["country"] = self.select_dropdown_by_text(
            loc.COUNTRY_DROPDOWN,
            data.get("country", "United States"),
            "Corporate Country"
        )
        
        # Phone - masked input (digits only, typed slowly)
        results["phone"] = self.fill_masked_input(
            loc.PHONE_INPUT,
            data.get("phone", ""),
            "Corporate Phone"
        )
        
        # Fax - masked input (digits only, typed slowly)
        results["fax"] = self.fill_masked_input(
            loc.FAX_INPUT,
            data.get("fax", ""),
            "Corporate Fax"
        )
        
        # Email
        results["email"] = self.fill_text(
            loc.EMAIL_INPUT,
            data.get("email", ""),
            "Corporate Email"
        )
        
        # Dunns & Bradstreet
        results["dunns_number"] = self.fill_text(
            loc.DUNNS_INPUT,
            data.get("dunns_number", ""),
            "Dunns & Bradstreet"
        )
        
        # Contact Title
        results["contact_title"] = self.fill_text(
            loc.CONTACT_TITLE_INPUT,
            data.get("contact_title", ""),
            "Contact Title"
        )
        
        # Contact First Name
        results["contact_first_name"] = self.fill_text(
            loc.CONTACT_FIRST_NAME_INPUT,
            data.get("contact_first_name", ""),
            "Contact First Name"
        )
        
        # Contact Last Name
        results["contact_last_name"] = self.fill_text(
            loc.CONTACT_LAST_NAME_INPUT,
            data.get("contact_last_name", ""),
            "Contact Last Name"
        )
        
        # Location Address Radio - Use different address
        if data.get("use_different_location", True):
            results["location_address_option"] = self.select_radio(
                loc.LOCATION_DIFFERENT_ADDRESS_RADIO,
                "Use Different Address"
            )
        else:
            results["location_address_option"] = self.select_radio(
                loc.LOCATION_SAME_ADDRESS_RADIO,
                "Use Same Address"
            )
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Corporate Information: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # LOCATION INFORMATION SECTION
    # =========================================================================
    
    @performance_step("fill_location_information_section")
    @log_step
    def fill_location_information_section(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the Location Information section.
        
        Args:
            data: Optional dictionary with location data. Uses LOCATION_INFO if not provided.
            
        Returns:
            Dict with success status for each field
        """
        data = data or LOCATION_INFO
        results = {}
        loc = LocationInformationLocators
        
        # Scroll to section
        self.scroll_to_section(loc.SECTION_LOCATION_INFORMATION)
        
        # DBA (Doing Business As)
        results["dba"] = self.fill_text(
            loc.DBA_INPUT,
            data.get("dba", ""),
            "DBA Name"
        )
        
        # Address
        results["address"] = self.fill_text(
            loc.ADDRESS_INPUT,
            data.get("address", ""),
            "Location Address"
        )
        
        # City
        results["city"] = self.fill_text(
            loc.CITY_INPUT,
            data.get("city", ""),
            "Location City"
        )
        
        # State dropdown
        results["state"] = self.select_dropdown_by_text(
            loc.STATE_DROPDOWN,
            data.get("state", "California"),
            "Location State"
        )
        
        # Zip Code
        results["zip_code"] = self.fill_text(
            loc.ZIP_INPUT,
            data.get("zip_code", ""),
            "Location Zip Code"
        )
        
        # Country dropdown
        results["country"] = self.select_dropdown_by_text(
            loc.COUNTRY_DROPDOWN,
            data.get("country", "United States"),
            "Location Country"
        )
        
        # Phone - masked input
        results["phone"] = self.fill_masked_input(
            loc.PHONE_INPUT,
            data.get("phone", ""),
            "Location Phone"
        )
        
        # Fax - masked input
        results["fax"] = self.fill_masked_input(
            loc.FAX_INPUT,
            data.get("fax", ""),
            "Location Fax"
        )
        
        # Customer Service Phone - masked input
        results["customer_service_phone"] = self.fill_masked_input(
            loc.CUSTOMER_SERVICE_PHONE_INPUT,
            data.get("customer_service_phone", ""),
            "Customer Service Phone"
        )
        
        # Website
        results["website"] = self.fill_text(
            loc.WEBSITE_INPUT,
            data.get("website", ""),
            "Website"
        )
        
        # Email
        results["email"] = self.fill_text(
            loc.EMAIL_INPUT,
            data.get("email", ""),
            "Location Email"
        )
        
        # Chargeback Email
        results["chargeback_email"] = self.fill_text(
            loc.CHARGEBACK_EMAIL_INPUT,
            data.get("chargeback_email", ""),
            "Chargeback Email"
        )
        
        # Business Open Date (masked input mm/dd/yyyy) - use special date method with retry
        results["business_open_date"] = self.fill_masked_date_input(
            loc.BUSINESS_OPEN_DATE_INPUT,
            data.get("business_open_date", ""),
            "Business Open Date"
        )
        
        # Existing Sage MID (optional)
        existing_mid = data.get("existing_sage_mid", "")
        if existing_mid:
            results["existing_sage_mid"] = self.fill_text(
                loc.EXISTING_MID_INPUT,
                existing_mid,
                "Existing Sage MID"
            )
        else:
            results["existing_sage_mid"] = True  # Skip if not provided
        
        # General Comments (optional)
        general_comments = data.get("general_comments", "")
        if general_comments:
            results["general_comments"] = self.fill_text(
                loc.GENERAL_COMMENTS_TEXTAREA,
                general_comments,
                "General Comments"
            )
        else:
            results["general_comments"] = True  # Skip if not provided
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Location Information: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # TAX INFORMATION SECTION
    # =========================================================================
    
    @performance_step("fill_tax_information")
    @log_step
    def fill_tax_information_section(self, tax_data: Dict = None) -> Dict[str, bool]:
        """
        Fill the Tax Information section of the application.
        
        Args:
            tax_data: Dictionary containing tax information. Defaults to TAX_INFO.
            
        Returns:
            Dict[str, bool]: Success status for each field.
        """
        data = tax_data or TAX_INFO
        results = {}
        loc = TaxInformationLocators
        
        self.logger.info("Filling Tax Information section...")
        
        # Federal Tax ID (masked input - 9 digits)
        results["federal_tax_id"] = self.fill_masked_input(
            loc.FEDERAL_TAX_ID_INPUT,
            data.get("federal_tax_id", ""),
            "Federal Tax ID"
        )
        
        # Tax Filing Corporation Name
        results["tax_filing_corp_name"] = self.fill_text(
            loc.TAX_FILING_CORP_NAME_INPUT,
            data.get("tax_filing_corp_name", ""),
            "Tax Filing Corp Name"
        )
        
        # Ownership Type dropdown
        results["ownership_type"] = self.select_dropdown_by_text(
            loc.OWNERSHIP_TYPE_DROPDOWN,
            data.get("ownership_type", ""),
            "Ownership Type"
        )
        
        # Tax Filing State dropdown
        results["tax_filing_state"] = self.select_dropdown_by_text(
            loc.TAX_FILING_STATE_DROPDOWN,
            data.get("tax_filing_state", ""),
            "Tax Filing State"
        )
        
        # Checkboxes
        # Location is Corporate Headquarters
        if data.get("is_corp_headquarters", False):
            results["is_corp_headquarters"] = self.set_checkbox(
                loc.LOCATION_IS_CORP_HQ_CHECKBOX,
                True,
                "Location is Corp HQ"
            )
        else:
            results["is_corp_headquarters"] = True  # Skip if not needed
        
        # Foreign Entity checkbox
        if data.get("is_foreign_entity", False):
            results["is_foreign_entity"] = self.set_checkbox(
                loc.FOREIGN_ENTITY_CHECKBOX,
                True,
                "Foreign Entity"
            )
        else:
            results["is_foreign_entity"] = True  # Skip if not checked
        
        # Authorize 1099 checkbox
        if data.get("authorize_1099", True):
            results["authorize_1099"] = self.set_checkbox(
                loc.AUTHORIZE_1099_CHECKBOX,
                True,
                "Authorize 1099"
            )
        else:
            results["authorize_1099"] = True  # Skip if not needed
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Tax Information: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # OWNER/OFFICER 1 SECTION
    # =========================================================================
    
    @performance_step("fill_owner1_information")
    @log_step
    def fill_owner1_information_section(self, owner_data: Dict = None) -> Dict[str, bool]:
        """
        Fill the Owner/Officer 1 section of the application.
        
        Args:
            owner_data: Dictionary containing owner information. Defaults to OWNER1_INFO.
            
        Returns:
            Dict[str, bool]: Success status for each field.
        """
        data = owner_data or OWNER1_INFO
        results = {}
        loc = Owner1Locators
        
        self.logger.info("Filling Owner/Officer 1 section...")
        
        # Title
        results["title"] = self.fill_text(
            loc.TITLE_INPUT,
            data.get("title", ""),
            "Title"
        )
        
        # First Name
        results["first_name"] = self.fill_text(
            loc.FIRST_NAME_INPUT,
            data.get("first_name", ""),
            "First Name"
        )
        
        # Last Name
        results["last_name"] = self.fill_text(
            loc.LAST_NAME_INPUT,
            data.get("last_name", ""),
            "Last Name"
        )
        
        # Address 1
        results["address1"] = self.fill_text(
            loc.ADDRESS1_INPUT,
            data.get("address1", ""),
            "Address 1"
        )
        
        # Address 2 (optional)
        address2 = data.get("address2", "")
        if address2:
            results["address2"] = self.fill_text(
                loc.ADDRESS2_INPUT,
                address2,
                "Address 2"
            )
        else:
            results["address2"] = True
        
        # City
        results["city"] = self.fill_text(
            loc.CITY_INPUT,
            data.get("city", ""),
            "City"
        )
        
        # State dropdown
        results["state"] = self.select_dropdown_by_text(
            loc.STATE_DROPDOWN,
            data.get("state", ""),
            "State"
        )
        
        # Zip Code
        results["zip_code"] = self.fill_text(
            loc.ZIP_INPUT,
            data.get("zip_code", ""),
            "Zip Code"
        )
        
        # Country dropdown
        results["country"] = self.select_dropdown_by_text(
            loc.COUNTRY_DROPDOWN,
            data.get("country", ""),
            "Country"
        )
        
        # Phone (masked input)
        results["phone"] = self.fill_masked_input(
            loc.PHONE_INPUT,
            data.get("phone", ""),
            "Phone"
        )
        
        # Fax (masked input)
        results["fax"] = self.fill_masked_input(
            loc.FAX_INPUT,
            data.get("fax", ""),
            "Fax"
        )
        
        # Email
        results["email"] = self.fill_text(
            loc.EMAIL_INPUT,
            data.get("email", ""),
            "Email"
        )
        
        # Date of Birth (masked input mm/dd/yyyy) - use special date method with retry
        results["dob"] = self.fill_masked_date_input(
            loc.DOB_INPUT,
            data.get("dob", ""),
            "Date of Birth"
        )
        
        # SSN (masked input)
        results["ssn"] = self.fill_masked_input(
            loc.SSN_INPUT,
            data.get("ssn", ""),
            "SSN"
        )
        
        # Date of Ownership (masked input mm/dd/yyyy) - use special date method with retry
        results["date_of_ownership"] = self.fill_masked_date_input(
            loc.DATE_OF_OWNERSHIP_INPUT,
            data.get("date_of_ownership", ""),
            "Date of Ownership"
        )
        
        # Equity percentage (masked input 0__)
        results["equity"] = self.fill_masked_equity_input(
            loc.EQUITY_INPUT,
            data.get("equity", ""),
            "Equity %"
        )
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Owner/Officer 1: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # OWNER/OFFICER 2 SECTION
    # =========================================================================
    
    @performance_step("fill_owner2_information")
    @log_step
    def fill_owner2_information_section(self, owner_data: Dict = None) -> Dict[str, bool]:
        """
        Fill the Owner/Officer 2 section of the application.
        
        Args:
            owner_data: Dictionary containing owner information. Defaults to OWNER2_INFO.
            
        Returns:
            Dict[str, bool]: Success status for each field.
        """
        data = owner_data or OWNER2_INFO
        results = {}
        loc = Owner2Locators
        
        self.logger.info("Filling Owner/Officer 2 section...")
        
        # Title
        results["title"] = self.fill_text(
            loc.TITLE_INPUT,
            data.get("title", ""),
            "Title"
        )
        
        # First Name
        results["first_name"] = self.fill_text(
            loc.FIRST_NAME_INPUT,
            data.get("first_name", ""),
            "First Name"
        )
        
        # Last Name
        results["last_name"] = self.fill_text(
            loc.LAST_NAME_INPUT,
            data.get("last_name", ""),
            "Last Name"
        )
        
        # Address 1
        results["address1"] = self.fill_text(
            loc.ADDRESS1_INPUT,
            data.get("address1", ""),
            "Address 1"
        )
        
        # Address 2 (optional)
        address2 = data.get("address2", "")
        if address2:
            results["address2"] = self.fill_text(
                loc.ADDRESS2_INPUT,
                address2,
                "Address 2"
            )
        else:
            results["address2"] = True
        
        # City
        results["city"] = self.fill_text(
            loc.CITY_INPUT,
            data.get("city", ""),
            "City"
        )
        
        # State dropdown
        results["state"] = self.select_dropdown_by_text(
            loc.STATE_DROPDOWN,
            data.get("state", ""),
            "State"
        )
        
        # Zip Code
        results["zip_code"] = self.fill_text(
            loc.ZIP_INPUT,
            data.get("zip_code", ""),
            "Zip Code"
        )
        
        # Country dropdown
        results["country"] = self.select_dropdown_by_text(
            loc.COUNTRY_DROPDOWN,
            data.get("country", ""),
            "Country"
        )
        
        # Phone (masked input)
        results["phone"] = self.fill_masked_input(
            loc.PHONE_INPUT,
            data.get("phone", ""),
            "Phone"
        )
        
        # Fax (masked input)
        results["fax"] = self.fill_masked_input(
            loc.FAX_INPUT,
            data.get("fax", ""),
            "Fax"
        )
        
        # Email
        results["email"] = self.fill_text(
            loc.EMAIL_INPUT,
            data.get("email", ""),
            "Email"
        )
        
        # Date of Birth (masked input mm/dd/yyyy) - use special date method with retry
        results["dob"] = self.fill_masked_date_input(
            loc.DOB_INPUT,
            data.get("dob", ""),
            "Date of Birth"
        )
        
        # SSN (masked input)
        results["ssn"] = self.fill_masked_input(
            loc.SSN_INPUT,
            data.get("ssn", ""),
            "SSN"
        )
        
        # Date of Ownership (masked input mm/dd/yyyy) - use special date method with retry
        results["date_of_ownership"] = self.fill_masked_date_input(
            loc.DATE_OF_OWNERSHIP_INPUT,
            data.get("date_of_ownership", ""),
            "Date of Ownership"
        )
        
        # Equity percentage (masked input 0__)
        results["equity"] = self.fill_masked_equity_input(
            loc.EQUITY_INPUT,
            data.get("equity", ""),
            "Equity %"
        )
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Owner/Officer 2: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # TRADE REFERENCE SECTION
    # =========================================================================
    
    @performance_step("fill_trade_reference")
    @log_step
    def fill_trade_reference_section(self, trade_data: Dict = None) -> Dict[str, bool]:
        """
        Fill the Trade Reference section of the application.
        
        Args:
            trade_data: Dictionary containing trade reference information. Defaults to TRADE_REFERENCE_INFO.
            
        Returns:
            Dict[str, bool]: Success status for each field.
        """
        data = trade_data or TRADE_REFERENCE_INFO
        results = {}
        loc = TradeReferenceLocators
        
        self.logger.info("Filling Trade Reference section...")
        
        # Title
        results["title"] = self.fill_text(
            loc.TITLE_INPUT,
            data.get("title", ""),
            "Title"
        )
        
        # Name
        results["name"] = self.fill_text(
            loc.NAME_INPUT,
            data.get("name", ""),
            "Name"
        )
        
        # Address
        results["address"] = self.fill_text(
            loc.ADDRESS_INPUT,
            data.get("address", ""),
            "Address"
        )
        
        # City
        results["city"] = self.fill_text(
            loc.CITY_INPUT,
            data.get("city", ""),
            "City"
        )
        
        # State dropdown
        results["state"] = self.select_dropdown_by_text(
            loc.STATE_DROPDOWN,
            data.get("state", ""),
            "State"
        )
        
        # Zip Code
        results["zip_code"] = self.fill_text(
            loc.ZIP_INPUT,
            data.get("zip_code", ""),
            "Zip Code"
        )
        
        # Country dropdown
        results["country"] = self.select_dropdown_by_text(
            loc.COUNTRY_DROPDOWN,
            data.get("country", ""),
            "Country"
        )
        
        # Phone (masked input)
        results["phone"] = self.fill_masked_input(
            loc.PHONE_INPUT,
            data.get("phone", ""),
            "Phone"
        )
        
        # Email
        results["email"] = self.fill_text(
            loc.EMAIL_INPUT,
            data.get("email", ""),
            "Email"
        )
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Trade Reference: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # GENERAL UNDERWRITING SECTION
    # =========================================================================
    
    @performance_step("fill_general_underwriting")
    @log_step
    def fill_general_underwriting_section(self, underwriting_data: Dict = None) -> Dict[str, bool]:
        """
        Fill the General Underwriting section of the application.
        
        Args:
            underwriting_data: Dictionary containing underwriting information. Defaults to GENERAL_UNDERWRITING_INFO.
            
        Returns:
            Dict[str, bool]: Success status for each field.
        """
        data = underwriting_data or GENERAL_UNDERWRITING_INFO
        results = {}
        loc = GeneralUnderwritingLocators
        
        self.logger.info("Filling General Underwriting section...")
        
        # Business Type dropdown
        results["business_type"] = self.select_dropdown_by_text(
            loc.BUSINESS_TYPE_DROPDOWN,
            data.get("business_type", ""),
            "Business Type"
        )
        
        # SIC Code (autocomplete input - type and select from dropdown)
        results["sic_code"] = self.fill_autocomplete_input(
            loc.SIC_CODE_INPUT,
            loc.SIC_CODE_AUTOCOMPLETE_DROPDOWN,
            loc.SIC_CODE_AUTOCOMPLETE_ITEM,
            data.get("sic_code", ""),
            "SIC Code"
        )
        
        # Products Sold
        results["products_sold"] = self.fill_text(
            loc.PRODUCTS_SOLD_TEXTAREA,
            data.get("products_sold", ""),
            "Products Sold"
        )
        
        # Return Policy dropdown
        results["return_policy"] = self.select_dropdown_by_text(
            loc.RETURN_POLICY_DROPDOWN,
            data.get("return_policy", ""),
            "Return Policy"
        )
        
        # Days Until Product Delivery
        days_until_delivery = data.get("days_until_delivery", "")
        if days_until_delivery:
            results["days_until_delivery"] = self.fill_text(
                loc.DAYS_UNTIL_PRODUCT_DELIVERY_INPUT,
                days_until_delivery,
                "Days Until Delivery"
            )
        else:
            results["days_until_delivery"] = True
        
        # Seasonal Months checkboxes
        seasonal_months = data.get("seasonal_months", [])
        
        # Map month names to checkbox locators
        month_checkbox_map = {
            "january": loc.SEASONAL_MONTH_JANUARY_CHECKBOX,
            "february": loc.SEASONAL_MONTH_FEBRUARY_CHECKBOX,
            "march": loc.SEASONAL_MONTH_MARCH_CHECKBOX,
            "april": loc.SEASONAL_MONTH_APRIL_CHECKBOX,
            "may": loc.SEASONAL_MONTH_MAY_CHECKBOX,
            "june": loc.SEASONAL_MONTH_JUNE_CHECKBOX,
            "july": loc.SEASONAL_MONTH_JULY_CHECKBOX,
            "august": loc.SEASONAL_MONTH_AUGUST_CHECKBOX,
            "september": loc.SEASONAL_MONTH_SEPTEMBER_CHECKBOX,
            "october": loc.SEASONAL_MONTH_OCTOBER_CHECKBOX,
            "november": loc.SEASONAL_MONTH_NOVEMBER_CHECKBOX,
            "december": loc.SEASONAL_MONTH_DECEMBER_CHECKBOX,
        }
        
        # Check the seasonal months if provided
        for month in seasonal_months:
            month_lower = month.lower()
            if month_lower in month_checkbox_map:
                checkbox_selector = month_checkbox_map[month_lower]
                results[f"seasonal_{month_lower}"] = self.set_checkbox(
                    checkbox_selector,
                    True,
                    f"Seasonal {month.capitalize()}"
                )
        
        # If no seasonal months, mark as success (skipped)
        if not seasonal_months:
            results["seasonal_months"] = True
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"General Underwriting: {success_count}/{total_count} fields successful")
        
        return results

    # =========================================================================
    # BILLING QUESTIONNAIRE SECTION
    # =========================================================================
    
    @performance_step("fill_billing_questionnaire")
    @log_step
    def fill_billing_questionnaire_section(self, billing_data: Dict = None) -> Dict[str, bool]:
        """
        Fill the Billing Questionnaire section of the application.
        
        Args:
            billing_data: Dictionary containing billing questionnaire data. 
                         Defaults to BILLING_QUESTIONNAIRE_INFO.
            
        Returns:
            Dict[str, bool]: Success status for each field.
        """
        data = billing_data or BILLING_QUESTIONNAIRE_INFO
        results = {}
        loc = BillingQuestionnaireLocators
        
        self.logger.info("Filling Billing Questionnaire section...")
        
        # Type of Merchant (Radio Buttons)
        merchant_type = data.get("merchant_type", "moto").lower()
        
        if merchant_type == "internet":
            results["merchant_type"] = self.select_radio(
                loc.MERCHANT_TYPE_INTERNET_RADIO,
                "Merchant Type - Internet"
            )
        elif merchant_type == "moto":
            results["merchant_type"] = self.select_radio(
                loc.MERCHANT_TYPE_MOTO_RADIO,
                "Merchant Type - MOTO"
            )
        elif merchant_type == "retail":
            results["merchant_type"] = self.select_radio(
                loc.MERCHANT_TYPE_RETAIL_RADIO,
                "Merchant Type - Retail"
            )
        else:
            self.logger.warning(f"Unknown merchant type: {merchant_type}, defaulting to MOTO")
            results["merchant_type"] = self.select_radio(
                loc.MERCHANT_TYPE_MOTO_RADIO,
                "Merchant Type - MOTO"
            )
        
        # Full Payment Upfront
        if data.get("full_payment_upfront", False):
            results["full_payment_checkbox"] = self.set_checkbox(
                loc.FULL_PAYMENT_CHECKBOX,
                True,
                "Full Payment Upfront"
            )
            # Fill days input if checkbox is checked
            full_payment_days = data.get("full_payment_days", "")
            if full_payment_days:
                results["full_payment_days"] = self.fill_text(
                    loc.FULL_PAYMENT_DAYS_INPUT,
                    full_payment_days,
                    "Full Payment Days"
                )
            else:
                results["full_payment_days"] = True
        else:
            results["full_payment_checkbox"] = True  # Skipped
            results["full_payment_days"] = True
        
        # Partial Payment Upfront
        if data.get("partial_payment_upfront", False):
            results["partial_payment_checkbox"] = self.set_checkbox(
                loc.PARTIAL_PAYMENT_CHECKBOX,
                True,
                "Partial Payment Upfront"
            )
            # Fill percentage and days if checkbox is checked
            partial_percentage = data.get("partial_payment_percentage", "")
            if partial_percentage:
                results["partial_payment_percentage"] = self.fill_text(
                    loc.PARTIAL_PAYMENT_PERCENTAGE_INPUT,
                    partial_percentage,
                    "Partial Payment Percentage"
                )
            else:
                results["partial_payment_percentage"] = True
            
            partial_days = data.get("partial_payment_days", "")
            if partial_days:
                results["partial_payment_days"] = self.fill_text(
                    loc.PARTIAL_PAYMENT_DAYS_INPUT,
                    partial_days,
                    "Partial Payment Days"
                )
            else:
                results["partial_payment_days"] = True
        else:
            results["partial_payment_checkbox"] = True  # Skipped
            results["partial_payment_percentage"] = True
            results["partial_payment_days"] = True
        
        # Payment Received After Delivery
        if data.get("payment_after_delivery", False):
            results["payment_after_delivery"] = self.set_checkbox(
                loc.PAYMENT_RECEIVED_CHECKBOX,
                True,
                "Payment After Delivery"
            )
        else:
            results["payment_after_delivery"] = True  # Skipped
        
        # Recurring Billing Options (Monthly, Quarterly, Semi-Annually, Annually)
        if data.get("billing_monthly", False):
            results["billing_monthly"] = self.set_checkbox(
                loc.BILLING_MONTHLY_CHECKBOX,
                True,
                "Billing Monthly"
            )
        else:
            results["billing_monthly"] = True  # Skipped
        
        if data.get("billing_quarterly", False):
            results["billing_quarterly"] = self.set_checkbox(
                loc.BILLING_QUARTERLY_CHECKBOX,
                True,
                "Billing Quarterly"
            )
        else:
            results["billing_quarterly"] = True  # Skipped
        
        if data.get("billing_semi_annually", False):
            results["billing_semi_annually"] = self.set_checkbox(
                loc.BILLING_SEMI_ANNUALLY_CHECKBOX,
                True,
                "Billing Semi-Annually"
            )
        else:
            results["billing_semi_annually"] = True  # Skipped
        
        if data.get("billing_annually", False):
            results["billing_annually"] = self.set_checkbox(
                loc.BILLING_ANNUALLY_CHECKBOX,
                True,
                "Billing Annually"
            )
        else:
            results["billing_annually"] = True  # Skipped
        
        # Outsourced to Third Party (Radio Buttons)
        if data.get("outsourced_to_third_party", False):
            results["outsourced"] = self.select_radio(
                loc.OUTSOURCED_YES_RADIO,
                "Outsourced - Yes"
            )
            # Fill explanation if YES is selected
            explanation = data.get("outsourced_explanation", "")
            if explanation:
                results["outsourced_explanation"] = self.fill_text(
                    loc.OUTSOURCED_EXPLANATION_TEXTAREA,
                    explanation,
                    "Outsourced Explanation"
                )
            else:
                results["outsourced_explanation"] = True
        else:
            results["outsourced"] = self.select_radio(
                loc.OUTSOURCED_NO_RADIO,
                "Outsourced - No"
            )
            results["outsourced_explanation"] = True  # Not needed
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Billing Questionnaire: {success_count}/{total_count} fields successful")
        
        return results

    def fill_bank_information_section(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the Bank Information section of the application.
        
        After filling verify fields for Depository Account, an alert appears.
        Clicking OK on the alert auto-populates the Fee Account section with same values.
        
        Args:
            data: Bank information data dictionary. Uses BANK_INFORMATION from osc_data if not provided.
        
        Returns:
            Dict with field names as keys and success status as values
        """
        if data is None:
            data = BANK_INFORMATION
        
        self.logger.info("Filling Bank Information section...")
        results = {}
        loc = BankInformationLocators
        
        # ===== Bank Basic Details =====
        
        # Bank Name
        results["bank_name"] = self.fill_text(
            loc.BANK_NAME_INPUT,
            data.get("bank_name", ""),
            "Bank Name"
        )
        
        # Bank Address 1
        results["address1"] = self.fill_text(
            loc.BANK_ADDRESS1_INPUT,
            data.get("address1", ""),
            "Bank Address 1"
        )
        
        # Bank Address 2
        results["address2"] = self.fill_text(
            loc.BANK_ADDRESS2_INPUT,
            data.get("address2", ""),
            "Bank Address 2"
        )
        
        # Bank City
        results["city"] = self.fill_text(
            loc.BANK_CITY_INPUT,
            data.get("city", ""),
            "Bank City"
        )
        
        # Bank State (dropdown)
        results["state"] = self.select_dropdown_by_text(
            loc.BANK_STATE_DROPDOWN,
            data.get("state", ""),
            "Bank State"
        )
        
        # Bank Zip
        results["zip_code"] = self.fill_text(
            loc.BANK_ZIP_INPUT,
            data.get("zip_code", ""),
            "Bank Zip"
        )
        
        # Bank Country (dropdown)
        results["country"] = self.select_dropdown_by_text(
            loc.BANK_COUNTRY_DROPDOWN,
            data.get("country", ""),
            "Bank Country"
        )
        
        # Bank Phone (masked input)
        phone = data.get("phone", "")
        if phone:
            results["phone"] = self.fill_masked_input(
                loc.BANK_PHONE_INPUT,
                phone,
                "Bank Phone"
            )
        else:
            results["phone"] = True  # Skipped
        
        # ===== Depository Account (Credit) =====
        
        routing_number = data.get("routing_number", "")
        account_number = data.get("account_number", "")
        
        # Routing Number
        results["routing_number"] = self.fill_text(
            loc.DEPOSITORY_ROUTING_NUMBER_INPUT,
            routing_number,
            "Depository Routing Number"
        )
        
        # Account Number
        results["account_number"] = self.fill_text(
            loc.DEPOSITORY_ACCOUNT_NUMBER_INPUT,
            account_number,
            "Depository Account Number"
        )
        
        # Verify Routing Number
        results["verify_routing"] = self.fill_text(
            loc.DEPOSITORY_ROUTING_VERIFY_INPUT,
            routing_number,
            "Verify Depository Routing"
        )
        
        # Verify Account Number
        results["verify_account"] = self.fill_text(
            loc.DEPOSITORY_ACCOUNT_VERIFY_INPUT,
            account_number,
            "Verify Depository Account"
        )
        
        # Set up dialog handler for the alert that appears when clicking Fee Routing field
        def handle_dialog(dialog):
            self.logger.info(f"Alert appeared: {dialog.message}")
            dialog.accept()
            self.logger.info("Clicked OK on alert - Fee Account should auto-populate")
        
        # Register the dialog handler
        self.page.on("dialog", handle_dialog)
        
        try:
            # Click on Fee Routing Number field to trigger the alert
            self.logger.info("Clicking Fee Routing Number field to trigger alert...")
            self.page.locator(loc.FEE_ROUTING_NUMBER_INPUT).click()
            
            # Wait for the alert to be handled and Fee Account to populate
            time.sleep(1.0)
            
        finally:
            # Remove the dialog handler to avoid affecting other operations
            self.page.remove_listener("dialog", handle_dialog)
        
        # ===== Backward Verification - Check all 4 Fee Account fields =====
        self.logger.info("Verifying Fee Account fields were auto-populated...")
        
        try:
            # Get all Fee Account field values
            fee_routing = self.page.locator(loc.FEE_ROUTING_NUMBER_INPUT).input_value()
            fee_account = self.page.locator(loc.FEE_NUMBER_INPUT).input_value()
            fee_routing_verify = self.page.locator(loc.FEE_ROUTING_VERIFY_INPUT).input_value()
            fee_account_verify = self.page.locator(loc.FEE_VERIFY_INPUT).input_value()
            
            # Verify Fee Routing Number
            if fee_routing == routing_number:
                self.logger.info(f"Fee Routing Number verified: {fee_routing}")
                results["fee_routing_auto"] = True
            else:
                self.logger.warning(f"Fee Routing mismatch. Expected: {routing_number}, Got: {fee_routing}")
                results["fee_routing_auto"] = False
            
            # Verify Fee Account Number
            if fee_account == account_number:
                self.logger.info(f"Fee Account Number verified: {fee_account}")
                results["fee_account_auto"] = True
            else:
                self.logger.warning(f"Fee Account mismatch. Expected: {account_number}, Got: {fee_account}")
                results["fee_account_auto"] = False
            
            # Verify Fee Routing Verify
            if fee_routing_verify == routing_number:
                self.logger.info(f"Fee Routing Verify verified: {fee_routing_verify}")
                results["fee_routing_verify_auto"] = True
            else:
                self.logger.warning(f"Fee Routing Verify mismatch. Expected: {routing_number}, Got: {fee_routing_verify}")
                results["fee_routing_verify_auto"] = False
            
            # Verify Fee Account Verify
            if fee_account_verify == account_number:
                self.logger.info(f"Fee Account Verify verified: {fee_account_verify}")
                results["fee_account_verify_auto"] = True
            else:
                self.logger.warning(f"Fee Account Verify mismatch. Expected: {account_number}, Got: {fee_account_verify}")
                results["fee_account_verify_auto"] = False
                
        except Exception as e:
            self.logger.warning(f"Could not verify Fee Account values: {e}")
            results["fee_routing_auto"] = False
            results["fee_account_auto"] = False
            results["fee_routing_verify_auto"] = False
            results["fee_account_verify_auto"] = False
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Bank Information: {success_count}/{total_count} fields successful")
        
        return results

    def fill_credit_card_information_section(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the Credit Card Information section of the application.
        
        This section contains dropdowns for:
        - Authorization Network
        - Settlement Bank
        - Settlement Network
        - Discount Paid
        - User Bank
        
        Args:
            data: Credit card information data dictionary. Uses CREDIT_CARD_INFORMATION from osc_data if not provided.
        
        Returns:
            Dict with field names as keys and success status as values
        """
        if data is None:
            data = CREDIT_CARD_INFORMATION
        
        self.logger.info("Filling Credit Card Information section...")
        results = {}
        loc = CreditCardInformationLocators
        
        # Authorization Network
        auth_network = data.get("authorization_network", "")
        if auth_network:
            results["authorization_network"] = self.select_dropdown_by_text(
                loc.AUTHORIZATION_NETWORK_DROPDOWN,
                auth_network,
                "Authorization Network"
            )
        else:
            results["authorization_network"] = True  # Skipped
        
        # Settlement Bank
        settlement_bank = data.get("settlement_bank", "")
        if settlement_bank:
            results["settlement_bank"] = self.select_dropdown_by_text(
                loc.SETTLEMENT_BANK_DROPDOWN,
                settlement_bank,
                "Settlement Bank"
            )
        else:
            results["settlement_bank"] = True  # Skipped
        
        # Settlement Network
        settlement_network = data.get("settlement_network", "")
        if settlement_network:
            results["settlement_network"] = self.select_dropdown_by_text(
                loc.SETTLEMENT_NETWORK_DROPDOWN,
                settlement_network,
                "Settlement Network"
            )
        else:
            results["settlement_network"] = True  # Skipped
        
        # Discount Paid
        discount_paid = data.get("discount_paid", "")
        if discount_paid:
            results["discount_paid"] = self.select_dropdown_by_text(
                loc.DISCOUNT_PAID_DROPDOWN,
                discount_paid,
                "Discount Paid"
            )
        else:
            results["discount_paid"] = True  # Skipped
        
        # User Bank
        user_bank = data.get("user_bank", "")
        if user_bank:
            results["user_bank"] = self.select_dropdown_by_text(
                loc.USER_BANK_DROPDOWN,
                user_bank,
                "User Bank"
            )
        else:
            results["user_bank"] = True  # Skipped
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Credit Card Information: {success_count}/{total_count} fields successful")
        
        return results

    def fill_credit_card_services_section(self, services: list = None) -> Dict[str, bool]:
        """
        Fill the Credit Card Services section by selecting services from the list.
        
        IMPORTANT: Each service selection causes a page reload.
        Services are selected one by one with wait for page stability after each.
        
        Args:
            services: List of service names to enable. Uses CREDIT_CARD_SERVICES from osc_data if not provided.
        
        Returns:
            Dict with service names as keys and success status as values
        """
        if services is None:
            services = CREDIT_CARD_SERVICES
        
        self.logger.info(f"Filling Credit Card Services section... ({len(services)} services to select)")
        results = {}
        
        # First, scroll to the Credit Card Services table to ensure it's visible
        services_table = self.page.locator("#ctl00_ContentPlaceHolder1_ctrlApplicationCredit1_GridView1")
        try:
            services_table.scroll_into_view_if_needed(timeout=10000)
            time.sleep(0.5)  # Brief wait after scroll
        except Exception as e:
            self.logger.warning(f"Could not scroll to services table: {e}")
        
        for service_name in services:
            try:
                self.logger.info(f"Selecting service: {service_name}")
                
                # Get the checkbox locator for this service using the static method
                checkbox_xpath = ServiceSelectionLocators.SERVICE_CHECKBOX_LOCATOR(service_name)
                self.logger.info(f"Using locator: {checkbox_xpath}")
                
                checkbox = self.page.locator(checkbox_xpath)
                
                # Wait for checkbox to be present in DOM
                try:
                    checkbox.wait_for(state="attached", timeout=10000)
                except Exception:
                    self.logger.warning(f"Service '{service_name}' checkbox not found in DOM")
                    results[service_name] = False
                    continue
                
                # Scroll to the checkbox if needed
                try:
                    checkbox.scroll_into_view_if_needed()
                    time.sleep(0.3)
                except Exception:
                    pass
                
                # Check if already selected
                if checkbox.is_checked():
                    self.logger.info(f"Service '{service_name}' already selected")
                    results[service_name] = True
                    continue
                
                # Click the checkbox - this will trigger a page reload via __doPostBack
                self.logger.info(f"Clicking checkbox for '{service_name}'...")
                checkbox.click()
                
                # Wait for page to reload/stabilize after selection
                # The onclick triggers __doPostBack which causes an ASP.NET postback
                time.sleep(2.0)  # Wait for postback to start
                
                # Wait for the page to be stable (network idle)
                self.page.wait_for_load_state("networkidle", timeout=30000)
                
                # Re-locate the checkbox after page reload
                checkbox = self.page.locator(checkbox_xpath)
                
                # Verify the checkbox is now checked after reload
                try:
                    checkbox.wait_for(state="attached", timeout=5000)
                    if checkbox.is_checked():
                        self.logger.info(f"Service '{service_name}' selected successfully")
                        results[service_name] = True
                    else:
                        self.logger.warning(f"Service '{service_name}' may not have been selected properly")
                        results[service_name] = False
                except Exception:
                    self.logger.warning(f"Could not verify '{service_name}' checkbox state after reload")
                    results[service_name] = False
                    
            except Exception as e:
                self.logger.error(f"Error selecting service '{service_name}': {e}")
                results[service_name] = False
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"Credit Card Services: {success_count}/{total_count} services selected")
        
        return results

    def fill_credit_card_underwriting_section(self, data: Dict[str, Any] = None, business_type: str = "Retail") -> Dict[str, bool]:
        """
        Fill the Credit Card Underwriting section of the application.
        
        Business Rules:
        - Card Present Swiped + Card Present Keyed + Card Not Present = 100%
        - For Grocery/Retail: Card Not Present max 30%
        - Consumer Sales + Business Sales + Government Sales = 100%
        - Monthly Volume > Average Ticket
        - Dropdown options format: '0 %', '5 %', '10 %', ... '100 %'
        
        Args:
            data: Credit card underwriting data. If None, generates random data with proper rules.
            business_type: Business type for applying rules (Grocery, Retail, MOTO, etc.)
        
        Returns:
            Dict with field names as keys and success status as values
        """
        # Generate data if not provided
        if data is None:
            data = generate_credit_card_underwriting_data(business_type)
        
        self.logger.info("Filling Credit Card Underwriting section...")
        self.logger.info(f"Data: Monthly Volume={data.get('monthly_volume')}, "
                        f"Avg Ticket={data.get('average_ticket')}, "
                        f"Swiped={data.get('card_present_swiped')}, "
                        f"Keyed={data.get('card_present_keyed')}, "
                        f"Not Present={data.get('card_not_present')}, "
                        f"Consumer={data.get('consumer_sales')}, "
                        f"Business={data.get('business_sales')}, "
                        f"Govt={data.get('government_sales')}")
        
        results = {}
        loc = CreditCardUnderwritingLocators
        
        # Scroll to Credit Card Underwriting section
        try:
            section = self.page.locator(loc.SECTION_CREDIT_CARD_UNDERWRITING)
            section.scroll_into_view_if_needed(timeout=5000)
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Could not scroll to Credit Card Underwriting section: {e}")
        
        # ===== Row 1: Monthly Volume, Card Present Swiped, Consumer Sales =====
        
        # Monthly Volume (input field)
        monthly_volume = data.get("monthly_volume", "")
        if monthly_volume:
            try:
                self.page.fill(loc.MONTHLY_VOLUME_INPUT, str(monthly_volume))
                self.logger.info(f"Monthly Volume: {monthly_volume}")
                results["monthly_volume"] = True
            except Exception as e:
                self.logger.error(f"Failed to fill Monthly Volume: {e}")
                results["monthly_volume"] = False
        
        # Card Present Swiped (dropdown)
        card_present_swiped = data.get("card_present_swiped", "")
        if card_present_swiped:
            results["card_present_swiped"] = self.select_dropdown_by_text(
                loc.CARD_PRESENT_SWIPED_DROPDOWN,
                card_present_swiped,
                "Card Present Swiped"
            )
        
        # Consumer Sales (dropdown)
        consumer_sales = data.get("consumer_sales", "")
        if consumer_sales:
            results["consumer_sales"] = self.select_dropdown_by_text(
                loc.SALES_TO_CONSUMER_DROPDOWN,
                consumer_sales,
                "Consumer Sales"
            )
        
        # ===== Row 2: Average Ticket, Card Present Keyed, Business Sales =====
        
        # Average Ticket (input field)
        average_ticket = data.get("average_ticket", "")
        if average_ticket:
            try:
                self.page.fill(loc.AVERAGE_TICKET_INPUT, str(average_ticket))
                self.logger.info(f"Average Ticket: {average_ticket}")
                results["average_ticket"] = True
            except Exception as e:
                self.logger.error(f"Failed to fill Average Ticket: {e}")
                results["average_ticket"] = False
        
        # Card Present Keyed (dropdown)
        card_present_keyed = data.get("card_present_keyed", "")
        if card_present_keyed:
            results["card_present_keyed"] = self.select_dropdown_by_text(
                loc.CARD_PRESENT_KEYED_DROPDOWN,
                card_present_keyed,
                "Card Present Keyed"
            )
        
        # Business Sales (dropdown)
        business_sales = data.get("business_sales", "")
        if business_sales:
            results["business_sales"] = self.select_dropdown_by_text(
                loc.BUSINESS_SALES_DROPDOWN,
                business_sales,
                "Business Sales"
            )
        
        # ===== Row 3: Highest Ticket, Card Not Present, Government Sales =====
        
        # Highest Ticket (input field)
        highest_ticket = data.get("highest_ticket", "")
        if highest_ticket:
            try:
                self.page.fill(loc.HIGHEST_TICKET_INPUT, str(highest_ticket))
                self.logger.info(f"Highest Ticket: {highest_ticket}")
                results["highest_ticket"] = True
            except Exception as e:
                self.logger.error(f"Failed to fill Highest Ticket: {e}")
                results["highest_ticket"] = False
        
        # Card Not Present (dropdown)
        card_not_present = data.get("card_not_present", "")
        if card_not_present:
            results["card_not_present"] = self.select_dropdown_by_text(
                loc.CARD_NOT_PRESENT_DROPDOWN,
                card_not_present,
                "Card Not Present"
            )
        
        # Government Sales (dropdown)
        government_sales = data.get("government_sales", "")
        if government_sales:
            results["government_sales"] = self.select_dropdown_by_text(
                loc.GOVERNMENT_SALES_DROPDOWN,
                government_sales,
                "Government Sales"
            )
        
        # ===== Validation: Check Totals =====
        # The totals are auto-calculated by the page, but we can log for verification
        try:
            card_total_elem = self.page.locator(loc.CREDIT_TOTAL_1_INPUT)
            if card_total_elem.is_visible():
                card_total = card_total_elem.input_value()
                self.logger.info(f"Card Present Total (auto-calculated): {card_total}")
        except Exception:
            pass
        
        try:
            sales_total_elem = self.page.locator(loc.CREDIT_TOTAL_2_INPUT)
            if sales_total_elem.is_visible():
                sales_total = sales_total_elem.input_value()
                self.logger.info(f"Sales Total (auto-calculated): {sales_total}")
        except Exception:
            pass
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        failed_fields = [k for k, v in results.items() if not v]
        
        self.logger.info(f"Credit Card Underwriting: {success_count}/{total_count} fields successful")
        if failed_fields:
            self.logger.warning(f"Failed fields: {failed_fields}")
        
        return results

    def _select_bet_from_modal(self, bet_button_locator: str, bet_number: str, card_type: str) -> bool:
        """
        Helper method to select a BET from the modal popup.
        
        Args:
            bet_button_locator: CSS selector for the BET button to click
            bet_number: The BET number to select in the modal
            card_type: Name of the card type for logging (Visa, MasterCard, etc.)
        
        Returns:
            True if BET was selected successfully, False otherwise
        """
        loc = CreditCardUnderwritingLocators
        
        try:
            self.logger.info(f"Selecting {card_type} BET: {bet_number}")
            
            # Click the BET button to open modal
            bet_button = self.page.locator(bet_button_locator)
            bet_button.scroll_into_view_if_needed()
            time.sleep(0.3)
            bet_button.click()
            
            # Wait for modal to appear
            modal = self.page.locator(loc.BET_MODAL)
            modal.wait_for(state="visible", timeout=10000)
            self.logger.info(f"{card_type} BET modal opened")
            time.sleep(0.5)  # Brief wait for modal content to load
            
            # Find the checkbox for the specific BET number
            checkbox_xpath = loc.BET_CHECKBOX_BY_NUMBER(bet_number)
            checkbox = self.page.locator(checkbox_xpath)
            
            # Try to scroll to the checkbox within the modal
            try:
                # First check if checkbox exists
                checkbox.wait_for(state="attached", timeout=5000)
                
                # Scroll the checkbox into view within the modal
                checkbox.scroll_into_view_if_needed()
                time.sleep(0.3)
            except Exception as scroll_err:
                self.logger.warning(f"Could not scroll to BET {bet_number}: {scroll_err}")
            
            # Click the checkbox
            checkbox.click()
            self.logger.info(f"Clicked checkbox for BET {bet_number}")
            
            # Wait for page to reload after BET selection
            time.sleep(2.0)
            self.page.wait_for_load_state("networkidle", timeout=30000)
            
            self.logger.info(f"{card_type} BET {bet_number} selected successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to select {card_type} BET {bet_number}: {e}")
            return False

    def _fill_input_fast(self, locator: str, value: str, field_name: str) -> bool:
        """
        Fast input fill without alert handling. Used for discount fields
        and when manually filling after alert cancel.
        
        Args:
            locator: The CSS/XPath locator for the input field
            value: The value to fill
            field_name: Name of the field for logging
        
        Returns:
            True if field was filled successfully, False otherwise
        """
        try:
            input_field = self.page.locator(locator)
            input_field.scroll_into_view_if_needed()
            input_field.clear()
            input_field.fill(str(value))
            self.logger.info(f"{field_name}: {value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to fill {field_name}: {e}")
            return False

    def _fill_rates_with_copy_alert(self, data: Dict[str, Any], does_not_accept_amex: bool) -> Dict[str, bool]:
        """
        Fill rate fields with smart alert handling.
        
        Logic:
        1. Fill VISA_QUALIFIED_RATE_INPUT
        2. Click VISA_SIGNATURE_RATE_INPUT to trigger the "copy to all" alert
        3. 90% of time: Accept (OK) → auto-copies to all rate/signature fields
        4. 10% of time: Cancel → manually fill all remaining fields
        
        Args:
            data: Credit card interchange data
            does_not_accept_amex: Whether merchant does not accept AMEX
        
        Returns:
            Dict with field names as keys and success status as values
        """
        import random
        
        results = {}
        loc = CreditCardUnderwritingLocators
        
        # Track whether alert was accepted (rates auto-copied)
        rates_copied = False
        dialog_appeared = False
        
        # Randomly decide: 90% accept, 10% cancel
        accept_copy = random.random() < 0.90
        self.logger.info(f"Rate copy decision: {'Accept (OK)' if accept_copy else 'Cancel'}")
        
        # Set up dialog handler
        def handle_dialog(dialog):
            nonlocal rates_copied, dialog_appeared
            dialog_appeared = True
            self.logger.info(f"Alert appeared: '{dialog.message}'")
            # Add small delay to make the alert visible
            time.sleep(0.5)
            if accept_copy:
                self.logger.info("Clicking OK (copying rates to all fields)")
                dialog.accept()
                rates_copied = True
            else:
                self.logger.info("Clicking Cancel (will fill fields manually)")
                dialog.dismiss()
        
        # Step 1: Fill Visa Qualified Rate
        visa_qualified_rate = data.get("visa_qualified_rate", "")
        if visa_qualified_rate:
            results["visa_qualified_rate"] = self._fill_input_fast(
                loc.VISA_QUALIFIED_RATE_INPUT,
                visa_qualified_rate,
                "Visa Qualified Rate"
            )
            # Small pause after typing qualified rate before clicking signature field
            time.sleep(0.3)
        
        # Step 2: Add dialog handler
        self.page.on("dialog", handle_dialog)
        
        try:
            # Scroll to and click on Visa Signature Rate field - this triggers the alert
            self.logger.info("Clicking on Visa Signature Rate field to trigger copy alert...")
            signature_field = self.page.locator(loc.VISA_SIGNATURE_RATE_INPUT)
            signature_field.scroll_into_view_if_needed()
            time.sleep(0.2)
            signature_field.click()
            
            # Wait for dialog to be handled
            time.sleep(0.8)
            
        except Exception as e:
            self.logger.error(f"Error clicking signature field: {e}")
        
        # Remove dialog handler
        try:
            self.page.remove_listener("dialog", handle_dialog)
        except:
            pass
        
        if rates_copied:
            # Rates were auto-copied by accepting the alert
            self.logger.info("✅ Rates auto-copied to all fields via OK selection")
            
            # Mark all rate fields as successful (they were copied)
            results["visa_signature_rate"] = True
            results["mc_qualified_rate"] = True
            results["mc_signature_rate"] = True
            results["discover_qualified_rate"] = True
            results["discover_signature_rate"] = True
            if not does_not_accept_amex:
                results["amex_qualified_rate"] = True
        else:
            # Alert was cancelled OR didn't appear - manually fill all remaining rate fields
            if dialog_appeared:
                self.logger.info("Alert was cancelled - manually filling all rate fields")
            else:
                self.logger.warning("No alert appeared - manually filling all rate fields")
            
            # Small pause after alert handling
            time.sleep(0.3)
            
            # Clear and fill Visa Signature Rate
            # Important: The field may have inherited value from qualified rate, so clear it first
            visa_signature_rate = data.get("visa_signature_rate", "")
            if visa_signature_rate:
                try:
                    sig_field = self.page.locator(loc.VISA_SIGNATURE_RATE_INPUT)
                    # Triple-click to select all, then clear
                    sig_field.click(click_count=3)
                    time.sleep(0.1)
                    sig_field.fill("")
                    time.sleep(0.1)
                    sig_field.fill(str(visa_signature_rate))
                    self.logger.info(f"Visa Signature Plan: {visa_signature_rate}")
                    results["visa_signature_rate"] = True
                except Exception as e:
                    self.logger.error(f"Failed to fill Visa Signature Plan: {e}")
                    results["visa_signature_rate"] = False
            
            # MasterCard Qualified Rate
            mc_qualified_rate = data.get("mc_qualified_rate", "")
            if mc_qualified_rate:
                results["mc_qualified_rate"] = self._fill_input_fast(
                    loc.MC_QUALIFIED_RATE_INPUT,
                    mc_qualified_rate,
                    "MasterCard Qualified Rate"
                )
            
            # MasterCard Signature Plan
            mc_signature_rate = data.get("mc_signature_rate", "")
            if mc_signature_rate:
                results["mc_signature_rate"] = self._fill_input_fast(
                    loc.MC_SIGNATURE_RATE_INPUT,
                    mc_signature_rate,
                    "MasterCard Signature Plan"
                )
            
            # Discover Qualified Rate
            discover_qualified_rate = data.get("discover_qualified_rate", "")
            if discover_qualified_rate:
                results["discover_qualified_rate"] = self._fill_input_fast(
                    loc.DISCOVER_QUALIFIED_RATE_INPUT,
                    discover_qualified_rate,
                    "Discover Qualified Rate"
                )
            
            # Discover Signature Plan
            discover_signature_rate = data.get("discover_signature_rate", "")
            if discover_signature_rate:
                results["discover_signature_rate"] = self._fill_input_fast(
                    loc.DISCOVER_SIGNATURE_RATE_INPUT,
                    discover_signature_rate,
                    "Discover Signature Plan"
                )
            
            # AMEX Qualified Rate (only if accepting AMEX)
            if not does_not_accept_amex:
                amex_qualified_rate = data.get("amex_qualified_rate", "")
                if amex_qualified_rate:
                    results["amex_qualified_rate"] = self._fill_input_fast(
                        loc.AMEX_QUALIFIED_RATE_INPUT,
                        amex_qualified_rate,
                        "AMEX Qualified Rate"
                    )
        
        return results

    def fill_credit_card_interchange_section(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the Credit Card Interchange section of the application.
        
        This section includes:
        - Interchange Type dropdown
        - Chargeback dropdown
        - FANF Type dropdown
        - Visa BET selection (opens modal)
        - MasterCard BET selection (opens modal)
        - Discover BET selection (opens modal)
        - AMEX BET selection (opens modal)
        - AMEX options (Does not accept, Opt out marketing, Annual Volume)
        
        Args:
            data: Credit card interchange data. Uses CREDIT_CARD_INTERCHANGE from osc_data if not provided.
        
        Returns:
            Dict with field names as keys and success status as values
        """
        if data is None:
            data = CREDIT_CARD_INTERCHANGE
        
        self.logger.info("Filling Credit Card Interchange section...")
        self.logger.info(f"Data: Type={data.get('interchange_type')}, "
                        f"Visa BET={data.get('visa_bet_number')}, "
                        f"MC BET={data.get('mastercard_bet_number')}, "
                        f"Discover BET={data.get('discover_bet_number')}, "
                        f"AMEX BET={data.get('amex_bet_number')}, "
                        f"Does not accept AMEX={data.get('does_not_accept_amex')}")
        
        results = {}
        loc = CreditCardUnderwritingLocators
        
        # Scroll to Credit Card Interchange section
        try:
            section = self.page.locator(loc.SECTION_CREDIT_CARD_INTERCHANGE)
            section.scroll_into_view_if_needed(timeout=5000)
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Could not scroll to Credit Card Interchange section: {e}")
        
        # ===== Interchange Type Dropdown =====
        interchange_type = data.get("interchange_type", "")
        if interchange_type:
            results["interchange_type"] = self.select_dropdown_by_text(
                loc.INTERCHANGE_TYPE_DROPDOWN,
                interchange_type,
                "Interchange Type"
            )
        
        # ===== Chargeback Dropdown =====
        chargeback = data.get("chargeback", "")
        if chargeback:
            results["chargeback"] = self.select_dropdown_by_text(
                loc.CHARGEBACK_BET_DROPDOWN,
                chargeback,
                "Chargeback"
            )
        
        # ===== FANF Type Dropdown =====
        fanf_type = data.get("fanf_type", "")
        if fanf_type:
            results["fanf_type"] = self.select_dropdown_by_text(
                loc.FANF_TYPE_DROPDOWN,
                fanf_type,
                "FANF Type"
            )
        
        # ===== Visa BET Selection =====
        visa_bet = data.get("visa_bet_number", "")
        if visa_bet:
            results["visa_bet"] = self._select_bet_from_modal(
                loc.VISA_BET_BUTTON,
                visa_bet,
                "Visa"
            )
        
        # ===== MasterCard BET Selection =====
        mc_bet = data.get("mastercard_bet_number", "")
        if mc_bet:
            results["mastercard_bet"] = self._select_bet_from_modal(
                loc.MC_BET_BUTTON,
                mc_bet,
                "MasterCard"
            )
        
        # ===== Discover BET Selection =====
        discover_bet = data.get("discover_bet_number", "")
        if discover_bet:
            results["discover_bet"] = self._select_bet_from_modal(
                loc.DISCOVER_BET_BUTTON,
                discover_bet,
                "Discover"
            )
        
        # ===== AMEX Section =====
        does_not_accept_amex = data.get("does_not_accept_amex", False)
        
        if does_not_accept_amex:
            # Select "Does not wish to accept Amex Cards" checkbox
            try:
                amex_checkbox = self.page.locator(loc.AMEX_NOT_ACCEPT_CHECKBOX)
                amex_checkbox.scroll_into_view_if_needed()
                time.sleep(0.3)
                
                if not amex_checkbox.is_checked():
                    amex_checkbox.click()
                    self.logger.info("Selected 'Does not wish to accept Amex Cards'")
                else:
                    self.logger.info("'Does not wish to accept Amex Cards' already selected")
                
                results["does_not_accept_amex"] = True
            except Exception as e:
                self.logger.error(f"Failed to select 'Does not accept AMEX' checkbox: {e}")
                results["does_not_accept_amex"] = False
        else:
            # Merchant accepts AMEX - select BET
            amex_bet = data.get("amex_bet_number", "")
            if amex_bet:
                results["amex_bet"] = self._select_bet_from_modal(
                    loc.AMEX_BET_BUTTON,
                    amex_bet,
                    "AMEX"
                )
        
        # =====================================================================
        # FILL RATES WITH SMART ALERT HANDLING
        # Logic: Fill Visa Qualified Rate, click Signature to trigger alert
        # 90% time: OK copies rates to all fields; 10% time: Cancel, fill manually
        # =====================================================================
        rate_results = self._fill_rates_with_copy_alert(data, does_not_accept_amex)
        results.update(rate_results)
        
        # =====================================================================
        # FILL ALL DISCOUNT PER ITEM FIELDS (no alert handling needed)
        # =====================================================================
        self.logger.info("Filling Discount Per Item for all card brands...")
        
        # Visa Discount Per Item
        visa_discount_per_item = data.get("visa_discount_per_item", "")
        if visa_discount_per_item:
            results["visa_discount_per_item"] = self._fill_input_fast(
                loc.VISA_DISCOUNT_PER_ITEM_INPUT,
                visa_discount_per_item,
                "Visa Discount Per Item"
            )
        
        # Visa Signature Discount Per Item
        visa_signature_discount = data.get("visa_signature_discount", "")
        if visa_signature_discount:
            results["visa_signature_discount"] = self._fill_input_fast(
                loc.VISA_SIGNATURE_DISCOUNT_INPUT,
                visa_signature_discount,
                "Visa Signature Discount"
            )
        
        # MasterCard Discount Per Item
        mc_discount_per_item = data.get("mc_discount_per_item", "")
        if mc_discount_per_item:
            results["mc_discount_per_item"] = self._fill_input_fast(
                loc.MC_DISCOUNT_PER_ITEM_INPUT,
                mc_discount_per_item,
                "MasterCard Discount Per Item"
            )
        
        # MasterCard Signature Discount Per Item
        mc_signature_discount = data.get("mc_signature_discount", "")
        if mc_signature_discount:
            results["mc_signature_discount"] = self._fill_input_fast(
                loc.MC_SIGNATURE_DISCOUNT_INPUT,
                mc_signature_discount,
                "MasterCard Signature Discount"
            )
        
        # Discover Discount Per Item
        discover_discount_per_item = data.get("discover_discount_per_item", "")
        if discover_discount_per_item:
            results["discover_discount_per_item"] = self._fill_input_fast(
                loc.DISCOVER_DISCOUNT_PER_ITEM_INPUT,
                discover_discount_per_item,
                "Discover Discount Per Item"
            )
        
        # Discover Signature Discount Per Item
        discover_signature_discount = data.get("discover_signature_discount", "")
        if discover_signature_discount:
            results["discover_signature_discount"] = self._fill_input_fast(
                loc.DISCOVER_SIGNATURE_DISCOUNT_INPUT,
                discover_signature_discount,
                "Discover Signature Discount"
            )
        
        # AMEX Discount Per Item (only if accepting AMEX)
        if not does_not_accept_amex:
            amex_discount_per_item = data.get("amex_discount_per_item", "")
            if amex_discount_per_item:
                results["amex_discount_per_item"] = self._fill_input_fast(
                    loc.AMEX_DISCOUNT_PER_ITEM_INPUT,
                    amex_discount_per_item,
                    "AMEX Discount Per Item"
                )
            
            # AMEX Annual Volume
            amex_annual_volume = data.get("amex_annual_volume", "")
            if amex_annual_volume:
                results["amex_annual_volume"] = self._fill_input_fast(
                    loc.AMEX_ANNUAL_VOLUME_INPUT,
                    amex_annual_volume,
                    "AMEX Annual Volume"
                )
        
        # ===== AMEX Opt-out Marketing (applies regardless of acceptance) =====
        amex_optout = data.get("amex_optout_marketing", False)
        if amex_optout:
            try:
                optout_checkbox = self.page.locator(loc.AMEX_OPTOUT_MARKETING_CHECKBOX)
                optout_checkbox.scroll_into_view_if_needed()
                time.sleep(0.3)
                
                if not optout_checkbox.is_checked():
                    optout_checkbox.click()
                    self.logger.info("Selected AMEX opt-out marketing checkbox")
                else:
                    self.logger.info("AMEX opt-out marketing already selected") 
                
                results["amex_optout_marketing"] = True
            except Exception as e:
                self.logger.error(f"Failed to select AMEX opt-out marketing checkbox: {e}")
                results["amex_optout_marketing"] = False
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        failed_fields = [k for k, v in results.items() if not v]
        
        self.logger.info(f"Credit Card Interchange: {success_count}/{total_count} fields successful")
        if failed_fields:
            self.logger.warning(f"Failed fields: {failed_fields}")
        
        return results

    # =========================================================================
    # TERMINAL WIZARD SECTION
    # =========================================================================
    
    @performance_step("add_terminals")
    @log_step
    def add_terminals(self, terminals_list: list = None) -> Dict[str, Any]:
        """
        Add terminals using the Terminal Wizard.
        
        This is a wrapper method that delegates to AddTerminalPage for the actual
        wizard automation. The AddTerminalPage is kept isolated for maintenance.
        
        Args:
            terminals_list: List of terminal configuration dicts. If None, uses
                           TERMINALS_TO_ADD from add_terminal_data.
        
        Returns:
            Dict with results:
                - success_count: Number of terminals successfully added
                - failed_count: Number of terminals that failed
                - results: Dict of individual results by terminal name
                - added_terminals: List of successfully added terminal configs
        """
        # Use default terminals if none provided
        if terminals_list is None:
            terminals_list = TERMINALS_TO_ADD
        
        self.logger.info(f"Adding {len(terminals_list)} terminal(s) via Terminal Wizard")
        
        # Log terminals to be added
        for terminal in terminals_list:
            self.logger.info(f"Terminal to add: {terminal.get('name')} "
                           f"(Part Type={terminal.get('part_type')}, Provider={terminal.get('provider')})")
        
        # Delegate to AddTerminalPage (isolated for maintenance)
        add_terminal_page = AddTerminalPage(self.page)
        results = add_terminal_page.add_terminals(terminals_list)
        
        # Log summary
        success_count = results.get("success_count", 0)
        total_count = len(terminals_list)
        added_terminals = results.get("added_terminals", [])
        
        if added_terminals:
            self.logger.info(f"Successfully added {len(added_terminals)} terminal(s)")
            for t in added_terminals:
                self.logger.info(f"  - {t['name']} (index: {t['index']})")
        
        if success_count == total_count:
            self.logger.info(f"Terminal Wizard: {success_count}/{total_count} terminals added successfully")
        else:
            failed = [name for name, res in results.get("results", {}).items() 
                     if not res.get("step1", False)]
            self.logger.warning(f"Terminal Wizard: {success_count}/{total_count}. Failed: {failed}")
        
        return results

    # =========================================================================
    # ACH SECTION
    # =========================================================================
    
    @performance_step("scroll_to_ach_section")
    @log_step
    def scroll_to_ach_section(self) -> bool:
        """
        Scroll to the ACH section and verify it's visible.
        
        Returns:
            bool: True if ACH section is visible, False otherwise
        """
        try:
            ach_header = self.page.locator(ACHSectionLocators.STEP_ACH_HEADER)
            ach_header.scroll_into_view_if_needed(timeout=10000)
            time.sleep(0.5)
            
            if ach_header.is_visible():
                self.logger.info("✅ Scrolled to ACH section - header visible")
                return True
            else:
                self.logger.error("ACH section header not visible after scroll")
                return False
        except Exception as e:
            self.logger.error(f"Failed to scroll to ACH section: {e}")
            return False

    @performance_step("select_ach_services")
    @log_step
    def select_ach_services(self, services: list = None) -> Dict[str, bool]:
        """
        Select ACH services from the ACH Services table.
        
        IMPORTANT: Each service selection causes a page reload (like Credit Card services).
        Services are selected one by one with wait for page stability after each.
        
        Args:
            services: List of ACH service names to enable. 
                     Uses ACH_SERVICES from test data if not provided.
        
        Returns:
            Dict with service names as keys and success status as values
        """
        # Import ACH_SERVICES from dynamically loaded data
        if services is None:
            services = _data.ACH_SERVICES
        
        self.logger.info(f"Selecting ACH Services... ({len(services)} services to select)")
        results = {}
        
        # First, scroll to the ACH section
        self.scroll_to_ach_section()
        time.sleep(0.5)
        
        for service_name in services:
            try:
                self.logger.info(f"Selecting ACH service: {service_name}")
                
                # Get the checkbox locator using the dynamic method
                checkbox_xpath = ACHSectionLocators.STEP_ACH_SERVICE_CHECKBOX(service_name)
                self.logger.info(f"Using locator: {checkbox_xpath}")
                
                checkbox = self.page.locator(checkbox_xpath)
                
                # Wait for checkbox to be present in DOM
                try:
                    checkbox.wait_for(state="attached", timeout=10000)
                except Exception:
                    self.logger.warning(f"ACH Service '{service_name}' checkbox not found in DOM")
                    results[service_name] = False
                    continue
                
                # Scroll to the checkbox if needed
                try:
                    checkbox.scroll_into_view_if_needed()
                    time.sleep(0.3)
                except Exception:
                    pass
                
                # Check if already selected
                if checkbox.is_checked():
                    self.logger.info(f"ACH Service '{service_name}' already selected")
                    results[service_name] = True
                    continue
                
                # Click the checkbox - this will trigger a page reload via __doPostBack
                self.logger.info(f"Clicking checkbox for ACH service '{service_name}'...")
                checkbox.click()
                
                # Wait for page to reload/stabilize after selection
                time.sleep(2.0)  # Wait for postback to start
                
                # Wait for the page to be stable (network idle)
                self.page.wait_for_load_state("networkidle", timeout=30000)
                
                # Re-locate the checkbox after page reload
                checkbox = self.page.locator(checkbox_xpath)
                
                # Verify the checkbox is now checked after reload
                try:
                    checkbox.wait_for(state="attached", timeout=5000)
                    if checkbox.is_checked():
                        self.logger.info(f"ACH Service '{service_name}' selected successfully")
                        results[service_name] = True
                    else:
                        self.logger.warning(f"ACH Service '{service_name}' may not have been selected properly")
                        results[service_name] = False
                except Exception:
                    self.logger.warning(f"Could not verify '{service_name}' checkbox state after reload")
                    results[service_name] = False
                    
            except Exception as e:
                self.logger.error(f"Error selecting ACH service '{service_name}': {e}")
                results[service_name] = False
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        self.logger.info(f"ACH Services: {success_count}/{total_count} services selected")
        
        return results

    @performance_step("fill_ach_underwriting_profile")
    @log_step
    def fill_ach_underwriting_profile(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the ACH Underwriting Profile section.
        
        Business Rules:
        - Written + Non-Written = 100% (interval of 1, auto-calculated)
        - Merchant + Consumer = 100% (interval of 1, auto-calculated)
        - Only Written and Merchant need to be selected; Non-Written and Consumer auto-fill
        
        Args:
            data: ACH underwriting data. If None, uses ACH_UNDERWRITING from test data.
        
        Returns:
            Dict with field names as keys and success status as values
        """
        # Import ACH_UNDERWRITING from dynamically loaded data
        if data is None:
            data = _data.ACH_UNDERWRITING
        
        self.logger.info("Filling ACH Underwriting Profile section...")
        self.logger.info(f"Data: Annual Volume={data.get('annual_volume')}, "
                        f"Avg Ticket={data.get('avg_ticket')}, "
                        f"Highest Ticket={data.get('highest_ticket')}, "
                        f"Written={data.get('written_pct')}%, "
                        f"Merchant={data.get('merchant_pct')}%")
        
        results = {}
        loc = ACHSectionLocators
        
        # Scroll to ACH section first
        self.scroll_to_ach_section()
        time.sleep(0.5)
        
        # ===== Row 1: Annual Volume, Written %, Merchant % =====
        
        # Annual Volume (input field)
        annual_volume = data.get("annual_volume", "")
        if annual_volume:
            try:
                self.page.fill(loc.STEP_ACH_ANNUAL_VOLUME_INPUT, str(annual_volume))
                self.logger.info(f"Annual Volume: {annual_volume}")
                results["annual_volume"] = True
            except Exception as e:
                self.logger.error(f"Failed to fill Annual Volume: {e}")
                results["annual_volume"] = False
        
        # Written % (dropdown) - format: "X %"
        written_pct = data.get("written_pct", "")
        if written_pct:
            try:
                written_value = f"{written_pct} %"
                self.page.select_option(loc.STEP_ACH_WRITTEN_DROPDOWN, label=written_value)
                self.logger.info(f"Written %: {written_value}")
                results["written_pct"] = True
            except Exception as e:
                self.logger.error(f"Failed to select Written %: {e}")
                results["written_pct"] = False
        
        # Merchant % (dropdown) - format: "X %"
        merchant_pct = data.get("merchant_pct", "")
        if merchant_pct:
            try:
                merchant_value = f"{merchant_pct} %"
                self.page.select_option(loc.STEP_ACH_MERCHANT_DROPDOWN, label=merchant_value)
                self.logger.info(f"Merchant %: {merchant_value}")
                results["merchant_pct"] = True
            except Exception as e:
                self.logger.error(f"Failed to select Merchant %: {e}")
                results["merchant_pct"] = False
        
        # ===== Row 2: Average Ticket =====
        
        # Average Ticket (input field)
        avg_ticket = data.get("avg_ticket", "")
        if avg_ticket:
            try:
                self.page.fill(loc.STEP_ACH_AVG_TICKET_INPUT, str(avg_ticket))
                self.logger.info(f"Average Ticket: {avg_ticket}")
                results["avg_ticket"] = True
            except Exception as e:
                self.logger.error(f"Failed to fill Average Ticket: {e}")
                results["avg_ticket"] = False
        
        # Non-Written and Consumer are auto-calculated, no need to fill
        
        # ===== Row 3: Highest Ticket =====
        
        # Highest Ticket (input field)
        highest_ticket = data.get("highest_ticket", "")
        if highest_ticket:
            try:
                self.page.fill(loc.STEP_ACH_HIGHEST_TICKET_INPUT, str(highest_ticket))
                self.logger.info(f"Highest Ticket: {highest_ticket}")
                results["highest_ticket"] = True
            except Exception as e:
                self.logger.error(f"Failed to fill Highest Ticket: {e}")
                results["highest_ticket"] = False
        
        # ===== Reporting Section =====
        
        # Send Email checkbox
        send_email = data.get("send_email", True)
        if send_email:
            try:
                email_checkbox = self.page.locator(loc.STEP_ACH_SEND_EMAIL_CHECKBOX)
                if not email_checkbox.is_checked():
                    email_checkbox.click()
                    time.sleep(0.3)
                self.logger.info("Send Email: checked")
                results["send_email"] = True
            except Exception as e:
                self.logger.error(f"Failed to check Send Email: {e}")
                results["send_email"] = False
        
        # Send Fax checkbox
        send_fax = data.get("send_fax", True)
        if send_fax:
            try:
                fax_checkbox = self.page.locator(loc.STEP_ACH_SEND_FAX_CHECKBOX)
                if not fax_checkbox.is_checked():
                    fax_checkbox.click()
                    time.sleep(0.3)
                self.logger.info("Send Fax: checked")
                results["send_fax"] = True
            except Exception as e:
                self.logger.error(f"Failed to check Send Fax: {e}")
                results["send_fax"] = False
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        failed_fields = [k for k, v in results.items() if not v]
        
        self.logger.info(f"ACH Underwriting Profile: {success_count}/{total_count} fields successful")
        if failed_fields:
            self.logger.warning(f"Failed fields: {failed_fields}")
        
        return results

    def _fill_ach_fee_field(self, locator: str, value: str, field_name: str, delay_ms: int = 100) -> bool:
        """
        Helper method to fill ACH fee fields with slow keyboard typing.
        
        Clears the field first, then types value character by character with delay.
        
        Args:
            locator: XPath or CSS selector for the input field
            value: Value to type (e.g., "123.45")
            field_name: Friendly name for logging
            delay_ms: Delay between keystrokes in milliseconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=5000)
            
            # Click to focus
            element.click()
            time.sleep(0.1)
            
            # Clear existing content
            element.clear()
            time.sleep(0.1)
            
            # Type each character slowly like keyboard press
            for char in str(value):
                self.page.keyboard.press(char)
                time.sleep(delay_ms / 1000)
            
            self.logger.info(f"{field_name}: {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to fill {field_name}: {e}")
            return False

    @performance_step("fill_ach_fees")
    @log_step
    def fill_ach_fees(self, data: Dict[str, Any] = None) -> Dict[str, bool]:
        """
        Fill the ACH Fees and Miscellaneous Fees sections.
        
        Uses slow keyboard typing (like phone fields) for reliable input.
        Clears each field before typing.
        Does NOT modify Billing Cycle dropdown.
        
        ACH Fees:
        - CCD Written (Rate, Fee)
        - CCD Non-Written (Rate, Fee)
        - PPD Written (Rate, Fee)
        - PPD Non-Written (Rate, Fee)
        - WEB (Rate, Fee)
        - ARC (Rate, Fee)
        
        Miscellaneous Fees:
        - Statement Fee, Minimum Fee, File Fee, Reject Fee, Gateway Fee, Maintenance Fee
        
        Args:
            data: ACH fees data dict. If None, uses ACH_FEES from test data.
        
        Returns:
            Dict with field names as keys and success status as values
        """
        # Import ACH_FEES from dynamically loaded data
        if data is None:
            data = _data.ACH_FEES
        
        self.logger.info("Filling ACH Fees and Miscellaneous Fees sections...")
        results = {}
        loc = ACHSectionLocators
        
        # Scroll to ACH section first to ensure visibility
        self.scroll_to_ach_section()
        time.sleep(0.5)
        
        # ===== ACH FEES SECTION =====
        # Using dynamic locators: ach_rate_input(label) and ach_fee_input(label)
        
        ach_fee_fields = [
            ("CCD Written", "ccd_written_rate", "ccd_written_fee"),
            ("CCD Non-Written", "ccd_non_written_rate", "ccd_non_written_fee"),
            ("PPD Written", "ppd_written_rate", "ppd_written_fee"),
            ("PPD Non-Written", "ppd_non_written_rate", "ppd_non_written_fee"),
            ("WEB", "web_rate", "web_fee"),
            ("ARC", "arc_rate", "arc_fee"),
        ]
        
        for label, rate_key, fee_key in ach_fee_fields:
            # Fill Rate column
            rate_value = data.get(rate_key, "")
            if rate_value:
                rate_locator = loc.ach_rate_input(label)
                results[rate_key] = self._fill_ach_fee_field(
                    rate_locator, rate_value, f"{label} Rate"
                )
            
            # Fill Fee column
            fee_value = data.get(fee_key, "")
            if fee_value:
                fee_locator = loc.ach_fee_input(label)
                results[fee_key] = self._fill_ach_fee_field(
                    fee_locator, fee_value, f"{label} Fee"
                )
        
        # ===== MISCELLANEOUS FEES SECTION =====
        # Using dynamic locator: misc_fee_input(fee_name)
        
        misc_fee_fields = [
            ("Statement Fee", "statement_fee"),
            ("Minimum Fee", "minimum_fee"),
            ("File Fee", "file_fee"),
            ("Reject Fee", "reject_fee"),
            ("Gateway Fee", "gateway_fee"),
            ("Maintenance Fee", "maintenance_fee"),
        ]
        
        for label, data_key in misc_fee_fields:
            fee_value = data.get(data_key, "")
            if fee_value:
                fee_locator = loc.misc_fee_input(label)
                results[data_key] = self._fill_ach_fee_field(
                    fee_locator, fee_value, label
                )
        
        # NOTE: Billing Cycle dropdown is NOT modified - left as default "Monthly"
        
        # Summary
        success_count = sum(1 for r in results.values() if r)
        total_count = len(results)
        failed_fields = [k for k, v in results.items() if not v]
        
        self.logger.info(f"ACH Fees: {success_count}/{total_count} fields successful")
        if failed_fields:
            self.logger.warning(f"Failed fields: {failed_fields}")
        
        return results

    @performance_step("add_ach_originator")
    @log_step
    def add_ach_originator(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Add an ACH Originator via the Add Originator modal wizard.
        
        Steps:
        1. Verify Originator section header
        2. Click Add Originator button
        3. Verify modal title
        4. Fill Step 1: Description, Transaction Type, Checkboxes, Bank Info
        5. Click Copy Below button to fill Fees and Rejects bank info
        6. Click Next button
        7. Verify originator added to table
        
        Args:
            data: ACH originator data dict. If None, uses ACH_ORIGINATOR from test data.
        
        Returns:
            Dict with:
                - success: bool
                - description: originator description added
                - results: dict of individual field results
                - verified: bool if originator appears in table
        """
        # Import ACH_ORIGINATOR from dynamically loaded data
        if data is None:
            data = _data.ACH_ORIGINATOR
        
        self.logger.info("Adding ACH Originator...")
        self.logger.info(f"Data: Description={data.get('description')}, "
                        f"Transaction Type={data.get('transaction_type')}, "
                        f"Written={data.get('written_authorization')}, "
                        f"Resubmit R01={data.get('resubmit_r01')}")
        
        results = {}
        loc = ACHOriginatorLocators
        description = data.get("description", "")
        
        try:
            # Step 1: Verify Originator section header
            self.logger.info("Step 1: Verifying Originator section header")
            try:
                originator_header = self.page.locator(loc.ORIGINATOR_HEADER)
                originator_header.scroll_into_view_if_needed(timeout=10000)
                time.sleep(0.5)
                if originator_header.is_visible():
                    self.logger.info("✅ Originator section header visible")
                    results["header_visible"] = True
                else:
                    self.logger.warning("Originator section header not visible")
                    results["header_visible"] = False
            except Exception as e:
                self.logger.warning(f"Could not verify header: {e}")
                results["header_visible"] = False
            
            # Step 2: Click Add Originator button
            self.logger.info("Step 2: Clicking Add Originator button")
            add_btn = self.page.locator(loc.ADD_ORIGINATOR_BUTTON)
            add_btn.wait_for(state="visible", timeout=10000)
            add_btn.click()
            time.sleep(1)  # Wait for modal to open
            results["add_button_clicked"] = True
            
            # Step 3: Verify modal title
            self.logger.info("Step 3: Verifying Add Originator modal")
            modal_title = self.page.locator(loc.MODAL_TITLE)
            try:
                modal_title.wait_for(state="visible", timeout=10000)
                self.logger.info("✅ Add Originator modal opened")
                results["modal_opened"] = True
            except Exception as e:
                self.logger.error(f"Modal did not open: {e}")
                results["modal_opened"] = False
                return {"success": False, "description": description, "results": results, "verified": False}
            
            # Step 4a: Fill Description
            self.logger.info("Step 4a: Filling Description")
            if description:
                try:
                    self.page.fill(loc.STEP_1_DESCRIPTION_INPUT, description)
                    self.logger.info(f"Description: {description}")
                    results["description"] = True
                except Exception as e:
                    self.logger.error(f"Failed to fill Description: {e}")
                    results["description"] = False
            
            # Step 4b: Select Transaction Type
            self.logger.info("Step 4b: Selecting Transaction Type")
            transaction_type = data.get("transaction_type", "ARC")
            try:
                self.page.select_option(loc.STEP_1_TRANSACTION_TYPE_DROPDOWN, label=transaction_type)
                self.logger.info(f"Transaction Type: {transaction_type}")
                results["transaction_type"] = True
            except Exception as e:
                self.logger.error(f"Failed to select Transaction Type: {e}")
                results["transaction_type"] = False
            
            # Step 4c: Set Written Authorization checkbox
            written_auth = data.get("written_authorization", False)
            self.logger.info(f"Step 4c: Written Authorization checkbox = {written_auth}")
            try:
                written_checkbox = self.page.locator(loc.STEP_1_CHECKBOX_WRITTEN)
                is_checked = written_checkbox.is_checked()
                if written_auth and not is_checked:
                    written_checkbox.click()
                    time.sleep(0.3)
                elif not written_auth and is_checked:
                    written_checkbox.click()
                    time.sleep(0.3)
                self.logger.info(f"Written Authorization: {'checked' if written_auth else 'unchecked'}")
                results["written_authorization"] = True
            except Exception as e:
                self.logger.error(f"Failed to set Written Authorization: {e}")
                results["written_authorization"] = False
            
            # Step 4d: Set Resubmit R01 checkbox
            resubmit_r01 = data.get("resubmit_r01", False)
            self.logger.info(f"Step 4d: Resubmit R01 checkbox = {resubmit_r01}")
            try:
                resubmit_checkbox = self.page.locator(loc.STEP_1_CHECKBOX_RESUBMIT_R01)
                is_checked = resubmit_checkbox.is_checked()
                if resubmit_r01 and not is_checked:
                    resubmit_checkbox.click()
                    time.sleep(0.3)
                elif not resubmit_r01 and is_checked:
                    resubmit_checkbox.click()
                    time.sleep(0.3)
                self.logger.info(f"Resubmit R01: {'checked' if resubmit_r01 else 'unchecked'}")
                results["resubmit_r01"] = True
            except Exception as e:
                self.logger.error(f"Failed to set Resubmit R01: {e}")
                results["resubmit_r01"] = False
            
            # Step 4e: Fill Disbursements Bank Info
            self.logger.info("Step 4e: Filling Disbursements Bank Information")
            routing_number = data.get("routing_number", "")
            account_number = data.get("account_number", "")
            
            if routing_number:
                try:
                    self.page.fill(loc.STEP_1_DISBURSE_ROUTING_INPUT, routing_number)
                    self.logger.info(f"Disbursements Routing #: {routing_number}")
                    results["disburse_routing"] = True
                except Exception as e:
                    self.logger.error(f"Failed to fill Disbursements Routing: {e}")
                    results["disburse_routing"] = False
            
            if account_number:
                try:
                    self.page.fill(loc.STEP_1_DISBURSE_ACCOUNT_INPUT, account_number)
                    self.logger.info(f"Disbursements Account #: {account_number}")
                    results["disburse_account"] = True
                except Exception as e:
                    self.logger.error(f"Failed to fill Disbursements Account: {e}")
                    results["disburse_account"] = False
            
            # Step 4f: Click Copy Below button to fill Fees and Rejects
            self.logger.info("Step 4f: Clicking Copy Below button")
            try:
                copy_btn = self.page.locator(loc.STEP_1_FEES_COPY_BUTTON)
                copy_btn.click()
                time.sleep(0.5)
                self.logger.info("✅ Clicked Copy Below - Fees and Rejects bank info copied")
                results["copy_button"] = True
            except Exception as e:
                self.logger.error(f"Failed to click Copy Below: {e}")
                results["copy_button"] = False
            
            # Step 5: Click Next button
            self.logger.info("Step 5: Clicking Next button")
            try:
                next_btn = self.page.locator(loc.STEP_1_NEXT_BUTTON)
                next_btn.click()
                time.sleep(2)  # Wait for originator to be added
                self.logger.info("✅ Next button clicked - Originator being added")
                results["next_button"] = True
            except Exception as e:
                self.logger.error(f"Failed to click Next: {e}")
                results["next_button"] = False
                return {"success": False, "description": description, "results": results, "verified": False}
            
            # Wait for modal to close and page to update
            self.page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(1)
            
            # Step 6: Verify originator added to table
            self.logger.info("Step 6: Verifying originator in table")
            verified = False
            try:
                # Check if originator table is visible
                originator_table = self.page.locator(loc.ORIGINATOR_TABLE)
                if originator_table.is_visible(timeout=5000):
                    # Look for the originator description in the table
                    originator_cell = self.page.locator(
                        f"//table[@id='ctl00_ContentPlaceHolder1_ctrlEFT1_GridView1']"
                        f"//tr[@datakeys]/td[1][contains(normalize-space(), '{description}')]"
                    )
                    if originator_cell.count() > 0:
                        self.logger.info(f"✅ Originator '{description}' verified in table")
                        verified = True
                    else:
                        # Try broader search
                        all_originators = self.page.locator(loc.ORIGINATOR_NAMES)
                        count = all_originators.count()
                        self.logger.info(f"Found {count} originator(s) in table")
                        if count > 0:
                            verified = True
                            self.logger.info(f"✅ Originator table has entries")
            except Exception as e:
                self.logger.warning(f"Could not verify originator in table: {e}")
            
            results["verified_in_table"] = verified
            
            # Summary
            success_count = sum(1 for r in results.values() if r)
            total_count = len(results)
            
            self.logger.info(f"ACH Originator: {success_count}/{total_count} steps successful")
            
            return {
                "success": verified,
                "description": description,
                "results": results,
                "verified": verified
            }
            
        except Exception as e:
            self.logger.error(f"Failed to add ACH Originator: {e}")
            return {
                "success": False,
                "description": description,
                "results": results,
                "verified": False
            }

    # =========================================================================
    # SAVE / SUBMIT ACTIONS
    # =========================================================================
    
    @performance_step("click_save_button")
    @log_step
    def click_save_button(self) -> bool:
        """
        Click the Save button to save the application.
        
        Returns:
            bool: True if save button clicked successfully, False otherwise
        """
        try:
            save_button = self.page.locator(NewApplicationPageLocators.BTN_SAVE)
            save_button.wait_for(state="visible", timeout=10000)
            save_button.click()
            self.logger.info("Save button clicked")
            
            # Wait for page to process the save
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to click Save button: {e}")
            return False

    @performance_step("click_submit_button")
    @log_step
    def click_submit_button(self) -> bool:
        """
        Click the Submit button to submit the application.
        
        Returns:
            bool: True if submit button clicked successfully, False otherwise
        """
        try:
            submit_button = self.page.locator(NewApplicationPageLocators.BTN_SUBMIT)
            submit_button.wait_for(state="visible", timeout=10000)
            submit_button.click()
            self.logger.info("Submit button clicked")
            
            # Wait for page to process the submission
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to click Submit button: {e}")
            return False

    @performance_step("click_validate_button")
    @log_step
    def click_validate_button(self) -> bool:
        """
        Click the Validate button to validate the application.
        
        Returns:
            bool: True if validate button clicked successfully, False otherwise
        """
        try:
            validate_button = self.page.locator(NewApplicationPageLocators.BTN_VALIDATE)
            validate_button.wait_for(state="visible", timeout=10000)
            validate_button.click()
            self.logger.info("Validate button clicked")
            
            # Wait for validation to process
            time.sleep(2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to click Validate button: {e}")
            return False

    @performance_step("get_validation_errors")
    @log_step
    def get_validation_errors(self) -> list:
        """
        Get all validation error messages from the error container.
        
        Returns:
            list: List of validation error messages, empty if no errors
        """
        errors = []
        try:
            # Check if validation errors container is visible
            error_container = self.page.locator(NewApplicationPageLocators.VALIDATION_ERRORS_CONTAINER)
            if error_container.is_visible(timeout=3000):
                # Get all error items
                error_items = self.page.locator(NewApplicationPageLocators.VALIDATION_ERROR_ITEMS)
                count = error_items.count()
                
                for i in range(count):
                    error_text = error_items.nth(i).inner_text().strip()
                    if error_text:
                        errors.append(error_text)
                
                self.logger.warning(f"Found {len(errors)} validation errors")
                for idx, error in enumerate(errors, 1):
                    self.logger.warning(f"  {idx}. {error}")
        except Exception as e:
            self.logger.debug(f"No validation errors found or error checking: {e}")
        
        return errors

    @performance_step("get_success_message")
    @log_step
    def get_success_message(self) -> Optional[str]:
        """
        Get the success toast message if visible.
        
        Returns:
            str: Success message text, None if not visible
        """
        try:
            success_toast = self.page.locator(NewApplicationPageLocators.SUCCESS_TOAST)
            if success_toast.is_visible(timeout=3000):
                # Get the message text from the inner div
                message_element = self.page.locator(NewApplicationPageLocators.SUCCESS_TOAST_MESSAGE)
                if message_element.is_visible():
                    message = message_element.inner_text().strip()
                    self.logger.info(f"Success message: {message}")
                    return message
                else:
                    # Fallback to getting text from the toast itself
                    message = success_toast.inner_text().strip()
                    self.logger.info(f"Success message: {message}")
                    return message
        except Exception as e:
            self.logger.debug(f"No success message visible: {e}")
        
        return None

    @performance_step("validate_application")
    @log_step
    def validate_application(self) -> Dict[str, Any]:
        """
        Validate the application by clicking the Validate button and checking results.
        
        Returns:
            Dict with:
                - success: bool - True if validation passed (no errors)
                - message: str - success message or summary
                - errors: list - list of validation errors (empty if valid)
                - app_info_id: str or None - the AppInfoID if available
        """
        result = {
            "success": False,
            "message": "",
            "errors": [],
            "app_info_id": None
        }
        
        # Click Validate button
        validate_clicked = self.click_validate_button()
        if not validate_clicked:
            result["message"] = "Failed to click Validate button"
            return result
        
        # Wait for validation to complete
        time.sleep(2)
        
        # Check for validation errors first
        errors = self.get_validation_errors()
        
        if errors:
            result["success"] = False
            result["errors"] = errors
            result["message"] = f"Validation failed with {len(errors)} error(s)"
            self.logger.error(result["message"])
            for idx, error in enumerate(errors, 1):
                self.logger.error(f"  ❌ {idx}. {error}")
        else:
            # Check for success message
            success_message = self.get_success_message()
            
            # Get AppInfoID
            app_info_id = self.get_application_id()
            result["app_info_id"] = app_info_id
            
            if success_message:
                result["success"] = True
                result["message"] = success_message
                self.logger.info(f"✅ Validation passed: {success_message}")
            else:
                # No errors and no success message - assume success
                result["success"] = True
                result["message"] = "Validation passed - no errors found"
                self.logger.info(result["message"])
            
            if app_info_id:
                self.logger.info(f"AppInfoID: {app_info_id}")
        
        return result

    @performance_step("get_application_id")
    @log_step
    def get_application_id(self) -> Optional[str]:
        """
        Get the Application ID from the page title after saving.
        
        The page title format is: "Sales Center - Application 313103"
        This extracts and returns the AppInfoID (e.g., "313103").
        
        Returns:
            str: The AppInfoID if found, None otherwise
        """
        try:
            # Use the span ID directly without text condition
            page_title_locator = "//span[@id='ctl00_ContentPlaceHolder1_lblTitle']"
            page_title_element = self.page.locator(page_title_locator)
            page_title_element.wait_for(state="visible", timeout=15000)
            
            title_text = page_title_element.inner_text()
            self.logger.info(f"Page title text: {title_text}")
            
            # Extract AppInfoID by splitting on space and getting last item
            # "Sales Center - Application 313103" -> "313103"
            if title_text:
                parts = title_text.strip().split()
                if parts:
                    app_info_id = parts[-1]  # Get last item
                    # Verify it's a number
                    if app_info_id.isdigit():
                        self.logger.info(f"Extracted AppInfoID: {app_info_id}")
                        return app_info_id
                    else:
                        self.logger.warning(f"Last part '{app_info_id}' is not a number")
            
            self.logger.warning(f"Could not extract AppInfoID from title: {title_text}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get Application ID: {e}")
            return None

    @performance_step("save_application")
    @log_step
    def save_application(self) -> Dict[str, Any]:
        """
        Save the application and extract the AppInfoID.
        
        Returns:
            Dict with:
                - success: bool - whether save was successful
                - app_info_id: str or None - the extracted AppInfoID
                - message: str - status message
        """
        result = {
            "success": False,
            "app_info_id": None,
            "message": ""
        }
        
        # Click Save button
        save_clicked = self.click_save_button()
        if not save_clicked:
            result["message"] = "Failed to click Save button"
            return result
        
        # Wait for page to update with the application ID
        time.sleep(2)
        
        # Extract the AppInfoID
        app_info_id = self.get_application_id()
        
        if app_info_id:
            result["success"] = True
            result["app_info_id"] = app_info_id
            result["message"] = f"Application saved successfully. AppInfoID: {app_info_id}"
            self.logger.info(result["message"])
        else:
            result["message"] = "Save clicked but could not extract AppInfoID"
            self.logger.warning(result["message"])
        
        return result

    @performance_step("submit_application")
    @log_step
    def submit_application(self) -> Dict[str, Any]:
        """
        Submit the application.
        
        Returns:
            Dict with:
                - success: bool - whether submit was successful
                - message: str - status message
        """
        result = {
            "success": False,
            "message": ""
        }
        
        # Click Submit button
        submit_clicked = self.click_submit_button()
        if not submit_clicked:
            result["message"] = "Failed to click Submit button"
            return result
        
        # Wait for page to process
        time.sleep(2)
        
        result["success"] = True
        result["message"] = "Application submitted successfully"
        self.logger.info(result["message"])
        
        return result

    # =========================================================================
    # GENERAL FEES SECTION
    # =========================================================================
    
    @performance_step("scroll_to_general_fees")
    @log_step
    def scroll_to_general_fees(self) -> bool:
        """
        Scroll to General Fees section and verify it's visible.
        
        Returns:
            bool: True if section is visible, False otherwise
        """
        try:
            # Use ID selector for header
            header_selector = f"#{GeneralFeesLocators.GENERAL_FEES_HEADER}"
            self.scroll_to_element(header_selector)
            time.sleep(0.3)
            
            if self.is_visible(header_selector):
                self.logger.info("General Fees section is visible")
                return True
            else:
                self.logger.warning("General Fees section not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to scroll to General Fees section: {e}")
            return False

    @performance_step("select_general_fees")
    @log_step
    def select_general_fees(self, fee_list: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Select fees from the General Fees section and fill amounts.
        
        This method:
        1. Scrolls to the General Fees section
        2. For each fee in the list:
           - Checks if fee exists in the table
           - Checks if checkbox is enabled (not disabled)
           - Checks if fee is already selected
           - If not selected and enabled, selects it
           - If amount field is enabled, fills the amount
        
        Args:
            fee_list: Dict with fee_name as key and dict with 'amount' as value
                     Example: {"MC Infrastructure Fee": {"amount": "25.50"}}
        
        Returns:
            Dict with:
                - success: bool - overall success
                - selected: list - fees successfully selected
                - already_selected: list - fees already checked
                - not_available: list - fees not found in table
                - disabled: list - fees with disabled checkbox
                - amounts_filled: list - fees with amounts filled
                - errors: list - any error messages
        """
        result = {
            "success": True,
            "selected": [],
            "already_selected": [],
            "not_available": [],
            "disabled": [],
            "amounts_filled": [],
            "errors": []
        }
        
        if not fee_list:
            self.logger.info("No fees to select")
            return result
        
        # Scroll to General Fees section
        self.scroll_to_general_fees()
        time.sleep(0.5)
        
        for fee_name, fee_data in fee_list.items():
            amount = fee_data.get("amount", "")
            
            try:
                # Get checkbox locator
                checkbox_xpath = GeneralFeesLocators.FEE_CHECKBOX(fee_name)
                checkbox = self.page.locator(checkbox_xpath)
                
                # Check if fee exists in the table using Playwright's count()
                if checkbox.count() == 0:
                    self.logger.warning(f"Fee '{fee_name}' not available in the list - skipping")
                    result["not_available"].append(fee_name)
                    continue
                
                # Scroll checkbox into view for better interaction
                checkbox.scroll_into_view_if_needed()
                time.sleep(0.1)
                
                # Check if checkbox is disabled
                # Note: In DOM, disabled checkbox is inside <span disabled="disabled">
                is_disabled = checkbox.is_disabled()
                if is_disabled:
                    self.logger.info(f"Fee '{fee_name}' checkbox is disabled - skipping")
                    result["disabled"].append(fee_name)
                    continue
                
                # Check if already selected
                is_checked = checkbox.is_checked()
                if is_checked:
                    self.logger.info(f"Fee '{fee_name}' is already selected")
                    result["already_selected"].append(fee_name)
                else:
                    # Select the fee
                    checkbox.click()
                    time.sleep(0.2)
                    
                    # Verify it's now checked
                    if checkbox.is_checked():
                        self.logger.info(f"Fee '{fee_name}' selected successfully")
                        result["selected"].append(fee_name)
                    else:
                        self.logger.warning(f"Fee '{fee_name}' click did not select it")
                        result["errors"].append(f"Failed to select: {fee_name}")
                        continue
                
                # Now try to fill the amount if provided
                if amount:
                    amount_xpath = GeneralFeesLocators.FEE_AMOUNT_INPUT(fee_name)
                    amount_input = self.page.locator(amount_xpath)
                    
                    # Check if amount field exists
                    if amount_input.count() > 0:
                        # Check if amount field is enabled
                        if not amount_input.is_disabled():
                            # Clear and fill the amount
                            amount_input.clear()
                            amount_input.fill(amount)
                            time.sleep(0.1)
                            
                            self.logger.info(f"Fee '{fee_name}' amount set to {amount}")
                            result["amounts_filled"].append(f"{fee_name}: {amount}")
                        else:
                            self.logger.info(f"Fee '{fee_name}' amount field is disabled (preset value)")
                    else:
                        self.logger.debug(f"Fee '{fee_name}' has no amount field")
                        
            except Exception as e:
                error_msg = f"Error processing fee '{fee_name}': {str(e)}"
                self.logger.error(error_msg)
                result["errors"].append(error_msg)
        
        # Determine overall success (at least some fees processed without errors)
        total_processed = len(result["selected"]) + len(result["already_selected"])
        if total_processed > 0 or len(result["not_available"]) == len(fee_list):
            result["success"] = True
        else:
            result["success"] = len(result["errors"]) == 0
        
        # Log summary
        self.logger.info(f"Fee selection summary: "
                        f"Selected={len(result['selected'])}, "
                        f"Already selected={len(result['already_selected'])}, "
                        f"Not available={len(result['not_available'])}, "
                        f"Disabled={len(result['disabled'])}, "
                        f"Amounts filled={len(result['amounts_filled'])}")
        
        return result

    
    