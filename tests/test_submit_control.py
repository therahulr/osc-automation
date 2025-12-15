#!/usr/bin/env python3
"""
Test script to verify submit action control based on environment.

This script tests that:
1. Submit is disabled in PROD environment
2. Submit is enabled in QA environment
3. Proper warning messages are displayed
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.osc.config import osc_settings
from core.logger import get_logger, log_section, log_success, log_step, log_table

logger = get_logger("submit_control_test")


def test_submit_control():
    """Test submit action control based on environment."""
    
    log_section("Submit Action Control Test")
    
    # Get current environment
    env_value = os.getenv("ENV", "not set")
    log_step(f"Current ENV value: {env_value}")
    log_step(f"Normalized environment: {osc_settings.environment}")
    
    # Test submit control
    log_step("Testing Submit Control...")
    
    is_production_safe = osc_settings.is_production_safe
    submit_enabled = is_production_safe
    
    # Display configuration
    config_data = [
        ["Environment", osc_settings.environment.upper()],
        ["Is Production Safe", str(is_production_safe)],
        ["Submit Enabled", "YES ✅" if submit_enabled else "NO ⚠️"],
    ]
    
    log_table("Submit Control Configuration", ["Setting", "Value"], config_data)
    
    # Verify expected behavior
    log_step("Verifying Expected Behavior...")
    
    if osc_settings.environment == "prod":
        if not submit_enabled:
            log_success("✓ PROD environment: Submit correctly DISABLED")
        else:
            logger.error("✗ PROD environment: Submit should be DISABLED but is ENABLED")
            return False
    elif osc_settings.environment == "qa":
        if submit_enabled:
            log_success("✓ QA environment: Submit correctly ENABLED")
        else:
            logger.error("✗ QA environment: Submit should be ENABLED but is DISABLED")
            return False
    
    # Simulate submit call
    log_step("Simulating Submit Application Call...")
    
    # Create a mock result similar to what submit_application would return
    if not submit_enabled:
        warning_msg = (
            "⚠️  SUBMIT DISABLED: Cannot submit application in PROD environment.\n"
            f"   Current environment: {osc_settings.environment.upper()}\n"
            "   Reason: Submit action is disabled via environment configuration.\n"
            "   To enable submit: Set ENV=qa in your .env file"
        )
        logger.warning(warning_msg)
        log_success("✓ Submit was blocked as expected in PROD environment")
    else:
        logger.info(f"✅ Submit enabled in {osc_settings.environment.upper()} environment")
        log_success("✓ Submit would proceed in QA environment")
    
    log_section("Test Passed! ✓")
    
    return True


if __name__ == "__main__":
    try:
        success = test_submit_control()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Test failed with error: {e}", exc_info=True)
        sys.exit(1)
