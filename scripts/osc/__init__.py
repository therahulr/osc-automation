"""
OSC Scripts Package

Contains automation scripts for OSC Sales Center application.
"""

from scripts.osc.create_credit_card_merchant import create_credit_card_merchant
from scripts.osc.discover_valid_terminals import discover_terminals

__all__ = ['create_credit_card_merchant', 'discover_terminals']