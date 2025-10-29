#!/usr/bin/env python3
"""Main OSC automation script for login workflow.

This script demonstrates the complete OSC login automation including:
1. Navigate to OSC login page
2. Enter username and password 
3. Click login button
4. Handle MFA by bypassing to dashboard
5. Verify dashboard is loaded
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from apps.osc.pages.login_page import LoginPage
from core.browser import BrowserManager
from core.config import settings
from core.logger import Logger
from core.utils import ensure_dir, get_env, now_ts

# Load environment variables
load_dotenv()


def main() -> None:
    """Execute main OSC automation workflow."""
    logger = Logger.get("osc")
    browser_manager = BrowserManager()

    logger.info("=" * 80)
    logger.info("Starting OSC Automation - Main Workflow")
    logger.info(f"Settings | headless={settings.headless}, trace={settings.trace_enabled}")
    logger.info("=" * 80)

    try:
        # Get credentials from environment
        username = get_env("OSC_USER", "contractordemo")
        password = get_env("OSC_PASS", "QAContractor@123")

        logger.info(f"Using credentials | username={username}")

        # ====================================================================
        # STEP 1: Launch browser with maximized window
        # ====================================================================
        logger.info("STEP 1: Launching browser")
        browser_manager.launch()
        
        # Create context with maximized viewport
        context = browser_manager.new_context(viewport={"width": 1920, "height": 1080})
        page = browser_manager.new_page(context)

        logger.info("✓ Browser launched successfully")

        # ====================================================================
        # STEP 2: Navigate to login page and perform login
        # ====================================================================
        logger.info("STEP 2: Performing login")
        login_page = LoginPage(page)

        # Navigate to login page
        login_page.open()
        logger.info(f"✓ Navigated to login page: {login_page.settings.login_url}")

        # Perform login (includes MFA bypass)
        login_page.login(username, password)
        logger.info("✓ Login completed successfully (MFA bypassed)")

        # ====================================================================
        # STEP 3: Verify dashboard is loaded
        # ====================================================================
        logger.info("STEP 3: Verifying dashboard loaded")
        login_page.verify_home_page()
        logger.info("✓ Dashboard verified - Home page is loaded")

        # ====================================================================
        # SUCCESS: Take screenshot
        # ====================================================================
        screenshot_dir = ensure_dir(Path(__file__).parent.parent / "reports")
        screenshot_path = screenshot_dir / f"success_{now_ts()}.png"
        login_page.ui.screenshot(str(screenshot_path))
        logger.info(f"✓ Success screenshot saved: {screenshot_path}")

        logger.info("=" * 80)
        logger.info("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)

        # TODO: Add more workflow steps here as needed
        # Example:
        # logger.info("STEP 4: Navigate to Work In Progress")
        # wip_page = WorkInProgressPage(page)
        # wip_page.open()
        # logger.info("✓ Work In Progress page loaded")

    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"❌ WORKFLOW FAILED: {e}")
        logger.error("=" * 80)

        # Error screenshot
        try:
            screenshot_dir = ensure_dir(Path(__file__).parent.parent / "reports")
            screenshot_path = screenshot_dir / f"error_{now_ts()}.png"
            login_page.ui.screenshot(str(screenshot_path))
            logger.info(f"Error screenshot saved: {screenshot_path}")
        except Exception as screenshot_error:
            logger.warning(f"Failed to capture error screenshot: {screenshot_error}")

        raise

    finally:
        # Always cleanup browser resources
        logger.info("Cleaning up browser resources")
        browser_manager.close()
        logger.info("Browser closed")


if __name__ == "__main__":
    try:
        main()
        print("\n🎉 Script completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Script failed: {e}")
        sys.exit(1)
