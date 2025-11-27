"""
Test Runner

Simple test script to verify the OSC automation framework components.
Tests imports, configuration, and basic functionality.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.logger import setup_logging, get_logger
from utils.config import config
from config.osc.config import get_osc_data
from utils.custom_data import CustomDataManager


async def test_imports():
    """Test that all imports work correctly"""
    logger = get_logger(__name__)
    logger.info("Testing imports...")
    
    try:
        # Test page imports
        from pages import BasePage, OSCNavigation, LoginPage, HomePage
        logger.info("✅ Page classes imported successfully")
        
        # Test script imports
        from scripts.osc.create_credit_card_merchant import create_credit_card_merchant
        logger.info("✅ Workflow script imported successfully")
        
        # Test data access
        osc_data = get_osc_data()
        sales_rep = osc_data.SALES_REPRESENTATIVE.get('name', 'N/A')
        logger.info(f"✅ Data access working: {sales_rep}")
        
        # Test config access
        headless = config.get('browser.headless')
        logger.info(f"✅ Config access working: headless={headless}")
        
        # Test custom data manager
        data_manager = CustomDataManager()
        logger.info("✅ Custom data manager created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import test failed: {str(e)}")
        return False


def test_config():
    """Test configuration system"""
    logger = get_logger(__name__)
    logger.info("Testing configuration...")
    
    try:
        # Test basic config access
        browser_config = config.browser_config
        osc_config = config.osc_config
        
        logger.info(f"Browser config: {browser_config}")
        logger.info(f"OSC config: {osc_config}")
        
        # Test config setting
        config.set('test.value', 'test_data')
        test_value = config.get('test.value')
        
        if test_value == 'test_data':
            logger.info("✅ Config set/get working")
            return True
        else:
            logger.error("❌ Config set/get failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Config test failed: {str(e)}")
        return False


def test_data_system():
    """Test data management system"""
    logger = get_logger(__name__)
    logger.info("Testing data system...")
    
    try:
        # Test default data access
        osc_data = get_osc_data()
        merchant_name = osc_data.CORPORATE_INFO.get('business_name', 'N/A')
        principal_name = osc_data.OWNER1_INFO.get('first_name', 'N/A')
        
        logger.info(f"Merchant name: {merchant_name}")
        logger.info(f"Principal name: {principal_name}")
        
        # Test custom data manager
        data_manager = CustomDataManager()
        
        # Test skeleton generation
        skeleton_data = data_manager.generate_skeleton()
        
        if 'sales_rep' in skeleton_data and 'merchant' in skeleton_data:
            logger.info("✅ Data skeleton generation working")
            return True
        else:
            logger.error("❌ Data skeleton generation failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Data system test failed: {str(e)}")
        return False


async def main():
    """Main test runner"""
    
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    logger.info("🚀 Starting OSC Automation Framework Tests")
    logger.info("=" * 50)
    
    tests = [
        ("Imports", test_imports()),
        ("Configuration", test_config()),
        ("Data System", test_data_system())
    ]
    
    results = []
    
    for test_name, test_coro in tests:
        logger.info(f"\n📋 Running {test_name} test...")
        
        if asyncio.iscoroutine(test_coro):
            result = await test_coro
        else:
            result = test_coro
            
        results.append((test_name, result))
        
        if result:
            logger.info(f"✅ {test_name} test PASSED")
        else:
            logger.error(f"❌ {test_name} test FAILED")
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Summary:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"  {test_name}: {status}")
    
    logger.info(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Framework is ready to use.")
        return True
    else:
        logger.error("❌ Some tests failed. Please check the logs above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)