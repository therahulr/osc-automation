"""OSC workflow example using the new UIAutomationCore.

This example shows how to:
1. Migrate existing OSC scripts to use UIAutomationCore
2. Use existing page objects with the new system
3. Leverage automatic performance tracking
4. Simplify browser and logger initialization

BEFORE (Old approach):
    - Initialize logger manually
    - Initialize browser manager manually
    - Create performance session manually
    - Manage cleanup manually

AFTER (New approach):
    - Just use UIAutomationCore context manager
    - Everything handled automatically
    - Cleaner, simpler code
"""

from core import UIAutomationCore, log_step, log_success

# Import existing OSC page objects (they work seamlessly!)
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage

# Import existing data
from data.osc.osc_data import (
    SALES_REPRESENTATIVE,
    APPLICATION_INFO,
    MERCHANT_INFO,
    BUSINESS_ADDRESS
)


def osc_create_application_workflow():
    """
    Complete OSC application workflow using UIAutomationCore.

    This is a simplified version of the existing create_credit_card_merchant.py
    script, demonstrating how much cleaner the code becomes.
    """

    # ==================== OLD WAY (Commented) ====================
    # from core.logger import Logger
    # from core.browser import BrowserManager
    # from core.performance_decorators import PerformanceSession
    #
    # logger = Logger.get("osc")
    # logger.info("Starting OSC automation...")
    #
    # with PerformanceSession(script_name="create_merchant", ...):
    #     with BrowserManager(enable_performance_tracking=True) as browser:
    #         page = browser.get_page()
    #         # ... rest of the code

    # ==================== NEW WAY ====================

    with UIAutomationCore(
        app_name="osc",
        script_name="create_credit_card_merchant",
        headless=False,  # Can be parameterized
        enable_performance_tracking=True
    ) as core:

        # Everything is already set up!
        page = core.page
        logger = core.logger

        logger.info("Starting OSC Credit Card Merchant Creation")

        # ==================== Step 1: Login ====================
        log_step("Step 1: Logging into OSC")

        login_page = LoginPage(page)
        login_success = login_page.complete_login(
            username="your_username",  # Replace with actual credentials
            password="your_password"
        )

        if not login_success:
            logger.error("Login failed")
            return

        log_success("Login successful")

        # ==================== Step 2: Navigate to Application ====================
        log_step("Step 2: Navigating to New Application")

        navigation = NavigationSteps(page)

        # Navigate through the wizard
        navigation.navigate_step1_sales_rep(
            sales_rep_name=SALES_REPRESENTATIVE["name"]
        )

        navigation.navigate_step2_existing_merchant()

        navigation.navigate_step3_new_application()

        log_success("Navigation completed")

        # ==================== Step 3: Fill Application ====================
        log_step("Step 3: Filling Application Form")

        app_page = NewApplicationPage(page)

        # Verify page sections
        app_page.verify_application_info_section()

        # In a real scenario, you would fill the form here
        # app_page.fill_merchant_info(MERCHANT_INFO)
        # app_page.fill_business_address(BUSINESS_ADDRESS)
        # etc.

        log_success("Application form filled")

        # Take screenshot of completed form
        screenshot = core.take_screenshot("application_completed")
        logger.info(f"Screenshot saved: {screenshot}")

        # ==================== Step 4: Submit (if needed) ====================
        # log_step("Step 4: Submitting Application")
        # app_page.submit_application()
        # log_success("Application submitted")

        logger.info("OSC workflow completed successfully")

    # Performance report automatically generated at the end!


