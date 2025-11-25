"""
OSC Credit Card Merchant Creation - Complete Workflow

This script automates the full merchant creation process:
1. Login to OSC
2. Navigate to new application
3. Fill Application Information
4. Fill Corporate Information
5. Fill Location Information
6. (More sections to be added)

BENEFITS:
- Uses UIAutomationCore for automatic browser/logging management
- Automatic cleanup and performance reporting
- Colored terminal output
"""

from core import UIAutomationCore, log_step, log_success, log_section

from config.osc.config import osc_settings
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage
from data.osc.osc_data import CORPORATE_INFO, LOCATION_INFO
import time

def create_credit_card_merchant():
    """Create credit card merchant workflow with comprehensive performance tracking."""

    username, password = osc_settings.credentials

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

        page = core.page
        logger = core.logger
        
        # Track results for all sections
        all_results = {}

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
        all_results["application_info"] = app_info_results

        app_success = sum(1 for r in app_info_results.values() if r)
        app_total = len(app_info_results)

        if app_success == app_total:
            log_success(f"Application Information: {app_success}/{app_total} fields")
        else:
            failed_fields = [f for f, r in app_info_results.items() if not r]
            logger.warning(f"Application Information: {app_success}/{app_total}. Failed: {failed_fields}")

        core.take_screenshot("application_info_completed")

        # ==================== Step 4: Fill Corporate Information ====================
        log_step("Step 4: Filling Corporate Information section")
        
        logger.info(f"Using Corporate Data: {CORPORATE_INFO['legal_business_name']}")

        corp_results = new_app_page.fill_corporate_information_section()
        all_results["corporate_info"] = corp_results

        corp_success = sum(1 for r in corp_results.values() if r)
        corp_total = len(corp_results)

        if corp_success == corp_total:
            log_success(f"Corporate Information: {corp_success}/{corp_total} fields")
        else:
            failed = [f for f, r in corp_results.items() if not r]
            logger.warning(f"Corporate Information: {corp_success}/{corp_total}. Failed: {failed}")

        core.take_screenshot("corporate_info_completed")

        # ==================== Step 5: Fill Location Information ====================
        log_step("Step 5: Filling Location Information section")
        
        logger.info(f"Using Location Data: {LOCATION_INFO['dba']}")

        loc_results = new_app_page.fill_location_information_section()
        all_results["location_info"] = loc_results

        loc_success = sum(1 for r in loc_results.values() if r)
        loc_total = len(loc_results)

        if loc_success == loc_total:
            log_success(f"Location Information: {loc_success}/{loc_total} fields")
        else:
            failed = [f for f, r in loc_results.items() if not r]
            logger.warning(f"Location Information: {loc_success}/{loc_total}. Failed: {failed}")

        # ==================== Summary ====================
        log_section("WORKFLOW SUMMARY")
        
        total_success = app_success + corp_success + loc_success
        total_fields = app_total + corp_total + loc_total
        
        logger.info(f"Application Information: {app_success}/{app_total}")
        logger.info(f"Corporate Information: {corp_success}/{corp_total}")
        logger.info(f"Location Information: {loc_success}/{loc_total}")
        logger.info(f"─" * 40)
        logger.info(f"TOTAL: {total_success}/{total_fields} ({(total_success/total_fields)*100:.1f}%)")

        if total_success == total_fields:
            log_success("All sections completed successfully!")
        else:
            logger.warning(f"Completed with {total_fields - total_success} field(s) failed")

        # TODO: Add next sections (Owner/Officer, Bank Information, etc.)

        core.take_screenshot("final_state")
        time.sleep(10)
        return {
            "results": all_results,
            "summary": {
                "total_success": total_success,
                "total_fields": total_fields,
                "success_rate": f"{(total_success/total_fields)*100:.1f}%"
            }
        }
    
    


if __name__ == "__main__":
    results = create_credit_card_merchant()
    
    if results:
        print(f"\n✅ Merchant creation completed: {results['summary']['success_rate']} success rate")
    else:
        print("\n❌ Merchant creation failed")
