"""Simple workflow example demonstrating UIAutomationCore usage.

This example shows how to:
1. Use UIAutomationCore for simplified automation
2. Automatic browser and logger management
3. Built-in performance tracking
4. Colored terminal output
"""

from core import UIAutomationCore, log_success, log_step


def simple_google_search():
    """Simple example: Navigate to Google and perform a search."""

    # Everything is managed automatically - no need to initialize browser or logger separately!
    with UIAutomationCore(
        app_name="google_search",
        script_name="simple_search",
        headless=False,  # Override settings
        enable_performance_tracking=True
    ) as core:

        # Access logger (already initialized)
        logger = core.logger

        # Access page (browser already launched)
        page = core.page

        log_step("Navigating to Google")
        page.goto("https://www.google.com")

        log_step("Performing search")
        page.fill("textarea[name='q']", "Playwright automation")
        page.press("textarea[name='q']", "Enter")

        log_step("Waiting for results")
        page.wait_for_selector("#search", timeout=10000)

        # Get result count
        results = page.locator("#search .g").count()
        log_success(f"Found {results} search results")

        # Take a screenshot (built-in helper)
        screenshot_path = core.take_screenshot("search_results")
        logger.info(f"Screenshot saved: {screenshot_path}")

    # Performance report is automatically generated at the end!
    log_success("Workflow completed! Check the performance report above.")


if __name__ == "__main__":
    simple_google_search()
