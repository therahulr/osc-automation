"""
OSC Login automation
"""

import logging
from typing import Optional

from playwright.sync_api import Page
from pages.osc.base_page import BasePage
from config.osc.config import osc_settings
from locators.osc_locators import LoginPageLocators
from utils.decorators import retry, log_step


class LoginPage(BasePage):
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @log_step
    def complete_login(self, username: str, password: str) -> bool:
        """Complete login workflow including MFA bypass"""
        if not self._navigate_to_login():
            return False
        
        if not self._perform_login(username, password):
            return False
            
        # Check if we hit MFA page and bypass it
        if "mfa" in self.page.url.lower():
            return self._bypass_mfa()
        
        return self._verify_login_success()
    
    def _navigate_to_login(self) -> bool:
        self.page.goto(osc_settings.login_url)
        self.page.wait_for_selector(LoginPageLocators.USERNAME_FIELD, timeout=10000)
        return True
    
    def _perform_login(self, username: str, password: str) -> bool:
        """Perform the actual login form submission."""
        self.logger.info(f"Performing login for user: {username}")
        
        # Fill in the login form
        self.page.fill(LoginPageLocators.USERNAME_FIELD, username)
        self.page.fill(LoginPageLocators.PASSWORD_FIELD, password)
        
        # Click the login button (no_wait_after=True to avoid navigation timeout)
        # The server redirect can be slow, so we handle waiting manually
        self.page.click(LoginPageLocators.LOGIN_BUTTON, no_wait_after=True)
        self.logger.info("Login form submitted")
        
        # Wait for navigation to complete (either MFA page or dashboard)
        self.page.wait_for_load_state("networkidle", timeout=60000)
        return True
    
    def _bypass_mfa(self) -> bool:
        """Direct navigation to bypass MFA"""
        self.page.goto(osc_settings.dashboard_url)
        self.page.wait_for_timeout(3000)
        return True
    
    def _verify_login_success(self) -> bool:
        return "Home" in self.page.url or "frmHome" in self.page.url