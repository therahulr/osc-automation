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
    "visa": "7000",
    "mastercard": "5000",
    "discover": "3231",
    "amex": "4132",
}

# Generate Credit Card Interchange with QA-specific BET numbers
CREDIT_CARD_INTERCHANGE = generate_credit_card_interchange_data(BET_NUMBERS)

# =============================================================================
# QA SERVICES - CREDIT CARD
# =============================================================================
CREDIT_CARD_SERVICES = [
    "Mobile Merchant",
    # "Account Updater V2",
    "Interchange Advantage Program",
    # "Verisign Merchant",
    # "Sage Gateway (Credit Card)",
    # "Advance Funding",
    # "Leasing",
    # "Sage Mobile Payments",
    # "Terminal Replacement Program",
    # "Chargeback & Loss Recovery Program",
    # "Sage Mobile Invoice Present & Pay",
    # "Amex OnePoint",
    # "Advanced Fraud Protection",
    # "Point to Point Encryption",
    # "EMV Mobile",
    # "Stmt Mailing and Handling",
    # "Flat Rate",
    # "Paya Connect Hosted Payment",
    # "Paya Connect Donation",
    # "Paya Connect TPP",
    # "Paya Connect Virtual Terminal",
    # "Paya Connect Recurring/Vault",
    # "Paya Connect Quick Invoice",
    # "Paya Connect Vault",
    # "Paya Connect Surcharge",
    # "Paya Connect Account Updater",
    # "Paya Connect Level 3/IAP",
    # "Service Fee Model",
    # "Paya Connect Vault Migration",
    # "Convenience Fee Model",
    # "3rd Party Gateway",
    # "Commerce Suite",
    # "ERP Fee Recovery",
    # "ERP Portal Standalone Fee",
    # "AP Automation - ACH Payouts",
    # "AP Automation - Paper Checks",
    # "AP Automation Fee",
    "Commerce Suite Bundle",
    # "Business Coach Trial"
]

# =============================================================================
# QA SERVICES - ACH
# =============================================================================
ACH_SERVICES = [
    "EFT Virtual Check Consumer Initiated (EFTVCCI)",
    "EFT Virtual Check Merchant Initiated (EFTVCMI)"
]

# =============================================================================
# QA FEE LISTS
# =============================================================================
# Credit Card related fees for QA
_QA_CREDIT_FEE_NAMES = [
    # "MC Infrastructure Fee",
    # "Misuse of Authorization Fee for Visa",
    # "Network Fee for Amex",
    # "Non-Swiped/Digital Wallet Fee for Amex",
    # "VS Infrastructure Fee",
    # "Zero Floor Limit Fee for Visa",
    # "Account Updater Enrollment Fee",
    # "Account Updater Per Item Fee for Visa",
    # "Account Updater Per Item Fee for Amex",
    # "Account Updater Per Item Fee for Discover",
    # "Account Updater Per Item Fee for MasterCard",
    # "Acquirer Processing Fee for Visa",
    # "Advanced Fraud Protection Per Item",
    # "Annual Assessment",
    # "AP Automation Return Fee - ACH",
    # "AP Automation Reversal Fee - ACH",
    # "AP Automation Tran Fee - ACH",
    # "AP Automation Tran Fee – Paper Check",
    # "Business Coach",
    # "Complimentary Online Reporting",
    # "Data Integrity Fee for Visa",
    # "ERP Fee Recovery",
    # "Inbound Fee for Amex",
    # "Level III Data",
    # "Magtek decrypt annual fee",
    # "MC Cyber Secure Fee",
    # "MSP Network Fee",
    # "Network Access & Brand Usage for MasterCard",
    # "PCI DSS Annual Fee",
    # "PCI DSS Non Compliance",
    # "Retrieval Fee",
    # "Sage Mobile Payments 2011/12 Promotion",
    # "SE Connection",
    # "Standard P2PE - Per Transaction Fee",
    "Account Updater Monthly Fee",
    # "Advanced Fraud Protection Monthly",
    # "AP Automation Fee",
    # "Click2Pay",
    # "Commerce Suite",
    # "Commerce Suite Bundle Fee",
    # "EMV Mobile Monthly",
    # "EnsureBill - Monthly Fee",
    # "Merchant location Fee for MasterCard",
    # "Monthly Clearing",
    # "Monthly Interchange Adv Pgrm fee",
    "Monthly Minimum",
    "Monthly Processing Fee",
    "Monthly Program Fee",
    "Monthly Statement",
    # "Monthly Voltage Encryption Fee Per Device",
    # "PCI Monthly Fee",
    # "Sage Exchange Couponing and Messaging",
]

# ACH related fees for QA
_QA_ACH_FEE_NAMES = [
    "Application ACH",
    "Additional Originator ID",
    "Expedite",
]

# Generate fee lists with random amounts
CREDIT_FEE_LIST = generate_fee_list(_QA_CREDIT_FEE_NAMES)
ACH_FEE_LIST = generate_fee_list(_QA_ACH_FEE_NAMES)
