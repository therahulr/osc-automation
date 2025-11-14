"""
Base Page - Minimal automation foundation
"""

from playwright.sync_api import Page

from core.logging_system import get_logger


class BasePage:
    """Minimal base class for page objects"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger()