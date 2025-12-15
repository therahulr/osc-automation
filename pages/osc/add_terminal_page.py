"""
Add Terminal Wizard Page - Handles Terminal Wizard multi-step automation.

This module provides functions for adding terminals through the 6-step wizard.
Each step is handled with proper wait strategies, verification, and retry logic.
"""

from playwright.sync_api import Page, TimeoutError
from typing import Dict, Any, Optional, List
import time

from core.logger import get_logger
from core.utils import SYMBOL_CHECK, SYMBOL_CROSS
from locators.osc_locators import TerminalWizardLocators, CommonLocators, EquipmentTableLocators

# Dynamic import of terminal data helper functions based on environment
def _load_terminal_helpers():
    """Load terminal data helper functions based on current environment."""
    from config.osc.config import osc_settings
    import importlib
    
    env = osc_settings.environment
    module_name = f"data.osc.add_terminal_{env}"
    
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        print(f"Warning: Terminal data module '{module_name}' not found. "
              f"Falling back to 'data.osc.add_terminal_prod'. Error: {e}")
        return importlib.import_module("data.osc.add_terminal_prod")

_terminal_helpers = _load_terminal_helpers()
add_to_added_terminals = _terminal_helpers.add_to_added_terminals
get_added_terminals = _terminal_helpers.get_added_terminals
clear_added_terminals = _terminal_helpers.clear_added_terminals
generate_serial_number = _terminal_helpers.generate_serial_number
generate_random_price = _terminal_helpers.generate_random_price
generate_random_fee = _terminal_helpers.generate_random_fee



