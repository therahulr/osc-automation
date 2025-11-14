# Automation Framework

> Production-grade automation framework built with Playwright for creating maintainable, scalable automation workflows.

## Overview

This framework provides a complete automation solution with zero boilerplate code, professional logging, performance tracking, and reusable components. Built for both simplicity and power.

### Key Features

- **UIAutomationCore** - One-line initialization for browser, logger, and performance tracking
- **Professional Logging** - Color-coded terminal output with structured file logging
- **Performance Tracking** - Automatic metrics collection and reporting to SQLite database
- **Reusable Components** - Build complex workflows from simple, tested building blocks
- **Highly Configurable** - 17+ environment-based configuration options
- **Production Ready** - Enterprise-grade error handling, cleanup, and resource management

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/therahulr/osc-automation.git
cd osc-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Your First Automation

```python
from core import UIAutomationCore, log_success

# Everything is automatic - no boilerplate!
with UIAutomationCore(app_name="my_app") as core:
    core.page.goto("https://example.com")
    log_success("Automation complete!")

# Performance report automatically generated!
```

### Example: Google Search

```python
from core import UIAutomationCore, log_step, log_success

with UIAutomationCore(app_name="google_search", headless=False) as core:
    page = core.page
    logger = core.logger

    log_step("Navigating to Google")
    page.goto("https://www.google.com")

    log_step("Performing search")
    page.fill("textarea[name='q']", "Playwright automation")
    page.press("textarea[name='q']", "Enter")

    results = page.locator("#search .g").count()
    log_success(f"Found {results} search results")

    core.take_screenshot("search_results")
```

## Architecture

```
osc-automation/
├── core/                       # Framework core (app-agnostic)
│   ├── automation_core.py     # UIAutomationCore - main entry point
│   ├── logging_system.py      # Professional logging with colors
│   ├── browser.py             # Browser lifecycle management
│   ├── components.py          # Reusable UI components
│   ├── performance.py         # Performance tracking
│   ├── performance_reporter.py # Report generation
│   ├── config.py              # Configuration system
│   └── ui.py                  # UI helper utilities
│
├── pages/                      # Page Object Model
│   ├── osc/                   # OSC-specific pages
│   │   ├── login_page.py      # Login page object
│   │   ├── navigation_steps.py # Navigation workflows
│   │   └── new_application_page.py
│   └── base_page.py           # Base page class
│
├── scripts/                    # Automation workflows
│   └── osc/
│       └── create_credit_card_merchant.py
│
├── examples/                   # Example workflows
│   ├── simple_workflow_example.py
│   ├── component_based_workflow.py
│   └── osc_workflow_example.py
│
├── data/                       # Test data
│   ├── osc/osc_data.py
│   └── performance.db         # Performance metrics database
│
├── config/                     # Configuration files
│   └── osc/config.py
│
├── locators/                   # UI element locators
│   └── osc_locators.py
│
└── logs/                       # Auto-generated logs
```

## Core Concepts

### 1. UIAutomationCore

The heart of the framework - manages everything automatically.

```python
from core import UIAutomationCore

with UIAutomationCore(
    app_name="osc",
    script_name="my_workflow",
    headless=False,                    # Visible browser
    enable_performance_tracking=True,  # Track metrics
    viewport={"width": 1920, "height": 1080}
) as core:
    # Everything ready to use:
    page = core.page        # Browser launched
    logger = core.logger    # Logger configured
    ui = core.ui           # UI helpers available

    # Your automation code
```

**Auto-managed resources:**
- ✅ Browser initialization and cleanup
- ✅ Logger setup (colored console + file)
- ✅ Performance tracking session
- ✅ Screenshot helpers
- ✅ Configuration loading

### 2. Professional Logging

Beautiful, informative console output + structured file logging.

```python
from core import log_step, log_success, log_metric, log_section

log_section("User Login Flow")
log_step("Navigating to login page")
log_metric("Page Load Time", 1.23, "seconds")
log_success("Login successful")
```

**Output:**
```
═══════════════════════════════════════════════════════════
USER LOGIN FLOW
═══════════════════════════════════════════════════════════

➜ Navigating to login page
📊 Page Load Time: 1.23 seconds
✓ Login successful
```

### 3. Reusable Components

Build modular workflows from simple components.

```python
from core import BaseComponent

class LoginForm(BaseComponent):
    """Reusable login component."""

    def login(self, username: str, password: str):
        self.input("#username", username)
        self.input("#password", password)
        self.click("#login-button")
        self.wait_for_navigation()

# Use anywhere
with UIAutomationCore(app_name="app") as core:
    login = LoginForm(core.page)
    login.login("user@example.com", "password")
```

**Built-in components:**
- `BaseComponent` - General purpose
- `FormComponent` - Form handling
- `TableComponent` - Table operations
- `ModalComponent` - Modal/dialog interactions

### 4. Automatic Performance Tracking

Every action is tracked automatically to SQLite database.

```python
with UIAutomationCore(app_name="app", enable_performance_tracking=True) as core:
    # All actions automatically tracked:
    core.page.goto("https://example.com")  # ✓ Tracked
    core.page.fill("#input", "value")       # ✓ Tracked
    core.page.click("#button")              # ✓ Tracked

# Automatic report at end:
# ═══════════════════════════════════════
# AUTOMATION RUN SUMMARY
# ═══════════════════════════════════════
# Total Duration:   5.23s
# Total Steps:      12
# Success Rate:     100%
```

## Configuration

All settings are environment-based and override-able.

### Environment Variables (.env)