def osc_modular_workflow_with_components():
    """
    Example showing how to create modular, reusable components for OSC.

    This demonstrates creating small, focused components that can be
    composed into larger workflows.
    """

    from core import BaseComponent

    class OSCSalesRepSelector(BaseComponent):
        """Component for selecting sales representative."""

        def select_sales_rep(self, rep_name: str):
            """Select a sales representative.

            Args:
                rep_name: Name of the sales representative
            """
            log_step(f"Selecting sales rep: {rep_name}")

            # Navigate to sales rep selection
            self.click("a:has-text('Applications')")
            self.click("a:has-text('New Application')")

            # Select the sales rep
            self.click(f"td:has-text('{rep_name}')")
            self.click("input[value='Next']")

            log_success(f"Sales rep '{rep_name}' selected")

    class OSCApplicationForm(BaseComponent):
        """Component for OSC application form."""

        def fill_merchant_info(self, merchant_data: dict):
            """Fill merchant information.

            Args:
                merchant_data: Dictionary with merchant info
            """
            log_step("Filling merchant information")

            self.fill_form({
                "#legal_business_name": merchant_data.get("legal_business_name", ""),
                "#dba_name": merchant_data.get("dba_name", ""),
                "#federal_tax_id": merchant_data.get("federal_tax_id", ""),
                # Add more fields as needed
            })

            log_success("Merchant information filled")

        def fill_address(self, address_data: dict):
            """Fill business address.

            Args:
                address_data: Dictionary with address info
            """
            log_step("Filling business address")

            self.fill_form({
                "#street_address": address_data.get("street_address", ""),
                "#city": address_data.get("city", ""),
                "#state": address_data.get("state", ""),
                # Add more fields as needed
            })

            log_success("Business address filled")

    # Use the components
    with UIAutomationCore(
        app_name="osc",
        script_name="modular_workflow",
        headless=False
    ) as core:

        page = core.page
        logger = core.logger

        # Login
        login = LoginPage(page)
        login.complete_login("username", "password")

        # Use modular components
        sales_rep_selector = OSCSalesRepSelector(page, logger=logger)
        sales_rep_selector.select_sales_rep(SALES_REPRESENTATIVE["name"])

        app_form = OSCApplicationForm(page, logger=logger)
        app_form.fill_merchant_info(MERCHANT_INFO)
        app_form.fill_address(BUSINESS_ADDRESS)

        logger.info("Modular workflow completed")


def parameterized_osc_workflow(
    environment: str = "qa",
    headless: bool = False,
    enable_screenshots: bool = True
):
    """
    Highly parameterized workflow example.

    This shows how to make workflows configurable and reusable
    across different environments and scenarios.

    Args:
        environment: Target environment (qa, prod)
        headless: Run in headless mode
        enable_screenshots: Take screenshots at key points
    """

    # Configure based on environment
    script_name = f"osc_workflow_{environment}"

    with UIAutomationCore(
        app_name="osc",
        script_name=script_name,
        headless=headless,
        enable_performance_tracking=True,
        metadata={
            "environment": environment,
            "screenshots_enabled": enable_screenshots
        }
    ) as core:

        logger = core.logger
        page = core.page

        logger.info(f"Running OSC workflow in {environment} environment")

        # Login with environment-specific credentials
        if environment == "qa":
            username = "qa_user"
            password = "qa_password"
        else:
            username = "prod_user"
            password = "prod_password"

        login = LoginPage(page)
        login.complete_login(username, password)

        if enable_screenshots:
            core.take_screenshot("after_login")

        # Rest of workflow...

        logger.info("Parameterized workflow completed")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("OSC WORKFLOW EXAMPLES - NEW SIMPLIFIED APPROACH")
    print("="*80 + "\n")

    print("Example 1: Basic OSC Workflow")
    print("-" * 80)
    # Uncomment when ready to run with credentials:
    # osc_create_application_workflow()

    print("\nExample 2: Modular Component-Based Workflow")
    print("-" * 80)
    # Uncomment when ready to run:
    # osc_modular_workflow_with_components()

    print("\nExample 3: Parameterized Workflow")
    print("-" * 80)
    # Run with different parameters:
    # parameterized_osc_workflow(environment="qa", headless=False)
    # parameterized_osc_workflow(environment="prod", headless=True)

    print("\n" + "="*80)
    print("BENEFITS OF THE NEW APPROACH:")
    print("="*80)
    print("✓ No manual browser initialization")
    print("✓ No manual logger setup")
    print("✓ No manual performance session management")
    print("✓ Automatic cleanup")
    print("✓ Colored terminal output")
    print("✓ Automatic performance reporting")
    print("✓ Reusable components")
    print("✓ Highly parameterized and configurable")
    print("✓ Less boilerplate code")
    print("✓ Easier to maintain and test")
    print("="*80 + "\n")
