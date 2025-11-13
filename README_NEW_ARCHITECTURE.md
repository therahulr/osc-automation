# 🚀 OSC Automation Framework - Next Generation

> **Modern, Simple, Powerful** - Enterprise-grade automation framework with zero boilerplate

## ✨ What's New

The automation framework has been completely refactored with a focus on **simplicity**, **modularity**, and **performance**.

### Key Improvements

| Feature | Before | After | Benefit |
|---------|--------|-------|---------|
| **Code Reduction** | 80+ lines | 30-40 lines | 50-70% less boilerplate |
| **Initialization** | Manual (logger, browser, performance) | Automatic (UIAutomationCore) | Simpler, cleaner code |
| **Terminal Output** | Plain text | **Colored & Formatted** | Better readability |
| **Performance Reports** | Manual generation | **Automatic** | Built-in insights |
| **Components** | Page objects only | **Reusable Components** | More modular |
| **Configuration** | Limited | **Highly Parameterized** | More flexible |
| **Cleanup** | Manual | **Automatic** | No resource leaks |

## 🎯 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Your First Workflow

```python
from core import UIAutomationCore

# That's it! Everything is automatic.
with UIAutomationCore(app_name="my_app") as core:
    core.page.goto("https://example.com")
    core.logger.info("Automation complete!")

# Performance report automatically generated!
```

### Before vs After

#### ❌ Before (Old Way)

```python
from core.logger import Logger
from core.browser import BrowserManager
from core.performance_decorators import PerformanceSession

# Manual initialization
logger = Logger.get("osc")
logger.info("Starting...")

# Manual session management
with PerformanceSession(script_name="script", ...):
    with BrowserManager(enable_performance_tracking=True) as browser:
        page = browser.get_page()

        # Your automation code
        page.goto("https://example.com")

# Manual report generation
# ... more code
```

#### ✅ After (New Way)

```python
from core import UIAutomationCore

# Everything automatic!
with UIAutomationCore(app_name="osc") as core:
    core.page.goto("https://example.com")

# Done! Automatic cleanup + report
```

**Result: 70% less code, same functionality, more features!**

## 📦 Core Features

### 1. UIAutomationCore - One Class to Rule Them All

Centralized management of everything you need:

```python
from core import UIAutomationCore

with UIAutomationCore(
    app_name="osc",
    script_name="my_workflow",
    headless=False,                    # Visible browser
    enable_performance_tracking=True,   # Track everything
    viewport={"width": 1920, "height": 1080}
) as core:
    page = core.page        # ✅ Browser already launched
    logger = core.logger    # ✅ Logger already configured
    ui = core.ui           # ✅ UI helpers ready

    # Your automation code
```

**What you get automatically:**
- ✅ Browser initialization
- ✅ Logger setup (colored output!)
- ✅ Performance tracking
- ✅ Screenshot helpers
- ✅ Automatic cleanup
- ✅ Performance reports

### 2. Beautiful Colored Output

```python
from core import log_step, log_success, log_metric, log_section

log_section("User Registration Flow")
log_step("Filling registration form")
log_metric("Form Load Time", 1.23, "seconds")
log_success("Registration completed!")
```

**Output:**
```
═══════════════════════════════════════════════════════════
USER REGISTRATION FLOW
═══════════════════════════════════════════════════════════

➜ Filling registration form
📊 Form Load Time: 1.23 seconds
✓ Registration completed!
```

### 3. Reusable Components

Build complex workflows from simple, tested components:

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
    login.login("user@example.com", "password123")
```

**Built-in components:**
- `BaseComponent` - General purpose
- `FormComponent` - Form handling
- `TableComponent` - Table interactions
- `ModalComponent` - Modal/dialog handling

### 4. Automatic Performance Tracking

Every operation is tracked automatically:

```python
with UIAutomationCore(
    app_name="app",
    enable_performance_tracking=True
) as core:
    # All actions automatically tracked:
    core.page.goto("https://example.com")  # ✓ Tracked
    core.page.fill("#input", "value")       # ✓ Tracked
    core.page.click("#button")              # ✓ Tracked

