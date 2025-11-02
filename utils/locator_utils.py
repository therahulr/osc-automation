"""
Locator building utilities for automation
"""

from typing import List


def build_table_row_checkbox_locator(name: str) -> str:
    """Build XPath for checkbox in table row with matching text"""
    return f"//tr[td[normalize-space(text())='{name}']]/td//input[@type='checkbox']"


def build_radio_button_locator(text: str) -> List[str]:
    """Build multiple XPath strategies for radio buttons with text"""
    return [
        f"//input[@type='radio'][following-sibling::text()[contains(., '{text}')]]",
        f"//label[contains(text(), '{text}')]/..//input[@type='radio']",
        f"//input[@type='radio'][@value='{text}']"
    ]


def build_button_locator(text: str) -> List[str]:
    """Build multiple selectors for buttons with text"""
    return [
        f"input[type='submit'][value*='{text}']",
        f"button:has-text('{text}')",
        f"*[onclick*='{text}']"
    ]