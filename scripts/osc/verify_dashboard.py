#!/usr/bin/env python3
"""OSC Dashboard Verification Script

Simple script to login to OSC and verify dashboard is accessible.
This script demonstrates:
1. Navigate to OSC login page
2. Enter credentials
3. Handle MFA by direct navigation bypass
4. Verify dashboard elements are present
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from core.browser import BrowserManager
from core.config import settings
from core.logger import Logger
from core.ui import Ui
from core.utils import get_env, now_ts
from locators.osc_locators import DashboardPageLocators, LoginPageLocators, MFAPageLocators

# Load environment variables
load_dotenv()


def verify_osc_dashboard() -> bool:
    """Login to OSC and verify dashboard accessibility.
    
    Returns:
        True if dashboard verification successful, False otherwise
    """
    logger = Logger.get("osc")
    browser_manager = BrowserManager()
    
    logger.info("=" * 60)
    logger.info("OSC Dashboard Verification Started")
    logger.info(f"Target: {get_env('OSC_BASE_URL')}/frmHome.aspx")
    logger.info("=" * 60)
    
    try:
        # Step 1: Launch browser and create page
        logger.info("Step 1: Launching browser")
        browser_manager.launch()  # Need to launch browser first
        context = browser_manager.new_context()
        page = browser_manager.new_page(context)
        ui = Ui(page)
        
        # Step 2: Navigate to login page
        login_url = f"{get_env('OSC_BASE_URL')}/frmHome.aspx"
        logger.info(f"Step 2: Navigating to login page | url={login_url}")
        page.goto(login_url)
        
        # Step 3: Fill login credentials based on environment
        logger.info("Step 3: Entering login credentials")
        from config.osc.config import osc_settings
        username, password = osc_settings.credentials
        
        # Log environment for clarity
        env_info = f"environment={osc_settings.environment}"
        safety_info = f"production_safe={osc_settings.is_production_safe}"
        logger.info(f"Using credentials for {env_info} | {safety_info}")
        
        ui.input_text(LoginPageLocators.USERNAME_FIELD, username)
        ui.input_text(LoginPageLocators.PASSWORD_FIELD, password)
        
        # Step 4: Click login button
        logger.info("Step 4: Submitting login form")
        ui.click(LoginPageLocators.LOGIN_BUTTON)
        
        # Step 5: Handle MFA by direct navigation
        logger.info("Step 5: Handling MFA via direct navigation bypass")
        page.wait_for_load_state()
        
        # Check if we hit MFA page
        current_url = page.url
        if "/mfa/" in current_url or "One-time Passcode" in page.content():
            logger.info("MFA page detected - bypassing with direct navigation")
            dashboard_url = f"{get_env('OSC_BASE_URL')}/frmHome.aspx"
            page.goto(dashboard_url)
            page.wait_for_load_state()
        
        # Step 6: Verify dashboard elements
        logger.info("Step 6: Verifying dashboard elements")
        
        # Check for Home heading
        try:
            ui.wait_visible(DashboardPageLocators.HOME_HEADING, timeout_ms=5000)
            logger.info("✓ Home heading found")
        except Exception:
            logger.error("✗ Home heading not found")
            return False
            
        # Check for Application Summary
        try:
            ui.wait_visible(DashboardPageLocators.APPLICATION_SUMMARY_HEADING, timeout_ms=5000)
            logger.info("✓ Application Summary heading found")
        except Exception:
            logger.error("✗ Application Summary heading not found")
            return False
            
        # Check for navigation menu
        try:
            ui.wait_visible(DashboardPageLocators.LOGOUT_LINK, timeout_ms=5000)
            logger.info("✓ Logout link found")
        except Exception:
            logger.error("✗ Logout link not found")
            return False
        
        # Take success screenshot
        timestamp = now_ts()
        screenshot_path = f"traces/osc_dashboard_success_{timestamp}.png"
        page.screenshot(path=screenshot_path)
        logger.info(f"✓ Success screenshot saved | path={screenshot_path}")
        
        logger.info("=" * 60)
        logger.info("✅ OSC Dashboard Verification SUCCESSFUL")
        logger.info("All required elements verified on dashboard")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Dashboard verification failed | error={e}")
        
        # Take failure screenshot
        try:
            timestamp = now_ts()
            screenshot_path = f"traces/osc_dashboard_failure_{timestamp}.png"
            page.screenshot(path=screenshot_path)
            logger.error(f"Failure screenshot saved | path={screenshot_path}")
        except:
            pass
            
        logger.error("=" * 60)
        logger.error("❌ OSC Dashboard Verification FAILED")
        logger.error("=" * 60)
        
        return False
        
    finally:
        browser_manager.close()


if __name__ == "__main__":
    """Run OSC dashboard verification."""
    success = verify_osc_dashboard()
    sys.exit(0 if success else 1)