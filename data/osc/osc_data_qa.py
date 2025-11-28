"""
OSC Test Data - QA Environment

QA environment test data with QA-specific BET numbers and business names.
All common data is imported from common_test_data.py.
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
    generate_fee_amount,
    generate_qa_business_names,
    generate_fee_list,
    
    # Data generators
    generate_credit_card_underwriting_data,
    generate_credit_card_interchange_data,
    generate_ach_underwriting_data,
    generate_ach_fees_data,
    generate_ach_originator_data,
    
    # Common data exports (will be modified below)
    APPLICATION_INFO,
    CORPORATE_INFO as _CORPORATE_INFO,
    LOCATION_INFO as _LOCATION_INFO,
    TAX_INFO,
    OWNER1_INFO,
    OWNER2_INFO,
    TRADE_REFERENCE_INFO,
    BILLING_QUESTIONNAIRE_INFO,
    BANK_INFORMATION,
    CREDIT_CARD_INFORMATION,
    CREDIT_CARD_SERVICES,
    ACH_SERVICES,
    ACH_UNDERWRITING,
    ACH_FEES,
    ACH_TRANSACTION_TYPES,
    ACH_ORIGINATOR,
    SALES_REPRESENTATIVE,
    MERCHANT_PRODUCTS,
    BUSINESS_TYPE,
    GENERAL_UNDERWRITING_INFO,
    CREDIT_CARD_UNDERWRITING,
    
    # Exported variables for coordination
    MERCHANT_TYPE,
    OWNERSHIP_TYPE,
)


# =============================================================================
# QA ENVIRONMENT SPECIFIC DATA
# =============================================================================

# Generate QA-specific business names
_qa_legal_name, _qa_dba = generate_qa_business_names()

# Override CORPORATE_INFO with QA-specific legal business name
CORPORATE_INFO = {**_CORPORATE_INFO, "legal_business_name": _qa_legal_name}

# Override LOCATION_INFO with QA-specific DBA
LOCATION_INFO = {**_LOCATION_INFO, "dba": _qa_dba}


# BET Numbers for QA environment
BET_NUMBERS = {
    "visa": "8693",
    "mastercard": "6693",
    "discover": "3192",
    "amex": "4884",
}

# Generate Credit Card Interchange with QA-specific BET numbers
CREDIT_CARD_INTERCHANGE = generate_credit_card_interchange_data(BET_NUMBERS)


# =============================================================================
# QA FEE LISTS
# =============================================================================
# Credit Card related fees for QA
_QA_CREDIT_FEE_NAMES = [
    "MC Infrastructure Fee",
    "Visa Acquirer Processing Fee (APF)",
    "Visa FANF Fee",
    "Visa NCCF Fee",
    "MC NABU Fee",
    "MC AAF Fee",
]

# ACH related fees for QA
_QA_ACH_FEE_NAMES = [
    "ACH Reject Fee",
    "ACH NSF Fee",
    "ACH Unauthorized Fee",
]

# Generate fee lists with random amounts
CREDIT_FEE_LIST = generate_fee_list(_QA_CREDIT_FEE_NAMES)
ACH_FEE_LIST = generate_fee_list(_QA_ACH_FEE_NAMES)
