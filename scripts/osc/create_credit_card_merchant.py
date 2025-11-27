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
12. Fill Billing Questionnaire
13. Fill Bank Information
14. Fill Credit Card Information
15. Fill Credit Card Services
16. Fill Credit Card Underwriting
17. Fill Credit Card Interchange
18. Add Terminal (Wizard Step 1)

BENEFITS:
- Uses UIAutomationCore for automatic browser/logging management
- Automatic cleanup and performance reporting
- Colored terminal output
"""

from core import UIAutomationCore, log_step, log_success, log_section

from config.osc.config import osc_settings, get_osc_data
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage

# Load environment-specific test data
_data = get_osc_data()
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
CREDIT_CARD_INTERCHANGE = _data.CREDIT_CARD_INTERCHANGE

import time

def create_credit_card_merchant():
    """Create credit card merchant workflow with comprehensive performance tracking."""

    username, password = osc_settings.credentials

    with UIAutomationCore(
        app_name="osc",
        script_name="create_credit_card_merchant",
        headless=False,
        enable_performance_tracking=True,
        # record_video and enable_tracing are driven from config/browser.config.yaml
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

        # core.take_screenshot("corporate_info_completed")

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

        # core.take_screenshot("location_info_completed")

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

        # ==================== Step 12: Fill Billing Questionnaire ====================
        log_step("Step 12: Filling Billing Questionnaire section")
        
        logger.info(f"Using Billing Data: Merchant Type = {BILLING_QUESTIONNAIRE_INFO['merchant_type']}")

        billing_results = new_app_page.fill_billing_questionnaire_section()
        all_results["billing_questionnaire"] = billing_results

        billing_success = sum(1 for r in billing_results.values() if r)
        billing_total = len(billing_results)

        if billing_success == billing_total:
            log_success(f"Billing Questionnaire: {billing_success}/{billing_total} fields")
        else:
            failed = [f for f, r in billing_results.items() if not r]
            logger.warning(f"Billing Questionnaire: {billing_success}/{billing_total}. Failed: {failed}")

        core.take_screenshot("billing_questionnaire_completed")

        # ==================== Step 13: Fill Bank Information ====================
        log_step("Step 13: Filling Bank Information section")
        
        logger.info(f"Using Bank Data: Routing={BANK_INFORMATION['routing_number']}, Account={BANK_INFORMATION['account_number']}")

        bank_results = new_app_page.fill_bank_information_section()
        all_results["bank_info"] = bank_results

        bank_success = sum(1 for r in bank_results.values() if r)
        bank_total = len(bank_results)

        if bank_success == bank_total:
            log_success(f"Bank Information: {bank_success}/{bank_total} fields")
        else:
            failed = [f for f, r in bank_results.items() if not r]
            logger.warning(f"Bank Information: {bank_success}/{bank_total}. Failed: {failed}")

        core.take_screenshot("bank_info_completed")

        # ==================== Step 14: Fill Credit Card Information ====================
        log_step("Step 14: Filling Credit Card Information section")
        
        logger.info(f"Using Credit Card Data: Auth Network={CREDIT_CARD_INFORMATION['authorization_network']}")

        cc_info_results = new_app_page.fill_credit_card_information_section()
        all_results["credit_card_info"] = cc_info_results

        cc_info_success = sum(1 for r in cc_info_results.values() if r)
        cc_info_total = len(cc_info_results)

        if cc_info_success == cc_info_total:
            log_success(f"Credit Card Information: {cc_info_success}/{cc_info_total} fields")
        else:
            failed = [f for f, r in cc_info_results.items() if not r]
            logger.warning(f"Credit Card Information: {cc_info_success}/{cc_info_total}. Failed: {failed}")

        core.take_screenshot("credit_card_info_completed")

        # ==================== Step 15: Fill Credit Card Services ====================
        log_step("Step 15: Filling Credit Card Services section")
        
        logger.info(f"Services to select: {CREDIT_CARD_SERVICES}")

        cc_services_results = new_app_page.fill_credit_card_services_section()
        all_results["credit_card_services"] = cc_services_results

        cc_services_success = sum(1 for r in cc_services_results.values() if r)
        cc_services_total = len(cc_services_results)

        if cc_services_success == cc_services_total:
            log_success(f"Credit Card Services: {cc_services_success}/{cc_services_total} services")
        else:
            failed = [f for f, r in cc_services_results.items() if not r]
            logger.warning(f"Credit Card Services: {cc_services_success}/{cc_services_total}. Failed: {failed}")

        core.take_screenshot("credit_card_services_completed")

        # ==================== Step 16: Fill Credit Card Underwriting ====================
        log_step("Step 16: Filling Credit Card Underwriting section")
        
        logger.info(f"Using Credit Card Underwriting Data: Monthly Volume={CREDIT_CARD_UNDERWRITING['monthly_volume']}, "
                   f"Avg Ticket={CREDIT_CARD_UNDERWRITING['average_ticket']}")
        logger.info(f"Card Distribution: Swiped={CREDIT_CARD_UNDERWRITING['card_present_swiped']}, "
                   f"Keyed={CREDIT_CARD_UNDERWRITING['card_present_keyed']}, "
                   f"Not Present={CREDIT_CARD_UNDERWRITING['card_not_present']}")
        logger.info(f"Sales Distribution: Consumer={CREDIT_CARD_UNDERWRITING['consumer_sales']}, "
                   f"Business={CREDIT_CARD_UNDERWRITING['business_sales']}, "
                   f"Govt={CREDIT_CARD_UNDERWRITING['government_sales']}")

        cc_underwriting_results = new_app_page.fill_credit_card_underwriting_section()
        all_results["credit_card_underwriting"] = cc_underwriting_results

        cc_underwriting_success = sum(1 for r in cc_underwriting_results.values() if r)
        cc_underwriting_total = len(cc_underwriting_results)

        if cc_underwriting_success == cc_underwriting_total:
            log_success(f"Credit Card Underwriting: {cc_underwriting_success}/{cc_underwriting_total} fields")
        else:
            failed = [f for f, r in cc_underwriting_results.items() if not r]
            logger.warning(f"Credit Card Underwriting: {cc_underwriting_success}/{cc_underwriting_total}. Failed: {failed}")

        core.take_screenshot("credit_card_underwriting_completed")

        # ==================== Step 17: Fill Credit Card Interchange ====================
        log_step("Step 17: Filling Credit Card Interchange section")
        
        logger.info(f"Using Credit Card Interchange Data: Type={CREDIT_CARD_INTERCHANGE['interchange_type']}")
        logger.info(f"BET Numbers: Visa={CREDIT_CARD_INTERCHANGE['visa_bet_number']}, "
                   f"MC={CREDIT_CARD_INTERCHANGE['mastercard_bet_number']}, "
                   f"Discover={CREDIT_CARD_INTERCHANGE['discover_bet_number']}, "
                   f"AMEX={CREDIT_CARD_INTERCHANGE['amex_bet_number']}")
        logger.info(f"Visa Rates: Qualified={CREDIT_CARD_INTERCHANGE['visa_qualified_rate']}, "
                   f"Signature={CREDIT_CARD_INTERCHANGE['visa_signature_rate']}")
        logger.info(f"MC Rates: Qualified={CREDIT_CARD_INTERCHANGE['mc_qualified_rate']}, "
                   f"Signature={CREDIT_CARD_INTERCHANGE['mc_signature_rate']}")
        logger.info(f"Discover Rates: Qualified={CREDIT_CARD_INTERCHANGE['discover_qualified_rate']}, "
                   f"Signature={CREDIT_CARD_INTERCHANGE['discover_signature_rate']}")
        logger.info(f"AMEX: Accept={not CREDIT_CARD_INTERCHANGE['does_not_accept_amex']}, "
                   f"Annual Volume={CREDIT_CARD_INTERCHANGE['amex_annual_volume']}")

        cc_interchange_results = new_app_page.fill_credit_card_interchange_section()
        all_results["credit_card_interchange"] = cc_interchange_results

        cc_interchange_success = sum(1 for r in cc_interchange_results.values() if r)
        cc_interchange_total = len(cc_interchange_results)

        if cc_interchange_success == cc_interchange_total:
            log_success(f"Credit Card Interchange: {cc_interchange_success}/{cc_interchange_total} fields")
        else:
            failed = [f for f, r in cc_interchange_results.items() if not r]
            logger.warning(f"Credit Card Interchange: {cc_interchange_success}/{cc_interchange_total}. Failed: {failed}")

        core.take_screenshot("credit_card_interchange_completed")

        # ==================== Step 18: Add Terminal (Wizard Step 1) ====================
        log_step("Step 18: Adding Terminal(s) - Wizard Step 1")
        
        # Add terminals using NewApplicationPage (delegates to AddTerminalPage internally)
        terminal_wizard_results = new_app_page.add_terminals()
        
        all_results["terminal_wizard"] = terminal_wizard_results["results"]
        
        terminal_success = terminal_wizard_results["success_count"]
        terminal_total = terminal_wizard_results["success_count"] + terminal_wizard_results["failed_count"]
        
        if terminal_success == terminal_total:
            log_success(f"Terminal Wizard Step 1: {terminal_success}/{terminal_total} terminals")
        else:
            failed = [name for name, res in terminal_wizard_results["results"].items() 
                     if not res.get("step1", False)]
            logger.warning(f"Terminal Wizard Step 1: {terminal_success}/{terminal_total}. Failed: {failed}")
        
        core.take_screenshot("terminal_wizard_step1_completed")

        # ==================== Step 19: Save Application ====================
        log_step("Step 19: Saving Application")
        
        save_result = new_app_page.save_application()
        all_results["save_application"] = save_result
        
        app_info_id = save_result.get("app_info_id")
        
        if save_result.get("success"):
            log_success(f"Application saved successfully. AppInfoID: {app_info_id}")
        else:
            logger.warning(f"Save application: {save_result.get('message')}")
        
        core.take_screenshot("application_saved")

        # ==================== Step 20: Validate Application ====================
        log_step("Step 20: Validating Application")
        
        validation_result = new_app_page.validate_application()
        all_results["validate_application"] = validation_result
        
        validation_success = validation_result.get("success", False)
        validation_message = validation_result.get("message", "")
        validation_errors = validation_result.get("errors", [])
        
        if validation_success:
            log_success(f"Validation passed: {validation_message}")
        else:
            logger.error(f"Validation failed: {validation_message}")
            if validation_errors:
                for idx, error in enumerate(validation_errors, 1):
                    logger.error(f"  {idx}. {error}")
        
        core.take_screenshot("application_validated")

        # ==================== Step 21: Submit Application (COMMENTED - Enable in lower env) ====================
        # log_step("Step 21: Submitting Application")
        # 
        # submit_result = new_app_page.submit_application()
        # all_results["submit_application"] = submit_result
        # 
        # if submit_result.get("success"):
        #     log_success("Application submitted successfully")
        # else:
        #     logger.warning(f"Submit application: {submit_result.get('message')}")
        # 
        # core.take_screenshot("application_submitted")

        # ==================== Summary ====================
        log_section("WORKFLOW SUMMARY")
        
        total_success = (app_success + corp_success + loc_success + 
                        tax_success + owner1_success + owner2_success +
                        trade_success + underwriting_success + billing_success +
                        bank_success + cc_info_success + cc_services_success +
                        cc_underwriting_success + cc_interchange_success +
                        terminal_success)
        total_fields = (app_total + corp_total + loc_total + 
                       tax_total + owner1_total + owner2_total +
                       trade_total + underwriting_total + billing_total +
                       bank_total + cc_info_total + cc_services_total +
                       cc_underwriting_total + cc_interchange_total +
                       terminal_total)
        
        logger.info(f"Application Information: {app_success}/{app_total}")
        logger.info(f"Corporate Information: {corp_success}/{corp_total}")
        logger.info(f"Location Information: {loc_success}/{loc_total}")
        logger.info(f"Tax Information: {tax_success}/{tax_total}")
        logger.info(f"Owner/Officer 1: {owner1_success}/{owner1_total}")
        logger.info(f"Owner/Officer 2: {owner2_success}/{owner2_total}")
        logger.info(f"Trade Reference: {trade_success}/{trade_total}")
        logger.info(f"General Underwriting: {underwriting_success}/{underwriting_total}")
        logger.info(f"Billing Questionnaire: {billing_success}/{billing_total}")
        logger.info(f"Bank Information: {bank_success}/{bank_total}")
        logger.info(f"Credit Card Information: {cc_info_success}/{cc_info_total}")
        logger.info(f"Credit Card Services: {cc_services_success}/{cc_services_total}")
        logger.info(f"Credit Card Underwriting: {cc_underwriting_success}/{cc_underwriting_total}")
        logger.info(f"Credit Card Interchange: {cc_interchange_success}/{cc_interchange_total}")
        logger.info(f"Terminal Wizard Step 1: {terminal_success}/{terminal_total}")
        logger.info(f"─" * 40)
        logger.info(f"TOTAL: {total_success}/{total_fields} ({(total_success/total_fields)*100:.1f}%)")

        if total_success == total_fields:
            log_success("All sections completed successfully!")
        else:
            logger.warning(f"Completed with {total_fields - total_success} field(s) failed")

        # ==================== Final Summary ====================
        log_section("APPLICATION SAVED & VALIDATED")
        if app_info_id:
            logger.info(f"✅ AppInfoID: {app_info_id}")
        else:
            logger.warning("⚠️ AppInfoID not extracted")
        
        if validation_success:
            logger.info(f"✅ Validation: {validation_message}")
        else:
            logger.error(f"❌ Validation Failed: {validation_message}")
            if validation_errors:
                logger.error(f"   Errors ({len(validation_errors)}):")
                for error in validation_errors:
                    logger.error(f"   • {error}")

        # TODO: Add next sections (Equipment, etc.)

        core.take_screenshot("final_state")
        
        return {
            "results": all_results,
            "app_info_id": app_info_id,
            "validation": {
                "success": validation_success,
                "message": validation_message,
                "errors": validation_errors
            },
            "summary": {
                "total_success": total_success,
                "total_fields": total_fields,
                "success_rate": f"{(total_success/total_fields)*100:.1f}%"
            }
        }
    
    


if __name__ == "__main__":
    results = create_credit_card_merchant()
    
    if results:
        app_id = results.get('app_info_id', 'Unknown')
        validation = results.get('validation', {})
        
        print(f"\n✅ Merchant creation completed: {results['summary']['success_rate']} success rate")
        print(f"📋 AppInfoID: {app_id}")
        
        if validation.get('success'):
            print(f"✅ Validation: {validation.get('message', 'Passed')}")
        else:
            print(f"❌ Validation Failed: {validation.get('message', 'Unknown')}")
            errors = validation.get('errors', [])
            if errors:
                print(f"   Errors ({len(errors)}):")
                for error in errors:
                    print(f"   • {error}")
    else:
        print("\n❌ Merchant creation failed")
