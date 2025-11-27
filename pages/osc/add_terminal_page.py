"""
Add Terminal Wizard Page - Handles Terminal Wizard multi-step automation.

This module provides functions for adding terminals through the 6-step wizard.
Each step is handled with proper wait strategies, verification, and retry logic.
"""

from playwright.sync_api import Page, TimeoutError
from typing import Dict, Any, Optional, List
import time

from core.logger import get_logger
from locators.osc_locators import TerminalWizardLocators
from data.osc.add_terminal_data import (
    add_to_added_terminals,
    get_added_terminals,
    clear_added_terminals,
)


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
            # Steps 5 and 6 can be added as needed
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
        
        # Wait for provider dropdown to update (may reload based on part type)
        time.sleep(0.5)
        
        # Step 1b: Select Provider
        if not self.select_dropdown_by_label(
            TerminalWizardLocators.STEP_1_PROVIDER_DROPDOWN,
            provider,
            "Provider"
        ):
            return False
        
        # Wait a moment
        time.sleep(0.3)
        
        # Step 1c: Select Part Condition
        if not self.select_dropdown_by_label(
            TerminalWizardLocators.STEP_1_PART_CONDITION_DROPDOWN,
            part_condition,
            "Part Condition"
        ):
            return False
        
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
    # FULL WIZARD FLOW (Step 1 only for now)
    # =========================================================================
    
    def add_terminal_step_1(self, terminal_config: Dict[str, Any]) -> bool:
        """
        Open wizard and complete Step 1.
        
        This is the main entry point for adding a terminal through Step 1.
        
        Args:
            terminal_config: Terminal configuration dict with all step data.
            
        Returns:
            bool: True if Step 1 completed successfully, False otherwise
        """
        terminal_name = terminal_config.get("name", "Unknown Terminal")
        
        self.logger.info("=" * 60)
        self.logger.info(f"STARTING TERMINAL WIZARD - STEP 1: {terminal_name}")
        self.logger.info(f"Terminal Config: {terminal_config}")
        self.logger.info("=" * 60)
        
        # Open the wizard
        if not self.open_terminal_wizard():
            return False
        
        # Complete Step 1 and move to Step 2
        if not self.complete_step_1(terminal_config):
            return False
        
        self.logger.info(f"Terminal Wizard Step 1 completed successfully for '{terminal_name}' - now on Step 2")
        return True
    
    def add_terminals(self, terminals_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple terminals from a list of configurations.
        
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
        self.logger.info(f"ADDING {len(terminals_list)} TERMINAL(S)")
        self.logger.info("=" * 60)
        
        results = {}
        success_count = 0
        failed_count = 0
        
        for idx, terminal_config in enumerate(terminals_list, 1):
            terminal_name = terminal_config.get("name", f"Terminal_{idx}")
            
            self.logger.info(f"\n--- Adding Terminal {idx}/{len(terminals_list)}: {terminal_name} ---")
            
            # Run Step 1
            step1_success = self.add_terminal_step_1(terminal_config)
            
            if step1_success:
                success_count += 1
                results[terminal_name] = {"step1": True, "status": "step1_complete"}
                
                # Track successfully added terminal
                add_to_added_terminals(terminal_config, terminal_name)
                
                self.logger.info(f"✓ Terminal '{terminal_name}' Step 1 completed")
                
                # Cancel wizard for now (since only Step 1 is implemented)
                self.cancel_wizard()
            else:
                failed_count += 1
                results[terminal_name] = {"step1": False, "status": "failed"}
                self.logger.error(f"✗ Terminal '{terminal_name}' Step 1 failed")
                
                # Try to cancel wizard if it's open
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
            TerminalWizardLocators.STEP_5_CANCEL,
            TerminalWizardLocators.STEP_6_CANCEL_BUTTON,
        ]
        
        for cancel_btn in cancel_buttons:
            try:
                if self.page.locator(cancel_btn).is_visible():
                    self.page.click(cancel_btn)
                    time.sleep(0.5)
                    self.logger.info("Wizard cancelled successfully")
                    return True
            except Exception:
                continue
        
        self.logger.warning("Could not find cancel button to close wizard")
        return False
