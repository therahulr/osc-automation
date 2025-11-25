"""
OSC Wizard Helpers - Reusable utilities for multi-step wizards
"""

from playwright.sync_api import Page, TimeoutError
from typing import Dict, Any, Optional, List, Callable
import time
import re

from pages.osc.base_page import OSCBasePage


class WizardNavigator(OSCBasePage):
    """
    Helper class for navigating multi-step wizards in OSC.
    
    Handles common wizard patterns:
    - Step tracking
    - Next/Previous navigation
    - Step validation
    - Modal-based wizards
    """
    
    def __init__(self, page: Page, wizard_config: Dict[str, Any] = None):
        """
        Initialize wizard navigator.
        
        Args:
            page: Playwright page object
            wizard_config: Optional configuration dict with:
                - modal_selector: XPath/CSS for the wizard modal
                - step_header_pattern: Pattern to extract current step (e.g., "Step {n} of {total}")
                - next_button: Selector for next button
                - previous_button: Selector for previous button
                - finish_button: Selector for finish button
                - processing_indicator: Selector for "Processing..." indicator
        """
        super().__init__(page)
        self.config = wizard_config or {}
        self._current_step = 1
        self._total_steps = 0
    
    @property
    def current_step(self) -> int:
        """Get current wizard step number."""
        return self._current_step
    
    @property
    def total_steps(self) -> int:
        """Get total number of wizard steps."""
        return self._total_steps
    
    def detect_current_step(self, step_header_selector: str = None, 
                            pattern: str = r"Step\s+(\d+)\s+of\s+(\d+)") -> tuple:
        """
        Detect the current step from the step header text.
        
        Args:
            step_header_selector: Selector for the step header element
            pattern: Regex pattern to extract step numbers
            
        Returns:
            tuple: (current_step, total_steps) or (0, 0) if not found
        """
        if not step_header_selector:
            step_header_selector = self.config.get("step_header_selector", "//h4[contains(text(),'Step')]")
        
        try:
            header_text = self.page.locator(step_header_selector).text_content()
            match = re.search(pattern, header_text)
            
            if match:
                self._current_step = int(match.group(1))
                self._total_steps = int(match.group(2))
                self.logger.info(f"Wizard: Step {self._current_step} of {self._total_steps}")
                return (self._current_step, self._total_steps)
            
        except Exception as e:
            self.logger.warning(f"Could not detect wizard step: {e}")
        
        return (0, 0)
    
    def wait_for_step_loaded(self, step_indicator_selector: str, timeout: int = None) -> bool:
        """
        Wait for a specific wizard step to load.
        
        Args:
            step_indicator_selector: Selector for an element unique to this step
            timeout: Maximum wait time in ms
            
        Returns:
            bool: True if step loaded, False otherwise
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        return self.wait_for_element(step_indicator_selector, timeout=timeout, state="visible")
    
    def wait_for_processing_complete(self, processing_selector: str = None, 
                                      timeout: int = None) -> bool:
        """
        Wait for "Processing..." indicator to disappear.
        
        Args:
            processing_selector: Selector for the processing indicator
            timeout: Maximum wait time in ms
            
        Returns:
            bool: True if processing completed, False if timeout
        """
        processing_selector = processing_selector or self.config.get(
            "processing_indicator", 
            "//div[contains(@class,'alert-success') and contains(text(),'Processing')]"
        )
        timeout = timeout or self.LONG_TIMEOUT
        
        try:
            # First check if processing indicator appears
            self.page.wait_for_selector(processing_selector, timeout=2000, state="visible")
            self.logger.info("Processing started...")
            
            # Now wait for it to disappear
            self.page.wait_for_selector(processing_selector, timeout=timeout, state="hidden")
            self.logger.info("Processing completed")
            return True
            
        except TimeoutError:
            # Processing might complete before we can detect it
            if not self.page.locator(processing_selector).is_visible():
                return True
            self.logger.warning("Processing timed out")
            return False
    
    def click_next(self, next_button_selector: str = None, 
                   wait_for_next_step: str = None) -> bool:
        """
        Click the Next button and optionally wait for next step.
        
        Args:
            next_button_selector: Selector for the Next button
            wait_for_next_step: Selector for an element on the next step
            
        Returns:
            bool: True if successful
        """
        next_button = next_button_selector or self.config.get("next_button")
        
        if not next_button:
            self.logger.error("No next button selector provided")
            return False
        
        if not self.click_button(next_button, "Next"):
            return False
        
        self._current_step += 1
        
        if wait_for_next_step:
            return self.wait_for_step_loaded(wait_for_next_step)
        
        return True
    
    def click_previous(self, previous_button_selector: str = None) -> bool:
        """Click the Previous button."""
        prev_button = previous_button_selector or self.config.get("previous_button")
        
        if not prev_button:
            self.logger.error("No previous button selector provided")
            return False
        
        if self.click_button(prev_button, "Previous"):
            self._current_step -= 1
            return True
        
        return False
    
    def click_finish(self, finish_button_selector: str = None, 
                     wait_for_close: bool = True) -> bool:
        """
        Click the Finish button to complete the wizard.
        
        Args:
            finish_button_selector: Selector for the Finish button
            wait_for_close: Wait for wizard modal to close
            
        Returns:
            bool: True if wizard completed successfully
        """
        finish_button = finish_button_selector or self.config.get("finish_button")
        
        if not finish_button:
            self.logger.error("No finish button selector provided")
            return False
        
        if not self.click_button(finish_button, "Finish"):
            return False
        
        if wait_for_close:
            modal_selector = self.config.get("modal_selector")
            if modal_selector:
                return self.wait_for_element(modal_selector, state="hidden")
        
        self.logger.info("Wizard completed successfully")
        return True
    
    def execute_step(self, step_number: int, step_action: Callable, 
                     step_indicator: str = None) -> bool:
        """
        Execute a wizard step with validation.
        
        Args:
            step_number: Expected step number
            step_action: Callable that performs the step actions
            step_indicator: Selector to verify correct step is loaded
            
        Returns:
            bool: True if step executed successfully
        """
        # Verify we're on the correct step
        if step_indicator:
            if not self.wait_for_step_loaded(step_indicator):
                self.logger.error(f"Step {step_number} indicator not found")
                return False
        
        current, _ = self.detect_current_step()
        if current != 0 and current != step_number:
            self.logger.warning(f"Expected step {step_number}, but on step {current}")
        
        try:
            result = step_action()
            if result:
                self.logger.info(f"Step {step_number} completed successfully")
            else:
                self.logger.error(f"Step {step_number} failed")
            return result
            
        except Exception as e:
            self.logger.error(f"Step {step_number} error: {e}")
            return False


class TerminalWizard(WizardNavigator):
    """
    Specialized helper for OSC Terminal Wizard (6-step equipment selection).
    """
    
    def __init__(self, page: Page):
        # Terminal Wizard specific configuration
        config = {
            "modal_selector": "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard']",
            "processing_indicator": "//div[contains(@class,'alert-success') and normalize-space(text())='Processing...']",
            "step_header_selector": "//h4[contains(text(),'Step')]"
        }
        super().__init__(page, config)
        self._total_steps = 6
    
    def open_wizard(self, wizard_button_selector: str = None) -> bool:
        """Open the Terminal Wizard modal."""
        button = wizard_button_selector or "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_aTerminalWizard"
        
        if self.click_button(button, "Terminal Wizard"):
            return self.wait_for_element(self.config["modal_selector"])
        return False
    
    def select_part_type(self, part_type: str, dropdown_selector: str = None) -> bool:
        """Step 1: Select the part type from dropdown."""
        dropdown = dropdown_selector or "//select[contains(@id,'ddlPartType')]"
        return self.select_dropdown_by_text(dropdown, part_type, "Part Type")
    
    def select_equipment_by_part_id(self, part_id: str, equipment_grid_selector: str = None) -> bool:
        """
        Select equipment by Part ID in the equipment grid.
        
        Args:
            part_id: The Part ID to select
            equipment_grid_selector: Optional custom grid selector
            
        Returns:
            bool: True if equipment selected successfully
        """
        grid = equipment_grid_selector or (
            "//table[@id='ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_TerminalWizard_TerminalGrid']"
        )
        
        checkbox_xpath = (
            f"{grid}//tr[td[2][normalize-space(text())='{part_id}']]"
            f"//input[contains(@id,'ckbSelectedPart')]"
        )
        
        return self.check_checkbox(checkbox_xpath, f"Equipment {part_id}")
    
    def click_step_next(self, step_number: int, next_button_id: str = None) -> bool:
        """Click next button for a specific step."""
        # Terminal Wizard uses dynamic button IDs based on step
        if not next_button_id:
            next_button_id = f"//input[contains(@id,'btnNext')]"
        
        return self.click_next(next_button_id)
    
    def complete_step_1(self, part_type: str) -> bool:
        """Complete Step 1: Select Type."""
        self.logger.info("Terminal Wizard Step 1: Select Type")
        if not self.select_part_type(part_type):
            return False
        return self.click_step_next(1)
    
    def complete_step_2(self, part_ids: List[str]) -> bool:
        """Complete Step 2: Select Equipment."""
        self.logger.info("Terminal Wizard Step 2: Select Equipment")
        
        for part_id in part_ids:
            if not self.select_equipment_by_part_id(part_id):
                return False
        
        return self.click_step_next(2)


class AddOnWizard(WizardNavigator):
    """
    Specialized helper for OSC Add-on Wizard.
    """
    
    def __init__(self, page: Page):
        config = {
            "modal_selector": "//div[contains(@class,'modal') and .//h4[contains(text(),'Add-on')]]",
            "step_header_selector": "//h4[contains(text(),'Step')]"
        }
        super().__init__(page, config)
    
    def open_wizard(self, addon_button_selector: str = None) -> bool:
        """Open the Add-on Wizard modal."""
        button = addon_button_selector or "#ctl00_ContentPlaceHolder1_ctrlApplicationEquipment21_aAddOnWizard"
        
        if self.click_button(button, "Add-on Wizard"):
            return self.wait_for_element(self.config["modal_selector"])
        return False
    
    def select_addon_type(self, addon_type: str, dropdown_selector: str = None) -> bool:
        """Select the add-on type."""
        dropdown = dropdown_selector or "//select[contains(@id,'ddlAddOnType')]"
        return self.select_dropdown_by_text(dropdown, addon_type, "Add-on Type")
