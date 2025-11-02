"""
Base Page - Minimal automation foundation
"""

from playwright.sync_api import Page


class BasePage:
    """Minimal base class for page objects"""
    
    def __init__(self, page: Page):
        self.page = page