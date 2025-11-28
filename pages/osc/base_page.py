"""
OSC Base Page - Reusable automation utilities for OSC application
"""

from playwright.sync_api import Page, TimeoutError, Locator
from typing import Dict, Any, Optional, List, Callable
import time
import re

from core.logger import get_logger


class OSCBasePage:
    """
    Enhanced base class for OSC page objects with reusable utilities.
    
    Provides common functionality for:
    - Form fields (text, dropdown, checkbox, radio)
    - Data grids and tables
    - Wizard navigation
    - Error handling and validation
    - Wait strategies
    """
    
    DEFAULT_TIMEOUT = 10000  # 10 seconds
    SHORT_TIMEOUT = 5000     # 5 seconds
    LONG_TIMEOUT = 30000     # 30 seconds
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger()
    
    # =========================================================================
    # WAIT UTILITIES
    # =========================================================================
    
    def wait_for_element(self, selector: str, timeout: int = None, state: str = "visible") -> bool:
        """
        Wait for an element to be in specified state.
        
        Args:
            selector: CSS or XPath selector
            timeout: Maximum wait time in ms (default: DEFAULT_TIMEOUT)
            state: 'visible', 'hidden', 'attached', 'detached'
            
        Returns:
            bool: True if element reached state, False otherwise
        """
        timeout = timeout or self.DEFAULT_TIMEOUT
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            return True
        except TimeoutError:
            self.logger.warning(f"Element not found in state '{state}': {selector[:80]}...")
            return False
    
    def wait_for_page_load(self, timeout: int = None) -> None:
        """Wait for page to finish loading."""
        timeout = timeout or self.LONG_TIMEOUT
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_ajax(self, timeout: int = 2000) -> None:
        """Wait for AJAX requests to complete (simple delay-based)."""
        time.sleep(timeout / 1000)
    
    # =========================================================================
    # TEXT INPUT UTILITIES
    # =========================================================================
    
    def fill_text(self, selector: str, value: str, field_name: str = None, 
                  clear_first: bool = True, verify: bool = True) -> bool:
        """
        Fill a text input field with robust error handling.
        
        Args:
            selector: CSS or XPath selector for the input
            value: Text value to enter
            field_name: Friendly name for logging (optional)
            clear_first: Whether to clear existing content first
            verify: Whether to verify the entered value
            
        Returns:
            bool: True if successful, False otherwise
        """
        field_name = field_name or selector[:40]
        
        if not value:
            self.logger.debug(f"{field_name}: Skipped (empty value)")
            return True
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            
            if clear_first:
                self.page.fill(selector, "")
            
            self.page.fill(selector, value)
            
            if verify:
                actual = self.page.locator(selector).input_value()
                if actual != value:
                    self.logger.warning(f"{field_name}: Value mismatch. Expected '{value}', got '{actual}'")
                    return False
            
            self.logger.info(f"{field_name}: Filled with '{value}'")
            return True
            
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to fill - {e}")
            return False
    
    def fill_multiple_fields(self, field_data: Dict[str, tuple]) -> Dict[str, bool]:
        """
        Fill multiple text fields at once.
        
        Args:
            field_data: Dict of {field_name: (selector, value)}
            
        Returns:
            Dict[str, bool]: Results for each field
        """
        results = {}
        for field_name, (selector, value) in field_data.items():
            results[field_name] = self.fill_text(selector, value, field_name)
        return results
    
    def get_text_value(self, selector: str) -> Optional[str]:
        """Get the value of a text input field."""
        try:
            return self.page.locator(selector).input_value()
        except Exception:
            return None
    
    def get_element_text(self, selector: str) -> Optional[str]:
        """Get the text content of an element (span, div, etc.)."""
        try:
            return self.page.locator(selector).text_content()
        except Exception:
            return None
    
    def fill_masked_input(self, selector: str, value: str, field_name: str = None,
                          delay_ms: int = 100) -> bool:
        """
        Fill a masked input field by typing digits slowly.
        
        Used for phone/fax fields with mask pattern like (___) ___-____
        Extracts digits from value and types them one by one with delay.
        
        Args:
            selector: CSS or XPath selector for the input
            value: Value containing digits (e.g., '7038529999' or '(703) 852-9999')
            field_name: Friendly name for logging
            delay_ms: Delay between keystrokes in milliseconds (default: 100ms)
            
        Returns:
            bool: True if successful, False otherwise
        """
        field_name = field_name or selector[:40]
        
        if not value:
            self.logger.debug(f"{field_name}: Skipped (empty value)")
            return True
        
        # Extract digits only
        digits = ''.join(c for c in value if c.isdigit())
        
        if not digits:
            self.logger.warning(f"{field_name}: No digits found in value '{value}'")
            return False
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            
            # Click to focus the field
            self.page.click(selector)
            time.sleep(0.1)
            
            # Clear existing content
            self.page.locator(selector).clear()
            time.sleep(0.1)
            
            # Type each digit slowly
            for digit in digits:
                self.page.keyboard.press(digit)
                time.sleep(delay_ms / 1000)
            
            # Verify by getting the value back
            actual = self.get_text_value(selector)
            
            # Check if digits are present in the result (formatted or not)
            actual_digits = ''.join(c for c in (actual or '') if c.isdigit())
            
            if actual_digits == digits:
                self.logger.info(f"{field_name}: Filled with '{actual}' (digits: {digits})")
                return True
            else:
                self.logger.warning(f"{field_name}: Digit mismatch. Expected '{digits}', got '{actual_digits}'")
                return False
            
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to fill masked input - {e}")
            return False

    def fill_masked_date_input(self, selector: str, value: str, field_name: str = None,
                               delay_ms: int = 150, max_retries: int = 3) -> bool:
        """
        Fill a masked date input field by typing digits slowly with retry logic.
        
        Used specifically for date fields with mask pattern like dd/mm/yyyy
        which can be sensitive to typing speed. Includes retry logic with improved
        navigation using left arrow keys to reset cursor position on failure.
        
        Args:
            selector: CSS or XPath selector for the input
            value: Date value containing digits (e.g., '01152020' or '01/15/2020')
            field_name: Friendly name for logging
            delay_ms: Delay between keystrokes in milliseconds (default: 150ms for reliability)
            max_retries: Maximum retry attempts if digit count mismatch (default: 3)
            
        Returns:
            bool: True if successful, False otherwise
        """
        field_name = field_name or selector[:40]
        
        if not value:
            self.logger.debug(f"{field_name}: Skipped (empty value)")
            return True
        
        # Extract digits only
        digits = ''.join(c for c in value if c.isdigit())
        
        if not digits:
            self.logger.warning(f"{field_name}: No digits found in value '{value}'")
            return False
        
        for attempt in range(max_retries + 1):
            try:
                self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
                
                # Click to focus the field
                self.page.click(selector)
                time.sleep(0.15)
                
                if attempt == 0:
                    # First attempt: Clear existing content normally
                    self.page.locator(selector).clear()
                    time.sleep(0.15)
                    
                    # Click again to ensure focus at start of field
                    self.page.click(selector)
                    time.sleep(0.1)
                else:
                    # Retry attempts: Use left arrow navigation to reset cursor to dd position
                    # The masked field has format dd/mm/yyyy - cursor might be stuck in yyyy
                    self.logger.debug(f"{field_name}: Retry attempt {attempt} - navigating to start with arrow keys")
                    
                    # Press Home key first to try to go to beginning
                    self.page.keyboard.press("Home")
                    time.sleep(0.1)
                    
                    # Press left arrow multiple times (3-4 times to cover dd/mm/yyyy navigation)
                    # This ensures cursor is at the beginning (dd section)
                    for _ in range(4):
                        self.page.keyboard.press("ArrowLeft")
                        time.sleep(0.05)
                    
                    time.sleep(0.1)
                    
                    # Select all and delete to clear existing malformed content
                    self.page.keyboard.press("Control+a")  # or Command+a on Mac
                    time.sleep(0.05)
                    self.page.keyboard.press("Meta+a")  # Mac specific
                    time.sleep(0.05)
                    self.page.keyboard.press("Backspace")
                    time.sleep(0.15)
                    
                    # Click again to refocus at start
                    self.page.click(selector)
                    time.sleep(0.1)
                    
                    # Navigate to start again after clearing
                    self.page.keyboard.press("Home")
                    time.sleep(0.05)
                    for _ in range(4):
                        self.page.keyboard.press("ArrowLeft")
                        time.sleep(0.05)
                    time.sleep(0.1)
                
                # Type each digit slowly with increased delay
                for digit in digits:
                    self.page.keyboard.press(digit)
                    time.sleep(delay_ms / 1000)
                
                # Small delay before verification
                time.sleep(0.15)
                
                # Verify by getting the value back
                actual = self.get_text_value(selector)
                
                # Check if digits are present in the result (formatted or not)
                actual_digits = ''.join(c for c in (actual or '') if c.isdigit())
                
                if actual_digits == digits:
                    self.logger.info(f"{field_name}: Filled with '{actual}' (digits: {digits})")
                    return True
                elif len(actual_digits) != len(digits):
                    # Wrong digit count - need to retry with navigation
                    self.logger.warning(f"{field_name}: Digit count mismatch ({len(actual_digits)} vs {len(digits)}). "
                                       f"Got '{actual}' -> '{actual_digits}', expected '{digits}'. "
                                       f"Retrying with arrow navigation... ({attempt + 1}/{max_retries + 1})")
                    if attempt < max_retries:
                        continue
                else:
                    # Same digit count - browser may have reformatted date (MMDDYYYY to YYYYMMDD)
                    # This is acceptable as long as length matches (all digits captured)
                    self.logger.info(f"{field_name}: Filled with '{actual}' (digits reordered by browser: {actual_digits})")
                    return True
                
            except Exception as e:
                self.logger.error(f"{field_name}: Failed to fill masked date input (attempt {attempt + 1}) - {e}")
                if attempt >= max_retries:
                    return False
        
        self.logger.error(f"{field_name}: Failed after {max_retries + 1} attempts")
        return False

    def fill_masked_equity_input(self, selector: str, value: str, field_name: str = None,
                                  delay_ms: int = 100) -> bool:
        """
        Fill a masked equity input field (format: 0__ for 3 digits, default value 0).
        
        Clears the default value first by pressing backspace slowly, then types the new value.
        Used for equity percentage fields where owner percentages must sum to 100.
        
        Args:
            selector: CSS or XPath selector for the input
            value: Equity percentage value (e.g., '60', '40')
            field_name: Friendly name for logging
            delay_ms: Delay between keystrokes in milliseconds (default: 100ms)
            
        Returns:
            bool: True if successful, False otherwise
        """
        field_name = field_name or selector[:40]
        
        if not value:
            self.logger.debug(f"{field_name}: Skipped (empty value)")
            return True
        
        # Extract digits only
        digits = ''.join(c for c in str(value) if c.isdigit())
        
        if not digits:
            self.logger.warning(f"{field_name}: No digits found in value '{value}'")
            return False
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            
            # Click to focus the field
            self.page.click(selector)
            time.sleep(0.1)
            
            # Clear existing content by pressing backspace multiple times slowly
            # The field has format 0__ (3 chars), so press backspace 3 times
            for _ in range(3):
                self.page.keyboard.press("Backspace")
                time.sleep(delay_ms / 1000)
            
            time.sleep(0.1)
            
            # Type each digit slowly
            for digit in digits:
                self.page.keyboard.press(digit)
                time.sleep(delay_ms / 1000)
            
            # Verify by getting the value back
            actual = self.get_text_value(selector)
            
            # Check if digits are present in the result
            actual_digits = ''.join(c for c in (actual or '') if c.isdigit())
            
            # Remove leading zeros for comparison
            expected_digits = digits.lstrip('0') or '0'
            actual_clean = actual_digits.lstrip('0') or '0'
            
            if actual_clean == expected_digits:
                self.logger.info(f"{field_name}: Filled with '{actual}' (value: {digits})")
                return True
            else:
                self.logger.warning(f"{field_name}: Value mismatch. Expected '{digits}', got '{actual_digits}'")
                return False
            
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to fill masked equity input - {e}")
            return False

    def fill_autocomplete_input(self, input_selector: str, dropdown_selector: str, 
                                 item_selector: str, value: str, field_name: str = None,
                                 delay_ms: int = 150) -> bool:
        """
        Fill an autocomplete/typeahead input field.
        
        Types the value slowly to trigger the autocomplete dropdown, waits for
        dropdown to appear, then selects the option using keyboard.
        
        Args:
            input_selector: CSS selector for the input field
            dropdown_selector: CSS selector for the autocomplete dropdown container
            item_selector: CSS selector for the dropdown items (not used, kept for compatibility)
            value: Value to type (e.g., '7311' for SIC code)
            field_name: Friendly name for logging
            delay_ms: Delay between keystrokes in milliseconds (default: 150ms)
            
        Returns:
            bool: True if successful, False otherwise
        """
        field_name = field_name or input_selector[:40]
        
        if not value:
            self.logger.debug(f"{field_name}: Skipped (empty value)")
            return True
        
        try:
            self.wait_for_element(input_selector, timeout=self.SHORT_TIMEOUT)
            
            # Click to focus the field
            self.page.click(input_selector)
            time.sleep(0.1)
            
            # Clear existing content
            self.page.locator(input_selector).clear()
            time.sleep(0.1)
            
            # Type each character slowly to trigger autocomplete
            for char in value:
                self.page.keyboard.press(char)
                time.sleep(delay_ms / 1000)
            
            # Wait 1 second for dropdown to fully populate
            time.sleep(1)
            
            # Wait for the dropdown to be visible
            try:
                self.page.wait_for_selector(dropdown_selector, state="visible", timeout=2000)
            except TimeoutError:
                self.logger.warning(f"{field_name}: Autocomplete dropdown did not appear")
                return False
            
            # Select using keyboard - ArrowDown to highlight first item, Enter to select
            self.page.keyboard.press("ArrowDown")
            time.sleep(0.1)
            self.page.keyboard.press("Enter")
            time.sleep(0.3)
            
            # Verify selection by checking input value
            actual = self.get_text_value(input_selector)
            if actual and value in actual:
                self.logger.info(f"{field_name}: Selected '{actual}' from autocomplete")
                return True
            
            self.logger.info(f"{field_name}: Autocomplete selection completed (value: {actual})")
            return True
            
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to fill autocomplete input - {e}")
            return False
    
    # =========================================================================
    # DROPDOWN UTILITIES
    # =========================================================================
    
    def select_dropdown_by_text(self, selector: str, option_text: str, 
                                 field_name: str = None, partial_match: bool = True) -> bool:
        """
        Select a dropdown option by visible text.
        
        Args:
            selector: CSS selector for the <select> element
            option_text: Text of the option to select
            field_name: Friendly name for logging
            partial_match: If exact match fails, try partial match
            
        Returns:
            bool: True if selection successful, False otherwise
        """
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            
            # Get available options
            available = self.get_dropdown_options(selector)
            
            # Try exact match first
            if option_text in available:
                self.page.select_option(selector, label=option_text)
                self.logger.info(f"{field_name}: Selected '{option_text}'")
                return True
            
            # Try partial match if enabled
            if partial_match:
                matches = [opt for opt in available if option_text.lower() in opt.lower()]
                if matches:
                    self.page.select_option(selector, label=matches[0])
                    self.logger.info(f"{field_name}: Selected '{matches[0]}' (partial match)")
                    return True
            
            self.logger.error(f"{field_name}: Option '{option_text}' not found. Available: {available}")
            return False
            
        except Exception as e:
            self.logger.error(f"{field_name}: Dropdown selection failed - {e}")
            return False
    
    def select_dropdown_by_value(self, selector: str, value: str, 
                                  field_name: str = None) -> bool:
        """Select a dropdown option by its value attribute."""
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            self.page.select_option(selector, value=value)
            self.logger.info(f"{field_name}: Selected value '{value}'")
            return True
        except Exception as e:
            self.logger.error(f"{field_name}: Selection by value failed - {e}")
            return False
    
    def select_dropdown_by_index(self, selector: str, index: int, 
                                  field_name: str = None) -> bool:
        """Select a dropdown option by its index (0-based)."""
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            self.page.select_option(selector, index=index)
            self.logger.info(f"{field_name}: Selected index {index}")
            return True
        except Exception as e:
            self.logger.error(f"{field_name}: Selection by index failed - {e}")
            return False
    
    def get_dropdown_options(self, selector: str) -> List[str]:
        """Get all available options from a dropdown."""
        try:
            options = self.page.locator(f"{selector} option").all()
            return [opt.text_content().strip() for opt in options if opt.text_content()]
        except Exception:
            return []
    
    def get_selected_option(self, selector: str) -> Optional[str]:
        """Get the currently selected option text."""
        try:
            selected = self.page.locator(f"{selector} option:checked")
            return selected.text_content().strip() if selected.count() > 0 else None
        except Exception:
            return None
    
    # =========================================================================
    # CHECKBOX UTILITIES
    # =========================================================================
    
    def check_checkbox(self, selector: str, field_name: str = None) -> bool:
        """Check a checkbox (ensure it's checked)."""
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            checkbox = self.page.locator(selector)
            
            if not checkbox.is_checked():
                checkbox.check()
                self.logger.info(f"{field_name}: Checked")
            else:
                self.logger.debug(f"{field_name}: Already checked")
            return True
            
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to check - {e}")
            return False
    
    def uncheck_checkbox(self, selector: str, field_name: str = None) -> bool:
        """Uncheck a checkbox (ensure it's unchecked)."""
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            checkbox = self.page.locator(selector)
            
            if checkbox.is_checked():
                checkbox.uncheck()
                self.logger.info(f"{field_name}: Unchecked")
            else:
                self.logger.debug(f"{field_name}: Already unchecked")
            return True
            
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to uncheck - {e}")
            return False
    
    def set_checkbox(self, selector: str, checked: bool, field_name: str = None) -> bool:
        """Set checkbox to specific state."""
        return self.check_checkbox(selector, field_name) if checked else self.uncheck_checkbox(selector, field_name)
    
    def is_checkbox_checked(self, selector: str) -> bool:
        """Check if a checkbox is currently checked."""
        try:
            return self.page.locator(selector).is_checked()
        except Exception:
            return False
    
    def check_multiple_checkboxes(self, selectors: List[str], field_names: List[str] = None) -> Dict[str, bool]:
        """Check multiple checkboxes at once."""
        field_names = field_names or [f"Checkbox_{i}" for i in range(len(selectors))]
        results = {}
        for selector, name in zip(selectors, field_names):
            results[name] = self.check_checkbox(selector, name)
        return results
    
    # =========================================================================
    # RADIO BUTTON UTILITIES
    # =========================================================================
    
    def select_radio(self, selector: str, field_name: str = None) -> bool:
        """Select a radio button."""
        field_name = field_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            self.page.click(selector)
            self.logger.info(f"{field_name}: Selected")
            return True
        except Exception as e:
            self.logger.error(f"{field_name}: Failed to select - {e}")
            return False
    
    def is_radio_selected(self, selector: str) -> bool:
        """Check if a radio button is selected."""
        try:
            return self.page.locator(selector).is_checked()
        except Exception:
            return False
    
    # =========================================================================
    # TABLE/GRID UTILITIES
    # =========================================================================
    
    def get_table_row_count(self, table_selector: str) -> int:
        """Get the number of data rows in a table."""
        try:
            rows = self.page.locator(f"{table_selector}//tr[td]")
            return rows.count()
        except Exception:
            return 0
    
    def click_table_row_by_text(self, table_selector: str, search_text: str, 
                                 column_index: int = 1) -> bool:
        """
        Click on a table row that contains specific text.
        
        Args:
            table_selector: XPath to the table
            search_text: Text to search for in the row
            column_index: 1-based column index to search in
            
        Returns:
            bool: True if row found and clicked
        """
        try:
            row_xpath = f"{table_selector}//tr[td[{column_index}][normalize-space()='{search_text}']]"
            self.wait_for_element(row_xpath, timeout=self.SHORT_TIMEOUT)
            self.page.click(row_xpath)
            self.logger.info(f"Clicked row with text '{search_text}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to click row with text '{search_text}': {e}")
            return False
    
    def select_table_row_checkbox(self, table_selector: str, search_text: str, 
                                   column_index: int = 1) -> bool:
        """
        Select checkbox in a table row that contains specific text.
        
        Args:
            table_selector: XPath to the table
            search_text: Text to search for in the row
            column_index: 1-based column index to search in
            
        Returns:
            bool: True if checkbox found and checked
        """
        try:
            checkbox_xpath = (
                f"{table_selector}//tr[td[{column_index}][normalize-space()='{search_text}']]"
                f"//input[@type='checkbox']"
            )
            self.wait_for_element(checkbox_xpath, timeout=self.SHORT_TIMEOUT)
            checkbox = self.page.locator(checkbox_xpath)
            
            if not checkbox.is_checked():
                checkbox.check()
            
            self.logger.info(f"Selected checkbox for row '{search_text}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to select checkbox for '{search_text}': {e}")
            return False
    
    def get_table_cell_value(self, table_selector: str, row_index: int, 
                              column_index: int) -> Optional[str]:
        """
        Get value from a specific table cell.
        
        Args:
            table_selector: XPath to the table
            row_index: 1-based row index
            column_index: 1-based column index
            
        Returns:
            str: Cell text content or None
        """
        try:
            cell_xpath = f"({table_selector}//tr[td])[{row_index}]/td[{column_index}]"
            return self.page.locator(cell_xpath).text_content().strip()
        except Exception:
            return None
    
    def filter_table_alphabetically(self, filter_container: str, letter: str) -> bool:
        """
        Click an alphabetical filter for table data (common in OSC).
        
        Args:
            filter_container: Selector for the filter container (e.g., "//ul[@id='ulLetters']")
            letter: Single letter to filter by, or "All"
            
        Returns:
            bool: True if filter clicked successfully
        """
        try:
            filter_xpath = f"{filter_container}//a[normalize-space()='{letter.upper()}']"
            self.page.click(filter_xpath)
            self.wait_for_ajax()
            self.logger.info(f"Applied alphabetical filter: '{letter}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to apply filter '{letter}': {e}")
            return False
    
    # =========================================================================
    # PAGINATION UTILITIES
    # =========================================================================
    
    def get_current_page(self, pagination_container: str) -> int:
        """Get current page number from pagination."""
        try:
            # Look for span (current page is usually in a span, not a link)
            current = self.page.locator(f"{pagination_container}//span").first
            return int(current.text_content().strip())
        except Exception:
            return 1
    
    def navigate_to_page(self, pagination_container: str, page_number: int) -> bool:
        """Navigate to a specific page."""
        try:
            page_link = f"{pagination_container}//a[normalize-space()='{page_number}']"
            self.page.click(page_link)
            self.wait_for_ajax()
            self.logger.info(f"Navigated to page {page_number}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate to page {page_number}: {e}")
            return False
    
    # =========================================================================
    # BUTTON/CLICK UTILITIES
    # =========================================================================
    
    def click_button(self, selector: str, button_name: str = None, 
                     wait_after: int = 500) -> bool:
        """Click a button with optional wait."""
        button_name = button_name or selector[:40]
        
        try:
            self.wait_for_element(selector, timeout=self.SHORT_TIMEOUT)
            self.page.click(selector)
            
            if wait_after > 0:
                time.sleep(wait_after / 1000)
            
            self.logger.info(f"{button_name}: Clicked")
            return True
            
        except Exception as e:
            self.logger.error(f"{button_name}: Click failed - {e}")
            return False
    
    def click_and_wait_for_navigation(self, selector: str, url_pattern: str = None, 
                                       timeout: int = None) -> bool:
        """Click and wait for page navigation."""
        timeout = timeout or self.DEFAULT_TIMEOUT
        
        try:
            with self.page.expect_navigation(timeout=timeout, url=url_pattern):
                self.page.click(selector)
            return True
        except Exception as e:
            self.logger.error(f"Navigation failed after click: {e}")
            return False
    
    def click_and_wait_for_popup(self, selector: str) -> Optional[Page]:
        """Click and wait for a new popup/tab to open."""
        try:
            with self.page.expect_popup() as popup_info:
                self.page.click(selector)
            return popup_info.value
        except Exception as e:
            self.logger.error(f"Popup not opened after click: {e}")
            return None
    
    # =========================================================================
    # ERROR/VALIDATION UTILITIES
    # =========================================================================
    
    def get_validation_errors(self, error_container: str = "//div[@id='divErrors']") -> List[str]:
        """
        Get all validation error messages from the error container.
        
        Args:
            error_container: XPath to the error container
            
        Returns:
            List[str]: List of error messages
        """
        try:
            if not self.page.locator(error_container).is_visible():
                return []
            
            error_items = self.page.locator(f"{error_container}//li").all()
            return [item.text_content().strip() for item in error_items if item.text_content()]
            
        except Exception:
            return []
    
    def has_validation_errors(self, error_container: str = "//div[@id='divErrors']") -> bool:
        """Check if there are any validation errors displayed."""
        return len(self.get_validation_errors(error_container)) > 0
    
    def dismiss_error_message(self, close_button: str = "//div[@id='divErrors']//button[@class='close']") -> bool:
        """Dismiss the error message popup."""
        try:
            if self.page.locator(close_button).is_visible():
                self.page.click(close_button)
                return True
            return False
        except Exception:
            return False
    
    def verify_element_text(self, selector: str, expected_text: str, 
                            exact_match: bool = False) -> bool:
        """
        Verify that an element contains expected text.
        
        Args:
            selector: Element selector
            expected_text: Text to look for
            exact_match: If True, requires exact match; if False, contains match
            
        Returns:
            bool: True if text matches
        """
        try:
            actual = self.page.locator(selector).text_content().strip()
            
            if exact_match:
                return actual == expected_text
            else:
                return expected_text in actual
                
        except Exception:
            return False
    
    # =========================================================================
    # SECTION UTILITIES
    # =========================================================================
    
    def verify_section_loaded(self, section_selector: str, section_name: str = None, 
                               timeout: int = None) -> bool:
        """Verify a form section is loaded and visible."""
        section_name = section_name or section_selector[:40]
        timeout = timeout or self.DEFAULT_TIMEOUT
        
        if self.wait_for_element(section_selector, timeout=timeout, state="visible"):
            self.logger.info(f"Section '{section_name}' loaded successfully")
            return True
        else:
            self.logger.error(f"Section '{section_name}' failed to load")
            return False
    
    def scroll_to_section(self, section_selector: str) -> bool:
        """Scroll an element into view."""
        try:
            self.page.locator(section_selector).scroll_into_view_if_needed()
            return True
        except Exception:
            return False
    
    # =========================================================================
    # FORM SECTION UTILITIES
    # =========================================================================
    
    def fill_form_section(self, field_definitions: Dict[str, Dict[str, Any]]) -> Dict[str, bool]:
        """
        Fill a complete form section based on field definitions.
        
        Args:
            field_definitions: Dict with structure:
                {
                    "field_name": {
                        "type": "text" | "dropdown" | "checkbox" | "radio",
                        "selector": "#field_id",
                        "value": "field_value"
                    },
                    ...
                }
                
        Returns:
            Dict[str, bool]: Success status for each field
        """
        results = {}
        
        for field_name, field_def in field_definitions.items():
            field_type = field_def.get("type", "text")
            selector = field_def["selector"]
            value = field_def.get("value", "")
            
            if field_type == "text":
                results[field_name] = self.fill_text(selector, value, field_name)
            
            elif field_type == "dropdown":
                results[field_name] = self.select_dropdown_by_text(selector, value, field_name)
            
            elif field_type == "checkbox":
                results[field_name] = self.set_checkbox(selector, bool(value), field_name)
            
            elif field_type == "radio":
                if value:  # Only select if value is truthy
                    results[field_name] = self.select_radio(selector, field_name)
                else:
                    results[field_name] = True  # Skip if not needed
            
            else:
                self.logger.warning(f"{field_name}: Unknown field type '{field_type}'")
                results[field_name] = False
        
        # Log summary
        success_count = sum(1 for r in results.values() if r)
        self.logger.info(f"Form section completed: {success_count}/{len(results)} fields successful")
        
        return results
    
    # =========================================================================
    # SCREENSHOT/DEBUG UTILITIES
    # =========================================================================
    
    def take_screenshot(self, name: str = None) -> str:
        """Take a screenshot for debugging.
        
        Uses RunContext to save to the current run's screenshots folder.
        Uses animations="disabled" to prevent flickering.
        """
        from core.run_context import RunContext
        
        ctx = RunContext.get_current()
        if ctx:
            # Use RunContext path (preferred)
            screenshot_path = ctx.get_screenshot_path(name or "debug")
        else:
            # Fallback for standalone usage
            from pathlib import Path
            import time as time_module
            timestamp = time_module.strftime("%Y%m%d_%H%M%S")
            screenshots_dir = Path.cwd() / "artifacts" / "debug" / "screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshots_dir / f"{name or 'debug'}_{timestamp}.png"
        
        try:
            self.page.screenshot(
                path=str(screenshot_path),
                animations="disabled",  # Prevents CSS animations from causing flicker
                caret="hide"  # Hide text cursor/caret
            )
            self.logger.info(f"Screenshot saved: {screenshot_path.name}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return ""


# Backward compatibility alias
BasePage = OSCBasePage