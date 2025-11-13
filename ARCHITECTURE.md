# OSC Automation Framework - Architecture Guide

## 🎯 Overview

This is a modern, enterprise-grade automation framework built with **simplicity**, **modularity**, and **performance** in mind. The framework is designed to make automation workflows easy to write, maintain, and scale.

## 🏗️ Core Architecture

### Design Principles

1. **Simplicity First**: No boilerplate code. Everything just works.
2. **Component-Based**: Build complex workflows from simple, reusable components
3. **Highly Parameterized**: Everything is configurable
4. **Performance Tracking**: Built-in detailed performance metrics
5. **Beautiful Output**: Colored terminal output for better readability
6. **Automatic Cleanup**: No manual resource management

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Scripts                          │
│              (Your automation workflows)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Page Components                            │
│          (Reusable UI components & page objects)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  UIAutomationCore                            │
│        (Centralized framework management)                    │
│  • Browser Manager  • Logger  • Performance Tracker          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Core Utilities                            │
│  • Playwright  • Rich (colored output)  • SQLite            │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Directory Structure

```
osc-automation/
├── core/                          # Framework core (app-agnostic)
│   ├── automation_core.py        # UIAutomationCore - main entry point
│   ├── browser.py                # Browser lifecycle management
│   ├── logger.py                 # Standard logger
│   ├── colored_logger.py         # Enhanced colored logger
│   ├── config.py                 # Configuration system
│   ├── components.py             # Reusable UI components
│   ├── performance.py            # Performance tracking
│   ├── performance_decorators.py # Performance decorators
│   ├── performance_reporter.py   # Report generation
│   ├── ui.py                     # UI helper utilities
│   └── utils.py                  # Utility functions
│
├── pages/                         # Page Object Model
│   ├── base_page.py              # Base page class
│   └── osc/                      # OSC-specific pages
│       ├── base_page.py          # OSC base page
│       ├── login_page.py         # Login page object
│       ├── navigation_steps.py   # Navigation workflows
│       └── new_application_page.py  # Application page
│
├── scripts/                       # Automation workflows
│   └── osc/                      # OSC-specific scripts
│       ├── create_credit_card_merchant.py
│       └── verify_dashboard.py
│
├── examples/                      # Example workflows
│   ├── simple_workflow_example.py
│   ├── component_based_workflow.py
│   └── osc_workflow_example.py
│
├── data/                          # Test data
│   ├── osc/                      # OSC-specific data
│   │   └── osc_data.py
│   └── performance.db            # Performance database
│
├── config/                        # Configuration files
│   └── osc/
│       └── config.py             # OSC-specific config
│
├── locators/                      # UI element locators
│   └── osc_locators.py
│
├── logs/                          # Log files (auto-generated)
├── screenshots/                   # Screenshots (auto-generated)
├── downloads/                     # Downloaded files (auto-generated)
│
├── requirements.txt               # Python dependencies
└── runner.py                      # CLI runner
```

## 🚀 Quick Start

### Basic Workflow

```python
from core import UIAutomationCore

# Everything is handled automatically!
with UIAutomationCore(app_name="my_app") as core:
    page = core.page      # Browser already launched
    logger = core.logger  # Logger already initialized

    logger.info("Starting automation")
    page.goto("https://example.com")
    page.fill("#username", "user@example.com")
    page.click("#login")

    # Screenshot helper
    core.take_screenshot("after_login")

# Automatic cleanup and performance report!
```

### Component-Based Workflow

```python
from core import UIAutomationCore, BaseComponent

class LoginForm(BaseComponent):
    """Reusable login component."""

    def login(self, username: str, password: str):
        self.input("#username", username)
        self.input("#password", password)
        self.click("#login-button")
        self.wait_for_navigation()

# Use the component
with UIAutomationCore(app_name="my_app") as core:
    login = LoginForm(core.page)
    login.login("user@example.com", "password123")
```

## 🎨 Core Features

### 1. UIAutomationCore - The Heart of the Framework

**Purpose**: Centralized management of all automation needs.

**Features**:
- ✅ Automatic browser initialization
- ✅ Automatic logger setup
- ✅ Built-in performance tracking
- ✅ Automatic cleanup
- ✅ Context manager support
- ✅ Screenshot helpers

**Usage**:

```python
from core import UIAutomationCore

# Basic usage
with UIAutomationCore(app_name="osc") as core:
    core.page.goto("https://example.com")

# Advanced usage with customization
with UIAutomationCore(
    app_name="osc",
    script_name="my_workflow",
    headless=False,
    enable_performance_tracking=True,
    enable_tracing=False,
    viewport={"width": 1920, "height": 1080},
    metadata={"environment": "qa", "tags": ["smoke_test"]}
) as core:
    # Your automation code
    pass
```

