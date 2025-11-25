# OSC Automation - Quick Reference Cheat Sheet

## 🚀 Quick Start

```bash
# Activate environment
source venv/bin/activate

# Run a script
python scripts/osc/create_credit_card_merchant.py

# Check logs
ls -la logs/osc/$(date +%Y-%m-%d)/
```

---

## 📁 File Locations

| What | Where |
|------|-------|
| Scripts | `scripts/osc/` |
| Page Objects | `pages/osc/` |
| Locators | `locators/osc_locators.py` |
| Test Data | `data/osc/osc_data.py` |
| Config | `config/osc/config.py` |
| Logs | `logs/osc/YYYY-MM-DD/` |

---

## 🔧 Script Template

```python
"""My Script Description"""

from core.browser import BrowserManager
from core.logger import Logger

logger = Logger.get("osc")

from pages.osc import LoginPage, NavigationSteps
from config.osc.config import osc_settings


def main():
    username, password = osc_settings.credentials
    
    with BrowserManager() as browser:
        page = browser.get_page()
        
        # Login
        LoginPage(page).complete_login(username, password)
        
        # Your automation here
        
    return True


if __name__ == "__main__":
    main()
```

---

## 🛠️ OSCBasePage Methods

### Text Fields
```python
self.fill_text("#input", "value", "Field Name")
self.get_text_value("#input")
self.get_element_text("#span")
```

### Dropdowns
```python
self.select_dropdown_by_text("#select", "Option Text", "Name")
self.select_dropdown_by_value("#select", "option_value", "Name")
self.select_dropdown_by_index("#select", 0, "Name")
self.get_dropdown_options("#select")
self.get_selected_option("#select")
```

### Checkboxes
```python
self.check_checkbox("#checkbox", "Name")
self.uncheck_checkbox("#checkbox", "Name")
self.set_checkbox("#checkbox", True, "Name")
self.is_checkbox_checked("#checkbox")
```

### Radio Buttons
```python
self.select_radio("#radio", "Name")
self.is_radio_selected("#radio")
```

### Buttons/Clicks
```python
self.click_button("#button", "Button Name")
self.click_and_wait_for_navigation("#link", ".*pattern.*")
new_page = self.click_and_wait_for_popup("#open_new")
```

### Tables
```python
self.get_table_row_count("//table")
self.click_table_row_by_text("//table", "search_text", column=1)
self.select_table_row_checkbox("//table", "search_text", column=1)
self.get_table_cell_value("//table", row=1, column=2)
self.filter_table_alphabetically("//ul[@id='filter']", "A")
```

### Waits
```python
self.wait_for_element("#elem", timeout=10000, state="visible")
self.wait_for_page_load()
self.wait_for_ajax(timeout=2000)
```

### Validation
```python
self.has_validation_errors()
self.get_validation_errors()
self.dismiss_error_message()
self.verify_element_text("#elem", "expected text")
```

### Sections
```python
self.verify_section_loaded("#section", "Section Name")
self.scroll_to_section("#section")
```

### Debug
```python
self.take_screenshot("debug_name")
```

---

## 📝 Form Section Helper

```python
results = self.fill_form_section({
    "field1": {"type": "text", "selector": "#f1", "value": "hello"},
    "field2": {"type": "dropdown", "selector": "#f2", "value": "Option"},
    "field3": {"type": "checkbox", "selector": "#f3", "value": True},
    "field4": {"type": "radio", "selector": "#f4", "value": True},
})
```

---

## 📍 Locator Patterns

### CSS Selectors
```python
"#elementId"              # By ID
".className"              # By class
"input[name='field']"     # By attribute
"#parent #child"          # Nested
```

### XPath
```python
"//input[@id='myId']"                    # By ID
"//button[text()='Submit']"              # By text
"//div[contains(@class, 'active')]"      # Contains
"//tr[td[1][normalize-space()='Value']]" # Table row
"//select/option[normalize-space()='X']" # Dropdown option
```

### Dynamic Locators
```python
# In locators file
SELECT_BY_NAME = lambda name: f"//tr[td[normalize-space()='{name}']]//input"

# Usage
locator = Locators.SELECT_BY_NAME("DEMONET1")
```

---

## 📊 Data with Faker

```python
from faker import Faker
import random

faker = Faker()

DATA = {
    "company": faker.company(),
    "name": faker.name(),
    "email": faker.email(),
    "phone": faker.phone_number(),
    "address": faker.street_address(),
    "city": faker.city(),
    "state": faker.state(),
    "zip": faker.zipcode(),
    "ssn": faker.ssn(),
    "ein": f"{random.randint(10,99)}-{random.randint(1000000,9999999)}",
    "date": faker.date_of_birth(minimum_age=25).strftime("%m/%d/%Y"),
}
```

---

## 🎯 Page Object Template

```python
"""My Page Object"""

from pages.osc.base_page import OSCBasePage
from locators.osc_locators import MyLocators as Locators
from data.osc.osc_data import MY_DATA


class MyPage(OSCBasePage):
    
    def __init__(self, page):
        super().__init__(page)
    
    def fill_section(self, data=None):
        """Fill the section with data."""
        data = data or MY_DATA
        
        results = {}
        results["field1"] = self.fill_text(Locators.FIELD1, data["field1"], "Field 1")
        results["field2"] = self.select_dropdown_by_text(Locators.FIELD2, data["field2"], "Field 2")
        
        success = sum(1 for r in results.values() if r)
        self.logger.info(f"Section: {success}/{len(results)} successful")
        
        return results
```

---

## 🔍 Debugging

```bash
# View recent logs
tail -f logs/osc/$(date +%Y-%m-%d)/*.log

# Find errors in logs
grep -i "error\|failed" logs/osc/$(date +%Y-%m-%d)/*.log

# List screenshots
ls -la screenshots/
```

```python
# In code
self.take_screenshot("step_1_before")
print(self.get_dropdown_options("#myDropdown"))  # Debug options
time.sleep(5)  # Pause to observe
```

---

## ⚠️ Common Fixes

| Problem | Solution |
|---------|----------|
| Element not found | Add `wait_for_element()` before action |
| Dropdown option not found | Check exact text with `get_dropdown_options()` |
| Click not working | Try `scroll_to_section()` first |
| Stale element | Re-locate element after page changes |
| Import error | Check class exists in locators file |

---

## 🏗️ Adding New Automation

1. **Add locators** → `locators/osc_locators.py`
2. **Add test data** → `data/osc/osc_data.py`
3. **Create page object** → `pages/osc/my_page.py`
4. **Update __init__.py** → `pages/osc/__init__.py`
5. **Create script** → `scripts/osc/my_script.py`
6. **Test** → `python scripts/osc/my_script.py`

---

**Full documentation: `docs/user_guide.md`**
