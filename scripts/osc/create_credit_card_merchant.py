"""
OSC Credit Card Merchant Creation - Clean Automation
"""

from core.browser import BrowserManager
from config.osc.config import osc_settings
from pages.osc.navigation_steps import NavigationSteps


def create_credit_card_merchant():
    """Create credit card merchant workflow"""
    username, password = osc_settings.credentials
    
    browser_manager = BrowserManager()
    
    try:
        browser_manager.launch()
        context = browser_manager.new_context()
        page = browser_manager.new_page(context)
        
        navigation = NavigationSteps(page)
        success = navigation.create_new_application(username, password)
        
        if success:
            print(f"✓ New application created: {page.url}")
        else:
            print("✗ Failed to create application")
        
        return success
        
    finally:
        browser_manager.close()


if __name__ == "__main__":
    create_credit_card_merchant()