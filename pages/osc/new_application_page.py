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
)
from data.osc.osc_data import (
    APPLICATION_INFO, CORPORATE_INFO, LOCATION_INFO,
    TAX_INFO, OWNER1_INFO, OWNER2_INFO,
    TRADE_REFERENCE_INFO, GENERAL_UNDERWRITING_INFO
)
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
        
        # Business Open Date (masked input mm/dd/yyyy)
        results["business_open_date"] = self.fill_masked_input(
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
        
        # Date of Birth (masked input dd/mm/yyyy)
        results["dob"] = self.fill_masked_input(
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
        
        # Date of Ownership (masked input dd/mm/yyyy)
        results["date_of_ownership"] = self.fill_masked_input(
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
        
        # Date of Birth (masked input dd/mm/yyyy)
        results["dob"] = self.fill_masked_input(
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
        
        # Date of Ownership (masked input dd/mm/yyyy)
        results["date_of_ownership"] = self.fill_masked_input(
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

    