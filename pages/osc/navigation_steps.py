"""
OSC Navigation automation - Simple workflow steps
"""

from playwright.sync_api import Page
from pages.osc.base_page import BasePage
from pages.osc.login_page import LoginPage
from config.osc.config import osc_settings
from data.data_importer import DataImporter
from utils.decorators import timeit, log_step
from utils.locator_utils import build_table_row_checkbox_locator, build_radio_button_locator, build_button_locator
from utils.logger import get_logger
from locators.osc_locators import NavigationLocators

logger = get_logger(__name__)


class NavigationSteps(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_page = LoginPage(page)
        self.data = DataImporter()
    
    @timeit
    @log_step
    def create_new_application(self, username: str, password: str) -> bool:
        """Navigate to new application page with complete setup"""
        return (self._login(username, password) and 
                self._navigate_to_new_application() and 
                self._select_sales_representative() and
                self._select_new_corporation())
    
    def _login(self, username: str, password: str) -> bool:
        return self.login_page.complete_login(username, password)
    
    def _navigate_to_new_application(self) -> bool:
        """Navigate to new application form"""
        self.page.goto(osc_settings.new_application_url)
        self.page.wait_for_timeout(2000)
        return "Application" in self.page.url
    
    def _select_sales_representative(self) -> bool:
        """Select sales rep and click next"""
        sales_rep_name = self.data.get_sales_rep_name()
        
        # Wait for table and select sales rep
        self.page.wait_for_selector(NavigationLocators.TABLE_ROWS, timeout=10000)
        locator = build_table_row_checkbox_locator(sales_rep_name)
        
        checkbox = self.page.locator(locator)
        if not checkbox.is_checked():
            checkbox.check()
        
        return self._click_next()
    
    def _select_new_corporation(self) -> bool:
        """Select new corporation option and proceed"""
        radio_selectors = build_radio_button_locator(NavigationLocators.NEW_CORPORATION_TEXT)
        
        for selector in radio_selectors:
            try:
                element = self.page.locator(selector)
                if element.count() > 0 and element.is_visible():
                    element.check()
                    break
            except:
                continue
        
        return self._click_next()
    
    def _click_next(self) -> bool:
        """Click next/continue button"""
        button_selectors = build_button_locator(NavigationLocators.NEXT_BUTTON_TEXT)
        
        for selector in button_selectors:
            try:
                button = self.page.locator(selector)
                if button.count() > 0 and button.is_visible():
                    button.click()
                    self.page.wait_for_timeout(2000)
                    return True
            except:
                continue
        
        return True