# Automatic report:
# ═══════════════════════════════════════
# AUTOMATION RUN SUMMARY
# ═══════════════════════════════════════
# Total Duration:   5.23s
# Total Steps:      12
# Success Rate:     100%
# ═══════════════════════════════════════
```

### 5. Advanced Configuration

Everything is parameterized:

```python
from core import settings

# Override settings
settings.override(
    headless=True,
    slow_mo_ms=500,
    viewport_width=1920,
    viewport_height=1080
)

# Or use environment variables
# HEADLESS=true
# SLOW_MO_MS=500
```

**Configurable settings:**
- Browser (headless, incognito, slow motion)
- Timeouts (default, navigation, actions)
- Viewport (width, height)
- Paths (downloads, screenshots, logs)
- Performance (tracking, tracing, video)
- Logging (level, colored output)
- Retries (max retries, delay)

## 📖 Examples

### Example 1: Simple Google Search

```python
from core import UIAutomationCore, log_step, log_success

with UIAutomationCore(app_name="google", headless=False) as core:
    log_step("Navigating to Google")
    core.page.goto("https://www.google.com")

    log_step("Performing search")
    core.page.fill("textarea[name='q']", "Playwright automation")
    core.page.press("textarea[name='q']", "Enter")

    results = core.page.locator("#search .g").count()
    log_success(f"Found {results} results!")
```

### Example 2: Component-Based Login

```python
from core import UIAutomationCore, BaseComponent, log_success

class GitHubLogin(BaseComponent):
    def login(self, username: str, password: str):
        self.goto("https://github.com/login")
        self.input("#login_field", username)
        self.input("#password", password)
        self.click("input[type='submit']")

with UIAutomationCore(app_name="github") as core:
    login = GitHubLogin(core.page)
    login.login("user@example.com", "password")
    log_success("Logged in!")
```

### Example 3: OSC Application Workflow

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
    log_step("Logging into OSC")
    login = LoginPage(core.page)
    login.complete_login(username, password)

    log_step("Navigating to application")
    navigation = NavigationSteps(core.page)
    app_page = navigation.navigate_to_new_application_page()

    log_step("Filling application")
    new_app = NewApplicationPage(app_page)
    new_app.fill_application_information()

    log_success("Application created!")
```

## 📁 Project Structure

```
osc-automation/
├── core/                      # Framework core
│   ├── automation_core.py    # ⭐ UIAutomationCore
│   ├── components.py         # ⭐ Reusable components
│   ├── colored_logger.py     # ⭐ Colored output
│   ├── performance_reporter.py # ⭐ Reports
│   └── ...
├── pages/                     # Page objects
├── scripts/                   # Automation workflows
├── examples/                  # ⭐ Example workflows
│   ├── simple_workflow_example.py
│   ├── component_based_workflow.py
│   └── osc_workflow_example.py
├── ARCHITECTURE.md           # ⭐ Detailed architecture guide
└── README_NEW_ARCHITECTURE.md # ⭐ This file
```

## 🎓 Learning Path

1. **Start Here**: Read this README
2. **Examples**: Check `/examples` directory
3. **Architecture**: Read `ARCHITECTURE.md` for deep dive
4. **Practice**: Try the example workflows
5. **Build**: Create your own workflows

### Recommended Reading Order

1. `README_NEW_ARCHITECTURE.md` (this file) - Overview
2. `examples/simple_workflow_example.py` - Basic usage
3. `examples/component_based_workflow.py` - Component patterns
4. `examples/osc_workflow_example.py` - Real-world example
5. `ARCHITECTURE.md` - Complete architecture guide

## 🔄 Migration Guide

### Step 1: Update imports

```python
# Before
from core.logger import Logger
from core.browser import BrowserManager

# After
from core import UIAutomationCore
```

### Step 2: Replace initialization

```python
# Before
logger = Logger.get("app")
with BrowserManager() as browser:
    page = browser.get_page()

# After
with UIAutomationCore(app_name="app") as core:
    page = core.page
    logger = core.logger
```

### Step 3: Keep your page objects

Your existing page objects work without changes!

```python
# These still work!
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps

with UIAutomationCore(app_name="osc") as core:
    login = LoginPage(core.page)
    login.complete_login(username, password)
```

