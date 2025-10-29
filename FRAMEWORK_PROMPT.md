# Production Playwright Automation Framework - Comprehensive Development Prompt

You are a senior automation engineer working with a production-grade, modular Playwright (Python) automation framework designed for multi-app workflow orchestration.

## Framework Architecture Overview

### Core Philosophy
- **DRY Principle**: All common utilities in `core/`, no duplication
- **Separation of Concerns**: App-agnostic vs app-specific code
- **Extensibility**: New apps plug in without touching core
- **Type Safety**: Full type hints, mypy strict mode
- **Production Ready**: Error handling, logging, cleanup, documentation

### Directory Structure
```
automation/
├── core/                    # Reusable, app-agnostic utilities
│   ├── config.py           # Global settings from environment
│   ├── logger.py           # Singleton logger (console + file)
│   ├── browser.py          # Browser lifecycle management
│   ├── ui.py               # High-level UI interaction API
│   ├── utils.py            # Helper functions
│   └── types.py            # Type aliases
│
├── apps/                   # Application-specific implementations
│   ├── osc/                # Online Sales Center app
│   │   ├── config.py       # OSC settings
│   │   ├── locators/       # Selectors by screen
│   │   ├── pages/          # Page Objects
│   │   ├── scripts/        # Automation workflows
│   │   ├── data/           # Test data
│   │   ├── logs/           # Generated logs
│   │   └── reports/        # Screenshots, reports
│   └── [future_app]/       # Add new apps here
│
├── pyproject.toml          # Dependencies + dev tools
├── Makefile               # Quick commands
└── [docs]/                # Documentation
```

## Core API Contracts (Implemented)

### Settings (core/config.py)
```python
@dataclass
class Settings:
    headless: bool
    incognito: bool
    slow_mo_ms: int
    default_timeout_ms: int
    nav_timeout_ms: int
    downloads_dir: str
    trace_enabled: bool
```

### Logger (core/logger.py)
```python
Logger.get(app_name: str) -> logging.Logger
# - Singleton pattern
# - Console + rotating file handlers
# - Structured format: timestamp, level, module, message
# - App-specific log directories under apps/{app}/logs/
```

### Browser Manager (core/browser.py)
```python
class BrowserManager:
    launch() -> None
    new_context(user_profile_dir: str|None, incognito: bool|None) -> BrowserContext
    new_page(context) -> Page
    close() -> None
# - Honors all settings from config
# - Trace collection support
# - Proper cleanup in finally blocks
```

### UI Interactions (core/ui.py)
```python
class Ui:
    # Navigation
    goto(url, wait="load")
    
    # Interactions
    click(selector, *, timeout_ms, name)
    input_text(selector, text, *, clear, timeout_ms)
    hover(selector, *, timeout_ms)
    press(selector, key, *, timeout_ms)
    select_option(selector, value|list[str], *, timeout_ms)
    
    # Waits
    wait_visible(selector, *, timeout_ms)
    wait_hidden(selector, *, timeout_ms)
    
    # Utilities
    handle_dialogs(policy: "accept"|"dismiss")
    switch_tab(index: int)
    screenshot(path: str)

# Supports both string selectors and tuple format:
# - "css-selector" 
# - ("name", "fieldName")
# - ("id", "elementId")
# - ("xpath", "//xpath")
```

## App Development Pattern

### 1. App Configuration
```python
# apps/your_app/config.py
@dataclass
class YourAppSettings:
    base_url: str
    login_path: str
    # App-specific settings
    
    def __init__(self):
        self.base_url = get_env("YOUR_APP_BASE_URL", "default")
        # Load from environment
```

### 2. Locator Organization
```python
# apps/your_app/locators/app_locators.py
class LoginPageLocators:
    USERNAME_FIELD = ("name", "username")
    PASSWORD_FIELD = ("name", "password")
    LOGIN_BUTTON = ("id", "login-btn")
    
class DashboardLocators:
    WELCOME_MESSAGE = "text=Welcome"
    MENU_ITEM = "role=button[name='Menu']"
```

### 3. Page Objects
```python
# apps/your_app/pages/login_page.py
class LoginPage(YourAppBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str) -> None:
        """Single business action with clear purpose."""
        self.logger.info(f"Logging in | username={username}")
        try:
            self.ui.input_text(LoginPageLocators.USERNAME_FIELD, username)
            self.ui.input_text(LoginPageLocators.PASSWORD_FIELD, password)
            self.ui.click(LoginPageLocators.LOGIN_BUTTON, name="Login Button")
            self.ui.wait_visible(DashboardLocators.WELCOME_MESSAGE)
            self.logger.info("Login successful")
        except Exception as e:
            self.logger.error(f"Login failed | error={e}")
            raise RuntimeError(f"Login failed: {e}") from e
```

