"""
OSC Credit Card Merchant Creation - Clean Automation with Performance Tracking
"""

from core.browser import BrowserManager
from core.logger import Logger
from core.performance_decorators import PerformanceSession
# Initialize shared OSC logger as early as possible so all modules/pages
# will use the same singleton logger instance and log directory.
logger = Logger.get("osc")

from config.osc.config import osc_settings
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage


def create_credit_card_merchant():
    """Create credit card merchant workflow with comprehensive performance tracking"""
    username, password = osc_settings.credentials
    
    logger.info("Starting credit card merchant creation workflow")
    
    # Use performance session to track the entire workflow
    with PerformanceSession(
        script_name="create_credit_card_merchant",
        environment="development",  # You can make this configurable
        browser_type="chromium",
        headless=False,  # From your settings
        tags=["osc", "merchant_creation", "automation"],
        notes="Credit card merchant creation automation workflow"
    ) as session:
        
        with BrowserManager(enable_performance_tracking=True) as browser_manager:
            page = browser_manager.get_page()
            
            # Step 1: Login (automatically tracked by existing decorators)
            logger.info("Step 1: Starting login process")
            login_page = LoginPage(page)
            login_success = login_page.complete_login(username, password)
            
            if not login_success:
                logger.error("Login failed")
                print("✗ Login failed")
                return None
            
            logger.info("✅ Login successful")
            
            # Step 2: Navigate to new application (automatically tracked)
            logger.info("Step 2: Starting navigation to new application page")
            navigation = NavigationSteps(page)
            application_page = navigation.navigate_to_new_application_page()
            
            if application_page:
                logger.info(f"✅ New application page opened successfully: {application_page.url}")
                print(f"✓ New application page opened: {application_page.url}")
                
                # Step 3: Fill Application Information section
                logger.info("Step 3: Starting Application Information section automation")
                new_app_page = NewApplicationPage(application_page)
                
                # Fill the Application Information section
                app_info_results = new_app_page.fill_application_information()
                
                # Check if all operations were successful
                successful_operations = sum(1 for result in app_info_results.values() if result)
                total_operations = len(app_info_results)
                
                if successful_operations == total_operations:
                    logger.info("✅ Application Information section completed successfully")
                    print("✓ Application Information section filled successfully")
                else:
                    failed_fields = [field for field, result in app_info_results.items() if not result]
                    logger.warning(f"⚠️ Application Information partially completed. Failed fields: {failed_fields}")
                    print(f"⚠️ Application Information partially completed. Failed: {failed_fields}")
                
                # TODO: Add next sections (Corporate Information, Location Information, etc.)
                
                return application_page
            else:
                logger.error("Failed to navigate to application page")
                print("✗ Failed to navigate to application page")
                return None


if __name__ == "__main__":
    create_credit_card_merchant()