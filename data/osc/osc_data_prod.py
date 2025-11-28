"""
OSC Test Data - PROD Environment

Production environment test data with PROD-specific BET numbers and business names.
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
    generate_prod_business_names,
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
# PROD ENVIRONMENT SPECIFIC DATA
# =============================================================================

# Generate PROD-specific business names
_prod_legal_name, _prod_dba = generate_prod_business_names()

# Override CORPORATE_INFO with PROD-specific legal business name
CORPORATE_INFO = {**_CORPORATE_INFO, "legal_business_name": _prod_legal_name}

# Override LOCATION_INFO with PROD-specific DBA
LOCATION_INFO = {**_LOCATION_INFO, "dba": _prod_dba}


# BET Numbers for PROD environment
BET_NUMBERS = {
    "visa": "7291",
    "mastercard": "5291",
    "discover": "3191",
    "amex": "4128",
}

# Generate Credit Card Interchange with PROD-specific BET numbers
CREDIT_CARD_INTERCHANGE = generate_credit_card_interchange_data(BET_NUMBERS)

# =============================================================================
# PROD SERVICES - CREDIT CARD
# =============================================================================
CREDIT_CARD_SERVICES = [
    "Mobile Merchant",
    "Interchange Advantage Program",
    "Commerce Suite Bundle",
]

# =============================================================================
# PROD SERVICES - ACH
# =============================================================================
ACH_SERVICES = [
    "EFT Virtual Check Consumer Initiated (EFTVCCI)",
    "EFT Virtual Check Merchant Initiated (EFTVCMI)"
]

# =============================================================================
# PROD FEE LISTS
# =============================================================================
# Credit Card related fees for PROD
_PROD_CREDIT_FEE_NAMES = [
    "AP Automation Return Fee - ACH",
    "AP Automation Reversal Fee - ACH",
    "AP Automation Tran Fee - ACH",
    "AP Automation Tran Fee - Paper Check",
    "Business Coach",
    "MSP Network Fee",
    "Retrieval Fee",
    "AP Automation Fee",
    "Click2Pay",
    "Click2Pay Premium",
    "Commerce Bundle Fee",
    "Monthly Processing Fee",
    "PCI Monthly Fee",
    "Application Credit",
    "Wireless Set Up",
    "Teletraining - Physical",
    "Teletraining - Virtual",
    "Expedite",
    "Lease/Rental Deposit",
    "PCI Compliant Encryption - Key Injection Fee",
    "P2PE Setup Services Fee",
    "Interchange Adv Pgrm enrollment fee",
    "Set Up Fee",
]

# ACH related fees for PROD
_PROD_ACH_FEE_NAMES = [
    "Application ACH",
    "Virtual Teletraining",
    "Additional Originator ID",
    "Expedite",
]

_DEBIT_CARD_FEE_NAMES = [
    "Annual Pin Debit Fee",
        "Debit Access",
        "Monthly Minimum Debit",
        "Pin Debit Discount %",
        "Application Debit",
        "Teletraining - Virtual",
        "Expedite",
        "Teletraining - Physical",
        "Injection"
]


# Generate fee lists with random amounts
CREDIT_FEE_LIST = generate_fee_list(_PROD_CREDIT_FEE_NAMES)
ACH_FEE_LIST = generate_fee_list(_PROD_ACH_FEE_NAMES)
