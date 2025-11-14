"""Reusable UI components for building automation workflows.

Components are modular, reusable pieces that encapsulate common UI interactions.
They make it easy to compose complex workflows from simple, tested building blocks.

Example:
    # Define a form component
    class LoginForm(BaseComponent):
        def fill(self, username: str, password: str):
            self.input("#username", username)
            self.input("#password", password)
            self.click("#login-button")

    # Use in workflow
    with UIAutomationCore("app") as core:
        login_form = LoginForm(core.page)
        login_form.fill("user@example.com", "password123")
"""

from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
from datetime import datetime

from playwright.sync_api import Page, Locator, ElementHandle

from core.logger import get_logger
from core.ui import Ui


class BaseComponent:
    """Base class for reusable UI components.

    Provides common functionality for interacting with UI elements in a
    structured, reusable way. All components have access to:
    - Page object
    - UI helper (wraps Playwright with enhancements)
    - Logger
    - Common actions (click, input, wait, etc.)

    Subclasses should implement specific component logic.
    """

    def __init__(self, page: Page, logger: Optional[Any] = None, root_selector: Optional[str] = None):
        """Initialize component.

        Args:
            page: Playwright page object
            logger: Logger instance (creates one if not provided)
            root_selector: Optional root element selector for scoped operations
        """
        self.page = page
        self.ui = Ui(page)
        self.logger = logger or get_logger()
        self.root_selector = root_selector
        self._root_element: Optional[Locator] = None

        if root_selector:
            self._root_element = self.page.locator(root_selector)

    @property
    def root(self) -> Locator:
        """Get the root element locator (if root_selector was provided)."""
        if self._root_element is None:
            raise ValueError("No root selector defined for this component")
        return self._root_element

    # ==================== Navigation ====================

    def goto(self, url: str, wait_until: str = "load"):
        """Navigate to a URL.

        Args:
            url: URL to navigate to
            wait_until: Wait condition ('load', 'domcontentloaded', 'networkidle')
        """
        self.logger.info(f"Navigating to: {url}")
        self.ui.goto(url, wait=wait_until)

    # ==================== Element Interactions ====================

    def click(self, selector: str, timeout_ms: Optional[int] = None, name: Optional[str] = None):
        """Click an element.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds
            name: Descriptive name for logging
        """
        self.ui.click(selector, timeout_ms=timeout_ms, name=name)

    def input(self, selector: str, text: str, clear: bool = True, timeout_ms: Optional[int] = None):
        """Input text into an element.

        Args:
            selector: Element selector
            text: Text to input
            clear: Clear existing text first
            timeout_ms: Wait timeout in milliseconds
        """
        self.ui.input_text(selector, text, clear=clear, timeout_ms=timeout_ms)

    def select(self, selector: str, value: str, timeout_ms: Optional[int] = None):
        """Select an option from a dropdown.

        Args:
            selector: Dropdown selector
            value: Value or label to select
            timeout_ms: Wait timeout in milliseconds
        """
        self.ui.select_option(selector, value, timeout_ms=timeout_ms)

    def check(self, selector: str, timeout_ms: Optional[int] = None):
        """Check a checkbox or radio button.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds
        """
        self.page.check(selector, timeout=timeout_ms)
        self.logger.debug(f"Checked: {selector}")

    def uncheck(self, selector: str, timeout_ms: Optional[int] = None):
        """Uncheck a checkbox.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds
        """
        self.page.uncheck(selector, timeout=timeout_ms)
        self.logger.debug(f"Unchecked: {selector}")

    def hover(self, selector: str, timeout_ms: Optional[int] = None):
        """Hover over an element.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds
        """
        self.ui.hover(selector, timeout_ms=timeout_ms)

    def press(self, selector: str, key: str, timeout_ms: Optional[int] = None):
        """Press a key on an element.

        Args:
            selector: Element selector
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape')
            timeout_ms: Wait timeout in milliseconds
        """
        self.ui.press(selector, key, timeout_ms=timeout_ms)

    # ==================== Element Queries ====================

    def get_text(self, selector: str, timeout_ms: Optional[int] = None) -> str:
        """Get text content of an element.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds

        Returns:
            Element text content
        """
        element = self.page.wait_for_selector(selector, timeout=timeout_ms)
        return element.inner_text() if element else ""

    def get_value(self, selector: str, timeout_ms: Optional[int] = None) -> str:
        """Get value of an input element.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds

        Returns:
            Input value
        """
        element = self.page.wait_for_selector(selector, timeout=timeout_ms)
        return element.input_value() if element else ""

    def get_attribute(self, selector: str, attribute: str, timeout_ms: Optional[int] = None) -> Optional[str]:
        """Get attribute value of an element.

        Args:
            selector: Element selector
            attribute: Attribute name
            timeout_ms: Wait timeout in milliseconds

        Returns:
            Attribute value or None
        """
        element = self.page.wait_for_selector(selector, timeout=timeout_ms)
        return element.get_attribute(attribute) if element else None

    def is_visible(self, selector: str, timeout_ms: int = 5000) -> bool:
        """Check if an element is visible.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds

        Returns:
            True if visible, False otherwise
        """
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def is_hidden(self, selector: str, timeout_ms: int = 5000) -> bool:
        """Check if an element is hidden.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds

        Returns:
            True if hidden, False otherwise
        """
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout_ms)
            return True
        except Exception:
            return False

    def is_enabled(self, selector: str, timeout_ms: Optional[int] = None) -> bool:
        """Check if an element is enabled.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds

        Returns:
            True if enabled, False otherwise
        """
        element = self.page.wait_for_selector(selector, timeout=timeout_ms)
        return element.is_enabled() if element else False

    def is_checked(self, selector: str, timeout_ms: Optional[int] = None) -> bool:
        """Check if a checkbox/radio is checked.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds

        Returns:
            True if checked, False otherwise
        """
        element = self.page.wait_for_selector(selector, timeout=timeout_ms)
        return element.is_checked() if element else False

    # ==================== Wait Operations ====================

    def wait_visible(self, selector: str, timeout_ms: Optional[int] = None):
        """Wait for an element to be visible.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds
        """
        self.ui.wait_visible(selector, timeout_ms=timeout_ms)

    def wait_hidden(self, selector: str, timeout_ms: Optional[int] = None):
        """Wait for an element to be hidden.

        Args:
            selector: Element selector
            timeout_ms: Wait timeout in milliseconds
        """
        self.ui.wait_hidden(selector, timeout_ms=timeout_ms)

    def wait_for_navigation(self, url_pattern: Optional[str] = None, timeout_ms: int = 30000):
        """Wait for navigation to complete.

        Args:
            url_pattern: Optional URL pattern to wait for
            timeout_ms: Wait timeout in milliseconds
        """
        self.page.wait_for_load_state("load", timeout=timeout_ms)
        if url_pattern:
            self.page.wait_for_url(url_pattern, timeout=timeout_ms)

    def wait_for_text(self, selector: str, text: str, timeout_ms: int = 30000):
        """Wait for element to contain specific text.

        Args:
            selector: Element selector
            text: Text to wait for
            timeout_ms: Wait timeout in milliseconds
        """
        self.page.wait_for_selector(f"{selector}:has-text('{text}')", timeout=timeout_ms)

    # ==================== Multiple Elements ====================

    def get_all_texts(self, selector: str) -> List[str]:
        """Get text content of all matching elements.

        Args:
            selector: Element selector

        Returns:
            List of text contents
        """
        elements = self.page.locator(selector).all()
        return [elem.inner_text() for elem in elements]

    def get_count(self, selector: str) -> int:
        """Get count of matching elements.

        Args:
            selector: Element selector

        Returns:
            Number of matching elements
        """
        return self.page.locator(selector).count()

    def click_nth(self, selector: str, index: int, timeout_ms: Optional[int] = None):
        """Click the nth matching element.

        Args:
            selector: Element selector
            index: Zero-based index
            timeout_ms: Wait timeout in milliseconds
        """
        self.page.locator(selector).nth(index).click(timeout=timeout_ms)
        self.logger.debug(f"Clicked {index}th element: {selector}")

    # ==================== Screenshots & Debugging ====================

    def screenshot(self, name: str = "component_screenshot", full_page: bool = False) -> Path:
        """Take a screenshot.

        Args:
            name: Screenshot file name
            full_page: Capture full page or just viewport

        Returns:
            Path to saved screenshot
        """
        screenshots_dir = Path.cwd() / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = screenshots_dir / f"{name}_{timestamp}.png"

        if self.root_selector:
            # Screenshot just the component
            self.root.screenshot(path=str(screenshot_path))
        else:
            # Screenshot the page
            self.page.screenshot(path=str(screenshot_path), full_page=full_page)

        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def highlight(self, selector: str, duration_ms: int = 2000):
        """Highlight an element for debugging.

        Args:
            selector: Element selector
            duration_ms: Highlight duration in milliseconds
        """
        self.page.evaluate(f"""
            (selector) => {{
                const element = document.querySelector(selector);
                if (element) {{
                    element.style.border = '3px solid red';
                    element.style.backgroundColor = 'yellow';
                    setTimeout(() => {{
                        element.style.border = '';
                        element.style.backgroundColor = '';
                    }}, {duration_ms});
                }}
            }}
        """, selector)

    # ==================== Form Helpers ====================

    def fill_form(self, fields: Dict[str, Any]):
        """Fill multiple form fields at once.

        Args:
            fields: Dictionary of selector -> value mappings
        """
        self.logger.info(f"Filling form with {len(fields)} fields")
        for selector, value in fields.items():
            if isinstance(value, bool):
                if value:
                    self.check(selector)
                else:
                    self.uncheck(selector)
            else:
                self.input(selector, str(value))

    def submit_form(self, form_selector: str, wait_for_navigation: bool = True):
        """Submit a form.

        Args:
            form_selector: Form element selector
            wait_for_navigation: Wait for navigation after submit
        """
        self.logger.info(f"Submitting form: {form_selector}")
        if wait_for_navigation:
            with self.page.expect_navigation():
                self.page.locator(form_selector).evaluate("form => form.submit()")
        else:
            self.page.locator(form_selector).evaluate("form => form.submit()")

    # ==================== Advanced Interactions ====================

    def drag_and_drop(self, source_selector: str, target_selector: str):
        """Drag and drop an element.

        Args:
            source_selector: Source element selector
            target_selector: Target element selector
        """
        self.page.drag_and_drop(source_selector, target_selector)
        self.logger.debug(f"Dragged {source_selector} to {target_selector}")

    def upload_file(self, selector: str, file_path: str):
        """Upload a file.

        Args:
            selector: File input selector
            file_path: Path to file to upload
        """
        self.page.set_input_files(selector, file_path)
        self.logger.debug(f"Uploaded file {file_path} to {selector}")

    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript in the page context.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script

        Returns:
            Script return value
        """
        return self.page.evaluate(script, *args)


class FormComponent(BaseComponent):
    """Specialized component for form interactions."""

    def __init__(self, page: Page, form_selector: str, logger: Optional[Any] = None):
        """Initialize form component.

        Args:
            page: Playwright page object
            form_selector: CSS selector for the form element
            logger: Logger instance
        """
        super().__init__(page, logger, root_selector=form_selector)
        self.form_selector = form_selector

    def fill_and_submit(self, fields: Dict[str, Any], wait_for_navigation: bool = True):
        """Fill form fields and submit.

        Args:
            fields: Dictionary of selector -> value mappings
            wait_for_navigation: Wait for navigation after submit
        """
        self.fill_form(fields)
        self.submit_form(self.form_selector, wait_for_navigation)


class TableComponent(BaseComponent):
    """Specialized component for table interactions."""

    def __init__(self, page: Page, table_selector: str, logger: Optional[Any] = None):
        """Initialize table component.

        Args:
            page: Playwright page object
            table_selector: CSS selector for the table element
            logger: Logger instance
        """
        super().__init__(page, logger, root_selector=table_selector)
        self.table_selector = table_selector

    def get_row_count(self) -> int:
        """Get number of rows in table (excluding header)."""
        return self.get_count(f"{self.table_selector} tbody tr")

    def get_headers(self) -> List[str]:
        """Get table header texts."""
        return self.get_all_texts(f"{self.table_selector} thead th")

    def get_row_texts(self, row_index: int) -> List[str]:
        """Get all cell texts from a specific row.

        Args:
            row_index: Zero-based row index

        Returns:
            List of cell texts
        """
        return self.get_all_texts(f"{self.table_selector} tbody tr:nth-child({row_index + 1}) td")

    def click_row(self, row_index: int):
        """Click a specific row.

        Args:
            row_index: Zero-based row index
        """
        self.click_nth(f"{self.table_selector} tbody tr", row_index)

    def find_row_by_text(self, text: str) -> int:
        """Find row index containing specific text.

        Args:
            text: Text to search for

        Returns:
            Row index or -1 if not found
        """
        rows = self.page.locator(f"{self.table_selector} tbody tr").all()
        for i, row in enumerate(rows):
            if text in row.inner_text():
                return i
        return -1


class ModalComponent(BaseComponent):
    """Specialized component for modal/dialog interactions."""

    def __init__(self, page: Page, modal_selector: str, logger: Optional[Any] = None):
        """Initialize modal component.

        Args:
            page: Playwright page object
            modal_selector: CSS selector for the modal element
            logger: Logger instance
        """
        super().__init__(page, logger, root_selector=modal_selector)
        self.modal_selector = modal_selector

    def wait_for_open(self, timeout_ms: int = 30000):
        """Wait for modal to open."""
        self.wait_visible(self.modal_selector, timeout_ms=timeout_ms)
        self.logger.info("Modal opened")

    def wait_for_close(self, timeout_ms: int = 30000):
        """Wait for modal to close."""
        self.wait_hidden(self.modal_selector, timeout_ms=timeout_ms)
        self.logger.info("Modal closed")

    def close(self, close_button_selector: Optional[str] = None):
        """Close the modal.

        Args:
            close_button_selector: Selector for close button (uses common patterns if not provided)
        """
        if close_button_selector:
            self.click(close_button_selector)
        else:
            # Try common close button patterns
            common_selectors = [
                f"{self.modal_selector} .close",
                f"{self.modal_selector} [data-dismiss='modal']",
                f"{self.modal_selector} .modal-close",
                f"{self.modal_selector} button[aria-label='Close']"
            ]
            for selector in common_selectors:
                if self.is_visible(selector, timeout_ms=1000):
                    self.click(selector)
                    break
