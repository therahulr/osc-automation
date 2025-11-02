"""
OSC Application Data Configuration

This file contains all default data used for OSC application workflows.
All values can be overridden at runtime using custom data files or dictionaries.

Data Categories:
- Sales Representatives
- Merchant Information
- Application Settings
- Contact Information
"""

from typing import Dict, Any
from datetime import datetime
from faker import Faker
import random
import string

faker = Faker()

# Sales Representative Configuration
SALES_REPRESENTATIVE = {
    "name": "DEMONET1",
}

MERCHANT_PRODUCTS = [
    "Credit"
]

# Merchant Business Information
MERCHANT_INFO = {
    "legal_business_name": "Rahul " + faker.company_suffix(),
    "dba_name": "Rahul" + faker.company_suffix(),
    "federal_tax_id": str(random.randint(7,9)) + str(random.randint(10**6, 10**7 - 1)),
    "business_type": "LLC",
    "years_in_business": "5",
    "ownership_type": "Private",
    "business_description": "Retail merchandise sales",
    "website": "www.testmerchant.com"
}

# Business Address Information
BUSINESS_ADDRESS = {
    "street_address": "123 Business Ave",
    "suite_unit": "Suite 100",
    "city": "Test City",
    "state": "CA",
    "zip_code": "90210",
    "country": "United States",
    "phone": "(555) 123-4567",
    "fax": "(555) 123-4568"
}

# Mailing Address (if different from business)
MAILING_ADDRESS = {
    "same_as_business": True,
    "street_address": "",
    "suite_unit": "",
    "city": "",
    "state": "",
    "zip_code": "",
    "country": ""
}

# Principal/Owner Information
PRINCIPAL_INFO = {
    "first_name": "John",
    "last_name": "Doe",
    "title": "Owner",
    "ssn": "123-45-6789",
    "date_of_birth": "01/15/1980",
    "home_phone": "(555) 987-6543",
    "mobile_phone": "(555) 987-6544",
    "email": "john.doe@testmerchant.com",
    "ownership_percentage": "100"
}

# Principal Address
PRINCIPAL_ADDRESS = {
    "street_address": "456 Home Street",
    "city": "Test City",
    "state": "CA",
    "zip_code": "90210",
    "country": "United States"
}

# Banking Information
BANKING_INFO = {
    "bank_name": "Test Bank",
    "account_type": "Checking",
    "routing_number": "123456789",
    "account_number": "987654321",
    "account_holder_name": "Test Merchant Solutions LLC"
}

# Processing Information
PROCESSING_INFO = {
    "average_monthly_volume": "50000",
    "average_transaction_amount": "75.00",
    "highest_transaction_amount": "500.00",
    "card_present_percentage": "80",
    "card_not_present_percentage": "20",
    "seasonal_business": False,
    "seasonal_months": []
}

# Product Selection
PRODUCTS = {
    "credit_card": True,
    "debit_card": True,
    "ach": False,
    "ebt": False,
    "check_guarantee": False
}

# Equipment Needs
EQUIPMENT = {
    "terminal_needed": True,
    "terminal_type": "Countertop",
    "quantity": "2",
    "printer_needed": True,
    "pin_pad_needed": True
}

# Application Settings
APPLICATION_SETTINGS = {
    "merchant_choice": "new_corporation",  # new_corporation or existing_merchant
    "auto_submit": False,
    "save_draft": True,
    "notification_email": "test@example.com"
}

# Workflow Control
WORKFLOW_CONTROL = {
    "skip_validation": False,
    "continue_on_error": False,
    "screenshot_on_error": True,
    "max_retries": 3,
    "timeout_seconds": 30
}

# Test Data Variations
TEST_VARIATIONS = {
    "minimal_data": {
        "merchant_info": {
            "legal_business_name": "Quick Test LLC",
            "dba_name": "Quick Test",
            "federal_tax_id": "98-7654321"
        },
        "principal_info": {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@quicktest.com"
        }
    },
    "large_volume": {
        "processing_info": {
            "average_monthly_volume": "500000",
            "average_transaction_amount": "150.00",
            "highest_transaction_amount": "2000.00"
        }
    },
    "restaurant_business": {
        "merchant_info": {
            "business_description": "Restaurant and food service",
            "business_type": "Corporation"
        },
        "processing_info": {
            "card_present_percentage": "95",
            "card_not_present_percentage": "5"
        }
    }
}

# Data validation rules
VALIDATION_RULES = {
    "required_fields": [
        "MERCHANT_INFO.legal_business_name",
        "MERCHANT_INFO.federal_tax_id",
        "PRINCIPAL_INFO.first_name",
        "PRINCIPAL_INFO.last_name",
        "PRINCIPAL_INFO.email",
        "BUSINESS_ADDRESS.street_address",
        "BUSINESS_ADDRESS.city",
        "BUSINESS_ADDRESS.state",
        "BUSINESS_ADDRESS.zip_code"
    ],
    "field_formats": {
        "federal_tax_id": r"^\d{2}-\d{7}$",
        "ssn": r"^\d{3}-\d{2}-\d{4}$",
        "phone": r"^\(\d{3}\) \d{3}-\d{4}$",
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "zip_code": r"^\d{5}(-\d{4})?$"
    }
}

# Custom data override configuration
CUSTOM_DATA_CONFIG = {
    "supported_formats": ["txt", "json", "yaml", "py"],
    "default_format": "txt",
    "custom_data_dir": "data/osc/custom_data",
    "skeleton_filename": "osc_data_skeleton.txt",
    "override_filename": "custom_override.txt"
}


