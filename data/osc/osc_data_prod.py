"""
OSC Test Data - PROD Environment

Production environment test data with PROD-specific BET numbers and business type.
Imports all common data from common_test_data.py.
"""

from data.osc.common_test_data import (
    # Dropdown options
    DropdownOptions,
    
    # Helper functions
    generate_phone_digits,
    generate_fax_digits,
    generate_random_date_past,
    generate_dunns_number,
    generate_federal_tax_id,
    generate_ssn_digits,
    generate_dob_digits,
    generate_date_of_ownership_digits,
    generate_rate_value,
    generate_annual_volume,
    
    # Data generators
    generate_credit_card_underwriting_data,
    generate_credit_card_interchange_data,
    
    # Common data exports
    APPLICATION_INFO,
    CORPORATE_INFO,
    LOCATION_INFO,
    TAX_INFO,
    OWNER1_INFO,
    OWNER2_INFO,
    TRADE_REFERENCE_INFO,
    BILLING_QUESTIONNAIRE_INFO,
    BANK_INFORMATION,
    CREDIT_CARD_INFORMATION,
    CREDIT_CARD_SERVICES,
    SALES_REPRESENTATIVE,
    MERCHANT_PRODUCTS,
)


# =============================================================================
# PROD ENVIRONMENT SPECIFIC DATA
# =============================================================================

# Business type for PROD
BUSINESS_TYPE = "Retail"

# General Underwriting with PROD business type
GENERAL_UNDERWRITING_INFO = {
    "business_type": BUSINESS_TYPE,
    "sic_code": "7311",
    "products_sold": "General retail merchandise and consumer goods",
    "return_policy": "30 Days Money Back Guarantee",
    "days_until_delivery": "5",
    "seasonal_months": [],
}

# BET Numbers for PROD environment
BET_NUMBERS = {
    "visa": "7291",
    "mastercard": "5291",
    "discover": "3191",
    "amex": "4128",
}

# Generate environment-specific data
CREDIT_CARD_UNDERWRITING = generate_credit_card_underwriting_data(BUSINESS_TYPE)
CREDIT_CARD_INTERCHANGE = generate_credit_card_interchange_data(BET_NUMBERS)
