# Quick Reference - OSC Automation Framework

## 🚀 Quick Start Commands

```bash
# Initial setup (one time)
make install              # Install all dependencies + Playwright browsers
cp .env.example .env      # Create environment config
# Edit .env with your credentials

# Run automation
make run-osc-login        # Run OSC login workflow

# Development
make fmt                  # Format code
make lint                 # Check code quality
make typecheck            # Type check
make clean                # Clean generated files
```

## 📦 Core Modules (Import These)

```python
from core import BrowserManager, settings, Logger, Ui
from core.utils import ensure_dir, now_ts, get_env
from core.types import Selector, JsonDict
```

## 🎯 Writing a New Script Pattern

```python
#!/usr/bin/env python3
"""Description of what this script does."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from apps.osc.pages.login_page import LoginPage
from apps.osc.pages.dashboard_page import DashboardPage
from core.browser import BrowserManager
from core.logger import Logger
from core.utils import ensure_dir, now_ts

load_dotenv()

def main() -> None:
    logger = Logger.get("osc")
    browser_manager = BrowserManager()
    
    try:
        # 1. Launch browser
        browser_manager.launch()
        context = browser_manager.new_context()
        page = browser_manager.new_page(context)
        
        # 2. Initialize pages
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # 3. Execute workflow
        login_page.open()
        login_page.login("user@example.com", "password")
        dashboard_page.wait_for_dashboard_loaded()
        
        logger.info("✅ Workflow completed")
        
    except Exception as e:
        logger.error(f"❌ Workflow failed: {e}")
        # Screenshot on error
        screenshot_path = ensure_dir("apps/osc/reports") / f"error_{now_ts()}.png"
        login_page.ui.screenshot(str(screenshot_path))
        raise
    finally:
        browser_manager.close()

if __name__ == "__main__":
    main()
```

## 📝 Writing Page Objects

```python
from playwright.sync_api import Page
from apps.osc.pages.base_page import OSCBasePage
from apps.osc.locators.your_screen_locators import *

class YourPage(OSCBasePage):
    """Page object for Your Screen."""
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)
    
    def open(self) -> None:
        """Navigate to your page."""
        self.logger.info(f"Opening your page | url={self.settings.your_url}")
        self.ui.goto(self.settings.your_url)
    
    def perform_action(self, param: str) -> None:
        """Perform single business action.
        
        Args:
            param: Description
            
        Raises:
            RuntimeError: If action fails
        """
        self.logger.info(f"Performing action | param={param}")
        try:
            self.ui.click(SOME_BUTTON, name="Action Button")
            self.ui.input_text(SOME_INPUT, param)
            self.ui.wait_visible(SUCCESS_MESSAGE)
            self.logger.info("Action completed successfully")
        except Exception as e:
            self.logger.error(f"Action failed | error={e}")
            raise RuntimeError(f"Failed to perform action: {e}") from e
```

## 🎨 Writing Locators

```python
# apps/osc/locators/your_screen_locators.py
"""Locators for Your Screen in OSC application."""

# Main elements
MAIN_HEADING = "h1.page-title"
SEARCH_INPUT = "input[name='search']"
SUBMIT_BUTTON = "button[type='submit']"

# Form fields
NAME_INPUT = "input#name"
EMAIL_INPUT = "input#email"
SAVE_BUTTON = "button:has-text('Save')"

# Success/error messages
SUCCESS_MESSAGE = ".alert-success"
ERROR_MESSAGE = ".alert-danger"

# Dynamic elements (use functions if needed)
def get_row_selector(row_id: str) -> str:
    """Get selector for specific row."""
    return f"tr[data-id='{row_id}']"
```

## 🔧 UI Interaction Methods

```python
# Available on self.ui (Ui class instance)

ui.goto(url)                                    # Navigate
ui.click(selector, name="Button")               # Click
ui.input_text(selector, "text")                 # Fill input
ui.select_option(selector, "value")             # Select dropdown
ui.hover(selector)                              # Hover
ui.press(selector, "Enter")                     # Press key
ui.wait_visible(selector)                       # Wait for element
ui.wait_hidden(selector)                        # Wait for element hidden
ui.screenshot("path/to/file.png")               # Screenshot
ui.switch_tab(1)                                # Switch tab
ui.handle_dialogs("accept")                     # Handle alerts
```

