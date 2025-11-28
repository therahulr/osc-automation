"""
Add Terminal Wizard Data - Terminal configurations for all 6 wizard steps.

Each terminal is defined as a complete configuration variable containing
all data needed from Step 1 through Step 6 (Finish).

Usage:
    from data.osc.add_terminal_data import SAGE_VIRTUAL_TERMINAL, TERMINALS_TO_ADD
    
    # Add terminals defined in TERMINALS_TO_ADD list
    add_terminal_page.add_terminals(TERMINALS_TO_ADD)
    
    # Get list of successfully added terminals for addon wizard
    added_terminals = get_added_terminals()
"""

import random
import string
from typing import Dict, List, Any, Optional


# =====================================================
# DATA GENERATION HELPERS
# =====================================================

def generate_serial_number() -> str:
    """
    Generate a random serial number in format TEST followed by random chars/digits.
    Example: TEST0B12XYGMK
    
    Returns:
        str: Random serial number like 'TEST0B12XYGMK'
    """
    # Generate 8-10 random uppercase letters and digits
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(8, 10)))
    return f"TEST{random_part}"


def generate_random_price(min_price: float = 50.0, max_price: float = 500.0) -> str:
    """
    Generate a random price within the given range.
    
    Args:
        min_price: Minimum price value
        max_price: Maximum price value
        
    Returns:
        str: Price formatted as string with 2 decimal places (e.g., '123.45')
    """
    price = random.uniform(min_price, max_price)
    return f"{price:.2f}"


def generate_random_fee(min_fee: float = 10.0, max_fee: float = 100.0) -> str:
    """
    Generate a random fee amount.
    
    Args:
        min_fee: Minimum fee value
        max_fee: Maximum fee value
        
    Returns:
        str: Fee formatted as string with 2 decimal places
    """
    fee = random.uniform(min_fee, max_fee)
    return f"{fee:.2f}"


# =====================================================
# ADDED TERMINALS TRACKER
# Stores successfully added terminals for addon wizard use
# =====================================================
_ADDED_TERMINALS: List[Dict[str, Any]] = []


def add_to_added_terminals(terminal_config: Dict[str, Any], terminal_name: str = None) -> None:
    """
    Track a successfully added terminal.
    
    Args:
        terminal_config: The terminal configuration that was added
        terminal_name: Optional name identifier for the terminal
    """
    _ADDED_TERMINALS.append({
        "config": terminal_config,
        "name": terminal_name or terminal_config.get("name", "Unknown"),
        "index": len(_ADDED_TERMINALS) + 1,
    })


def get_added_terminals() -> List[Dict[str, Any]]:
    """
    Get list of all successfully added terminals.
    
    Returns:
        List of added terminal records with config and metadata
    """
    return _ADDED_TERMINALS.copy()


def clear_added_terminals() -> None:
    """Clear the list of added terminals (for fresh test runs)."""
    _ADDED_TERMINALS.clear()


def get_added_terminal_count() -> int:
    """Get count of successfully added terminals."""
    return len(_ADDED_TERMINALS)


# =====================================================
# TERMINAL CONFIGURATIONS
# Each terminal contains ALL data for wizard steps 1-6
# =====================================================

SAGE_50_TERMINAL: Dict[str, Any] = {
    # Terminal identifier
    "name": "Sage 50",
    
    # ===== Step 1: Select Type =====
    "part_type": "Software",
    "provider": "Sage Payment Solutions",
    "part_condition": "New",
    
    # ===== Step 2: Select Terminal =====
    # Part ID to select from the terminal grid (exact text from PartID column)
    "part_id": "Sage 50",
    
    # ===== Step 3: Terminal Details (ALL OPTIONAL - decided randomly at runtime) =====
    # Values here are used IF the random decision is to fill the field
    # Use "random" to generate at runtime, or specific value to use that value
    "serial_number": "random",  # "random" = generate TEST<random>, "" = skip, "specific" = use that value
    "merchant_sale_price": "random",  # "random" = generate random price, "" = skip
    "file_built_by": "random",  # "random" = select random option, "" = skip, "SPS" = select SPS
    "reprogram_fee": "random",  # "random" = decide at runtime, True/False = use that
    "reprogram_fee_amount": "random",  # "random" = generate if checkbox checked
    "welcome_kit_fee": "random",  # "random" = decide at runtime, True/False = use that
    "welcome_kit_fee_amount": "random",  # "random" = generate if checkbox checked
    
    # ===== Step 4: Terminal Application =====
    "terminal_program": "VAR / STAGE",  # Program name to select from table
    "front_end_processor": "",  # Dropdown selection (usually pre-selected)
    
    # ===== Step 5: Billing & Shipping =====
    "bill_to": "Location",  # Dropdown: "Location", "Corporate", etc.
    "ship_to": "Location",
    "ship_method": "Ground",
    
    # ===== Step 6: Review =====
    # No data needed - just verification and finish
}

SAGE_VIRTUAL_TERMINAL: Dict[str, Any] = {
    "name": "Sage Virtual Terminal",
    "part_type": "Gateway",
    "provider": "Sage Payment Solutions",
    "part_condition": "New",
    "part_id": "Sage Virtual Terminal",
    "serial_number": "",
    "merchant_sale_price": "random",
    "file_built_by": "",
    "reprogram_fee": "random",
    "reprogram_fee_amount": "",
    "welcome_kit_fee": "random",
    "welcome_kit_fee_amount": "",
    "terminal_program": "VAR / STAGE",
    "front_end_processor": "",
    "bill_to": "Location",
    "ship_to": "Location",
    "ship_method": "Ground",
}