class AddTerminalPage:
    """
    Handles the Terminal Wizard automation for adding terminals.
    
    The wizard consists of 6 steps:
    1. Select Type (Part Type, Provider, Condition)
    2. Select Terminal from grid
    3. Terminal details (Serial, Price, Fees)
    4. Select Terminal Program
    5. Billing & Shipping Information
    6. Review & Finish
    
    This class provides:
    - Robust wait strategies for wizard loading
    - Step verification before actions
    - Retry logic for unreliable elements
    - Clear logging of all actions
    """
    
    # Timeouts in milliseconds
    DEFAULT_TIMEOUT = 10000  # 10 seconds
    SHORT_TIMEOUT = 5000     # 5 seconds
    LONG_TIMEOUT = 30000     # 30 seconds
    WIZARD_OPEN_TIMEOUT = 15000  # 15 seconds for wizard to open
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger()
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def wait_for_element(self, selector: str, timeout: int = None, state: str = "visible") -> bool:
        """
        Wait for an element to be in specified state.
        
        Args:
            selector: CSS or XPath selector
            timeout: Maximum wait time in ms
            state: 'visible', 'hidden', 'attached', 'detached'
            
        Returns:
            bool: True if element reached state, False otherwise
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            return True
        except TimeoutError:
            self.logger.debug(f"Element not found in state '{state}': {selector[:80]}...")
            return False
    
    def wait_for_processing_banner_hidden(self, timeout: int = None) -> bool:
        """
        Wait for the processing banner to disappear.
        
        Args:
            timeout: Maximum wait time in ms
            
        Returns:
            bool: True if banner hidden or not found, False on timeout
        """
        timeout = timeout or self.LONG_TIMEOUT
        try:
            # First check if banner exists
            if self.page.locator(TerminalWizardLocators.PROCESSING_BANNER).count() > 0:
                self.page.wait_for_selector(
                    TerminalWizardLocators.PROCESSING_BANNER,
                    timeout=timeout,
                    state="hidden"
                )
                self.logger.debug("Processing banner hidden")
            return True
        except TimeoutError:
            self.logger.warning("Processing banner did not disappear in time")
            return False
    
    def get_equipment_list(self) -> Dict[str, Any]:
        """
        Get the current list of equipment/terminals from the Equipment Table.
        
        Returns:
            Dict with:
                - terminals: List of terminal names
                - count: Number of terminals
                - has_equipment: True if equipment exists, False if empty
        """
        result = {
            "terminals": [],
            "count": 0,
            "has_equipment": False
        }
        
        try:
            # First check if "No configured equipment" message is displayed
            no_equipment = self.page.locator(EquipmentTableLocators.NO_CONFIGURED_TERMINAL_TEXT)
            if no_equipment.count() > 0 and no_equipment.is_visible():
                self.logger.info("Equipment Table: No configured equipment found")
                return result
            
            # Check if the table exists
            table = self.page.locator(EquipmentTableLocators.TABLE)
            if table.count() == 0:
                self.logger.debug("Equipment Table not found on page")
                return result
            
            # Get all terminal rows
            terminal_rows = self.page.locator(EquipmentTableLocators.ALL_TERMINALS)
            count = terminal_rows.count()
            
            if count == 0:
                self.logger.info("Equipment Table: No terminals in table")
                return result
            
            # Extract terminal names from each row
            terminals = []
            for i in range(count):
                row = terminal_rows.nth(i)
                # Get the datakeys attribute which contains the terminal name
                datakeys = row.get_attribute("datakeys")
                if datakeys:
                    terminals.append(datakeys)
            
            result["terminals"] = terminals
            result["count"] = len(terminals)
            result["has_equipment"] = len(terminals) > 0
            
            self.logger.info(f"Equipment Table: Found {len(terminals)} terminal(s): {terminals}")
            
        except Exception as e:
            self.logger.error(f"Error getting equipment list: {e}")
        
        return result
    
    def wait_for_equipment_table(self, timeout: int = None) -> bool:
        """
        Wait for the Equipment Table to be visible after page reload.
        
        Args:
            timeout: Maximum wait time in ms
            
        Returns:
            bool: True if table is visible, False on timeout
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            # Wait for either the table or the "no equipment" message
            self.page.wait_for_selector(
                f"{EquipmentTableLocators.TABLE} | {EquipmentTableLocators.NO_CONFIGURED_TERMINAL_TEXT}",
                timeout=timeout,
                state="visible"
            )
            return True
        except TimeoutError:
            self.logger.warning("Equipment Table did not appear in time")
            return False
    
    def verify_terminal_added(self, terminal_name: str, equipment_before: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify if a terminal was successfully added by comparing equipment lists.
        
        Args:
            terminal_name: The name of the terminal that should have been added
            equipment_before: The equipment list captured before adding
            
        Returns:
            Dict with:
                - success: True if terminal was added
                - terminals_before: List of terminals before adding
                - terminals_after: List of terminals after adding
                - newly_added: List of newly added terminals
                - total_count: Total terminals after adding
        """
        result = {
            "success": False,
            "terminals_before": equipment_before.get("terminals", []),
            "terminals_after": [],
            "newly_added": [],
            "total_count": 0
        }
        
        # Wait for Equipment Table to reload
        self.logger.info("Waiting for Equipment Table to reload...")
        time.sleep(2)  # Brief wait for page reload
        self.wait_for_equipment_table()
        
        # Get current equipment list
        equipment_after = self.get_equipment_list()
        result["terminals_after"] = equipment_after.get("terminals", [])
        result["total_count"] = equipment_after.get("count", 0)
        
        # Find newly added terminals
        terminals_before_set = set(result["terminals_before"])
        terminals_after_set = set(result["terminals_after"])
        newly_added = list(terminals_after_set - terminals_before_set)
        result["newly_added"] = newly_added
        
        # Check if the expected terminal was added
        if terminal_name in result["terminals_after"]:
            if terminal_name in newly_added or terminal_name not in result["terminals_before"]:
                result["success"] = True
                self.logger.info(f"{SYMBOL_CHECK} Terminal '{terminal_name}' verified in Equipment Table")
            else:
                # Terminal was already there
                self.logger.warning(f"Terminal '{terminal_name}' was already in the table before adding")
                result["success"] = True  # Still consider success if it exists
        else:
            self.logger.error(f"{SYMBOL_CROSS} Terminal '{terminal_name}' NOT found in Equipment Table")
        
        # Log the comparison
        self.logger.info("=" * 60)
        self.logger.info("EQUIPMENT TABLE VERIFICATION")
        self.logger.info(f"Before: {result['terminals_before']} (count: {len(result['terminals_before'])})")
        self.logger.info(f"After:  {result['terminals_after']} (count: {result['total_count']})")
        self.logger.info(f"Newly Added: {result['newly_added']}")
        self.logger.info(f"Verification: {'PASSED' if result['success'] else 'FAILED'}")
        self.logger.info("=" * 60)
        
        return result
    
    def verify_step_header(self, step_number: int, timeout: int = None) -> bool:
        """
        Verify that the correct step header is displayed.
        
        Args:
            step_number: The step number (1-6)
            timeout: Maximum wait time in ms
            
        Returns:
            bool: True if correct header is visible, False otherwise
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        
        # Get the header locator for this step
        header_locators = {
            1: TerminalWizardLocators.STEP_1_HEADER,
            2: TerminalWizardLocators.STEP_2_HEADING,
            3: TerminalWizardLocators.STEP_3_HEADING,
            4: TerminalWizardLocators.STEP_4_HEADING,
            5: TerminalWizardLocators.STEP_5_HEADING,
            6: TerminalWizardLocators.STEP_6_HEADING,
        }
        
        header_locator = header_locators.get(step_number)
        if not header_locator:
            self.logger.error(f"No header locator defined for step {step_number}")
            return False
        
        try:
            self.page.wait_for_selector(header_locator, timeout=timeout, state="visible")
            self.logger.info(f"Step {step_number} of 6 header verified")
            return True
        except TimeoutError:
            self.logger.warning(f"Step {step_number} header not visible")
            return False
    
    def select_dropdown_by_label(self, selector: str, label: str, field_name: str = None) -> bool:
        """
        Select dropdown option by visible label text.
        
        Args:
            selector: CSS or XPath selector for the dropdown
            label: The visible text of the option to select
            field_name: Friendly name for logging
            
        Returns:
            bool: True if successful, False otherwise
        """
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            self.page.select_option(selector, label=label)
            self.logger.info(f"{field_name}: Selected '{label}'")
            return True
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to select '{label}' - {e}")
            return False
    
    # =========================================================================
    # WIZARD OPEN & INITIALIZATION
    # =========================================================================
    
    def open_terminal_wizard(self, max_retries: int = None) -> bool:
        """
        Click Terminal Wizard button and wait for wizard to open.
        
        Handles potential delays due to internet speed by:
        1. Clicking the wizard button
        2. Waiting for Step 1 header to appear
        3. Retrying if wizard doesn't open
        
        Args:
            max_retries: Maximum number of retry attempts
            
        Returns:
            bool: True if wizard opened successfully, False otherwise
        """
        max_retries = max_retries or self.MAX_RETRIES
        
        for attempt in range(1, max_retries + 1):
            self.logger.info(f"Opening Terminal Wizard (attempt {attempt}/{max_retries})...")
            
            try:
                # Scroll to Equipment section and wait for wizard button
                wizard_button = self.page.locator(TerminalWizardLocators.TERMINAL_WIZARD_BUTTON)
                
                # Scroll the button into view first
                wizard_button.scroll_into_view_if_needed()
                self.logger.debug("Scrolled Terminal Wizard button into view")
                
                # Wait for button to be visible and clickable
                wizard_button.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
                self.logger.debug("Terminal Wizard button is visible")
                
                # Click the wizard button
                wizard_button.click()
                self.logger.debug("Clicked Terminal Wizard button")
                
                # Wait a moment for modal to start opening
                time.sleep(1)
                
                # Verify Step 1 header is visible
                if self.verify_step_header(1, timeout=self.WIZARD_OPEN_TIMEOUT):
                    self.logger.info("Terminal Wizard opened successfully - Step 1 visible")
                    return True
                else:
                    self.logger.warning(f"Attempt {attempt}: Step 1 header not visible, retrying...")
                    
                    # Close any partial modal if exists
                    try:
                        if self.page.locator(TerminalWizardLocators.STEP_1_CANCEL_BUTTON).is_visible():
                            self.page.click(TerminalWizardLocators.STEP_1_CANCEL_BUTTON)
                            time.sleep(0.5)
                    except Exception:
                        pass
                    
                    time.sleep(self.RETRY_DELAY)
                    
            except Exception as e:
                self.logger.warning(f"Attempt {attempt}: Error opening wizard - {e}")
                time.sleep(self.RETRY_DELAY)
        
        self.logger.error(f"Failed to open Terminal Wizard after {max_retries} attempts")
        return False
    
    # =========================================================================
    # STEP 1: SELECT TYPE
    # =========================================================================
    
    def fill_step_1(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Fill Step 1 of the Terminal Wizard: Select Type.
        
        This step involves:
        1. Selecting Part Type from dropdown
        2. Selecting Provider from dropdown
        3. Selecting Part Condition from dropdown (always "New")
        
        Args:
            terminal_config: Dict with 'part_type', 'provider', 'part_condition'
                Example: {"name": "Sage Virtual Terminal", "part_type": "Gateway", ...}
            
        Returns:
            bool: True if Step 1 completed successfully, False otherwise
        """
        self.logger.info("=== Step 1: Select Type ===")
        
        # Verify we're on Step 1
        if not self.verify_step_header(1, timeout=self.SHORT_TIMEOUT):
            self.logger.error("Not on Step 1 - cannot proceed")
            return False
        
        # Extract config values
        part_type = terminal_config.get("part_type", "Terminal")
        provider = terminal_config.get("provider", "Merchant")
        part_condition = terminal_config.get("part_condition", "New")
        
        self.logger.info(f"Configuration: Part Type='{part_type}', Provider='{provider}', Condition='{part_condition}'")
        
        # Step 1a: Select Part Type
        if not self.select_dropdown_by_label(
            TerminalWizardLocators.STEP_1_PART_TYPE_DROPDOWN,
            part_type,
            "Part Type"
        ):
            return False
        
        # Wait for processing banner (dynamic form may show loading)
        time.sleep(0.5)
        self.wait_for_processing_banner_hidden(timeout=self.DEFAULT_TIMEOUT)
        
        # Step 1b: Select Provider
        if not self.select_dropdown_by_label(
            TerminalWizardLocators.STEP_1_PROVIDER_DROPDOWN,
            provider,
            "Provider"
        ):
            return False
        
        # Wait for processing banner
        time.sleep(0.5)
        self.wait_for_processing_banner_hidden(timeout=self.DEFAULT_TIMEOUT)
        
        # Step 1c: Select Part Condition
        if not self.select_dropdown_by_label(
            TerminalWizardLocators.STEP_1_PART_CONDITION_DROPDOWN,
            part_condition,
            "Part Condition"
        ):
            return False
        
        # Wait for processing banner before proceeding
        time.sleep(0.5)
        self.wait_for_processing_banner_hidden(timeout=self.DEFAULT_TIMEOUT)
        
        self.logger.info("Step 1 fields filled successfully")
        return True
    
    def complete_step_1(self, terminal_config: Dict[str, str]) -> bool:
        """
        Complete Step 1 and navigate to Step 2.
        
        This includes:
        1. Filling all Step 1 fields
        2. Clicking Next button
        3. Waiting for processing
        4. Verifying Step 2 header
        
        Args:
            terminal_config: Dict with terminal configuration
            
        Returns:
            bool: True if successfully moved to Step 2, False otherwise
        """
        # Fill Step 1 fields
        if not self.fill_step_1(terminal_config):
            return False
        
        # Click Next button
        self.logger.info("Clicking Next button to proceed to Step 2...")
        
        try:
            self.page.click(TerminalWizardLocators.STEP_1_NEXT_BUTTON)
            
            # Wait for processing banner to appear and disappear
            time.sleep(0.5)
            self.wait_for_processing_banner_hidden(timeout=self.LONG_TIMEOUT)
            
            # Verify Step 2 header
            if self.verify_step_header(2, timeout=self.DEFAULT_TIMEOUT):
                self.logger.info("Successfully moved to Step 2")
                return True
            else:
                self.logger.error("Step 2 header not visible after clicking Next")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to complete Step 1: {e}")
            return False
    
    # =========================================================================
    # STEP 2: SELECT PART
    # =========================================================================
    
    def fill_step_2(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Fill Step 2 of the Terminal Wizard: Select Part.
        
        This step involves:
        1. Verifying Step 2 header is visible
        2. Finding the Part ID in the grid (scroll within modal if needed)
        3. Selecting the checkbox for the Part ID
        
        Args:
            terminal_config: Dict with 'part_id' key for the part to select
                Example: {"part_id": "Sage 50", ...}
            
        Returns:
            bool: True if Part ID found and selected, False otherwise
        """
        self.logger.info("=== Step 2: Select Part ===")
        
        # Verify we're on Step 2
        if not self.verify_step_header(2, timeout=self.SHORT_TIMEOUT):
            self.logger.error("Not on Step 2 - cannot proceed")
            return False
        
        # Extract part_id from config
        part_id = terminal_config.get("part_id", "")
        part_type = terminal_config.get("part_type", "Unknown")
        provider = terminal_config.get("provider", "Unknown")
        
        if not part_id:
            self.logger.error("No part_id specified in terminal config")
            return False
        
        self.logger.info(f"Looking for Part ID: '{part_id}' (Type: {part_type}, Provider: {provider})")
        
        # Build the checkbox locator for this part_id
        checkbox_locator = TerminalWizardLocators.STEP_2_PART_ID_CHECKBOX(part_id)
        
        try:
            # First, try to find the checkbox directly
            checkbox = self.page.locator(checkbox_locator)
            
            # Check if element exists in DOM
            if checkbox.count() == 0:
                self.logger.warning(f"Part ID '{part_id}' not found in grid")
                self.logger.warning(f"This part may not be available for Part Type: '{part_type}' and Provider: '{provider}'")
                return False
            
            # Scroll the checkbox into view within the modal
            self.logger.debug(f"Found Part ID '{part_id}', scrolling into view...")
            checkbox.scroll_into_view_if_needed()
            time.sleep(0.3)
            
            # Wait for it to be visible
            checkbox.wait_for(state="visible", timeout=self.SHORT_TIMEOUT)
            
            # Check if already selected
            if checkbox.is_checked():
                self.logger.info(f"Part ID '{part_id}' already selected")
            else:
                # Click to select
                checkbox.click()
                self.logger.info(f"Selected Part ID: '{part_id}'")
            
            time.sleep(0.3)
            return True
            
        except TimeoutError:
            self.logger.error(f"Part ID '{part_id}' not visible within timeout")
            self.logger.error(f"This part may not be available for Part Type: '{part_type}' and Provider: '{provider}'")
            return False
        except Exception as e:
            self.logger.error(f"Failed to select Part ID '{part_id}': {e}")
            return False
    
    def complete_step_2(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Complete Step 2 and navigate to Step 3.
        
        This includes:
        1. Selecting the Part ID from the grid
        2. Clicking Next button
        3. Waiting for processing
        4. Verifying Step 3 header
        
        Args:
            terminal_config: Dict with terminal configuration
            
        Returns:
            bool: True if successfully moved to Step 3, False otherwise
        """
        # Fill Step 2 (select part)
        if not self.fill_step_2(terminal_config):
            return False
        
        # Click Next button
        self.logger.info("Clicking Next button to proceed to Step 3...")
        
        try:
            next_button = self.page.locator(TerminalWizardLocators.STEP_2_NEXT_BUTTON)
            next_button.scroll_into_view_if_needed()
            next_button.click()
            
            # Wait for processing banner to appear and disappear
            time.sleep(0.5)
            self.wait_for_processing_banner_hidden(timeout=self.LONG_TIMEOUT)
            
            # Verify Step 3 header
            if self.verify_step_header(3, timeout=self.DEFAULT_TIMEOUT):
                self.logger.info("Successfully moved to Step 3")
                return True
            else:
                self.logger.error("Step 3 header not visible after clicking Next")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to complete Step 2: {e}")
            return False
    
    # =========================================================================
    # STEP 3: ENTER PART DETAILS
    # =========================================================================
    
    def _should_fill_field(self, config_value: Any) -> bool:
        """
        Determine if a field should be filled based on config value.
        
        Args:
            config_value: The config value - "random" means decide randomly,
                         "" or None means skip, anything else means fill
                         
        Returns:
            bool: True if field should be filled
        """
        import random
        
        if config_value == "random":
            return random.choice([True, False])
        elif config_value in ("", None, False):
            return False
        else:
            return True
    
    def fill_step_3(self, terminal_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill Step 3 of the Terminal Wizard: Enter Part Details.
        
        All fields are optional. For each field, randomly decide whether to fill or skip.
        This simulates realistic user behavior where not all optional fields are filled.
        
        Fields:
        - Serial Number: Optional, if filled use TEST<random_chars>
        - Merchant Sale Price: Optional, random price if filled
        - File Built By: Optional dropdown selection
        - Reprogram Fee: Optional checkbox + amount
        - Welcome Kit Fee: Optional checkbox + amount
        
        Args:
            terminal_config: Dict with step 3 configuration values.
                            Use "random" to decide at runtime.
            
        Returns:
            Dict with field names and their fill status/values
        """
        import random
        
        self.logger.info("=== Step 3: Enter Part Details ===")
        
        # Verify we're on Step 3
        if not self.verify_step_header(3, timeout=self.SHORT_TIMEOUT):
            self.logger.error("Not on Step 3 - cannot proceed")
            return {"success": False, "error": "Not on Step 3"}
        
        results = {"success": True, "fields_filled": {}}
        
        # ----- Serial Number -----
        serial_config = terminal_config.get("serial_number", "")
        fill_serial = self._should_fill_field(serial_config)
        
        if fill_serial:
            serial_value = generate_serial_number() if serial_config == "random" else serial_config
            try:
                self.page.fill(TerminalWizardLocators.SERIAL_NUMBER_INPUT, serial_value)
                self.logger.info(f"Serial Number: Filled with '{serial_value}'")
                results["fields_filled"]["serial_number"] = serial_value
            except Exception as e:
                self.logger.warning(f"Serial Number: Failed to fill - {e}")
        else:
            self.logger.info("Serial Number: Skipped (random decision: No)")
            results["fields_filled"]["serial_number"] = None
        
        time.sleep(0.3)
        
        # ----- Merchant Sale Price -----
        price_config = terminal_config.get("merchant_sale_price", "")
        fill_price = self._should_fill_field(price_config)
        
        if fill_price:
            price_value = generate_random_price() if price_config == "random" else str(price_config)
            try:
                # Clear existing value first
                self.page.locator(TerminalWizardLocators.MERCHANT_SALE_PRICE_INPUT).clear()
                self.page.fill(TerminalWizardLocators.MERCHANT_SALE_PRICE_INPUT, price_value)
                self.logger.info(f"Merchant Sale Price: Filled with '{price_value}'")
                results["fields_filled"]["merchant_sale_price"] = price_value
            except Exception as e:
                self.logger.warning(f"Merchant Sale Price: Failed to fill - {e}")
        else:
            self.logger.info("Merchant Sale Price: Skipped (random decision: No)")
            results["fields_filled"]["merchant_sale_price"] = None
        
        time.sleep(0.3)
        
        # ----- File Built By Dropdown -----
        file_built_config = terminal_config.get("file_built_by", "")
        fill_file_built = self._should_fill_field(file_built_config)
        
        if fill_file_built:
            try:
                dropdown = self.page.locator(TerminalWizardLocators.FILE_BUILT_BY_DROPDOWN)
                
                if file_built_config == "random":
                    # Get available options and select random one (excluding empty/default)
                    options = dropdown.locator("option").all_text_contents()
                    valid_options = [opt for opt in options if opt.strip() and opt.strip() != ""]
                    
                    if valid_options:
                        selected_option = random.choice(valid_options)
                        self.page.select_option(TerminalWizardLocators.FILE_BUILT_BY_DROPDOWN, label=selected_option)
                        self.logger.info(f"File Built By: Selected '{selected_option}'")
                        results["fields_filled"]["file_built_by"] = selected_option
                    else:
                        self.logger.info("File Built By: No valid options available, skipped")
                        results["fields_filled"]["file_built_by"] = None
                else:
                    # Use specific value from config
                    self.page.select_option(TerminalWizardLocators.FILE_BUILT_BY_DROPDOWN, label=file_built_config)
                    self.logger.info(f"File Built By: Selected '{file_built_config}'")
                    results["fields_filled"]["file_built_by"] = file_built_config
            except Exception as e:
                self.logger.warning(f"File Built By: Failed to select - {e}")
        else:
            self.logger.info("File Built By: Skipped (random decision: No)")
            results["fields_filled"]["file_built_by"] = None
        
        time.sleep(0.3)
        
        # ----- Reprogram Fee (Checkbox + Amount) -----
        reprogram_config = terminal_config.get("reprogram_fee", False)
        reprogram_amount_config = terminal_config.get("reprogram_fee_amount", "")
        
        # Decide if we check the reprogram checkbox
        if reprogram_config == "random":
            check_reprogram = random.choice([True, False])
        else:
            check_reprogram = bool(reprogram_config)
        
        if check_reprogram:
            try:
                checkbox = self.page.locator(TerminalWizardLocators.REPROGRAM_CHECKBOX)
                if not checkbox.is_checked():
                    checkbox.click()
                    time.sleep(0.3)
                    self.logger.info("Reprogram Fee: Checkbox checked")
                
                # Fill the amount
                amount = generate_random_fee() if reprogram_amount_config == "random" else str(reprogram_amount_config)
                self.page.locator(TerminalWizardLocators.REPROGRAM_FEE_INPUT).clear()
                self.page.fill(TerminalWizardLocators.REPROGRAM_FEE_INPUT, amount)
                self.logger.info(f"Reprogram Fee Amount: Filled with '{amount}'")
                results["fields_filled"]["reprogram_fee"] = True
                results["fields_filled"]["reprogram_fee_amount"] = amount
            except Exception as e:
                self.logger.warning(f"Reprogram Fee: Failed - {e}")
        else:
            self.logger.info("Reprogram Fee: Skipped (random decision: No)")
            results["fields_filled"]["reprogram_fee"] = False
            results["fields_filled"]["reprogram_fee_amount"] = None
        
        time.sleep(0.3)
        
        # ----- Welcome Kit Fee (Checkbox + Amount) -----
        welcome_config = terminal_config.get("welcome_kit_fee", False)
        welcome_amount_config = terminal_config.get("welcome_kit_fee_amount", "")
        
        # Decide if we check the welcome kit checkbox
        if welcome_config == "random":
            check_welcome = random.choice([True, False])
        else:
            check_welcome = bool(welcome_config)
        
        if check_welcome:
            try:
                checkbox = self.page.locator(TerminalWizardLocators.WELCOME_KIT_CHECKBOX)
                if not checkbox.is_checked():
                    checkbox.click()
                    time.sleep(0.3)
                    self.logger.info("Welcome Kit Fee: Checkbox checked")
                
                # Fill the amount
                amount = generate_random_fee() if welcome_amount_config == "random" else str(welcome_amount_config)
                self.page.locator(TerminalWizardLocators.WELCOME_KIT_FEE_INPUT).clear()
                self.page.fill(TerminalWizardLocators.WELCOME_KIT_FEE_INPUT, amount)
                self.logger.info(f"Welcome Kit Fee Amount: Filled with '{amount}'")
                results["fields_filled"]["welcome_kit_fee"] = True
                results["fields_filled"]["welcome_kit_fee_amount"] = amount
            except Exception as e:
                self.logger.warning(f"Welcome Kit Fee: Failed - {e}")
        else:
            self.logger.info("Welcome Kit Fee: Skipped (random decision: No)")
            results["fields_filled"]["welcome_kit_fee"] = False
            results["fields_filled"]["welcome_kit_fee_amount"] = None
        
        self.logger.info(f"Step 3 fields completed. Filled: {[k for k, v in results['fields_filled'].items() if v is not None and v is not False]}")
        return results
    
    def complete_step_3(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Complete Step 3 and navigate to Step 4.
        
        This includes:
        1. Filling all Step 3 fields (with random decisions)
        2. Clicking Next button
        3. Waiting for processing banner
        4. Verifying Step 4 header
        
        Args:
            terminal_config: Dict with terminal configuration
            
        Returns:
            bool: True if successfully moved to Step 4, False otherwise
        """
        # Fill Step 3 fields
        step3_results = self.fill_step_3(terminal_config)
        
        if not step3_results.get("success", False):
            return False
        
        # Click Next button
        self.logger.info("Clicking Next button to proceed to Step 4...")
        
        try:
            next_button = self.page.locator(TerminalWizardLocators.STEP_3_NEXT_BUTTON)
            next_button.scroll_into_view_if_needed()
            next_button.click()
            
            # Wait for processing banner to appear and disappear
            time.sleep(0.5)
            self.wait_for_processing_banner_hidden(timeout=self.LONG_TIMEOUT)
            
            # Verify Step 4 header
            if self.verify_step_header(4, timeout=self.DEFAULT_TIMEOUT):
                self.logger.info("Successfully moved to Step 4")
                return True
            else:
                self.logger.error("Step 4 header not visible after clicking Next")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to complete Step 3: {e}")
            return False
    
    # =========================================================================
    # STEP 4: SELECT TERMINAL APPLICATION
    # =========================================================================
    
    def fill_step_4(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Fill Step 4 of the Terminal Wizard: Select Terminal Application.
        
        This step involves selecting a terminal program from the available list.
        
        Args:
            terminal_config: Dict with step 4 configuration values.
                            Expected key: "terminal_program" (e.g., "VAR / STAGE")
            
        Returns:
            bool: True if successfully filled Step 4
        """
        self.logger.info("=== Step 4: Select Terminal Application ===")
        
        # Verify we're on Step 4
        if not self.verify_step_header(4, timeout=self.SHORT_TIMEOUT):
            self.logger.error("Not on Step 4 - cannot proceed")
            return False
        
        # Get the terminal program to select
        terminal_program = terminal_config.get("terminal_program", "VAR / STAGE")
        
        try:
            # Get the checkbox locator for the specified program
            checkbox_xpath = TerminalWizardLocators.STEP_4_SELECT_TERMINAL_PROGRAM_CHECKBOX(terminal_program)
            
            checkbox = self.page.locator(checkbox_xpath)
            
            # Wait for checkbox to be visible
            checkbox.wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)
            
            # Check if already checked
            if not checkbox.is_checked():
                checkbox.click()
                self.logger.info(f"Terminal Program: Selected '{terminal_program}'")
            else:
                self.logger.info(f"Terminal Program: '{terminal_program}' already selected")
            
            time.sleep(0.3)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to select terminal program '{terminal_program}': {e}")
            return False
    
    def complete_step_4(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Complete Step 4 and navigate to Step 5.
        
        This includes:
        1. Selecting the terminal program checkbox
        2. Clicking Next button
        3. Waiting for processing banner
        4. Verifying Step 5 header
        
        Args:
            terminal_config: Dict with terminal configuration
            
        Returns:
            bool: True if successfully moved to Step 5, False otherwise
        """
        # Fill Step 4 fields
        if not self.fill_step_4(terminal_config):
            return False
        
        # Click Next button
        self.logger.info("Clicking Next button to proceed to Step 5...")
        
        try:
            next_button = self.page.locator(TerminalWizardLocators.STEP_4_NEXT_BUTTON)
            next_button.scroll_into_view_if_needed()
            next_button.click()
            
            # Wait for processing banner to appear and disappear
            time.sleep(0.5)
            self.wait_for_processing_banner_hidden(timeout=self.LONG_TIMEOUT)
            
            # Verify Step 5 header
            if self.verify_step_header(5, timeout=self.DEFAULT_TIMEOUT):
                self.logger.info("Successfully moved to Step 5")
                return True
            else:
                self.logger.error("Step 5 header not visible after clicking Next")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to complete Step 4: {e}")
            return False
    
    # =========================================================================
    # STEP 5: ENTER BILLING / SHIPPING INFORMATION
    # =========================================================================
    
    def complete_step_5(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Complete Step 5 and navigate to Step 6.
        
        Step 5 contains billing/shipping information which is typically
        pre-filled from the application. This method just verifies we're
        on Step 5 and clicks Next to proceed.
        
        Args:
            terminal_config: Dict with terminal configuration (not used for Step 5)
            
        Returns:
            bool: True if successfully moved to Step 6, False otherwise
        """
        self.logger.info("=== Step 5: Enter Billing / Shipping Information ===")
        
        # Verify we're on Step 5
        if not self.verify_step_header(5, timeout=self.SHORT_TIMEOUT):
            self.logger.error("Not on Step 5 - cannot proceed")
            return False
        
        self.logger.info("Step 5: Address details are pre-filled. Proceeding to next step...")
        
        # Click Next button
        self.logger.info("Clicking Next button to proceed to Step 6...")
        
        try:
            next_button = self.page.locator(f"#{TerminalWizardLocators.STEP_5_NEXT}")
            next_button.scroll_into_view_if_needed()
            next_button.click()
            
            # Wait for processing banner to appear and disappear
            time.sleep(0.5)
            self.wait_for_processing_banner_hidden(timeout=self.LONG_TIMEOUT)
            
            # Verify Step 6 header
            if self.verify_step_header(6, timeout=self.DEFAULT_TIMEOUT):
                self.logger.info("Successfully moved to Step 6")
                return True
            else:
                self.logger.error("Step 6 header not visible after clicking Next")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to complete Step 5: {e}")
            return False
    
    # =========================================================================
    # STEP 6: REVIEW AND FINISH
    # =========================================================================
    
    def log_step_6_review_values(self) -> Dict[str, str]:
        """
        Log all review values displayed on Step 6.
        
        Returns:
            Dict with all review field values
        """
        self.logger.info("=== Step 6: Review - Logging all values ===")
        
        review_values = {}
        
        # Define fields to log with their locators
        fields = {
            "Terminal": TerminalWizardLocators.STEP_6_TERMINAL_VALUE,
            "Serial Number (S/N)": TerminalWizardLocators.STEP_6_SERIAL_NUMBER_VALUE,
            "Total Sales Price": TerminalWizardLocators.STEP_6_TOTAL_SALES_PRICE_VALUE,
            "Ship Method": TerminalWizardLocators.STEP_6_SHIP_METHOD_VALUE,
            "Bill To": TerminalWizardLocators.STEP_6_BILL_TO_VALUE,
            "Ship To": TerminalWizardLocators.STEP_6_SHIP_TO_VALUE,
            "Contact": TerminalWizardLocators.STEP_6_CONTACT_VALUE,
        }
        
        for field_name, locator in fields.items():
            try:
                element = self.page.locator(locator)
                if element.is_visible(timeout=2000):
                    value = element.text_content() or ""
                    value = value.strip()
                    review_values[field_name] = value
                    self.logger.info(f"  {field_name}: {value if value else '(empty)'}")
                else:
                    review_values[field_name] = "(not visible)"
                    self.logger.info(f"  {field_name}: (not visible)")
            except Exception as e:
                review_values[field_name] = f"(error: {e})"
                self.logger.warning(f"  {field_name}: Failed to read - {e}")
        
        return review_values
    
    def complete_step_6(self, terminal_config: Dict[str, Any], equipment_before: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Complete Step 6 (Review) and finish the wizard.
        
        This is the final step that:
        1. Logs all review values
        2. Clicks Finish button
        3. Waits for processing (may take several minutes)
        4. Verifies terminal was added by checking Equipment Table
        
        Args:
            terminal_config: Dict with terminal configuration
            equipment_before: Equipment list captured before adding (for verification)
            
        Returns:
            Dict with:
                - success: bool
                - review_values: Dict of all review values
                - terminals_before: List of terminals before adding
                - terminals_after: List of terminals after adding
                - newly_added: List of newly added terminals
                - total_count: Total terminals after adding
        """
        self.logger.info("=== Step 6: Review and Finish ===")
        
        terminal_name = terminal_config.get("name", "Unknown")
        
        result = {
            "success": False,
            "review_values": {},
            "terminals_before": equipment_before.get("terminals", []) if equipment_before else [],
            "terminals_after": [],
            "newly_added": [],
            "total_count": 0
        }
        
        # Verify we're on Step 6
        if not self.verify_step_header(6, timeout=self.SHORT_TIMEOUT):
            self.logger.error("Not on Step 6 - cannot proceed")
            return result
        
        # Log all review values
        result["review_values"] = self.log_step_6_review_values()
        
        # Click Finish button
        self.logger.info("Clicking Finish button to complete the wizard...")
        self.logger.info("(This may take several minutes while processing...)")
        
        try:
            finish_button = self.page.locator(TerminalWizardLocators.STEP_6_FINISH_BUTTON)
            finish_button.scroll_into_view_if_needed()
            finish_button.click()
            
            # Wait for processing banner - this can take several minutes
            time.sleep(1)
            self.logger.info("Waiting for processing to complete...")
            
            # Use longer timeout for final step processing (up to 5 minutes)
            FINISH_TIMEOUT = 300000  # 5 minutes in ms
            self.wait_for_processing_banner_hidden(timeout=FINISH_TIMEOUT)
            
            # Verify terminal was added by checking Equipment Table
            self.logger.info("Processing complete. Verifying terminal in Equipment Table...")
            
            # Use equipment_before if provided, otherwise use empty list
            if equipment_before is None:
                equipment_before = {"terminals": [], "count": 0, "has_equipment": False}
            
            verification = self.verify_terminal_added(terminal_name, equipment_before)
            
            result["success"] = verification["success"]
            result["terminals_before"] = verification["terminals_before"]
            result["terminals_after"] = verification["terminals_after"]
            result["newly_added"] = verification["newly_added"]
            result["total_count"] = verification["total_count"]
            
            if result["success"]:
                self.logger.info("=" * 60)
                self.logger.info(f"{SYMBOL_CHECK} TERMINAL '{terminal_name}' ADDED SUCCESSFULLY!")
                self.logger.info(f"Total Terminals: {result['total_count']}")
                self.logger.info(f"Newly Added: {result['newly_added']}")
                self.logger.info("=" * 60)
            else:
                self.logger.error(f"{SYMBOL_CROSS} Terminal '{terminal_name}' verification FAILED")
                
        except Exception as e:
            self.logger.error(f"Failed to complete Step 6: {e}")
        
        return result
    
    # =========================================================================
    # FULL WIZARD FLOW - ALL 6 STEPS
    # =========================================================================
    
    def add_terminal_complete(self, terminal_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete the entire Terminal Wizard (all 6 steps).
        
        This method:
        1. Captures equipment list BEFORE starting
        2. Opens the Terminal Wizard
        3. Completes Step 1 (Select Type) → Step 2
        4. Completes Step 2 (Select Part) → Step 3
        5. Completes Step 3 (Enter Part Details) → Step 4
        6. Completes Step 4 (Select Terminal Application) → Step 5
        7. Completes Step 5 (Billing/Shipping - pre-filled) → Step 6
        8. Completes Step 6 (Review) → Finish
        9. Verifies terminal in Equipment Table
        
        Args:
            terminal_config: Terminal configuration dict with all step data.
            
        Returns:
            Dict with all step results, equipment tracking, and final outcome:
                - step1-step6: bool for each step
                - success: bool overall success
                - review_values: Dict of review values from Step 6
                - terminals_before: List of terminals before adding
                - terminals_after: List of terminals after adding
                - newly_added: List of newly added terminals
                - total_count: Total terminals after adding
        """
        terminal_name = terminal_config.get("name", "Unknown Terminal")
        results = {
            "step1": False, 
            "step2": False, 
            "step3": False,
            "step4": False,
            "step5": False,
            "step6": False,
            "success": False,
            "review_values": {},
            "terminals_before": [],
            "terminals_after": [],
            "newly_added": [],
            "total_count": 0
        }
        
        self.logger.info("=" * 60)
        self.logger.info(f"STARTING TERMINAL WIZARD (FULL): {terminal_name}")
        self.logger.info(f"Terminal Config: {terminal_config}")
        self.logger.info("=" * 60)
        
        # CAPTURE EQUIPMENT LIST BEFORE STARTING
        self.logger.info("Capturing Equipment Table state BEFORE adding terminal...")
        equipment_before = self.get_equipment_list()
        results["terminals_before"] = equipment_before.get("terminals", [])
        self.logger.info(f"Equipment Before: {results['terminals_before']} (count: {len(results['terminals_before'])})")
        
        # Open the wizard
        if not self.open_terminal_wizard():
            return results
        
        # Complete Step 1 and move to Step 2
        if not self.complete_step_1(terminal_config):
            return results
        results["step1"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 1 completed for '{terminal_name}' - now on Step 2")
        
        # Complete Step 2 and move to Step 3
        if not self.complete_step_2(terminal_config):
            return results
        results["step2"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 2 completed for '{terminal_name}' - now on Step 3")
        
        # Complete Step 3 and move to Step 4
        if not self.complete_step_3(terminal_config):
            return results
        results["step3"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 3 completed for '{terminal_name}' - now on Step 4")
        
        # Complete Step 4 and move to Step 5
        if not self.complete_step_4(terminal_config):
            return results
        results["step4"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 4 completed for '{terminal_name}' - now on Step 5")
        
        # Complete Step 5 and move to Step 6
        if not self.complete_step_5(terminal_config):
            return results
        results["step5"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 5 completed for '{terminal_name}' - now on Step 6")
        
        # Complete Step 6 (Review) and finish - pass equipment_before for verification
        step6_result = self.complete_step_6(terminal_config, equipment_before=equipment_before)
        results["step6"] = step6_result["success"]
        results["success"] = step6_result["success"]
        results["review_values"] = step6_result["review_values"]
        results["terminals_after"] = step6_result.get("terminals_after", [])
        results["newly_added"] = step6_result.get("newly_added", [])
        results["total_count"] = step6_result.get("total_count", 0)
        
        if step6_result["success"]:
            self.logger.info(f"{SYMBOL_CHECK} Step 6 completed for '{terminal_name}' - Terminal Added!")
        else:
            self.logger.error(f"{SYMBOL_CROSS} Step 6 failed for '{terminal_name}'")
        
        return results

    # =========================================================================
    # LEGACY METHODS (for backward compatibility)
    # =========================================================================
    
    def add_terminal_steps_1_3(self, terminal_config: Dict[str, Any]) -> Dict[str, bool]:
        """
        Open wizard and complete Steps 1, 2, and 3.
        
        This method:
        1. Opens the Terminal Wizard
        2. Completes Step 1 (Select Type) and moves to Step 2
        3. Completes Step 2 (Select Part) and moves to Step 3
        4. Completes Step 3 (Enter Part Details) and moves to Step 4
        
        Args:
            terminal_config: Terminal configuration dict with all step data.
            
        Returns:
            Dict with step results: {"step1": bool, "step2": bool, "step3": bool}
        """
        terminal_name = terminal_config.get("name", "Unknown Terminal")
        results = {"step1": False, "step2": False, "step3": False}
        
        self.logger.info("=" * 60)
        self.logger.info(f"STARTING TERMINAL WIZARD: {terminal_name}")
        self.logger.info(f"Terminal Config: {terminal_config}")
        self.logger.info("=" * 60)
        
        # Open the wizard
        if not self.open_terminal_wizard():
            return results
        
        # Complete Step 1 and move to Step 2
        if not self.complete_step_1(terminal_config):
            return results
        
        results["step1"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 1 completed for '{terminal_name}' - now on Step 2")
        
        # Complete Step 2 and move to Step 3
        if not self.complete_step_2(terminal_config):
            return results
        
        results["step2"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 2 completed for '{terminal_name}' - now on Step 3")
        
        # Complete Step 3 and move to Step 4
        if not self.complete_step_3(terminal_config):
            return results
        
        results["step3"] = True
        self.logger.info(f"{SYMBOL_CHECK} Step 3 completed for '{terminal_name}' - now on Step 4")
        
        return results
    
    def add_terminals(self, terminals_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple terminals from a list of configurations.
        
        This method runs the COMPLETE 6-step wizard for each terminal.
        
        Args:
            terminals_list: List of terminal configuration dicts
            
        Returns:
            Dict with results:
                - success_count: Number of terminals successfully added
                - failed_count: Number of terminals that failed
                - results: Dict of individual results by terminal name
                - added_terminals: List of successfully added terminal configs
        """
        self.logger.info("=" * 60)
        self.logger.info(f"ADDING {len(terminals_list)} TERMINAL(S) - FULL WIZARD")
        self.logger.info("=" * 60)
        
        results = {}
        success_count = 0
        failed_count = 0
        
        for idx, terminal_config in enumerate(terminals_list, 1):
            terminal_name = terminal_config.get("name", f"Terminal_{idx}")
            
            self.logger.info(f"\n--- Adding Terminal {idx}/{len(terminals_list)}: {terminal_name} ---")
            
            # Run complete wizard (all 6 steps)
            step_results = self.add_terminal_complete(terminal_config)
            
            if step_results["success"]:
                success_count += 1
                results[terminal_name] = {
                    "step1": step_results["step1"], 
                    "step2": step_results["step2"],
                    "step3": step_results["step3"],
                    "step4": step_results["step4"],
                    "step5": step_results["step5"],
                    "step6": step_results["step6"],
                    "status": "completed",
                    "review_values": step_results["review_values"],
                    "terminals_before": step_results.get("terminals_before", []),
                    "terminals_after": step_results.get("terminals_after", []),
                    "newly_added": step_results.get("newly_added", []),
                    "total_count": step_results.get("total_count", 0)
                }
                
                # Track successfully added terminal
                add_to_added_terminals(terminal_config, terminal_name)
                
                self.logger.info(f"{SYMBOL_CHECK} Terminal '{terminal_name}' added successfully!")
            else:
                failed_count += 1
                # Determine which step failed
                failed_step = "Step 1"
                if step_results["step1"]:
                    failed_step = "Step 2"
                if step_results["step2"]:
                    failed_step = "Step 3"
                if step_results["step3"]:
                    failed_step = "Step 4"
                if step_results["step4"]:
                    failed_step = "Step 5"
                if step_results["step5"]:
                    failed_step = "Step 6"
                    
                results[terminal_name] = {
                    "step1": step_results["step1"], 
                    "step2": step_results["step2"],
                    "step3": step_results["step3"],
                    "step4": step_results["step4"],
                    "step5": step_results["step5"],
                    "step6": step_results["step6"],
                    "status": "failed",
                    "failed_at": failed_step
                }
                self.logger.error(f"{SYMBOL_CROSS} Terminal '{terminal_name}' failed at {failed_step}")
                
                # Try to cancel wizard if it's still open
                self.cancel_wizard()
        
        self.logger.info("=" * 60)
        self.logger.info(f"TERMINAL ADDITION COMPLETE: {success_count}/{len(terminals_list)} successful")
        self.logger.info("=" * 60)
        
        return {
            "success_count": success_count,
            "failed_count": failed_count,
            "results": results,
            "added_terminals": get_added_terminals(),
        }
    
    def cancel_wizard(self) -> bool:
        """
        Cancel and close the wizard at any step.
        
        Returns:
            bool: True if wizard closed successfully
        """
        self.logger.info("Canceling Terminal Wizard...")
        
        cancel_buttons = [
            TerminalWizardLocators.STEP_1_CANCEL_BUTTON,
            TerminalWizardLocators.STEP_2_CANCEL_BUTTON,
            TerminalWizardLocators.STEP_3_CANCEL_BUTTON,
            TerminalWizardLocators.STEP_4_CANCEL_BUTTON,
            f"#{TerminalWizardLocators.STEP_5_CANCEL}",  # ID without # prefix in locator
            TerminalWizardLocators.STEP_6_CANCEL_BUTTON,
        ]
        
        for cancel_btn in cancel_buttons:
            try:
                btn_locator = self.page.locator(cancel_btn)
                if btn_locator.is_visible(timeout=1000):
                    btn_locator.click()
                    time.sleep(0.5)
                    self.logger.info("Wizard cancelled successfully")
                    return True
            except Exception:
                continue
        
        self.logger.warning("Could not find cancel button to close wizard")
        return False
