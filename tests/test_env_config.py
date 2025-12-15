#!/usr/bin/env python3
"""
Test script to verify the simplified environment configuration.

This script tests that:
1. ENV variable is read correctly (case-insensitive)
2. Credentials are selected based on ENV
3. Data environment matches ENV
"""

import os
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.osc.config import osc_settings
from core.logger import get_logger, log_section, log_success, log_step, log_table

logger = get_logger("env_test")

def test_environment_config():
    """Test the environment configuration."""
    
    log_section("Environment Configuration Test")
    
    # Get current ENV value
    env_value = os.getenv("ENV", "not set")
    log_step(f"Current ENV value: {env_value}")
    
    # Test OSC settings
    log_step("Testing OSC Settings...")
    
    # Display configuration
    config_data = [
        ["Setting", "Value"],
        ["Environment", osc_settings.environment],
        ["Data Environment", osc_settings.data_env],
        ["Base URL", osc_settings.base_url],
        ["Is Production Safe", str(osc_settings.is_production_safe)],
    ]
    
    log_table("OSC Configuration", ["Setting", "Value"], config_data[1:])
    
    # Test credentials
    log_step("Testing Credentials Selection...")
    username, password = osc_settings.credentials
    
    creds_data = [
        ["Credential", "Value"],
        ["Username", username],
        ["Password", "*" * len(password)],  # Mask password
    ]
    
    log_table("Selected Credentials", ["Credential", "Value"], creds_data[1:])
    
    # Verify environment normalization
    log_step("Verifying Environment Normalization...")
    
    if osc_settings.environment in ("prod", "qa"):
        log_success(f"✓ Environment correctly normalized to: {osc_settings.environment}")
    else:
        logger.error(f"✗ Invalid environment value: {osc_settings.environment}")
        return False
    
    # Verify data environment matches
    if osc_settings.data_env == osc_settings.environment:
        log_success(f"✓ Data environment matches: {osc_settings.data_env}")
    else:
        logger.error(f"✗ Data environment mismatch: {osc_settings.data_env} != {osc_settings.environment}")
        return False
    
    # Verify credentials based on environment
    log_step("Verifying Credential Selection...")
    
    if osc_settings.environment == "qa":
        expected_user = os.getenv("OSC_QA_USER", "ContractorQA")
        if username == expected_user:
            log_success(f"✓ QA credentials selected correctly")
        else:
            logger.error(f"✗ Expected QA user {expected_user}, got {username}")
            return False
    else:  # prod
        expected_user = os.getenv("OSC_USER", "contractordemo")
        if username == expected_user:
            log_success(f"✓ PROD credentials selected correctly")
        else:
            logger.error(f"✗ Expected PROD user {expected_user}, got {username}")
            return False
    
    # Test data module name
    log_step("Verifying Data Module Selection...")
    expected_module = f"osc_data_{osc_settings.data_env}"
    actual_module = osc_settings.data_module_name
    
    if actual_module == expected_module:
        log_success(f"✓ Data module name correct: {actual_module}")
    else:
        logger.error(f"✗ Expected module {expected_module}, got {actual_module}")
        return False
    
    log_section("All Tests Passed! ✓")
    
    # Print summary
    summary_data = [
        ["ENV Variable", env_value],
        ["Normalized Environment", osc_settings.environment],
        ["Data Environment", osc_settings.data_env],
        ["Selected User", username],
        ["Data Module", actual_module],
        ["Production Safe", str(osc_settings.is_production_safe)],
    ]
    
    log_table("Configuration Summary", ["Setting", "Value"], summary_data)
    
    return True


if __name__ == "__main__":
    try:
        success = test_environment_config()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)
        sys.exit(1)
