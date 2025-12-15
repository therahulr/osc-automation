#!/usr/bin/env python3
"""
Terminal Discovery Script - Identifies all valid terminal combinations in OSC.

This script systematically tests all Part Type + Provider combinations to discover
which terminals can be successfully added. Results are saved to valid_prod_parts_osc.json.

Usage:
    python scripts/osc/discover_valid_terminals.py
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.sync_api import Page
from core import UIAutomationCore, log_step, log_success, log_section
from pages.osc.login_page import LoginPage
from pages.osc.add_terminal_page import AddTerminalPage
from config.osc.config import osc_settings

logger = None  # Will be set by UIAutomationCore

# Constants
APPLICATION_URL = "https://uno.eftsecure.net/SalesCenter/frmApplicationRecord.aspx?ApplicationID=313320"
RESULTS_FILE = Path(__file__).parent.parent.parent / "data" / "osc" / "valid_prod_parts_osc.json"

# Part Type and Provider combinations
# PART_TYPES = ["Software", "Terminal", "Terminal/Printer", "Gateway"]
PART_TYPES = ["Terminal", "Terminal/Printer", "Gateway"]
PROVIDERS = ["Merchant", "Sage Payment Solutions", "ISO"]


def generate_combinations() -> List[Tuple[str, str]]:
    """Generate all Part Type + Provider combinations."""
    combinations = []
    for part_type in PART_TYPES:
        for provider in PROVIDERS:
            combinations.append((part_type, provider))
    return combinations


def load_results() -> Dict[str, Any]:
    """Load existing results from JSON file."""
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return {
        "discovery_date": None,
        "application_id": "313320",
        "total_combinations": 0,
        "combinations_tested": 0,
        "total_parts_found": 0,
        "total_parts_tested": 0,
        "successful_parts": 0,
        "failed_parts": 0,
        "combinations": {}
    }


def save_results(results: Dict[str, Any]) -> None:
    """Save results to JSON file."""
    results["discovery_date"] = datetime.now().isoformat()
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {RESULTS_FILE}")


def get_combination_key(part_type: str, provider: str) -> str:
    """Generate combination key for JSON storage."""
    return f"{part_type.replace(' ', '_').replace('/', '_')}_{provider.replace(' ', '_')}"


def extract_part_ids(page: Page) -> List[str]:
    """Extract all Part IDs from Step 2 grid."""
    try:
        # Wait for grid to load
        time.sleep(1)
        
        # Locator for all PartID cells (2nd column, excluding header)
        partid_cells = page.locator(
            "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_TerminalGrid tr:not(:first-child) td:nth-child(2)"
        )
        
        # Extract text into list
        part_ids = [text.strip() for text in partid_cells.all_text_contents() if text.strip()]
        
        logger.info(f"Found {len(part_ids)} Part IDs: {part_ids[:5]}{'...' if len(part_ids) > 5 else ''}")
        return part_ids
        
    except Exception as e:
        logger.error(f"Failed to extract Part IDs: {e}")
        return []


def is_next_button_enabled(page: Page, step: int) -> bool:
    """Check if Next button is enabled for given step."""
    next_button_locators = {
        3: "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnNext3",
        4: "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnNext4",
        5: "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnNext5",
    }
    
    locator = next_button_locators.get(step)
    if not locator:
        return True
    
    try:
        button = page.locator(locator)
        return not button.is_disabled()
    except:
        return False


def click_previous_button(page: Page, step: int) -> bool:
    """Click Previous button to go back."""
    previous_button_locators = {
        3: "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnPrevious3",
        4: "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnPrevious4",
        5: "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnPrevious5",
    }
    
    locator = previous_button_locators.get(step)
    if not locator:
        return False
    
    try:
        page.click(locator)
        time.sleep(1)
        return True
    except Exception as e:
        logger.error(f"Failed to click Previous button: {e}")
        return False


def test_terminal_addition(
    page: Page,
    add_terminal_page: AddTerminalPage,
    part_type: str,
    provider: str,
    part_id: str
) -> Dict[str, Any]:
    """Test adding a single terminal and return result."""
    
    result = {
        "status": "unknown",
        "notes": "",
        "failed_at_step": None
    }
    
    try:
        # Get equipment count before
        equipment_before = add_terminal_page.get_equipment_list()
        
        # Open wizard
        if not add_terminal_page.open_terminal_wizard():
            result["status"] = "failed"
            result["notes"] = "Failed to open wizard"
            return result
        
        # Step 1: Select Type
        terminal_config = {
            "part_type": part_type,
            "provider": provider,
            "part_condition": "New",
            "part_id": part_id,
            "terminal_program": "VAR / STAGE",
            "bill_to": "Location",
            "ship_to": "Location",
            "ship_method": "Ground"
        }
        
        if not add_terminal_page.complete_step_1(terminal_config):
            result["status"] = "failed"
            result["notes"] = "Failed at Step 1"
            result["failed_at_step"] = 1
            return result
        
        # Step 2: Select Part
        if not add_terminal_page.complete_step_2(terminal_config):
            result["status"] = "failed"
            result["notes"] = "Failed at Step 2 - Part ID not found or not selectable"
            result["failed_at_step"] = 2
            return result
        
        # Step 3: Terminal Details
        # Note: complete_step_3 fills fields AND clicks Next to go to Step 4
        if not add_terminal_page.complete_step_3(terminal_config):
            result["status"] = "failed"
            result["notes"] = "Failed at Step 3 or Next button disabled"
            result["failed_at_step"] = 3
            # Try to close wizard
            try:
                page.click("#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnCancel3")
            except:
                pass
            return result
        
        # Step 4: Terminal Application
        if not add_terminal_page.complete_step_4(terminal_config):
            result["status"] = "failed"
            result["notes"] = "Failed at Step 4"
            result["failed_at_step"] = 4
            return result
        
        # Step 5: Billing & Shipping
        if not add_terminal_page.complete_step_5(terminal_config):
            result["status"] = "failed"
            result["notes"] = "Failed at Step 5"
            result["failed_at_step"] = 5
            return result
        
        # Step 6: Review & Finish (includes verification)
        step6_result = add_terminal_page.complete_step_6(terminal_config, equipment_before=equipment_before)
        
        if step6_result["success"]:
            result["status"] = "success"
            result["notes"] = "Terminal added successfully"
        else:
            result["status"] = "failed"
            result["notes"] = "Failed at Step 6 or verification failed"
            result["failed_at_step"] = 6
        
    except Exception as e:
        result["status"] = "failed"
        result["notes"] = f"Exception: {str(e)}"
        logger.error(f"Error testing terminal {part_id}: {e}")
    
    return result


def discover_terminals():
    """Main discovery function."""
    global logger
    
    username, password = osc_settings.credentials
    
    with UIAutomationCore(
        app_name="osc",
        script_name="discover_valid_terminals",
        headless=False,
        enable_performance_tracking=False,
        metadata={
            "environment": "discovery",
            "tags": ["terminal", "discovery", "equipment"],
            "notes": "Terminal discovery automation"
        }
    ) as core:
        
        page = core.page
        logger = core.logger
        
        log_section("Terminal Discovery Script")
        
        # Load existing results
        results = load_results()
        combinations = generate_combinations()
        results["total_combinations"] = len(combinations)
        
        logger.info(f"Testing {len(combinations)} Part Type + Provider combinations")
        logger.info(f"Results will be saved to: {RESULTS_FILE}")
        
        # Login
        log_step("Logging in to OSC...")
        login_page = LoginPage(page)
        if not login_page.complete_login(username, password):
            logger.error("Login failed")
            return
        
        log_success("Login successful")
        
        # Navigate to application
        log_step(f"Navigating to application {APPLICATION_URL}")
        page.goto(APPLICATION_URL)
        time.sleep(2)
        
        # Initialize AddTerminalPage
        add_terminal_page = AddTerminalPage(page)
        
        # Scroll to Equipment section
        log_step("Scrolling to Equipment section...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        
        # Test each combination
        for idx, (part_type, provider) in enumerate(combinations, 1):
            combo_key = get_combination_key(part_type, provider)
            
            log_section(f"Combination {idx}/{len(combinations)}: {part_type} + {provider}")
            
            # Initialize combination result
            if combo_key not in results["combinations"]:
                results["combinations"][combo_key] = {
                    "part_type": part_type,
                    "provider": provider,
                    "available_parts": [],
                    "valid_parts": {}
                }
            
            combo_result = results["combinations"][combo_key]
            
            # Open wizard and navigate to Step 2
            if not add_terminal_page.open_terminal_wizard():
                logger.error("Failed to open wizard, skipping combination")
                continue
            
            # Fill Step 1 and navigate to Step 2
            temp_config = {
                "part_type": part_type,
                "provider": provider,
                "part_condition": "New"
            }
            
            if not add_terminal_page.complete_step_1(temp_config):
                logger.error("Failed to complete Step 1, skipping combination")
                try:
                    page.click("#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnCancel1")
                except:
                    pass
                continue
            
            # Now on Step 2 - extract Part IDs
            part_ids = extract_part_ids(page)
            combo_result["available_parts"] = part_ids
            results["total_parts_found"] += len(part_ids)
            
            # Close wizard before testing individual parts
            try:
                page.click("#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_btnCancel2")
                time.sleep(1)
            except:
                pass
            
            # Test each Part ID (limit to 3 for production)
            max_parts_to_test = min(3, len(part_ids))  # Only test first 3 parts per combination
            logger.info(f"Testing {max_parts_to_test} of {len(part_ids)} parts for this combination")
            
            for part_idx in range(max_parts_to_test):
                part_id = part_ids[part_idx]
                logger.info(f"Testing Part {part_idx + 1}/{max_parts_to_test}: {part_id}")
                
                test_result = test_terminal_addition(page, add_terminal_page, part_type, provider, part_id)
                combo_result["valid_parts"][part_id] = test_result
                
                results["total_parts_tested"] += 1
                if test_result["status"] == "success":
                    results["successful_parts"] += 1
                    logger.info(f"✓ {part_id}: SUCCESS")
                else:
                    results["failed_parts"] += 1
                    logger.info(f"✗ {part_id}: FAILED - {test_result['notes']}")
                
                # Save results after each part
                save_results(results)
                
                time.sleep(1)
            
            results["combinations_tested"] += 1
            save_results(results)
        
        log_section("Discovery Complete")
        logger.info(f"Combinations tested: {results['combinations_tested']}/{results['total_combinations']}")
        logger.info(f"Parts found: {results['total_parts_found']}")
        logger.info(f"Parts tested: {results['total_parts_tested']}")
        logger.info(f"Successful: {results['successful_parts']}")
        logger.info(f"Failed: {results['failed_parts']}")


if __name__ == "__main__":
    discover_terminals()