## 🎯 Real-World Comparison

### Old Script (87 lines)

See `scripts/osc/create_credit_card_merchant.py`

### New Script (52 lines)

See `scripts/osc/create_credit_card_merchant_v2.py`

**Improvements:**
- ✅ 40% less code
- ✅ Colored output
- ✅ Automatic reports
- ✅ Easier to read
- ✅ Same functionality

## 🛠️ Advanced Features

### Custom Components

```python
from core import BaseComponent

class CustomForm(BaseComponent):
    def fill_and_submit(self, data: dict):
        for field, value in data.items():
            self.input(field, value)
        self.click("#submit")
        self.wait_for_navigation()
```

### Performance Analysis

```python
from core import PerformanceReporter

reporter = PerformanceReporter()
reporter.print_rich_summary()  # Beautiful colored report!
```

### Parameterized Workflows

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

## 📊 Performance Reports

After every run, get automatic reports:

```
═══════════════════════════════════════════════════════════
AUTOMATION RUN SUMMARY
═══════════════════════════════════════════════════════════

Script Name:      create_merchant
Session ID:       abc123
Status:           SUCCESS
Environment:      development
Browser:          chromium

Started:          2024-01-15 10:30:00
Completed:        2024-01-15 10:35:23
Total Duration:   5:23.45

Total Steps:      15
Failed Steps:     0
Success Rate:     100%

═══════════════════════════════════════════════════════════
STEP BREAKDOWN
═══════════════════════════════════════════════════════════

✓ [1] Login Process
    Type: action | Duration: 2.34s | Status: success

✓ [2] Navigate to Application
    Type: navigation | Duration: 1.45s | Status: success

✓ [3] Fill Application Form
    Type: action | Duration: 3.67s | Status: success

═══════════════════════════════════════════════════════════
```

## 🎨 Beautiful Terminal Output

The framework uses **rich** library for stunning terminal output:

- 🎨 Color-coded messages
- 📊 Beautiful tables
- ✨ Progress bars
- 📦 Formatted panels
- ✓ Success indicators
- ➜ Step markers

## 🚀 Getting Started Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install Playwright: `playwright install chromium`
- [ ] Read this README
- [ ] Try `examples/simple_workflow_example.py`
- [ ] Try `examples/component_based_workflow.py`
- [ ] Read `ARCHITECTURE.md`
- [ ] Create your first workflow with UIAutomationCore
- [ ] Build reusable components for your application
- [ ] Enjoy the simplified automation! 🎉

## 📚 Documentation

- **This File**: Overview and quick start
- **`ARCHITECTURE.md`**: Detailed architecture guide
- **`/examples`**: Working code examples
- **`/core`**: Framework source code (well-documented)

## 💡 Tips

1. **Start Simple**: Begin with basic workflows, then add complexity
2. **Use Components**: Create reusable components for common tasks
3. **Review Reports**: Check performance reports to optimize
4. **Parameterize**: Make everything configurable
5. **Log Wisely**: Use log_step, log_success for better visibility

## 🎉 Benefits Summary

| Aspect | Improvement |
|--------|-------------|
| **Code Size** | 50-70% reduction |
| **Readability** | Much better |
| **Maintainability** | Significantly easier |
| **Features** | More (colored output, auto reports) |
| **Complexity** | Much simpler |
| **Setup Time** | Near zero |
| **Learning Curve** | Gentler |
| **Flexibility** | Higher |
| **Performance Tracking** | Automatic |
| **Error Handling** | Better |

## 🤝 Contributing

When creating new workflows:
1. Use `UIAutomationCore` as the entry point
2. Create reusable components when possible
3. Use colored logging helpers
4. Enable performance tracking
5. Add meaningful comments
6. Follow the examples

## 📞 Support

- Check `/examples` for working code
- Read `ARCHITECTURE.md` for details
- Review existing scripts in `/scripts`

---

## 🌟 Start Building!

```python
from core import UIAutomationCore, log_success

with UIAutomationCore(app_name="my_app") as core:
    # Your automation code here
    pass

log_success("You're ready to automate!")
```

**Happy Automating! 🚀**