**Properties**:
- `core.page` - Playwright Page object (auto-initialized)
- `core.logger` - Logger instance (auto-initialized)
- `core.ui` - UI helper utilities
- `core.browser` - BrowserManager instance
- `core.config` - Global settings

**Methods**:
- `core.take_screenshot(name)` - Take a screenshot
- `core.get_performance_report(format)` - Get performance report

### 2. Colored Logger - Beautiful Terminal Output

**Purpose**: Enhanced logging with beautiful colored output.

**Features**:
- 🎨 Color-coded log levels
- 📊 Rich tables and panels
- ✨ Success/step/metric helpers
- 📝 File + console logging

**Usage**:

```python
from core import log_success, log_step, log_metric, log_section

log_section("User Login Flow")
log_step("Navigating to login page")
log_metric("Page Load Time", 1.23, "seconds")
log_success("Login successful")
```

### 3. BaseComponent - Reusable UI Components

**Purpose**: Create modular, reusable UI components.

**Features**:
- 🧩 Encapsulate UI logic
- 🔄 Reusable across workflows
- 🎯 Domain-specific components
- 🛠️ Rich interaction methods

**Built-in Components**:
- `BaseComponent` - Base class for all components
- `FormComponent` - For form interactions
- `TableComponent` - For table interactions
- `ModalComponent` - For modal/dialog interactions

**Example**:

```python
from core import BaseComponent

class SearchBar(BaseComponent):
    """Reusable search bar component."""

    def search(self, query: str):
        self.input("#search-input", query)
        self.press("#search-input", "Enter")
        self.wait_for_navigation()

    def get_results_count(self) -> int:
        return self.get_count(".search-result")

# Use in workflow
with UIAutomationCore(app_name="app") as core:
    search = SearchBar(core.page)
    search.search("automation testing")
    count = search.get_results_count()
    core.logger.info(f"Found {count} results")
```

### 4. Performance Tracking & Reporting

**Purpose**: Comprehensive performance metrics with database storage.

**Features**:
- ⏱️ Automatic timing of all operations
- 💾 SQLite database storage
- 📊 Detailed reports (summary, detailed, JSON)
- 📈 Action-level metrics
- 🔍 Browser performance metrics

**Database Schema**:
- `automation_runs` - Run-level metrics
- `step_metrics` - Step-level metrics
- `browser_metrics` - Browser performance
- `action_metrics` - Action-level details

**Usage**:

```python
from core import UIAutomationCore

with UIAutomationCore(app_name="app", enable_performance_tracking=True) as core:
    # Your automation code
    pass

# Automatic report at the end!

# Or get report programmatically
report = core.get_performance_report(format="summary")
print(report)
```

**Report Formats**:
- `summary` - High-level overview
- `detailed` - Step-by-step breakdown with actions
- `json` - Machine-readable format

### 5. Configuration System

**Purpose**: Highly parameterized, flexible configuration.

**Features**:
- 🔧 Environment variable support
- 💻 Programmatic override
- 📝 Sensible defaults
- 🎯 Categorized settings

**Configuration Categories**:

| Category | Settings |
|----------|----------|
| **Browser** | headless, incognito, slow_mo_ms, browser_type |
| **Timeouts** | default_timeout_ms, nav_timeout_ms, action_timeout_ms |
| **Viewport** | viewport_width, viewport_height |
| **Paths** | downloads_dir, screenshots_dir, logs_dir, data_dir |
| **Performance** | trace_enabled, performance_tracking, video_recording |
| **Logging** | log_level, colored_output |
| **Retry** | max_retries, retry_delay_ms |
| **Environment** | env (dev/qa/prod) |

**Usage**:

```python
from core import settings

# View all settings
settings.print_settings()

# Override settings programmatically
settings.override(headless=True, slow_mo_ms=500)

# Or via environment variables
# HEADLESS=true
# SLOW_MO_MS=500
```

## 🔄 Workflow Patterns

### Pattern 1: Simple Linear Workflow

```python
with UIAutomationCore(app_name="app") as core:
    core.page.goto("https://example.com")
    core.page.fill("#input", "value")
    core.page.click("#button")
```

### Pattern 2: Component-Based Workflow

```python
class LoginComponent(BaseComponent):
    def login(self, username, password):
        self.input("#username", username)
        self.input("#password", password)
        self.click("#login")

with UIAutomationCore(app_name="app") as core:
    login = LoginComponent(core.page)
    login.login("user", "pass")
```

### Pattern 3: Multi-Step Workflow