def get_all_data() -> Dict[str, Any]:
    """
    Get all OSC data as a single dictionary
    
    Returns:
        Dict containing all OSC application data
    """
    return {
        "SALES_REPRESENTATIVE": SALES_REPRESENTATIVE,
        "MERCHANT_INFO": MERCHANT_INFO,
        "BUSINESS_ADDRESS": BUSINESS_ADDRESS,
        "MAILING_ADDRESS": MAILING_ADDRESS,
        "PRINCIPAL_INFO": PRINCIPAL_INFO,
        "PRINCIPAL_ADDRESS": PRINCIPAL_ADDRESS,
        "BANKING_INFO": BANKING_INFO,
        "PROCESSING_INFO": PROCESSING_INFO,
        "PRODUCTS": PRODUCTS,
        "EQUIPMENT": EQUIPMENT,
        "APPLICATION_SETTINGS": APPLICATION_SETTINGS,
        "WORKFLOW_CONTROL": WORKFLOW_CONTROL,
        "TEST_VARIATIONS": TEST_VARIATIONS,
        "VALIDATION_RULES": VALIDATION_RULES,
        "CUSTOM_DATA_CONFIG": CUSTOM_DATA_CONFIG
    }


def get_flattened_data() -> Dict[str, Any]:
    """
    Get all data in flattened format for easy override
    
    Returns:
        Dict with flattened keys like 'MERCHANT_INFO.legal_business_name'
    """
    def flatten_dict(d: Dict, prefix: str = "") -> Dict[str, Any]:
        items = []
        for k, v in d.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and k not in ["TEST_VARIATIONS", "VALIDATION_RULES", "CUSTOM_DATA_CONFIG"]:
                items.extend(flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    return flatten_dict(get_all_data())


def get_overridable_fields() -> Dict[str, Any]:
    """
    Get only the fields that should be available for custom override
    
    Returns:
        Dict containing user-configurable fields
    """
    all_data = get_all_data()
    
    # Exclude system configuration from override
    overridable = {k: v for k, v in all_data.items() 
                  if k not in ["VALIDATION_RULES", "CUSTOM_DATA_CONFIG"]}
    
    return overridable


# Convenience functions for specific data access
def get_sales_rep_config() -> Dict[str, Any]:
    """Get sales representative configuration"""
    return SALES_REPRESENTATIVE.copy()


def get_merchant_config() -> Dict[str, Any]:
    """Get merchant information configuration"""
    return {
        "merchant_info": MERCHANT_INFO.copy(),
        "business_address": BUSINESS_ADDRESS.copy(),
        "mailing_address": MAILING_ADDRESS.copy()
    }


def get_principal_config() -> Dict[str, Any]:
    """Get principal/owner configuration"""
    return {
        "principal_info": PRINCIPAL_INFO.copy(),
        "principal_address": PRINCIPAL_ADDRESS.copy()
    }


def get_processing_config() -> Dict[str, Any]:
    """Get processing and product configuration"""
    return {
        "processing_info": PROCESSING_INFO.copy(),
        "products": PRODUCTS.copy(),
        "equipment": EQUIPMENT.copy()
    }


def get_test_variation(variation_name: str) -> Dict[str, Any]:
    """
    Get a specific test data variation
    
    Args:
        variation_name: Name of the test variation
        
    Returns:
        Dict containing the variation data, or empty dict if not found
    """
    return TEST_VARIATIONS.get(variation_name, {})


class OSCDataAccess:
    """
    Data access class for OSC configuration data.
    Provides dot notation access to all configuration values.
    """
    
    def __init__(self):
        self._data = self._build_data_structure()
    
    def _build_data_structure(self) -> Dict[str, Any]:
        """Build the complete data structure"""
        return {
            "sales_rep": SALES_REPRESENTATIVE,
            "merchant": MERCHANT_INFO,
            "business_address": BUSINESS_ADDRESS,
            "mailing_address": MAILING_ADDRESS,
            "principal": PRINCIPAL_INFO,
            "principal_address": PRINCIPAL_ADDRESS,
            "banking": BANKING_INFO,
            "processing": PROCESSING_INFO,
            "products": PRODUCTS,
            "equipment": EQUIPMENT,
            "application_settings": APPLICATION_SETTINGS,
            "workflow_control": WORKFLOW_CONTROL,
            "validation": VALIDATION_RULES,
            "test_variations": TEST_VARIATIONS,
            "custom_data_config": CUSTOM_DATA_CONFIG
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value (e.g., "merchant.business_name")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation
        
        Args:
            key_path: Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        data = self._data
        
        # Navigate to parent dictionary
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]
        
        # Set the value
        data[keys[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data"""
        return self._data.copy()
    
    def get_flattened(self) -> Dict[str, Any]:
        """Get flattened configuration data with dot-notation keys"""
        result = {}
        
        def flatten(obj, prefix=''):
            for key, value in obj.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    flatten(value, new_key)
                else:
                    result[new_key] = value
        
        flatten(self._data)
        return result


# Global data access instance
OSC_DATA = OSCDataAccess()


def get_all_data() -> Dict[str, Any]:
    """Get all OSC configuration data"""
    return OSC_DATA.get_all()


def get_flattened_data() -> Dict[str, Any]:
    """Get flattened OSC configuration data with dot-notation keys"""
    return OSC_DATA.get_flattened()


def get_overridable_fields() -> Dict[str, Any]:
    """Get data fields that can be overridden by custom data"""
    # Return the complete data structure for now
    # In the future, this could be filtered to only return user-overridable fields
    return OSC_DATA.get_all()
