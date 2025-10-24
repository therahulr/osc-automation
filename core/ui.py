"""High-level UI interaction layer wrapping Playwright Page API."""

from typing import Literal

from playwright.sync_api import Page

from core.config import settings
from core.logger import Logger
from core.types import Selector


class Ui:
    """Wrapper around Playwright Page with enhanced logging and error handling.

    Provides clean, consistent API for common UI operations with
    contextual error messages and automatic timeout handling.
    """

    def __init__(self, page: Page) -> None:
        """Initialize UI wrapper.

        Args:
            page: Playwright Page instance to wrap
        """
        self._page = page
        self._logger = Logger.get()

    def goto(
        self, url: str, wait: Literal["load", "domcontentloaded", "networkidle", "commit"] = "load"
    ) -> None:
        """Navigate to URL with specified wait condition.

        Args:
            url: Target URL
            wait: Wait condition - 'load' (default), 'domcontentloaded', 'networkidle', 'commit'

        Raises:
            Error: If navigation fails or times out
        """
        self._logger.info(f"Navigating to URL | url={url}, wait={wait}")
        try:
            self._page.goto(url, wait_until=wait)
            self._logger.info(f"Navigation successful | url={url}")
        except Exception as e:
            self._logger.error(f"Navigation failed | url={url}, error={e}")
            raise RuntimeError(f"Failed to navigate to {url}: {e}") from e

    def click(
        self, selector: Selector, *, timeout_ms: int | None = None, name: str | None = None
    ) -> None:
        """Click element identified by selector.

        Args:
            selector: Element selector
            timeout_ms: Override default timeout
            name: Human-readable element name for logging

        Raises:
            Error: If element not found or not clickable
        """
        element_name = name or selector
        timeout = timeout_ms or settings.default_timeout_ms

        self._logger.info(f"Clicking element | element={element_name}, selector={selector}")
        try:
            self._page.click(selector, timeout=timeout)
            self._logger.debug(f"Click successful | element={element_name}")
        except Exception as e:
            self._logger.error(
                f"Click failed | element={element_name}, selector={selector}, error={e}"
            )
            raise RuntimeError(f"Failed to click '{element_name}': {e}") from e

    def input_text(
        self, selector: Selector, text: str, *, clear: bool = True, timeout_ms: int | None = None
    ) -> None:
        """Input text into element.

        Args:
            selector: Element selector
            text: Text to input (logged as masked if contains 'pass')
            clear: Clear existing text before input
            timeout_ms: Override default timeout

        Raises:
            Error: If element not found or not editable
        """
        timeout = timeout_ms or settings.default_timeout_ms
        # Mask sensitive data in logs
        display_text = "***MASKED***" if "pass" in selector.lower() else text[:50]

        self._logger.info(
            f"Inputting text | selector={selector}, text={display_text}, clear={clear}"
        )
        try:
            if clear:
                self._page.fill(selector, text, timeout=timeout)
            else:
                self._page.type(selector, text, timeout=timeout)
            self._logger.debug(f"Text input successful | selector={selector}")
        except Exception as e:
            self._logger.error(f"Text input failed | selector={selector}, error={e}")
            raise RuntimeError(f"Failed to input text into '{selector}': {e}") from e

    def hover(self, selector: Selector, *, timeout_ms: int | None = None) -> None:
        """Hover over element.

        Args:
            selector: Element selector
            timeout_ms: Override default timeout

        Raises:
            Error: If element not found
        """
        timeout = timeout_ms or settings.default_timeout_ms

        self._logger.debug(f"Hovering over element | selector={selector}")
        try:
            self._page.hover(selector, timeout=timeout)
        except Exception as e:
            self._logger.error(f"Hover failed | selector={selector}, error={e}")
            raise RuntimeError(f"Failed to hover over '{selector}': {e}") from e

    def press(self, selector: Selector, key: str, *, timeout_ms: int | None = None) -> None:
        """Press key on element.

        Args:
            selector: Element selector
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape')
            timeout_ms: Override default timeout

        Raises:
            Error: If element not found
        """
        timeout = timeout_ms or settings.default_timeout_ms

        self._logger.debug(f"Pressing key | selector={selector}, key={key}")
        try:
            self._page.press(selector, key, timeout=timeout)
        except Exception as e:
            self._logger.error(f"Key press failed | selector={selector}, key={key}, error={e}")
            raise RuntimeError(f"Failed to press '{key}' on '{selector}': {e}") from e

    def select_option(
        self, selector: Selector, value: str | list[str], *, timeout_ms: int | None = None
    ) -> None:
        """Select option(s) in dropdown.

        Args:
            selector: Select element selector
            value: Single value or list of values to select
            timeout_ms: Override default timeout

        Raises:
            Error: If element not found or value invalid
        """
        timeout = timeout_ms or settings.default_timeout_ms

        self._logger.info(f"Selecting option | selector={selector}, value={value}")
        try:
            self._page.select_option(selector, value, timeout=timeout)
            self._logger.debug(f"Option selected | selector={selector}, value={value}")
        except Exception as e:
            self._logger.error(
                f"Select option failed | selector={selector}, value={value}, error={e}"
            )
            raise RuntimeError(f"Failed to select option '{value}' in '{selector}': {e}") from e

    def wait_visible(self, selector: Selector, *, timeout_ms: int | None = None) -> None:
        """Wait for element to be visible.

        Args:
            selector: Element selector
            timeout_ms: Override default timeout

        Raises:
            Error: If element doesn't become visible within timeout
        """
        timeout = timeout_ms or settings.default_timeout_ms

        self._logger.debug(f"Waiting for element visible | selector={selector}")
        try:
            self._page.wait_for_selector(selector, state="visible", timeout=timeout)
            self._logger.debug(f"Element visible | selector={selector}")
        except Exception as e:
            self._logger.error(f"Wait visible failed | selector={selector}, error={e}")
            raise RuntimeError(f"Element '{selector}' did not become visible: {e}") from e

    def wait_hidden(self, selector: Selector, *, timeout_ms: int | None = None) -> None:
        """Wait for element to be hidden.

        Args:
            selector: Element selector
            timeout_ms: Override default timeout

        Raises:
            Error: If element doesn't become hidden within timeout
        """
        timeout = timeout_ms or settings.default_timeout_ms

        self._logger.debug(f"Waiting for element hidden | selector={selector}")
        try:
            self._page.wait_for_selector(selector, state="hidden", timeout=timeout)
            self._logger.debug(f"Element hidden | selector={selector}")
        except Exception as e:
            self._logger.error(f"Wait hidden failed | selector={selector}, error={e}")
            raise RuntimeError(f"Element '{selector}' did not become hidden: {e}") from e

    def handle_dialogs(self, policy: Literal["accept", "dismiss"] = "accept") -> None:
        """Set dialog handling policy for alerts, confirms, prompts.

        Args:
            policy: 'accept' (default) or 'dismiss'
        """
        self._logger.info(f"Setting dialog handler | policy={policy}")

        def dialog_handler(dialog):
            self._logger.info(f"Dialog detected | type={dialog.type}, message={dialog.message}")
            if policy == "accept":
                dialog.accept()
            else:
                dialog.dismiss()

        self._page.on("dialog", dialog_handler)

    def switch_tab(self, index: int) -> None:
        """Switch to tab by index.

        Args:
            index: Zero-based tab index

        Raises:
            IndexError: If index out of range
        """
        pages = self._page.context.pages

        if index < 0 or index >= len(pages):
            self._logger.error(f"Invalid tab index | index={index}, total_tabs={len(pages)}")
            raise IndexError(f"Tab index {index} out of range (0-{len(pages) - 1})")

        self._logger.info(f"Switching to tab | index={index}")
        target_page = pages[index]
        target_page.bring_to_front()

        # Update internal page reference
        object.__setattr__(self, "_page", target_page)

    def screenshot(self, path: str) -> None:
        """Capture screenshot of current page.

        Args:
            path: Output file path (should end with .png)
        """
        self._logger.info(f"Taking screenshot | path={path}")
        try:
            self._page.screenshot(path=path, full_page=True)
            self._logger.info(f"Screenshot saved | path={path}")
        except Exception as e:
            self._logger.error(f"Screenshot failed | path={path}, error={e}")
            raise RuntimeError(f"Failed to save screenshot to '{path}': {e}") from e