```python
def step1_login(core):
    log_step("Step 1: Login")
    # Login logic

def step2_navigate(core):
    log_step("Step 2: Navigate")
    # Navigation logic

def step3_submit(core):
    log_step("Step 3: Submit")
    # Submission logic

with UIAutomationCore(app_name="app") as core:
    step1_login(core)
    step2_navigate(core)
    step3_submit(core)
```

### Pattern 4: Parameterized Workflow

```python
def run_workflow(env: str, headless: bool):
    with UIAutomationCore(
        app_name="app",
        script_name=f"workflow_{env}",
        headless=headless,
        metadata={"environment": env}
    ) as core:
        # Environment-specific logic
        pass

# Run in different environments
run_workflow("qa", headless=False)
run_workflow("prod", headless=True)
```

## 📊 Performance Tracking

### Automatic Tracking

All operations are automatically tracked when `enable_performance_tracking=True`:
- Navigation timing
- Element wait times
- Click/fill/select actions
- Page load metrics
- Step durations

### Manual Step Tracking

```python
from core import performance_step

@performance_step("Custom Step Name", "action")
def my_custom_step():
    # Your code
    pass
```

### Viewing Reports

```python
from core import PerformanceReporter

reporter = PerformanceReporter()

# Print beautiful summary
reporter.print_rich_summary()

# Get text report
report = reporter.generate_summary_report()

# Export to file
reporter.export_report(Path("report.txt"), format="detailed")
```

## 🎯 Best Practices

### 1. Component Design

**DO**:
- Create small, focused components
- Encapsulate domain logic
- Make components reusable
- Use meaningful names

**DON'T**:
- Create monolithic components
- Mix concerns
- Hard-code values
- Duplicate logic

### 2. Workflow Organization

**DO**:
- Break workflows into logical steps
- Use descriptive logging
- Take screenshots at key points
- Handle errors gracefully

**DON'T**:
- Create overly complex workflows
- Skip logging
- Ignore errors
- Mix test data with code

### 3. Configuration

**DO**:
- Use environment variables for secrets
- Parameterize everything
- Use sensible defaults
- Document custom settings

**DON'T**:
- Hard-code credentials
- Use magic numbers
- Skip configuration documentation

### 4. Performance

**DO**:
- Enable performance tracking
- Review performance reports
- Optimize slow steps
- Track trends over time

**DON'T**:
- Ignore performance metrics
- Over-optimize prematurely
- Skip performance analysis

## 🔧 Migration Guide

### Migrating from Old Approach

**Before**:
```python
from core.logger import Logger
from core.browser import BrowserManager
from core.performance_decorators import PerformanceSession

logger = Logger.get("osc")
logger.info("Starting...")

with PerformanceSession(script_name="script", ...):
    with BrowserManager(enable_performance_tracking=True) as browser:
        page = browser.get_page()
        # Automation code
```

**After**:
```python
from core import UIAutomationCore

with UIAutomationCore(app_name="osc", script_name="script") as core:
    # Everything already initialized!
    page = core.page
    logger = core.logger
    # Automation code
```

**Benefits**:
- ✅ 70% less boilerplate code
- ✅ Automatic cleanup
- ✅ Cleaner, more readable
- ✅ Easier to maintain

## 🚀 Advanced Topics

### Custom Components

Create domain-specific components for your application:

```python
class OSCApplicationForm(BaseComponent):
    """OSC-specific application form component."""

    def fill_merchant_info(self, data: dict):
        # OSC-specific logic
        pass

    def submit_application(self):
        # OSC-specific logic
        pass
```

### Performance Optimization

Tips for better performance:
1. Use appropriate timeouts
2. Leverage component reusability
3. Minimize page reloads
4. Use efficient selectors
5. Review performance reports regularly

### Testing Components

Components are easy to test:

```python
def test_login_component():
    with UIAutomationCore(app_name="test") as core:
        login = LoginComponent(core.page)
        result = login.login("test@example.com", "password")
        assert result == True
```

## 📚 Additional Resources

- `/examples` - Working examples
- `/docs` - Detailed documentation
- `requirements.txt` - Dependencies
- `.env.example` - Environment variables

## 🎉 Summary

The OSC Automation Framework provides:
- ✅ **Simple API** - No boilerplate, just automation
- ✅ **Modular Design** - Reusable components
- ✅ **Performance Tracking** - Built-in metrics
- ✅ **Beautiful Output** - Colored terminal logging
- ✅ **Highly Configurable** - Everything is parameterized
- ✅ **Production-Ready** - Enterprise-grade reliability

Start building amazing automation workflows today! 🚀