PAYA_CONNECT_INTEGRATED: Dict[str, Any] = {
    "name": "Paya Connect Integrated",
    "part_type": "Gateway",
    "provider": "Sage Payment Solutions",
    "part_condition": "New",
    "part_id": "Paya Connect Integrated",
    "serial_number": "",
    "merchant_sale_price": "random",
    "file_built_by": "",
    "reprogram_fee": "random",
    "reprogram_fee_amount": "",
    "welcome_kit_fee": "random",
    "welcome_kit_fee_amount": "",
    "terminal_program": "VAR / STAGE",
    "front_end_processor": "",
    "bill_to": "Location",
    "ship_to": "Location",
    "ship_method": "Ground",
}

PAYA_GATEWAY_LEVEL_3_VT3: Dict[str, Any] = {
    "name": "Paya Gateway Level 3 / VT3",
    "part_type": "Gateway",
    "provider": "Sage Payment Solutions",
    "part_condition": "New",
    "part_id": "Paya Gateway Level 3 / VT3",
    "serial_number": "",
    "merchant_sale_price": "random",
    "file_built_by": "",
    "reprogram_fee": "random",
    "reprogram_fee_amount": "",
    "welcome_kit_fee": "random",
    "welcome_kit_fee_amount": "",
    "terminal_program": "VAR / STAGE",
    "front_end_processor": "",
    "bill_to": "Location",
    "ship_to": "Location",
    "ship_method": "Ground",
}   


# =====================================================
# TERMINAL QUANTITIES
# Define how many of each terminal type to add
# Set quantity to 0 to skip that terminal type
# Maps directly to terminal configuration variables
# =====================================================
TERMINAL_QUANTITIES: List[tuple] = [
    (SAGE_50_TERMINAL, 1),
    # (SAGE_VIRTUAL_TERMINAL, 2),
]


def build_terminal_list() -> List[Dict[str, Any]]:
    """
    Build the terminal list based on TERMINAL_QUANTITIES.
    
    Each terminal config is copied (not referenced) so that random values
    generated at runtime are unique per instance.
    
    Returns:
        List of terminal configurations to add
        
    Example:
        TERMINAL_QUANTITIES = [
            (SAGE_50_TERMINAL, 5),
            (SAGE_VIRTUAL_TERMINAL, 10),
        ]
        # Returns list of 15 terminal configs (5 SAGE_50 + 10 SAGE_VIRTUAL)
    """
    terminals: List[Dict[str, Any]] = []
    
    for terminal_config, quantity in TERMINAL_QUANTITIES:
        if quantity <= 0:
            continue
        
        for i in range(quantity):
            # Create a copy so each instance is independent
            # Random values will be generated at runtime in complete_step_3()
            terminal_copy = terminal_config.copy()
            terminals.append(terminal_copy)
    
    return terminals


# =====================================================
# TERMINALS TO ADD
# Built dynamically from TERMINAL_QUANTITIES
# =====================================================
TERMINALS_TO_ADD: List[Dict[str, Any]] = build_terminal_list()


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_terminal_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a terminal configuration by name.
    
    Args:
        name: Terminal name to search for
        
    Returns:
        Terminal configuration dict or None if not found
    """
    # Search in common terminals
    all_terminals = [SAGE_50_TERMINAL]
    
    for terminal in all_terminals:
        if terminal.get("name") == name:
            return terminal
    return None


def create_terminal_config(
    name: str,
    part_type: str,
    provider: str,
    part_condition: str = "New",
    **kwargs
) -> Dict[str, Any]:
    """
    Create a new terminal configuration with defaults.
    
    Args:
        name: Terminal identifier name
        part_type: Part type (Gateway, Terminal, etc.)
        provider: Provider (Merchant, ISO, Sage Payment Solutions)
        part_condition: Condition (default: New)
        **kwargs: Additional step data
        
    Returns:
        Complete terminal configuration dict
    """
    config = {
        "name": name,
        "part_type": part_type,
        "provider": provider,
        "part_condition": part_condition,
        
        # Step 2 defaults
        "part_id": kwargs.get("part_id", ""),
        
        # Step 3 defaults
        "serial_number": kwargs.get("serial_number", ""),
        "merchant_sale_price": kwargs.get("merchant_sale_price", "0.00"),
        "file_built_by": kwargs.get("file_built_by", ""),
        "reprogram_fee": kwargs.get("reprogram_fee", False),
        "reprogram_fee_amount": kwargs.get("reprogram_fee_amount", "0.00"),
        "welcome_kit_fee": kwargs.get("welcome_kit_fee", False),
        "welcome_kit_fee_amount": kwargs.get("welcome_kit_fee_amount", "0.00"),
        
        # Step 4 defaults
        "terminal_program": kwargs.get("terminal_program", ""),
        "front_end_processor": kwargs.get("front_end_processor", ""),
        
        # Step 5 defaults
        "bill_to": kwargs.get("bill_to", "Location"),
        "ship_to": kwargs.get("ship_to", "Location"),
        "ship_method": kwargs.get("ship_method", "Ground"),
    }
    
    return config