```bash
# Browser Settings
HEADLESS=false
INCOGNITO=true
SLOW_MO_MS=0
BROWSER_TYPE=chromium

# Timeouts
DEFAULT_TIMEOUT_MS=30000
NAV_TIMEOUT_MS=60000
ACTION_TIMEOUT_MS=10000

# Viewport
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Performance
PERFORMANCE_TRACKING=true
TRACE_ENABLED=false
VIDEO_RECORDING=false

# Logging
LOG_LEVEL=INFO
COLORED_OUTPUT=true

# Environment
ENV=dev
```

### Programmatic Override

```python
from core import settings

settings.override(
    headless=True,
    slow_mo_ms=500,
    viewport_width=1280
)
```

## Working with OSC

### OSC Automation Example

```python
from core import UIAutomationCore, log_step, log_success

from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage

with UIAutomationCore(
    app_name="osc",
    script_name="create_merchant",
    headless=False
) as core:
    page = core.page
    logger = core.logger

    log_step("Step 1: Logging into OSC")
    login = LoginPage(page)
    login.complete_login(username, password)

    log_step("Step 2: Navigating to application")
    navigation = NavigationSteps(page)
    app_page = navigation.navigate_to_new_application_page()

    log_step("Step 3: Filling application")
    new_app = NewApplicationPage(app_page)
    new_app.fill_application_information()

    log_success("Application created successfully")
```

### Running OSC Scripts

```bash
# Run with visible browser
python scripts/osc/create_credit_card_merchant.py

# Or with environment overrides
HEADLESS=false ENV=dev python scripts/osc/create_credit_card_merchant.py
```

## Examples

Check the `/examples` directory for complete working examples:

- `simple_workflow_example.py` - Basic usage patterns
- `component_based_workflow.py` - Building with components
- `osc_workflow_example.py` - Real-world OSC automation

## Performance Reports

After each run, get detailed insights:

```
═══════════════════════════════════════════════════════════
AUTOMATION RUN SUMMARY
═══════════════════════════════════════════════════════════

Script Name:      create_merchant
Status:           SUCCESS
Environment:      development
Browser:          chromium

Started:          2024-01-15 10:30:00
Duration:         5:23.45

Total Steps:      15
Failed Steps:     0
Success Rate:     100%

═══════════════════════════════════════════════════════════
STEP BREAKDOWN
═══════════════════════════════════════════════════════════

✓ [1] Login Process
    Type: action | Duration: 2.34s

✓ [2] Navigate to Application
    Type: navigation | Duration: 1.45s

✓ [3] Fill Application Form
    Type: action | Duration: 3.67s
```

## Development Workflow

### Creating a New Workflow

1. **Define your workflow:**

```python
from core import UIAutomationCore, log_step

with UIAutomationCore(app_name="my_app") as core:
    log_step("My automation step")
    # Your code here
```

2. **Create reusable components** (optional):

```python
from core import BaseComponent

class MyComponent(BaseComponent):
    def my_action(self):
        self.click("#button")
```

3. **Run and iterate:**

```bash
python scripts/my_workflow.py
```

### Best Practices

1. **Use components** - Encapsulate reusable logic
2. **Log steps** - Use `log_step()`, `log_success()` for visibility
3. **Enable tracking** - Review performance reports to optimize
4. **Parameterize** - Use configuration for flexibility
5. **Take screenshots** - Use `core.take_screenshot()` at key points

## API Reference

### UIAutomationCore

```python
core = UIAutomationCore(
    app_name="my_app",                 # Required: app name for logging
    script_name="my_script",           # Optional: script identifier
    headless=False,                    # Optional: browser visibility
    enable_performance_tracking=True,  # Optional: track metrics
    enable_tracing=False,              # Optional: Playwright traces
    viewport={"width": 1920, "height": 1080},  # Optional: viewport size
    metadata={"key": "value"}          # Optional: custom metadata
)

# Properties
core.page       # Playwright Page (auto-initialized)
core.logger     # Logger instance
core.ui         # UI helper utilities
core.browser    # BrowserManager instance
core.config     # Global settings

# Methods
core.take_screenshot(name)              # Take screenshot
core.get_performance_report(format)     # Get performance report
```

### Logging Functions

```python
from core import log_step, log_success, log_metric, log_section, log_panel, log_table

log_step("Description")                 # Step indicator
log_success("Message")                  # Success message
log_metric("Name", value, "unit")       # Metric display
log_section("Title")                    # Section header
log_panel("Content", "Title")           # Panel display
log_table("Title", columns, rows)       # Table display
```

### BaseComponent Methods

```python
component = BaseComponent(page, logger, root_selector)

# Navigation
component.goto(url, wait_until)

# Interactions
component.click(selector, timeout_ms, name)
component.input(selector, text, clear, timeout_ms)
component.select(selector, value, timeout_ms)
component.check(selector, timeout_ms)
component.hover(selector, timeout_ms)

# Queries
component.get_text(selector, timeout_ms)
component.get_value(selector, timeout_ms)
component.is_visible(selector, timeout_ms)
component.is_enabled(selector, timeout_ms)

# Wait operations
component.wait_visible(selector, timeout_ms)
component.wait_hidden(selector, timeout_ms)

# Helpers
component.screenshot(name, full_page)
component.fill_form(fields_dict)
```

## Troubleshooting

### Common Issues

**Issue:** "Failed to generate performance report: no such column: name"
**Solution:** This is fixed in the latest version. Make sure you pulled the latest changes.

**Issue:** Browser doesn't launch
**Solution:** Run `playwright install chromium`

**Issue:** Import errors
**Solution:** Make sure you activated the virtual environment: `source venv/bin/activate`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary software for internal use.

---

**Built with** Playwright • Python • Rich • SQLite

For detailed architecture documentation, see the examples in `/examples` directory.