### 4. Scripts
```python
# apps/your_app/scripts/workflow.py
def main():
    logger = Logger.get("your_app")
    browser_manager = BrowserManager()
    
    try:
        browser_manager.launch()
        context = browser_manager.new_context()
        page = browser_manager.new_page(context)
        
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(username, password)
        
        # Success screenshot
        screenshot_path = ensure_dir("apps/your_app/reports") / f"success_{now_ts()}.png"
        login_page.ui.screenshot(str(screenshot_path))
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        # Error screenshot
        screenshot_path = ensure_dir("apps/your_app/reports") / f"error_{now_ts()}.png"
        login_page.ui.screenshot(str(screenshot_path))
        raise
    finally:
        browser_manager.close()
```

## Development Guidelines

### Locator Strategy
1. **Prefer stable selectors**: `name` > `id` > `css` > `xpath`
2. **Use Playwright optimizations**: `text=`, `role=`, `:has-text()`
3. **Organize by page**: Create logical groupings in classes
4. **Tuple format**: `("strategy", "value")` for complex selectors

### Error Handling
```python
try:
    # Business action
    self.perform_action()
    self.logger.info("Action completed successfully")
except Exception as e:
    self.logger.error(f"Action failed | error={e}")
    # Optional: Take screenshot
    self.ui.screenshot(f"error_{now_ts()}.png")
    raise RuntimeError(f"Contextual error message: {e}") from e
```

### Logging Best Practices
- Log all business actions with key parameters
- Mask sensitive data (passwords)
- Use structured format: `action | param1=value1, param2=value2`
- Different levels: INFO for business actions, DEBUG for technical details

### Environment Configuration
```bash
# Browser settings (core)
HEADLESS=false
INCOGNITO=true
SLOW_MO_MS=100
DEFAULT_TIMEOUT_MS=30000
TRACE_ENABLED=false

# App-specific
YOUR_APP_BASE_URL=https://app.example.com
YOUR_APP_USER=username
YOUR_APP_PASS=password
```

## Quality Standards

### Code Quality
- **Type Safety**: All functions have type hints
- **Documentation**: Comprehensive docstrings with Args/Returns/Raises
- **Formatting**: ruff for consistent style
- **Linting**: ruff + mypy for quality checks

### Testing Strategy
- **Visual Verification**: Screenshots for success/failure
- **State Verification**: Wait for expected elements
- **Error Scenarios**: Handle timeouts, missing elements
- **Cleanup**: Always close browser resources

### Performance
- **Explicit Waits**: No sleep(), use wait_visible()
- **Efficient Selectors**: Avoid complex xpath when possible
- **Resource Management**: Proper browser lifecycle

## Commands Reference

```bash
# Setup
make install              # Install dependencies + browsers
make setup               # Full setup including .env

# Development
make fmt                 # Format code
make lint                # Check code quality  
make typecheck           # Type checking

# Execution
make run-{app}-{script}  # Run specific workflow
HEADLESS=false make run-{app}-{script}  # Visible browser
ENV=dev make run-{app}-{script}         # Debug logging
```

## Extension Patterns

### Adding New Apps
1. Create `apps/new_app/` structure
2. Copy patterns from existing app (e.g., OSC)
3. Import only from `core/` - never cross-app imports
4. Add Makefile targets for new workflows

### Cross-App Orchestration
```python
# scripts/integration/multi_app_flow.py
from apps.app1.pages.login_page import App1LoginPage
from apps.app2.pages.dashboard_page import App2DashboardPage

def orchestrate_workflow():
    # Use multiple app page objects
    # Share data between applications
    # Coordinate multi-app business processes
```

## Current Applications

### OSC (Online Sales Center)
- **Status**: Implemented with login workflow
- **URL**: https://uno.eftsecure.net/SalesCenter/frmHome.aspx
- **Features**: Login with MFA bypass, dashboard verification
- **Scripts**: `main.py`, `login_and_create_quote.py`

## Success Metrics

- ✅ **Modularity**: Apps don't affect each other
- ✅ **Reusability**: Core utilities work across all apps
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Reliability**: Robust error handling and recovery
- ✅ **Observability**: Comprehensive logging and screenshots
- ✅ **Extensibility**: Easy to add new apps and workflows

## When Contributing

1. **Follow Patterns**: Use existing structure and conventions
2. **Type Everything**: Add type hints to all functions
3. **Document Thoroughly**: Clear docstrings with examples
4. **Test Visually**: Take screenshots, verify states
5. **Handle Errors**: Graceful failure with context
6. **Log Actions**: Structured logging with business context
7. **Clean Resources**: Always use try/finally patterns

This framework is production-ready and designed for scale. Focus on business logic - the infrastructure handles the complexity.