"""
OSC Automation Pages - Modular page objects and utilities

Base Classes:
    - OSCBasePage: Enhanced base class with reusable form/table/validation utilities

Page Objects:
    - LoginPage: Login and MFA handling
    - NavigationSteps: Navigation workflows
    - NewApplicationPage: Application form automation (includes Corporate & Location)

Wizard Helpers:
    - WizardNavigator: Base class for multi-step wizards
    - TerminalWizard: Equipment selection wizard (6 steps)
    - AddOnWizard: Add-on selection wizard
"""

from pages.osc.base_page import OSCBasePage, BasePage
from pages.osc.login_page import LoginPage
from pages.osc.navigation_steps import NavigationSteps
from pages.osc.new_application_page import NewApplicationPage
from pages.osc.wizard_helpers import WizardNavigator, TerminalWizard, AddOnWizard

__all__ = [
    # Base classes
    "OSCBasePage",
    "BasePage",
    
    # Page objects
    "LoginPage",
    "NavigationSteps",
    "NewApplicationPage",
    
    # Wizard helpers
    "WizardNavigator",
    "TerminalWizard",
    "AddOnWizard",
]