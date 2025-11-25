"""
New Application Page - OSC Application Information automation
"""

from playwright.sync_api import Page, TimeoutError
from typing import Dict, Any, Optional
import time

from pages.osc.base_page import BasePage
from locators.osc_locators import ApplicationInformationLocators
from data.osc.osc_data import APPLICATION_INFO
from utils.decorators import log_step, timeit
from core.performance_decorators import performance_step


class NewApplicationPage(BasePage):
    """Page object for handling New Application form - Application Information section"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = ApplicationInformationLocators
        
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
    
    @performance_step("select_dropdown_option")
    @log_step
    def select_dropdown_option(self, dropdown_selector: str, option_text: str, field_name: str) -> bool:
        """
        Select an option from a dropdown by text value with robust error handling
        
        Args:
            dropdown_selector: CSS selector for the dropdown
            option_text: Text of the option to select
            field_name: Name of the field for logging
            
        Returns:
            bool: True if selection successful, False otherwise
        """
        try:
            # Wait for dropdown to be available
            self.page.wait_for_selector(dropdown_selector, timeout=5000)
            
            # First, get available options to verify the option exists
            available_options = self.get_available_dropdown_options(dropdown_selector, field_name)
            
            # Check if the exact option exists
            if option_text not in available_options:
                self.logger.warning(f"{field_name} option '{option_text}' not found in available options: {available_options}")
                
                # Try to find a partial match (case-insensitive)
                partial_matches = [opt for opt in available_options if option_text.lower() in opt.lower()]
                if partial_matches:
                    option_text = partial_matches[0]
                    self.logger.info(f"Using partial match for {field_name}: '{option_text}'")
                else:
                    self.logger.error(f"No suitable option found for {field_name}")
                    return False
            
            # Select the option by text
            self.page.select_option(dropdown_selector, label=option_text)
            
            # Small delay to ensure selection is processed
            time.sleep(0.5)
            
            # Verify selection by checking the selected option
            selected_element = self.page.locator(f"{dropdown_selector} option:checked")
            if selected_element.count() > 0:
                selected_text = selected_element.text_content()
                self.logger.info(f"{field_name} selected successfully: '{selected_text}'")
                return True
            else:
                # Alternative verification: check the value of the select element
                try:
                    current_value = self.page.locator(dropdown_selector).input_value()
                    selected_option = self.page.locator(f"{dropdown_selector} option[value='{current_value}']")
                    if selected_option.count() > 0:
                        selected_text = selected_option.text_content()
                        self.logger.info(f"{field_name} selected successfully (alt method): '{selected_text}'")
                        return True
                except Exception:
                    pass
                
                self.logger.error(f"Failed to verify {field_name} selection - no option marked as selected")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to select {field_name} option '{option_text}': {e}")
            return False
    
    @performance_step("fill_text_field")
    @log_step
    def fill_text_field(self, field_selector: str, text_value: str, field_name: str) -> bool:
        """
        Fill a text input field
        
        Args:
            field_selector: CSS selector for the input field
            text_value: Text to fill in the field
            field_name: Name of the field for logging
            
        Returns:
            bool: True if filling successful, False otherwise
        """
        try:
            if not text_value:  # Skip empty values
                self.logger.info(f"{field_name} field skipped (empty value)")
                return True
                
            # Wait for field to be available
            self.page.wait_for_selector(field_selector, timeout=5000)
            
            # Clear and fill the field
            self.page.fill(field_selector, text_value)
            
            # Verify the text was entered
            filled_value = self.page.locator(field_selector).input_value()
            if filled_value == text_value:
                self.logger.info(f"{field_name} filled successfully: {text_value}")
                return True
            else:
                self.logger.warning(f"{field_name} value mismatch. Expected: {text_value}, Got: {filled_value}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to fill {field_name} field: {e}")
            return False
    
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
        
        # Fill Association dropdown
        results["association"] = self.select_dropdown_option(
            self.locators.ASSOCIATION_DROPDOWN,
            app_data["association"],
            "Association"
        )
        
        # Fill Lead Source dropdown
        results["lead_source"] = self.select_dropdown_option(
            self.locators.LEAD_SOURCE_DROPDOWN,
            app_data["lead_source"],
            "Lead Source"
        )
        
        # Fill Referral Partner dropdown
        results["referral_partner"] = self.select_dropdown_option(
            self.locators.REFERRAL_PARTNER_DROPDOWN,
            app_data["referral_partner"],
            "Referral Partner"
        )
        
        # Fill Promo Code (if provided)
        results["promo_code"] = self.fill_text_field(
            self.locators.PROMO_CODE_INPUT,
            app_data.get("promo_code", ""),
            "Promo Code"
        )
        
        # Fill Corporate Atlas ID (if provided)
        results["corporate_atlas_id"] = self.fill_text_field(
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
    
    @performance_step("get_available_dropdown_options")
    @log_step
    def get_available_dropdown_options(self, dropdown_selector: str, field_name: str) -> list:
        """
        Get all available options from a dropdown
        
        Args:
            dropdown_selector: CSS selector for the dropdown
            field_name: Name of the field for logging
            
        Returns:
            list: List of available option texts
        """
        try:
            self.page.wait_for_selector(dropdown_selector, timeout=5000)
            
            # Get all option elements
            options = self.page.locator(f"{dropdown_selector} option").all()
            option_texts = [option.text_content() for option in options if option.text_content()]
            
            self.logger.info(f"{field_name} available options: {option_texts}")
            return option_texts
            
        except Exception as e:
            self.logger.error(f"Failed to get {field_name} options: {e}")
            return []
    
    @performance_step("get_all_available_options")
    @log_step
    def get_all_available_options(self) -> Dict[str, list]:
        """
        Get all available options from all dropdowns for analysis
        
        Returns:
            Dict[str, list]: Dictionary mapping field names to their available options
        """
        options = {}
        
        options["association"] = self.get_available_dropdown_options(
            self.locators.ASSOCIATION_DROPDOWN, "Association"
        )
        
        options["lead_source"] = self.get_available_dropdown_options(
            self.locators.LEAD_SOURCE_DROPDOWN, "Lead Source"
        )
        
        options["referral_partner"] = self.get_available_dropdown_options(
            self.locators.REFERRAL_PARTNER_DROPDOWN, "Referral Partner"
        )
        
        return options