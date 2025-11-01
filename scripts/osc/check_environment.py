#!/usr/bin/env python3
"""Environment validation and safety check script."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from config.osc.config import osc_settings
from core.logger import Logger

# Load environment variables
load_dotenv()

def main() -> None:
    """Validate environment configuration and show safety status."""
    logger = Logger.get("env_check")
    
    logger.info("=== OSC Environment Validation ===")
    logger.info(f"Environment: {osc_settings.environment}")
    logger.info(f"Production Safe: {osc_settings.is_production_safe}")
    
    username, password = osc_settings.credentials
    logger.info(f"Username: {username}")
    logger.info(f"Password: {'*' * len(password)}")
    
    # Environment-specific warnings
    if osc_settings.environment == "prod":
        logger.warning("🚨 PRODUCTION ENVIRONMENT DETECTED")
        logger.warning("⚠️  READ-ONLY MODE: Do not submit/save any data")
        logger.warning("📝 Use this only for automation development and testing")
        logger.info("💡 To switch to QA: Set OSC_ENV=qa in your .env file")
    
    elif osc_settings.environment == "qa":
        logger.info("✅ QA ENVIRONMENT DETECTED")
        logger.info("🔓 Full operations allowed: Submit, save, modify data")
        logger.info("🏢 Suitable for org laptop with QA credentials")
    
    else:
        logger.error(f"❌ Unknown environment: {osc_settings.environment}")
        logger.error("Valid options: 'prod' or 'qa'")
        sys.exit(1)
    
    logger.info("=== Configuration Valid ===")

if __name__ == "__main__":
    main()