"""
Base Page - Minimal automation foundation
"""

from playwright.sync_api import Page
import logging


from core.logger import Logger as CoreLogger


class BasePage:
    """Minimal base class for page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        # Attach a shared logger to the page object.
        # Use the core Logger singleton if it has been initialized by the script
        # (so all modules use the same handlers and log directory). If it
        # hasn't been initialized yet, fall back to a module-specific logger.
        core_logger = getattr(CoreLogger, "_instance", None)
        if core_logger is not None:
            self.logger = core_logger
        else:
            # Fallback to standard logger for this module/class
            self.logger = logging.getLogger(self.__class__.__name__)