## 🧪 Common Patterns

### Wait for element before interaction
```python
self.ui.wait_visible(ELEMENT)
self.ui.click(ELEMENT)
```

### Handle optional elements
```python
try:
    self.ui.wait_visible(OPTIONAL_ELEMENT, timeout_ms=3000)
    self.ui.click(OPTIONAL_ELEMENT)
except Exception:
    self.logger.debug("Optional element not present, continuing")
```

### Loop with wait
```python
for item in items:
    self.ui.input_text(ITEM_INPUT, item)
    self.ui.click(ADD_BUTTON)
    self.ui.wait_visible(SUCCESS_MESSAGE)
```

### Error handling with screenshot
```python
try:
    self.perform_risky_action()
except Exception as e:
    self.logger.error(f"Action failed: {e}")
    screenshot_path = f"apps/osc/reports/error_{now_ts()}.png"
    self.ui.screenshot(screenshot_path)
    raise
```

## 📂 File Organization

```
apps/your_app/
├── config.py              # YourAppSettings
├── locators/
│   ├── __init__.py        # Export common locators
│   ├── login_locators.py  # One file per screen
│   ├── screen1_locators.py
│   └── screen2_locators.py
├── pages/
│   ├── base_page.py       # YourAppBasePage
│   ├── login_page.py      # One page object per screen
│   ├── screen1_page.py
│   └── screen2_page.py
├── data/
│   └── test_data.json     # Test data
├── scripts/
│   ├── workflow1.py       # Automation scripts
│   └── workflow2.py
├── logs/                  # Auto-generated
└── reports/               # Auto-generated
```

## 🌍 Environment Variables

```bash
# Browser (core/config.py)
HEADLESS=false              # Run in headless mode
INCOGNITO=true              # Use incognito/private mode
SLOW_MO_MS=100              # Slow down automation
DEFAULT_TIMEOUT_MS=30000    # Default element timeout
NAV_TIMEOUT_MS=60000        # Navigation timeout
DOWNLOADS_DIR=./downloads   # Download directory
TRACE_ENABLED=false         # Enable Playwright traces

# Logging (core/logger.py)
ENV=dev                     # dev = DEBUG, prod = INFO

# App-specific (apps/osc/config.py)
OSC_BASE_URL=https://...
OSC_USER=user@example.com
OSC_PASS=secret123
```

## 🎯 Best Practices

1. **One action per method** - Keep page methods small and focused
2. **Log everything** - Use `self.logger.info()` for business actions
3. **Named selectors** - Always use named constants from locators/
4. **Error context** - Provide clear error messages with context
5. **Screenshot on failure** - Capture visual state for debugging
6. **No sleep()** - Always use explicit waits (`wait_visible()`)
7. **Cleanup resources** - Always use try/finally with `browser_manager.close()`
8. **Type hints** - Add type hints to all function signatures
9. **Docstrings** - Document all public methods with Args/Returns/Raises
10. **Composable workflows** - Build complex flows from simple page methods

## 🔗 Useful Selector Patterns

```python
# By ID
"#element-id"

# By class
".class-name"

# By attribute
"input[name='username']"
"button[type='submit']"

# By text content
"button:has-text('Login')"
"text=/Login|Sign In/i"  # Regex, case-insensitive

# Combined selectors (fallback)
"input#username, input[name='username']"

# Nested
"form.login-form input[type='password']"

# nth-child
"table tr:nth-child(2)"

# Data attributes
"[data-testid='submit-button']"
```

## 📊 Debug Tips

```bash
# Run with visible browser
HEADLESS=false make run-osc-login

# Slow down for visibility
SLOW_MO_MS=500 make run-osc-login

# Enable debug logging
ENV=dev make run-osc-login

# Enable traces
TRACE_ENABLED=true make run-osc-login
# View traces at https://trace.playwright.dev/

# Check logs
tail -f apps/osc/logs/automation.log
```

## 💡 Pro Tips

- Use browser DevTools to find reliable selectors
- Prefer `data-testid` or `id` selectors over classes
- Test locators in browser console: `document.querySelector("selector")`
- Use Playwright Inspector: `PWDEBUG=1 python your_script.py`
- Break complex workflows into smaller, testable page methods
- Keep test data in JSON files, never hardcode credentials
- Use environment variables for all configuration
- Screenshot both success and failure states for documentation
