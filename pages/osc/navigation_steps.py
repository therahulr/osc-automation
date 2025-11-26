"""
OSC Navigation automation - Simple workflow steps
"""

from playwright.sync_api import Page
from pages.osc.base_page import BasePage
from data.data_importer import DataImporter
from utils.decorators import log_step
from utils.locator_utils import build_table_row_checkbox_locator
from core.logger import get_logger
from locators.osc_locators import (
    DashboardPageLocators,
    Step1SalesRepLocators,
    Step2ExistingMerchantLocators,
    ApplicationInformationLocators
)

# Use logger attached to BasePage instances (self.logger). Module-level
# logger creation is avoided so the page objects can share the core
# Logger singleton when it is initialized by the script.


class NavigationSteps(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.data = DataImporter()
    
    @log_step
    def navigate_to_new_application_page(self) -> Page:
        """Complete new application navigation workflow
        
        Returns:
            Page: The new application page object for subsequent automation steps
        """
        # 1. Click on Applications menu
        self.logger.info("Step 1: Clicking Applications menu")
        self.page.click(DashboardPageLocators.MENU_APPLICATIONS)

        # 2. Click on New Application
        self.logger.info("Step 2: Clicking New Application")
        self.page.click(DashboardPageLocators.APPLICATIONS_NEW_APPLICATION)

        # 3. Wait for Step 1 to load
        self.logger.info("Step 3: Waiting for Step 1 to load")
        self.page.wait_for_selector(Step1SalesRepLocators.CONTRACTOR_ROWS, timeout=10000)

        # 4. Select sales representative DEMONET1
        self.logger.info("Step 4: Selecting sales representative")
        sales_rep_name = self.data.get_sales_rep_name()
        locator = build_table_row_checkbox_locator(sales_rep_name)
        checkbox = self.page.locator(locator)
        if not checkbox.is_checked():
            checkbox.check()

        # 5. Click Next button (Step 1)
        self.logger.info("Step 5: Clicking Next button (Step 1)")
        self.page.click(Step1SalesRepLocators.STEP1_NEXT_BUTTON)

        # 6. Wait for Step 2 to load
        self.logger.info("Step 6: Waiting for Step 2 to load")
        self.page.wait_for_selector(Step2ExistingMerchantLocators.EXISTING_MERCHANT_NO, timeout=10000)

        # 7. Select "No, this is a new corporation" radio button
        self.logger.info("Step 7: Selecting 'No, this is a new corporation'")
        self.page.click(Step2ExistingMerchantLocators.EXISTING_MERCHANT_NO)

        # 8. Wait for new tab to open and click Next button (Step 2)
        self.logger.info("Step 8: Setting up popup handler and clicking Next button (Step 2)")
        with self.page.expect_popup(timeout=60000) as popup_info:
            self.page.click(Step2ExistingMerchantLocators.STEP2_NEXT_BUTTON)

        # 9. Switch to the new tab
        new_page = popup_info.value
        self.logger.info(f"Step 9: New tab opened, switching to URL: {new_page.url}")

        # 10. Wait for application form to load in new tab
        self.logger.info("Step 10: Waiting for application form to load in new tab")
        new_page.wait_for_selector(ApplicationInformationLocators.SECTION_TITLE, timeout=10000)

        # Update page reference to new tab
        self.page = new_page
        self.logger.info(f"✅ Successfully switched to new application page: {self.page.url}")

        self.logger.info("✅ Successfully navigated to new application page")
        return new_page