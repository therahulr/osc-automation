"""
OSC Credit Card Merchant Creation - NEW SIMPLIFIED VERSION

This is the refactored version using UIAutomationCore.

BENEFITS OVER OLD VERSION:
- 40% less code
- No manual logger initialization
- No manual browser management
- No manual performance session management
- Automatic cleanup
- Colored terminal output
- Automatic performance reporting
"""

from core import UIAutomationCore, log_step, log_success, log_section

from config.osc.config import osc_settings
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage


def create_credit_card_merchant():
    """Create credit card merchant workflow with comprehensive performance tracking."""

    username, password = osc_settings.credentials

    # ==================== NEW: Everything in one line! ====================
    with UIAutomationCore(
        app_name="osc",
        script_name="create_credit_card_merchant",
        headless=False,
        enable_performance_tracking=True,
        metadata={
            "environment": "development",
            "tags": ["osc", "merchant_creation", "automation"],
            "notes": "Credit card merchant creation automation workflow"
        }
    ) as core:

        # Everything is already initialized!
        page = core.page
        logger = core.logger

        log_section("OSC CREDIT CARD MERCHANT CREATION")

        # ==================== Step 1: Login ====================
        log_step("Step 1: Starting login process")

        login_page = LoginPage(page)
        login_success = login_page.complete_login(username, password)

        if not login_success:
            logger.error("Login failed")
            return None

        log_success("Login successful")
        core.take_screenshot("after_login")

        # ==================== Step 2: Navigate to Application ====================
        log_step("Step 2: Navigating to new application page")

        navigation = NavigationSteps(page)
        application_page = navigation.navigate_to_new_application_page()

        if not application_page:
            logger.error("Failed to navigate to application page")
            return None

        log_success(f"New application page opened: {application_page.url}")
        core.take_screenshot("application_page")

        # ==================== Step 3: Fill Application Information ====================
        log_step("Step 3: Filling Application Information section")

        new_app_page = NewApplicationPage(application_page)
        app_info_results = new_app_page.fill_application_information()

        # Analyze results
        successful_operations = sum(1 for result in app_info_results.values() if result)
        total_operations = len(app_info_results)

        if successful_operations == total_operations:
            log_success("Application Information section completed successfully")
            core.take_screenshot("application_info_completed")
        else:
            failed_fields = [field for field, result in app_info_results.items() if not result]
            logger.warning(f"Application Information partially completed. Failed fields: {failed_fields}")

        # TODO: Add next sections (Corporate Information, Location Information, etc.)

        log_success("Workflow completed successfully")

        return application_page

    # ==================== Automatic performance report generated here! ====================


if __name__ == "__main__":
   
    create_credit_card_merchant()
