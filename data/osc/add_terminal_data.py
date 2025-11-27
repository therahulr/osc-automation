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

from typing import Dict, List, Any, Optional


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
    
    # ===== Step 3: Terminal Details =====
    "serial_number": "",  # Optional - leave empty for auto-generation
    "merchant_sale_price": "0.00",
    "file_built_by": "",  # Dropdown selection
    "reprogram_fee": False,  # Checkbox + fee
    "reprogram_fee_amount": "0.00",
    "welcome_kit_fee": False,  # Checkbox + fee
    "welcome_kit_fee_amount": "0.00",
    
    # ===== Step 4: Terminal Program =====
    "terminal_program": "",  # Program name to select
    "front_end_processor": "",  # Dropdown selection
    
    # ===== Step 5: Billing & Shipping =====
    "bill_to": "Location",  # Dropdown: "Location", "Corporate", etc.
    "ship_to": "Location",
    "ship_method": "Ground",
    
    # ===== Step 6: Review =====
    # No data needed - just verification and finish
}


# =====================================================
# TERMINALS TO ADD
# List of terminal configurations to process
# =====================================================
TERMINALS_TO_ADD: List[Dict[str, Any]] = [
    SAGE_50_TERMINAL,
]


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
