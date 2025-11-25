# OSC Automation Framework - User Guide

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Creating a New Script](#creating-a-new-script)
5. [Working with Page Objects](#working-with-page-objects)
6. [Data Management](#data-management)
7. [Locators](#locators)
8. [Reusable Utilities](#reusable-utilities)
9. [Best Practices](#best-practices)
10. [Examples](#examples)
11. [Troubleshooting](#troubleshooting)

---

## Overview

The OSC Automation Framework is a modular, maintainable automation solution built on **Playwright** for browser automation. It follows the **Page Object Model (POM)** pattern and provides reusable utilities for common automation tasks.

### Key Features

- ✅ **Page Object Model** - Clean separation of page logic and test scripts
- ✅ **Reusable Components** - Form filling, dropdowns, tables, wizards
- ✅ **Performance Tracking** - Built-in metrics and reporting
- ✅ **Structured Logging** - Date-organized logs with console output
- ✅ **Data Management** - Faker-based dynamic test data
- ✅ **Error Handling** - Robust retry and validation mechanisms

---

## Project Structure

```
automation/
├── core/                       # Framework core modules
│   ├── browser.py              # Browser lifecycle management
│   ├── logger.py               # Logging utilities
│   ├── performance.py          # Performance tracking
│   └── performance_decorators.py
│
├── config/                     # Configuration files
│   └── osc/
│       └── config.py           # OSC-specific settings (URLs, credentials)
│
├── data/                       # Test data
│   └── osc/
│       ├── osc_data.py         # Dynamic data using Faker
│       └── osc_default_data.py # Static default values
│
├── locators/                   # Element locators
│   └── osc_locators.py         # All OSC application locators
│
├── pages/                      # Page Objects
│   └── osc/
│       ├── base_page.py        # OSCBasePage with reusable utilities
│       ├── login_page.py       # Login automation
│       ├── navigation_steps.py # Navigation workflows
│       ├── new_application_page.py # Application form sections
│       └── wizard_helpers.py   # Multi-step wizard utilities
│
├── scripts/                    # Executable automation scripts
│   └── osc/
│       └── create_credit_card_merchant.py
│
├── logs/                       # Generated logs (date-organized)
├── screenshots/                # Debug screenshots
├── reports/                    # Generated reports
└── utils/                      # Utility functions
    ├── decorators.py           # @log_step, @retry decorators
    └── locator_utils.py        # Dynamic locator builders
```

---

## Quick Start

### 1. Prerequisites

```bash
# Ensure Python 3.10+ is installed
python --version

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\activate   # Windows
```

### 2. Run Existing Script

```bash
# Run the credit card merchant creation script
python scripts/osc/create_credit_card_merchant.py
```

### 3. Check Logs

Logs are stored in: `logs/osc/YYYY-MM-DD/osc_HH_MM_AM_PM.log`

---

## Creating a New Script

### Step-by-Step Process

#### Step 1: Define Your Goal

Before writing code, understand:
- What workflow are you automating?
- What data inputs are needed?
- What pages/sections are involved?
- What is the expected outcome?

#### Step 2: Create the Script File

Create a new file in `scripts/osc/`:

```python
# scripts/osc/my_new_script.py
"""
Script: My New Automation Script
Description: Automates XYZ workflow in OSC
Author: Your Name
Date: 2025-11-25
"""

from core.browser import BrowserManager
from core.logger import Logger
from core.performance_decorators import PerformanceSession

# Initialize logger FIRST (before other imports that use it)
logger = Logger.get("osc")

# Import page objects
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from config.osc.config import osc_settings


def my_automation_workflow():
    """Main automation workflow."""
    
    username, password = osc_settings.credentials
    logger.info("Starting my automation workflow")
    
    # Use performance session for tracking
    with PerformanceSession(
        script_name="my_new_script",
        environment="development",
        browser_type="chromium",
        headless=False,
        tags=["osc", "my_workflow"],
        notes="Automation for XYZ workflow"
    ) as session:
        
        # Use BrowserManager for automatic cleanup
        with BrowserManager(enable_performance_tracking=True) as browser_manager:
            page = browser_manager.get_page()
            
            # Step 1: Login
            logger.info("Step 1: Login")
            login_page = LoginPage(page)
            if not login_page.complete_login(username, password):
                logger.error("Login failed")
                return False
            
            # Step 2: Navigate
            logger.info("Step 2: Navigate to target page")
            navigation = NavigationSteps(page)
            # ... navigation logic
            
            # Step 3: Perform actions
            logger.info("Step 3: Perform main actions")
            # ... your automation logic
            
            logger.info("✅ Workflow completed successfully")
            return True


if __name__ == "__main__":
    my_automation_workflow()
```

#### Step 3: Run Your Script

```bash
python scripts/osc/my_new_script.py
```

---

## Working with Page Objects

### Understanding OSCBasePage

All page objects inherit from `OSCBasePage` which provides reusable utilities:

```python
from pages.osc.base_page import OSCBasePage

class MyPage(OSCBasePage):
    def __init__(self, page):
        super().__init__(page)
        # Your page-specific initialization
```

### Available Utilities in OSCBasePage

#### Text Input

```python
# Fill a text field
self.fill_text("#myInput", "Hello World", "My Field Name")

# Fill multiple fields at once
self.fill_multiple_fields({
    "First Name": ("#firstName", "John"),
    "Last Name": ("#lastName", "Doe"),
    "Email": ("#email", "john@example.com")
})

# Get current value
value = self.get_text_value("#myInput")
```

#### Dropdown Selection

```python
# Select by visible text
self.select_dropdown_by_text("#stateDropdown", "California", "State")

# Select by value attribute
self.select_dropdown_by_value("#countryDropdown", "US", "Country")

# Select by index (0-based)
self.select_dropdown_by_index("#options", 2, "Option")

# Get all available options
options = self.get_dropdown_options("#stateDropdown")
print(options)  # ['Alabama', 'Alaska', 'Arizona', ...]

# Get currently selected option
selected = self.get_selected_option("#stateDropdown")
```

#### Checkboxes

```python
# Check a checkbox
self.check_checkbox("#agreeTerms", "Terms Agreement")

# Uncheck a checkbox
self.uncheck_checkbox("#newsletter", "Newsletter")

# Set to specific state
self.set_checkbox("#option1", True, "Option 1")
self.set_checkbox("#option2", False, "Option 2")

# Check if checkbox is checked
is_checked = self.is_checkbox_checked("#agreeTerms")

# Check multiple checkboxes
results = self.check_multiple_checkboxes(
    ["#option1", "#option2", "#option3"],
    ["Option 1", "Option 2", "Option 3"]
)
```

#### Radio Buttons

```python
# Select a radio button
self.select_radio("#paymentCreditCard", "Credit Card Payment")

# Check if selected
is_selected = self.is_radio_selected("#paymentCreditCard")
```

#### Tables and Grids

```python
# Get row count
count = self.get_table_row_count("//table[@id='dataGrid']")

# Click a row by text
self.click_table_row_by_text("//table[@id='dataGrid']", "DEMONET1", column_index=1)

# Select checkbox in a row
self.select_table_row_checkbox("//table[@id='dataGrid']", "DEMONET1", column_index=1)

# Get cell value
value = self.get_table_cell_value("//table[@id='dataGrid']", row_index=1, column_index=2)

# Apply alphabetical filter
self.filter_table_alphabetically("//ul[@id='ulLetters']", "D")
```

#### Buttons and Clicks

```python
# Click a button
self.click_button("#submitBtn", "Submit")

# Click and wait for navigation
self.click_and_wait_for_navigation("#nextBtn", url_pattern=".*step2.*")

# Click and wait for popup/new tab
new_page = self.click_and_wait_for_popup("#openNewWindow")
```

#### Wait Utilities

```python
# Wait for element to be visible
self.wait_for_element("#myElement", timeout=10000, state="visible")

# Wait for page to finish loading
self.wait_for_page_load()

# Wait for AJAX requests (simple delay)
self.wait_for_ajax(timeout=2000)
```

#### Error Handling

```python
# Get validation errors
errors = self.get_validation_errors()
if errors:
    print("Errors found:", errors)

# Check if errors exist
if self.has_validation_errors():
    self.dismiss_error_message()

# Verify element text
if self.verify_element_text("#status", "Success"):
    print("Status is Success!")
```

#### Form Section Filling

```python
# Fill entire form section with field definitions
results = self.fill_form_section({
    "first_name": {
        "type": "text",
        "selector": "#firstName",
        "value": "John"
    },
    "state": {
        "type": "dropdown",
        "selector": "#state",
        "value": "California"
    },
    "agree_terms": {
        "type": "checkbox",
        "selector": "#terms",
        "value": True
    },
    "payment_type": {
        "type": "radio",
        "selector": "#creditCard",
        "value": True
    }
})

# Check results
for field, success in results.items():
    print(f"{field}: {'✅' if success else '❌'}")
```

---

## Data Management

### Using osc_data.py

Data is stored in `data/osc/osc_data.py` using the Faker library for realistic random data:

```python
# data/osc/osc_data.py
from faker import Faker
import random

faker = Faker()

# Static configuration
SALES_REPRESENTATIVE = {
    "name": "DEMONET1",
}

# Dynamic data using Faker
MERCHANT_INFO = {
    "legal_business_name": faker.company(),
    "dba_name": faker.company_suffix(),
    "federal_tax_id": str(random.randint(100000000, 999999999)),
    "phone": faker.phone_number(),
    "email": faker.company_email(),
}

OWNER_INFO = {
    "first_name": faker.first_name(),
    "last_name": faker.last_name(),
    "ssn": faker.ssn(),
    "dob": faker.date_of_birth(minimum_age=25, maximum_age=65).strftime("%m/%d/%Y"),
}
```

### Using Data in Scripts

```python
from data.osc.osc_data import MERCHANT_INFO, OWNER_INFO, APPLICATION_INFO

# Use in page objects
def fill_merchant_info(self):
    self.fill_text("#legalName", MERCHANT_INFO["legal_business_name"], "Legal Name")
    self.fill_text("#phone", MERCHANT_INFO["phone"], "Phone")
```

### Creating Custom Data Sets

```python
# For specific test scenarios
def get_high_volume_merchant():
    return {
        **MERCHANT_INFO,
        "monthly_volume": "500000",
        "average_ticket": "250.00",
        "highest_ticket": "5000.00"
    }

def get_restaurant_merchant():
    return {
        **MERCHANT_INFO,
        "business_type": "Restaurant",
        "sic_code": "5812",
    }
```

---

## Locators

### Understanding osc_locators.py

All locators are organized in classes by page/section:

```python
# locators/osc_locators.py

class LoginPageLocators:
    USERNAME_FIELD = "#txtUsername"
    PASSWORD_FIELD = "#txtPassword"
    LOGIN_BUTTON = "#btnLogin"


class CorporateInformationLocators:
    LEGAL_BUSINESS_NAME_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpName"
    ADDRESS_LINE_1_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpAddress1"
    CITY_INPUT = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_txtCorpCity"
    STATE_DROPDOWN = "#ctl00_ContentPlaceHolder1_ctrlApplicationCorp1_FormView1_ddlCorpState"
```

### Using Locators in Page Objects

```python
from locators.osc_locators import CorporateInformationLocators as Locators

class CorporateInfoPage(OSCBasePage):
    def fill_corporate_info(self, data):
        self.fill_text(Locators.LEGAL_BUSINESS_NAME_INPUT, data["legal_name"], "Legal Name")
        self.fill_text(Locators.CITY_INPUT, data["city"], "City")
        self.select_dropdown_by_text(Locators.STATE_DROPDOWN, data["state"], "State")
```

### Dynamic Locators

For elements that require dynamic values (like selecting a specific row):

```python
class Step1SalesRepLocators:
    # Lambda function for dynamic locator
    SELECT_REP_CHECKBOX = lambda rep_name: (
        f"//table[@id='ContractorGrid']//tr[td[1][normalize-space()='{rep_name}']]//input[@type='checkbox']"
    )

# Usage
locator = Step1SalesRepLocators.SELECT_REP_CHECKBOX("DEMONET1")
self.page.click(locator)
```

---

## Reusable Utilities

### Decorators

#### @log_step

Automatically logs function entry:

```python
from utils.decorators import log_step

class MyPage(OSCBasePage):
    @log_step
    def fill_section(self):
        # Automatically logs: "Executing: fill_section"
        self.fill_text("#field1", "value1")
```

#### @retry

Retry on failure:

```python
from utils.decorators import retry

@retry(attempts=3, delay=1)
def unstable_operation():
    # Will retry up to 3 times with 1 second delay
    pass
```

### Performance Tracking

```python
from core.performance_decorators import performance_step, PerformanceSession

class MyPage(OSCBasePage):
    @performance_step("fill_corporate_info")
    def fill_corporate_info(self, data):
        # Performance automatically tracked
        pass

# In your script
with PerformanceSession(script_name="my_script") as session:
    # All operations tracked
    pass
```

---

## Best Practices

### 1. Follow the Pattern

```
Script (scripts/osc/) 
    → Uses Page Objects (pages/osc/)
        → Uses Locators (locators/osc_locators.py)
        → Uses Data (data/osc/osc_data.py)
        → Inherits from OSCBasePage (pages/osc/base_page.py)
```

### 2. Keep Scripts Clean

Scripts should orchestrate, not contain detailed logic:

```python
# ✅ GOOD - Clean script
def create_merchant():
    login_page.complete_login(username, password)
    navigation.navigate_to_new_application()
    application_page.fill_application_info(APP_DATA)
    application_page.fill_corporate_info(CORP_DATA)
    application_page.submit()

# ❌ BAD - Logic in script
def create_merchant():
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#login")
    # ... detailed implementation
```

### 3. Use Meaningful Names

```python
# ✅ GOOD
def fill_corporate_information(self, corporate_data):
    pass

# ❌ BAD
def fill_form(self, data):
    pass
```

### 4. Handle Errors Gracefully

```python
def fill_section(self, data):
    results = {}
    
    results["field1"] = self.fill_text("#field1", data.get("field1", ""))
    results["field2"] = self.fill_text("#field2", data.get("field2", ""))
    
    # Log summary
    success = sum(1 for r in results.values() if r)
    self.logger.info(f"Section completed: {success}/{len(results)} fields")
    
    return results
```

### 5. Add Verification Steps

```python
def complete_section(self, data):
    # Fill the form
    self.fill_section(data)
    
    # Verify no errors
    if self.has_validation_errors():
        errors = self.get_validation_errors()
        self.logger.error(f"Validation errors: {errors}")
        return False
    
    return True
```

---

## Examples

### Example 1: Simple Form Filling

```python
# pages/osc/corporate_info_page.py
from pages.osc.base_page import OSCBasePage
from locators.osc_locators import CorporateInformationLocators as Locators
from data.osc.osc_data import CORPORATE_INFO


class CorporateInfoPage(OSCBasePage):
    
    def fill_corporate_information(self, data=None):
        """Fill the Corporate Information section."""
        data = data or CORPORATE_INFO
        
        results = self.fill_form_section({
            "legal_name": {
                "type": "text",
                "selector": Locators.LEGAL_BUSINESS_NAME_INPUT,
                "value": data["legal_business_name"]
            },
            "address": {
                "type": "text",
                "selector": Locators.ADDRESS_LINE_1_INPUT,
                "value": data["address"]
            },
            "city": {
                "type": "text",
                "selector": Locators.CITY_INPUT,
                "value": data["city"]
            },
            "state": {
                "type": "dropdown",
                "selector": Locators.STATE_DROPDOWN,
                "value": data["state"]
            }
        })
        
        return results
```

### Example 2: Multi-Section Workflow

```python
# scripts/osc/complete_application.py
from core.browser import BrowserManager
from core.logger import Logger

logger = Logger.get("osc")

from pages.osc import (
    LoginPage,
    NavigationSteps,
    NewApplicationPage
)
from data.osc.osc_data import (
    APPLICATION_INFO,
    CORPORATE_INFO,
    LOCATION_INFO,
    OWNER_INFO
)


def complete_full_application():
    """Complete entire merchant application."""
    
    with BrowserManager() as browser_manager:
        page = browser_manager.get_page()
        
        # Login
        login = LoginPage(page)
        login.complete_login(username, password)
        
        # Navigate to new application
        nav = NavigationSteps(page)
        app_page = nav.navigate_to_new_application_page()
        
        # Fill all sections
        application = NewApplicationPage(app_page)
        
        sections = [
            ("Application Info", application.fill_application_information, APPLICATION_INFO),
            ("Corporate Info", application.fill_corporate_information, CORPORATE_INFO),
            ("Location Info", application.fill_location_information, LOCATION_INFO),
            ("Owner Info", application.fill_owner_information, OWNER_INFO),
        ]
        
        for section_name, fill_method, data in sections:
            logger.info(f"Filling: {section_name}")
            results = fill_method(data)
            
            success = all(results.values())
            if not success:
                logger.error(f"{section_name} failed")
                return False
        
        logger.info("✅ All sections completed")
        return True


if __name__ == "__main__":
    complete_full_application()
```

### Example 3: Using Wizard Helper

```python
from pages.osc.wizard_helpers import TerminalWizard

def add_terminal_equipment(page):
    """Add terminal equipment using the wizard."""
    
    wizard = TerminalWizard(page)
    
    # Open the wizard
    if not wizard.open_wizard():
        return False
    
    # Step 1: Select part type
    wizard.complete_step_1("Terminal")
    
    # Step 2: Select equipment
    wizard.complete_step_2(["PART001", "PART002"])
    
    # Continue through remaining steps...
    
    return True
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

```
ImportError: cannot import name 'XYZ' from 'locators.osc_locators'
```

**Solution**: Check that the class exists in `locators/osc_locators.py`

#### 2. Element Not Found

```
TimeoutError: Element not found: #myElement
```

**Solutions**:
- Verify the locator is correct
- Add explicit wait: `self.wait_for_element("#myElement")`
- Check if element is in iframe
- Take screenshot for debugging: `self.take_screenshot("debug")`

#### 3. Dropdown Selection Failed

```
Option 'California' not found in available options
```

**Solution**: Use `get_dropdown_options()` to see available options:
```python
options = self.get_dropdown_options("#stateDropdown")
print(options)  # Check actual option texts
```

#### 4. Login Fails

**Solutions**:
- Check credentials in `config/osc/config.py`
- Verify login URL is correct
- Check for MFA requirements

### Debug Tips

1. **Enable Screenshots**
```python
self.take_screenshot("before_click")
self.click_button("#submit")
self.take_screenshot("after_click")
```

2. **Check Logs**
```bash
# View latest log
cat logs/osc/$(date +%Y-%m-%d)/osc_*.log | tail -100
```

3. **Run in Headed Mode**
```python
# In BrowserManager
with BrowserManager(headless=False) as browser:
    # Watch the browser actions
```

4. **Add Pauses for Debugging**
```python
import time
time.sleep(5)  # Pause to observe
```

---

## Summary

| Task | Location |
|------|----------|
| Create new script | `scripts/osc/my_script.py` |
| Add page object | `pages/osc/my_page.py` |
| Add locators | `locators/osc_locators.py` |
| Add test data | `data/osc/osc_data.py` |
| Check logs | `logs/osc/YYYY-MM-DD/` |
| Debug screenshots | `screenshots/` |

### Quick Reference

```python
# Fill text
self.fill_text(selector, value, name)

# Select dropdown
self.select_dropdown_by_text(selector, option, name)

# Check checkbox
self.check_checkbox(selector, name)

# Click button
self.click_button(selector, name)

# Wait for element
self.wait_for_element(selector, timeout=10000)

# Get validation errors
errors = self.get_validation_errors()

# Take screenshot
self.take_screenshot("debug_name")
```

---

**For questions or issues, check the logs first, then review this guide.**
