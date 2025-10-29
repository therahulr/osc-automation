---
mode: agent
model: Claude Sonnet 4 (copilot)
---

# OSC (Online Sales Center) Automation Prompt

You are an expert automation engineer working on the OSC (Online Sales Center) automation project. This is a production-grade Playwright (Python) automation framework with a modular architecture.

## Project Architecture

### Core Framework (Reusable)
- `core/config.py` - Global settings from environment variables
- `core/logger.py` - Singleton logger with console + file handlers  
- `core/browser.py` - BrowserManager for lifecycle management
- `core/ui.py` - High-level UI interaction API with locator resolution
- `core/utils.py` - Utility functions (ensure_dir, now_ts, env helpers)
- `core/types.py` - Type aliases and definitions

### OSC Application Layer
- `apps/osc/config.py` - OSC-specific settings and URLs
- `apps/osc/locators/osc_locators.py` - Organized locator classes
- `apps/osc/pages/` - Page Objects (LoginPage, DashboardPage, etc.)
- `apps/osc/scripts/` - Automation workflows
- `apps/osc/data/` - Test data and configuration

## OSC Application Details

### Target Application
- **URL**: https://uno.eftsecure.net/SalesCenter/frmHome.aspx
- **Credentials**: contractordemo / QAContractor@123
- **MFA Handling**: Bypass by direct navigation to dashboard

### Current Implementation Status

#### Locators (apps/osc/locators/osc_locators.py)
```python
class LoginPageLocators:
    USERNAME_FIELD = ("name", "txtUsername")
    PASSWORD_FIELD = ("name", "txtPassword") 
    LOGIN_BUTTON = ("name", "btnLogin")
    
class DashboardPageLocators:
    HOME_HEADING = "h2:has-text('Home')"
    APPLICATION_SUMMARY_TEXT = "text=Application Summary"
    
class MFAPageLocators:
    MFA_URL_PATTERN = "/SalesCenter/mfa/frmMFAMenuOptionPage.aspx"
```

#### Login Workflow (apps/osc/pages/login_page.py)
1. Navigate to login page
2. Enter username (txtUsername)
3. Enter password (txtPassword)  
4. Click login button (btnLogin)
5. Detect MFA redirect
6. Bypass MFA by navigating directly to dashboard
7. Verify dashboard loaded (Home heading or Application Summary)

#### Scripts
- `apps/osc/scripts/main.py` - Complete login workflow
- `apps/osc/scripts/login_and_create_quote.py` - Extended workflow example

## Development Guidelines

### Locator Strategy
- Use tuple format: `("strategy", "value")` where strategy is "name", "id", "css", "xpath", "text", "role"
- Organize in classes by page: `LoginPageLocators`, `DashboardPageLocators`, etc.
- Prefer stable selectors: name > id > css > xpath
- Use Playwright-optimized selectors: `text=`, `role=`, `:has-text()`

### Page Object Pattern
```python
class YourPage(OSCBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
    
    def perform_action(self, param: str) -> None:
        """Single business action with clear purpose."""
        self.logger.info(f"Performing action | param={param}")
        try:
            self.ui.click(YourLocators.BUTTON, name="Action Button")
            self.ui.input_text(YourLocators.INPUT, param)
            self.ui.wait_visible(YourLocators.SUCCESS)
            self.logger.info("Action completed successfully")
        except Exception as e:
            self.logger.error(f"Action failed | error={e}")
            raise RuntimeError(f"Failed to perform action: {e}") from e
```

### Error Handling
- Always use try/catch with contextual error messages
- Take screenshots on failures
- Log all business actions with parameters (mask passwords)
- Use `finally` blocks for cleanup

### Environment Configuration
```bash
# Browser settings
HEADLESS=false
OSC_BASE_URL=https://uno.eftsecure.net
OSC_USER=contractordemo
OSC_PASS=QAContractor@123
```

## Common Tasks

### Adding New Locators
1. Inspect element in browser DevTools
2. Add to appropriate class in `osc_locators.py`
3. Use in page objects with `self.ui.click(YourLocators.ELEMENT)`

### Creating New Page Objects
1. Inherit from `OSCBasePage`
2. Import locators: `from apps.osc.locators.osc_locators import YourPageLocators`
3. Implement single-purpose methods
4. Add comprehensive logging and error handling

### Writing Scripts
1. Follow `main.py` pattern
2. Use `Logger.get("osc")` for logging
3. Initialize `BrowserManager` in try/finally
4. Take screenshots for success/failure
5. Load credentials from environment

### Running Automation
```bash
# Run main login workflow
make run-osc-main

# Run with visible browser for debugging
HEADLESS=false make run-osc-main

# Enable debug logging
ENV=dev HEADLESS=false make run-osc-main
```

## Code Quality Standards

- **Type Safety**: Full type hints, mypy strict mode
- **Logging**: Structured logs with context
- **Error Handling**: Clear, actionable error messages
- **Documentation**: Comprehensive docstrings
- **Testing**: Take screenshots, verify expected states
- **Cleanup**: Always close browser resources

## Current Priorities

1. **Inspect Real Elements**: Use browser to find actual selectors
2. **Update Locators**: Replace placeholders with real selectors from OSC
3. **Extend Workflows**: Add more business processes beyond login
4. **Error Scenarios**: Handle common failure cases
5. **Data Management**: Expand test data and configuration

## Success Criteria

- ✅ Stable login automation without manual intervention
- ✅ Reliable MFA bypass mechanism  
- ✅ Clear error messages and debugging information
- ✅ Screenshots for both success and failure scenarios
- ✅ Extensible architecture for additional OSC workflows

When working on this project, always:
1. Check current locators in DevTools first
2. Update locators in the organized class structure
3. Test with visible browser initially
4. Add comprehensive logging
5. Handle errors gracefully with screenshots
6. Follow the established patterns and architecture