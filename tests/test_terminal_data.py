#!/usr/bin/env python3
"""
Test script to verify terminal data loading based on environment.

This script tests that:
1. Correct terminal data file is loaded for each environment
2. Serial number prefixes match the environment
3. Terminal quantities are appropriate for each environment
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.osc.config import osc_settings
from core.logger import get_logger, log_section, log_success, log_step, log_table

logger = get_logger("terminal_data_test")


def test_terminal_data_loading():
    """Test terminal data loading based on environment."""
    
    log_section("Terminal Data Loading Test")
    
    # Get current environment
    env_value = os.getenv("ENV", "not set")
    log_step(f"Current ENV value: {env_value}")
    log_step(f"Normalized environment: {osc_settings.environment}")
    
    # Import terminal data dynamically
    log_step("Loading terminal data...")
    
    import importlib
    env = osc_settings.environment
    module_name = f"data.osc.add_terminal_{env}"
    
    try:
        terminal_module = importlib.import_module(module_name)
        log_success(f"✓ Successfully loaded: {module_name}")
    except ImportError as e:
        logger.error(f"✗ Failed to load terminal data module: {e}")
        return False
    
    # Get terminal data
    terminals = terminal_module.TERMINALS_TO_ADD
    terminal_count = len(terminals)
    
    log_step(f"Loaded {terminal_count} terminals")
    
    # Test serial number generation
    log_step("Testing serial number generation...")
    
    sample_serial = terminal_module.generate_serial_number()
    expected_prefix = "PROD" if env == "prod" else "QA"
    
    if sample_serial.startswith(expected_prefix):
        log_success(f"✓ Serial number has correct prefix: {sample_serial}")
    else:
        logger.error(f"✗ Serial number has wrong prefix. Expected: {expected_prefix}, Got: {sample_serial}")
        return False
    
    # Display terminal configuration
    log_step("Terminal Configuration Summary...")
    
    # Count terminals by type
    terminal_types = {}
    for terminal in terminals:
        name = terminal.get("name", "Unknown")
        terminal_types[name] = terminal_types.get(name, 0) + 1
    
    config_data = [
        ["Terminal Type", "Quantity"],
    ]
    
    for name, count in terminal_types.items():
        config_data.append([name, str(count)])
    
    config_data.append(["TOTAL", str(terminal_count)])
    
    log_table("Terminal Quantities by Type", ["Terminal Type", "Quantity"], config_data[1:])
    
    # Verify expected quantities based on environment
    log_step("Verifying quantities for environment...")
    
    if env == "prod":
        # Production should have smaller quantities (2-2 per type)
        expected_total_range = (5, 10)
        if expected_total_range[0] <= terminal_count <= expected_total_range[1]:
            log_success(f"✓ PROD environment has appropriate quantity: {terminal_count} terminals")
        else:
            logger.warning(f"⚠️  PROD quantity outside expected range {expected_total_range}: {terminal_count}")
    elif env == "qa":
        # QA should have larger quantities (3-5 per type)
        expected_total_range = (10, 20)
        if expected_total_range[0] <= terminal_count <= expected_total_range[1]:
            log_success(f"✓ QA environment has appropriate quantity: {terminal_count} terminals")
        else:
            logger.warning(f"⚠️  QA quantity outside expected range {expected_total_range}: {terminal_count}")
    
    # Test a sample terminal configuration
    log_step("Verifying terminal configuration structure...")
    
    if terminals:
        sample_terminal = terminals[0]
        required_fields = [
            "name", "part_type", "provider", "part_condition", "part_id",
            "terminal_program", "bill_to", "ship_to", "ship_method"
        ]
        
        missing_fields = [field for field in required_fields if field not in sample_terminal]
        
        if not missing_fields:
            log_success(f"✓ Terminal configuration has all required fields")
        else:
            logger.error(f"✗ Missing fields in terminal configuration: {missing_fields}")
            return False
    
    log_section("Test Passed! ✓")
    
    # Print summary
    summary_data = [
        ["Environment", env.upper()],
        ["Module Loaded", module_name],
        ["Serial Prefix", expected_prefix],
        ["Total Terminals", str(terminal_count)],
        ["Terminal Types", str(len(terminal_types))],
    ]
    
    log_table("Terminal Data Summary", ["Setting", "Value"], summary_data)
    
    return True


if __name__ == "__main__":
    try:
        success = test_terminal_data_loading()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)
        sys.exit(1)
