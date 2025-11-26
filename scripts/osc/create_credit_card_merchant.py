"""
OSC Credit Card Merchant Creation - Complete Workflow

This script automates the full merchant creation process:
1. Login to OSC
2. Navigate to new application
3. Select Credit Card product
4. Fill Application Information
5. Fill Corporate Information
6. Fill Location Information
7. Fill Tax Information
8. Fill Owner/Officer 1
9. Fill Owner/Officer 2
10. Fill Trade Reference
11. Fill General Underwriting

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
from data.osc.osc_data import (
    CORPORATE_INFO, LOCATION_INFO, TAX_INFO, OWNER1_INFO, OWNER2_INFO,
    TRADE_REFERENCE_INFO, GENERAL_UNDERWRITING_INFO
)
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

        # ==================== Step 3: Select Credit Card Product ====================
        log_step("Step 3: Selecting Credit Card product")

        new_app_page = NewApplicationPage(application_page)
        
        credit_card_selected = new_app_page.select_credit_card_product()
        
        if not credit_card_selected:
            logger.error("Failed to select Credit Card product")
            return None
        
        log_success("Credit Card product selected and verified")
        core.take_screenshot("credit_card_product_selected")

        # ==================== Step 4: Fill Application Information ====================
        log_step("Step 4: Filling Application Information section")

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

        # ==================== Step 5: Fill Corporate Information ====================
        log_step("Step 5: Filling Corporate Information section")
        
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

        # ==================== Step 6: Fill Location Information ====================
        log_step("Step 6: Filling Location Information section")
        
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

        core.take_screenshot("location_info_completed")

        # ==================== Step 7: Fill Tax Information ====================
        log_step("Step 7: Filling Tax Information section")
        
        logger.info(f"Using Tax Data: {TAX_INFO['tax_filing_corp_name']}")

        tax_results = new_app_page.fill_tax_information_section()
        all_results["tax_info"] = tax_results

        tax_success = sum(1 for r in tax_results.values() if r)
        tax_total = len(tax_results)

        if tax_success == tax_total:
            log_success(f"Tax Information: {tax_success}/{tax_total} fields")
        else:
            failed = [f for f, r in tax_results.items() if not r]
            logger.warning(f"Tax Information: {tax_success}/{tax_total}. Failed: {failed}")

        core.take_screenshot("tax_info_completed")

        # ==================== Step 8: Fill Owner/Officer 1 ====================
        log_step("Step 8: Filling Owner/Officer 1 section")
        
        logger.info(f"Using Owner 1 Data: {OWNER1_INFO['first_name']} {OWNER1_INFO['last_name']}")

        owner1_results = new_app_page.fill_owner1_information_section()
        all_results["owner1_info"] = owner1_results

        owner1_success = sum(1 for r in owner1_results.values() if r)
        owner1_total = len(owner1_results)

        if owner1_success == owner1_total:
            log_success(f"Owner/Officer 1: {owner1_success}/{owner1_total} fields")
        else:
            failed = [f for f, r in owner1_results.items() if not r]
            logger.warning(f"Owner/Officer 1: {owner1_success}/{owner1_total}. Failed: {failed}")

        core.take_screenshot("owner1_info_completed")

        # ==================== Step 9: Fill Owner/Officer 2 ====================
        log_step("Step 9: Filling Owner/Officer 2 section")
        
        logger.info(f"Using Owner 2 Data: {OWNER2_INFO['first_name']} {OWNER2_INFO['last_name']}")

        owner2_results = new_app_page.fill_owner2_information_section()
        all_results["owner2_info"] = owner2_results

        owner2_success = sum(1 for r in owner2_results.values() if r)
        owner2_total = len(owner2_results)

        if owner2_success == owner2_total:
            log_success(f"Owner/Officer 2: {owner2_success}/{owner2_total} fields")
        else:
            failed = [f for f, r in owner2_results.items() if not r]
            logger.warning(f"Owner/Officer 2: {owner2_success}/{owner2_total}. Failed: {failed}")

        core.take_screenshot("owner2_info_completed")

        # ==================== Step 10: Fill Trade Reference ====================
        log_step("Step 10: Filling Trade Reference section")
        
        logger.info(f"Using Trade Reference Data: {TRADE_REFERENCE_INFO['name']}")

        trade_results = new_app_page.fill_trade_reference_section()
        all_results["trade_reference"] = trade_results

        trade_success = sum(1 for r in trade_results.values() if r)
        trade_total = len(trade_results)

        if trade_success == trade_total:
            log_success(f"Trade Reference: {trade_success}/{trade_total} fields")
        else:
            failed = [f for f, r in trade_results.items() if not r]
            logger.warning(f"Trade Reference: {trade_success}/{trade_total}. Failed: {failed}")

        core.take_screenshot("trade_reference_completed")

        # ==================== Step 11: Fill General Underwriting ====================
        log_step("Step 11: Filling General Underwriting section")
        
        logger.info(f"Using Underwriting Data: {GENERAL_UNDERWRITING_INFO['business_type']}")

        underwriting_results = new_app_page.fill_general_underwriting_section()
        all_results["general_underwriting"] = underwriting_results

        underwriting_success = sum(1 for r in underwriting_results.values() if r)
        underwriting_total = len(underwriting_results)

        if underwriting_success == underwriting_total:
            log_success(f"General Underwriting: {underwriting_success}/{underwriting_total} fields")
        else:
            failed = [f for f, r in underwriting_results.items() if not r]
            logger.warning(f"General Underwriting: {underwriting_success}/{underwriting_total}. Failed: {failed}")

        core.take_screenshot("general_underwriting_completed")

        time.sleep(10)

        # ==================== Summary ====================
        log_section("WORKFLOW SUMMARY")
        
        total_success = (app_success + corp_success + loc_success + 
                        tax_success + owner1_success + owner2_success +
                        trade_success + underwriting_success)
        total_fields = (app_total + corp_total + loc_total + 
                       tax_total + owner1_total + owner2_total +
                       trade_total + underwriting_total)
        
        logger.info(f"Application Information: {app_success}/{app_total}")
        logger.info(f"Corporate Information: {corp_success}/{corp_total}")
        logger.info(f"Location Information: {loc_success}/{loc_total}")
        logger.info(f"Tax Information: {tax_success}/{tax_total}")
        logger.info(f"Owner/Officer 1: {owner1_success}/{owner1_total}")
        logger.info(f"Owner/Officer 2: {owner2_success}/{owner2_total}")
        logger.info(f"Trade Reference: {trade_success}/{trade_total}")
        logger.info(f"General Underwriting: {underwriting_success}/{underwriting_total}")
        logger.info(f"─" * 40)
        logger.info(f"TOTAL: {total_success}/{total_fields} ({(total_success/total_fields)*100:.1f}%)")

        if total_success == total_fields:
            log_success("All sections completed successfully!")
        else:
            logger.warning(f"Completed with {total_fields - total_success} field(s) failed")

        # TODO: Add next sections (Bank Information, Credit Card Information, etc.)

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
