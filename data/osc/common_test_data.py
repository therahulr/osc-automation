"""
Common Test Data - Shared data for all OSC environments (QA/PROD)

This file contains all common test data used across environments.
Environment-specific data (BET numbers, business type) should be defined
in the respective osc_data_qa.py or osc_data_prod.py files.
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from faker import Faker
import random

faker = Faker()


# =============================================================================
# DROPDOWN OPTIONS
# =============================================================================
class DropdownOptions:
    """All available dropdown options across the application"""
    
    ASSOCIATION_OPTIONS = ["Big Association", "DEMO NET1", "TestWelcomeEmails"]
    
    LEAD_SOURCE_OPTIONS = ["AdvanceMe", "Merchant Call In", "Referral", "Rocky Gingg", "Yellow Pages"]
    
    REFERRAL_PARTNER_OPTIONS = ["None", "Test Troy1"]
    
    COUNTRY_OPTIONS = ["Canada", "United States"]
    
    STATE_OPTIONS = [
        "Please select...", "NA", "Alaska", "Alabama", "Arkansas", "Arizona",
        "California", "Colorado", "Connecticut", "Dist. of Columbia", "Delaware",
        "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois",
        "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland",
        "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana",
        "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
        "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont",
        "Washington", "Wisconsin", "West Virginia", "Wyoming", "Alberta",
        "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador",
        "Nova Scotia", "Northwest Territories", "Nunavut", "Ontario",
        "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"
    ]
    
    US_STATES = [
        "Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa",
        "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana",
        "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri",
        "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska",
        "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York",
        "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
        "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
        "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"
    ]
    
    OWNERSHIP_TYPE_OPTIONS = [
        "C Corporation", "Government (Fed,St,Local)", "LLC- C Corp",
        "LLC- Disregarded Entity", "LLC- Partnership", "LLC- S Corp",
        "LLC- Sole Proprietor", "Non-Profit", "Non-US Entity", "Partnership",
        "S Corporation", "Sole Proprietor", "Trust/Estate", "Please select..."
    ]
    
    BUSINESS_TYPE_OPTIONS = ["Grocery", "GSA", "Hotel/Restaurant", "MOTO", "Retail"]
    
    SIC_CODE_LIST = ['7311', '7321', '3030']
    
    RETURN_POLICY_OPTIONS = [
        "30 Days Money Back Guarantee", "30 Days Exchange Only",
        "60 Days Money Back Guarantee", "60 Days Exchange Only",
        "90 Days Money Back Guarantee", "90 Days Exchange Only", "Other"
    ]
    
    TAX_FILING_STATE_OPTIONS = STATE_OPTIONS
    
    TITLE_OPTIONS = [
        "CEO", "CFO", "COO", "President", "Vice President",
        "Owner", "Partner", "Manager", "Director", "Secretary", "Treasurer"
    ]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def generate_phone_digits() -> str:
    """Generate a 10-digit phone number"""
    area_code = random.randint(200, 999)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"{area_code}{prefix}{line}"


def generate_fax_digits() -> str:
    """Generate a 10-digit fax number"""
    return generate_phone_digits()


def generate_random_date_past(years_back: int = 10) -> str:
    """
    Generate a random past date (mmddyyyy format).
    
    Ensures mm and dd start with non-zero digit (10-12 for month, 10-28 for day)
    to avoid issues with masked date input fields that can mishandle leading zeros.
    """
    # Generate month 10-12 (October, November, December) to avoid leading zeros
    month = random.randint(10, 12)
    # Generate day 10-28 to avoid leading zeros and stay safe for all months
    day = random.randint(10, 28)
    # Generate year (years_back years ago to 1 year ago)
    current_year = datetime.now().year
    year = random.randint(current_year - years_back, current_year - 1)
    return f"{month:02d}{day:02d}{year}"


def generate_dunns_number() -> str:
    """Generate a random 9-digit D&B number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])


def generate_federal_tax_id() -> str:
    """Generate a 9-digit Federal Tax ID"""
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])


def generate_ssn_digits() -> str:
    """Generate a 9-digit SSN"""
    first = random.randint(100, 665)
    if first == 666:
        first = 667
    second = random.randint(1, 99)
    third = random.randint(1, 9999)
    return f"{first:03d}{second:02d}{third:04d}"


def generate_dob_digits(min_age: int = 25, max_age: int = 65) -> str:
    """
    Generate date of birth (mmddyyyy format for US date entry).
    
    Ensures mm and dd start with non-zero digit (10-12 for month, 10-28 for day)
    to avoid issues with masked date input fields that can mishandle leading zeros.
    """
    # Generate month 10-12 to avoid leading zeros
    month = random.randint(10, 12)
    # Generate day 10-28 to avoid leading zeros
    day = random.randint(10, 28)
    # Generate year based on age range
    current_year = datetime.now().year
    year = random.randint(current_year - max_age, current_year - min_age)
    return f"{month:02d}{day:02d}{year}"


def generate_date_of_ownership_digits(years_back: int = 10) -> str:
    """
    Generate date of ownership (mmddyyyy format for US date entry).
    
    Ensures mm and dd start with non-zero digit (10-12 for month, 10-28 for day)
    to avoid issues with masked date input fields that can mishandle leading zeros.
    """
    # Generate month 10-12 to avoid leading zeros
    month = random.randint(10, 12)
    # Generate day 10-28 to avoid leading zeros
    day = random.randint(10, 28)
    # Generate year (years_back years ago to 1 year ago)
    current_year = datetime.now().year
    year = random.randint(current_year - years_back, current_year - 1)
    return f"{month:02d}{day:02d}{year}"


def generate_rate_value() -> str:
    """Generate a random rate value (X.XXX format)"""
    whole = random.randint(0, 9)        
    decimal = random.randint(0, 999)
    return f"{whole}.{decimal:03d}"


def generate_annual_volume() -> str:
    """Generate a random annual volume"""
    volume = round(random.uniform(1000.00, 99999.99), 2)
    return f"{volume:.2f}"


def generate_fee_amount() -> str:
    """Generate a random fee amount (1.00 to 99.99)"""
    amount = round(random.uniform(1.00, 99.99), 2)
    return f"{amount:.2f}"


def generate_qa_business_names() -> tuple:
    """
    Generate QA-specific business names with QA prefix pattern.
    Returns tuple: (legal_business_name, dba)
    """
    legal_name_base = faker.company()
    dba_base = faker.company()
    legal_name = f"QA Test {legal_name_base}"
    dba = f"QA Rahul Test {dba_base} " + random.choice(["Store", "Shop", "Center", "Outlet"])
    return legal_name, dba


def generate_prod_business_names() -> tuple:
    """
    Generate PROD-specific business names with PROD prefix pattern.
    Returns tuple: (legal_business_name, dba)
    """
    company_base = faker.company()
    legal_name = f"Automation {company_base} LLC"
    dba = f"Auto {company_base} " + random.choice(["Services", "Solutions", "Group", "Corp"])
    return legal_name, dba


# =============================================================================
# APPLICATION INFO
# =============================================================================
APPLICATION_INFO = {
    "office": "DEMO NET1",
    "phone": "7038529999",
    "contractor": "DEMONET1",
    "association": "TestWelcomeEmails",
    "lead_source": "Yellow Pages",
    "referral_partner": "None",
    "promo_code": "",
    "corporate_atlas_id": ""
}


# =============================================================================
# CORPORATE INFORMATION
# =============================================================================
# Note: legal_business_name is set by environment-specific data (QA/PROD)
CORPORATE_INFO = {
    "legal_business_name": "",  # Set by QA/PROD specific data
    "address": faker.street_address(),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "fax": generate_fax_digits(),
    "email": "rahul.raj@nuvei.com",
    "dunns_number": generate_dunns_number(),
    "contact_title": random.choice(["CEO", "President", "Owner", "Manager", "Director"]),
    "contact_first_name": faker.first_name(),
    "contact_last_name": faker.last_name(),
    "use_different_location": True,
}


# =============================================================================
# LOCATION INFORMATION
# =============================================================================
# Note: dba is set by environment-specific data (QA/PROD)
LOCATION_INFO = {
    "dba": "",  # Set by QA/PROD specific data
    "address": faker.street_address(),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "fax": generate_fax_digits(),
    "customer_service_phone": generate_phone_digits(),
    "website": "www.nuvei.com",
    "email": faker.email(),
    "chargeback_email": "rahul.raj@nuvei.com",
    "business_open_date": generate_random_date_past(years_back=15),
    "existing_sage_mid": "",
    "general_comments": faker.sentence(nb_words=10),
}


# =============================================================================
# TAX INFORMATION
# =============================================================================
# Generate ownership type first as it affects owner equity
_ownership_type = random.choice([
    "C Corporation", "S Corporation", "LLC- C Corp", "LLC- S Corp", "Sole Proprietor"
])

TAX_INFO = {
    "federal_tax_id": generate_federal_tax_id(),
    "tax_filing_corp_name": faker.company() + " Holdings Inc",
    "ownership_type": _ownership_type,
    "tax_filing_state": "Georgia",
    "is_corp_headquarters": True,
    "is_foreign_entity": False,
    "authorize_1099": True,
}


# =============================================================================
# OWNER EQUITY CALCULATION
# Based on ownership type:
# - Sole Proprietor: Owner 1 = 100%, Owner 2 = 0%
# - Other types: Random split
# =============================================================================
if _ownership_type == "Sole Proprietor":
    _owner1_equity = 100
    _owner2_equity = 0
else:
    _owner1_equity = random.randint(20, 90)
    _owner2_equity = 100 - _owner1_equity


# =============================================================================
# OWNER/OFFICER 1 INFORMATION
# =============================================================================
OWNER1_INFO = {
    "title": random.choice(DropdownOptions.TITLE_OPTIONS),
    "first_name": "Rahul",
    "last_name": "Raj",
    "address1": faker.street_address(),
    "address2": faker.secondary_address(),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "fax": generate_fax_digits(),
    "email": "rahul.raj@nuvei.com",
    "dob": generate_dob_digits(min_age=25, max_age=65),
    "ssn": generate_ssn_digits(),
    "date_of_ownership": generate_date_of_ownership_digits(years_back=10),
    "equity": str(_owner1_equity),
}


# =============================================================================
# OWNER/OFFICER 2 INFORMATION
# =============================================================================
_owner2_first_name = faker.first_name()
_owner2_last_name = faker.last_name()

OWNER2_INFO = {
    "title": random.choice(DropdownOptions.TITLE_OPTIONS),
    "first_name": _owner2_first_name,
    "last_name": _owner2_last_name,
    "address1": faker.street_address(),
    "address2": faker.secondary_address(),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "fax": generate_fax_digits(),
    "email": f"{_owner2_first_name.lower()}.{_owner2_last_name.lower()}@email.com",
    "dob": generate_dob_digits(min_age=25, max_age=65),
    "ssn": generate_ssn_digits(),
    "date_of_ownership": generate_date_of_ownership_digits(years_back=10),
    "equity": str(_owner2_equity),
}


# =============================================================================
# TRADE REFERENCE INFORMATION
# =============================================================================
TRADE_REFERENCE_INFO = {
    "title": random.choice(["Vendor", "Supplier", "Partner", "Contractor", "Distributor"]),
    "name": faker.company(),
    "address": faker.street_address(),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "email": faker.company_email(),
}


# =============================================================================
# BILLING QUESTIONNAIRE
# Generate merchant_type first as it affects Credit Card Underwriting
# =============================================================================
_merchant_type = random.choice(["internet", "moto", "retail"])

BILLING_QUESTIONNAIRE_INFO = {
    "merchant_type": _merchant_type,
    "full_payment_upfront": True,
    "full_payment_days": str(random.randint(1, 30)),
    "partial_payment_upfront": True,
    "partial_payment_percentage": str(random.randint(10, 90)),
    "partial_payment_days": str(random.randint(1, 30)),
    "payment_after_delivery": True,
    "billing_monthly": False,
    "billing_quarterly": True,
    "billing_semi_annually": False,
    "billing_annually": False,
    "outsourced_to_third_party": True,
    "outsourced_explanation": "Outsourced billing to third party provider for efficiency.",
}


# =============================================================================
# BANK INFORMATION
# =============================================================================
BANK_INFORMATION = {
    "bank_name": "Test Bank " + faker.company_suffix(),
    "address1": faker.street_address(),
    "address2": "Suite " + str(random.randint(100, 999)),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "routing_number": "061000052",
    "account_number": "61000543270",
}


# =============================================================================
# CREDIT CARD INFORMATION
# =============================================================================
CREDIT_CARD_INFORMATION = {
    "authorization_network": "Visanet/TSYS",
    "settlement_bank": "Citizens Bank, N.A.",
    "settlement_network": "Vital",
    "discount_paid": "Monthly",
    "user_bank": "3948",
}


# =============================================================================
# CREDIT CARD UNDERWRITING GENERATOR
# =============================================================================
def generate_credit_card_underwriting_data(
    business_type: str = "Retail",
    merchant_type: str = "retail"
) -> Dict[str, Any]:
    """Generate Credit Card Underwriting data with proper business logic.
    
    Args:
        business_type: The business type (e.g., "Retail", "Grocery", etc.)
        merchant_type: The merchant type from billing questionnaire 
                      ("internet", "moto", "retail")
    """
    percentage_options = list(range(0, 101, 5))
    is_retail_or_grocery = business_type.lower() in ["retail", "grocery"]
    is_internet_or_moto = merchant_type.lower() in ["internet", "moto"]
    
    # Card Not Present logic:
    # - If merchant_type is "internet" or "moto", Card Not Present must be >= 70%
    # - If business_type is "retail" or "grocery", Card Not Present must be <= 30%
    if is_internet_or_moto:
        # Internet/MOTO merchants need Card Not Present >= 70%
        card_not_present_options = [p for p in percentage_options if p >= 70]
        card_not_present = random.choice(card_not_present_options)
    elif is_retail_or_grocery:
        # Retail/Grocery merchants need Card Not Present <= 30%
        card_not_present_options = [p for p in percentage_options if p <= 30]
        card_not_present = random.choice(card_not_present_options)
    else:
        card_not_present = random.choice(percentage_options)
    
    remaining = 100 - card_not_present
    valid_swiped_options = [p for p in percentage_options if p <= remaining]
    card_present_swiped = random.choice(valid_swiped_options)
    card_present_keyed = remaining - card_present_swiped
    
    if card_present_keyed not in percentage_options:
        card_present_keyed = min(percentage_options, key=lambda x: abs(x - card_present_keyed))
        card_present_swiped = remaining - card_present_keyed
        if card_present_swiped < 0:
            card_present_swiped = 0
            card_present_keyed = remaining
    
    consumer_sales = random.choice(percentage_options)
    remaining_sales = 100 - consumer_sales
    valid_business_options = [p for p in percentage_options if p <= remaining_sales]
    business_sales = random.choice(valid_business_options) if valid_business_options else 0
    government_sales = remaining_sales - business_sales
    
    if government_sales not in percentage_options:
        government_sales = min(percentage_options, key=lambda x: abs(x - government_sales))
        business_sales = remaining_sales - government_sales
        if business_sales < 0:
            business_sales = 0
            government_sales = remaining_sales
    
    average_ticket = round(random.uniform(10.00, 999.99), 2)
    min_volume = max(average_ticket + 1, 100.00)
    max_volume = 99999.99
    monthly_volume = round(random.uniform(min_volume, max_volume), 2)
    highest_ticket = round(random.uniform(average_ticket, min(monthly_volume, average_ticket * 10)), 2)
    
    def format_percent(value: int) -> str:
        return f"{value} %"
    
    return {
        "monthly_volume": f"{monthly_volume:.2f}",
        "average_ticket": f"{average_ticket:.2f}",
        "highest_ticket": f"{highest_ticket:.2f}",
        "card_present_swiped": format_percent(card_present_swiped),
        "card_present_keyed": format_percent(card_present_keyed),
        "card_not_present": format_percent(card_not_present),
        "consumer_sales": format_percent(consumer_sales),
        "business_sales": format_percent(business_sales),
        "government_sales": format_percent(government_sales),
    }


# =============================================================================
# CREDIT CARD INTERCHANGE GENERATOR
# =============================================================================
def generate_credit_card_interchange_data(bet_numbers: Dict[str, str]) -> Dict[str, Any]:
    """Generate Credit Card Interchange data with provided BET numbers"""
    return {
        "interchange_type": "Tiered",
        "chargeback": "0.00",
        "fanf_type": "FANF CP/CNP (Varies*)",
        "visa_bet_number": bet_numbers["visa"],
        "mastercard_bet_number": bet_numbers["mastercard"],
        "discover_bet_number": bet_numbers["discover"],
        "amex_bet_number": bet_numbers["amex"],
        "visa_qualified_rate": generate_rate_value(),
        "visa_discount_per_item": generate_rate_value(),
        "visa_signature_rate": generate_rate_value(),
        "visa_signature_discount": generate_rate_value(),
        "mc_qualified_rate": generate_rate_value(),
        "mc_discount_per_item": generate_rate_value(),
        "mc_signature_rate": generate_rate_value(),
        "mc_signature_discount": generate_rate_value(),
        "discover_qualified_rate": generate_rate_value(),
        "discover_discount_per_item": generate_rate_value(),
        "discover_signature_rate": generate_rate_value(),
        "discover_signature_discount": generate_rate_value(),
        "amex_qualified_rate": generate_rate_value(),
        "amex_discount_per_item": generate_rate_value(),
        "does_not_accept_amex": False,
        "amex_optout_marketing": False,
        "amex_annual_volume": generate_annual_volume(),
    }


# =============================================================================
# CREDIT CARD SERVICES
# =============================================================================
CREDIT_CARD_SERVICES = ["Mobile Merchant", "Interchange Advantage Program"]


# =============================================================================
# ACH SERVICES
# =============================================================================
ACH_SERVICES = [
    "EFT Virtual Check Consumer Initiated (EFTVCCI)",
    "EFT Virtual Check Merchant Initiated (EFTVCMI)"
]


# =============================================================================
# ACH UNDERWRITING DATA GENERATOR
# =============================================================================
def generate_ach_underwriting_data() -> Dict[str, Any]:
    """
    Generate ACH Underwriting Profile data.
    
    Rules:
    - Written + Non-Written = 100% (interval of 1, not 5)
    - Merchant + Consumer = 100% (same logic)
    - Only Written and Merchant need to be selected, others auto-fill with remainder
    """
    # Generate Written percentage (0-100, interval of 1)
    written_pct = random.randint(0, 100)
    
    # Generate Merchant percentage (0-100, interval of 1)
    merchant_pct = random.randint(0, 100)
    
    # Generate volumes and tickets
    annual_volume = round(random.uniform(10000.00, 500000.00), 2)
    avg_ticket = round(random.uniform(50.00, 500.00), 2)
    highest_ticket = round(avg_ticket * random.uniform(2.0, 5.0), 2)
    
    return {
        "annual_volume": f"{annual_volume:.2f}",
        "avg_ticket": f"{avg_ticket:.2f}",
        "highest_ticket": f"{highest_ticket:.2f}",
        "written_pct": str(written_pct),  # Non-written will auto-fill with 100 - written
        "merchant_pct": str(merchant_pct),  # Consumer will auto-fill with 100 - merchant
        "send_email": True,
        "send_fax": True,
    }


# Generate ACH Underwriting data at module load
ACH_UNDERWRITING = generate_ach_underwriting_data()


# =============================================================================
# ACH FEES DATA GENERATOR
# =============================================================================
def generate_ach_fee_value() -> str:
    """Generate a random fee value between 10.00 and 1000.00 with 2 decimal places."""
    value = round(random.uniform(10.00, 1000.00), 2)
    return f"{value:.2f}"


def generate_ach_fees_data() -> Dict[str, Any]:
    """
    Generate ACH Fees data for both Rate and Fee columns.
    
    ACH Fees section has:
    - CCD Written (Rate, Fee)
    - CCD Non-Written (Rate, Fee)
    - PPD Written (Rate, Fee)
    - PPD Non-Written (Rate, Fee)
    - WEB (Rate, Fee)
    - ARC (Rate, Fee)
    
    Miscellaneous Fees:
    - Statement Fee
    - Minimum Fee
    - File Fee
    - Reject Fee
    - Gateway Fee
    - Maintenance Fee
    - Billing Cycle (dropdown - do not change)
    """
    return {
        # ACH Fees - Rate and Fee for each type
        "ccd_written_rate": generate_ach_fee_value(),
        "ccd_written_fee": generate_ach_fee_value(),
        "ccd_non_written_rate": generate_ach_fee_value(),
        "ccd_non_written_fee": generate_ach_fee_value(),
        "ppd_written_rate": generate_ach_fee_value(),
        "ppd_written_fee": generate_ach_fee_value(),
        "ppd_non_written_rate": generate_ach_fee_value(),
        "ppd_non_written_fee": generate_ach_fee_value(),
        "web_rate": generate_ach_fee_value(),
        "web_fee": generate_ach_fee_value(),
        "arc_rate": generate_ach_fee_value(),
        "arc_fee": generate_ach_fee_value(),
        
        # Miscellaneous Fees
        "statement_fee": generate_ach_fee_value(),
        "minimum_fee": generate_ach_fee_value(),
        "file_fee": generate_ach_fee_value(),
        "reject_fee": generate_ach_fee_value(),
        "gateway_fee": generate_ach_fee_value(),
        "maintenance_fee": generate_ach_fee_value(),
        # billing_cycle is NOT included - leave as default "Monthly"
    }


# Generate ACH Fees data at module load
ACH_FEES = generate_ach_fees_data()


# =============================================================================
# ACH ORIGINATOR DATA
# =============================================================================
# Transaction types available for ACH Originator
ACH_TRANSACTION_TYPES = ["ARC", "CCD", "PPD", "RCK", "TEL", "WEB"]


def generate_ach_originator_data() -> Dict[str, Any]:
    """
    Generate ACH Originator data.
    
    Uses same bank routing/account from BANK_INFORMATION.
    Transaction type is randomly selected.
    Checkboxes (Written, Resubmit R01) are randomly set.
    """
    return {
        "description": f"Originator_{faker.word().capitalize()}_{random.randint(100, 999)}",
        "transaction_type": random.choice(ACH_TRANSACTION_TYPES),
        "written_authorization": random.choice([True, False]),
        "resubmit_r01": random.choice([True, False]),
        # Bank info - same as BANK_INFORMATION
        "routing_number": BANK_INFORMATION["routing_number"],
        "account_number": BANK_INFORMATION["account_number"],
    }


# Generate ACH Originator data at module load
ACH_ORIGINATOR = generate_ach_originator_data()


# =============================================================================
# SALES REPRESENTATIVE
# =============================================================================
SALES_REPRESENTATIVE = {"name": "DEMONET1"}


# =============================================================================
# MERCHANT PRODUCTS
# =============================================================================
MERCHANT_PRODUCTS = ["Credit"]


# =============================================================================
# BUSINESS TYPE & GENERAL UNDERWRITING (Common across environments)
# =============================================================================
BUSINESS_TYPE = "Retail"

GENERAL_UNDERWRITING_INFO = {
    "business_type": BUSINESS_TYPE,
    "sic_code": "7311",
    "products_sold": "General retail merchandise and consumer goods",
    "return_policy": "30 Days Money Back Guarantee",
    "days_until_delivery": "5",
    "seasonal_months": [],
}


# =============================================================================
# CREDIT CARD UNDERWRITING (Generated using common BUSINESS_TYPE)
# Note: This does NOT depend on BET numbers, so it can be generated here
# =============================================================================
CREDIT_CARD_UNDERWRITING = generate_credit_card_underwriting_data(
    business_type=BUSINESS_TYPE,
    merchant_type=_merchant_type
)


# =============================================================================
# EXPORTED VARIABLES FOR ENVIRONMENT-SPECIFIC FILES
# =============================================================================
# These are used by osc_data_qa.py and osc_data_prod.py
MERCHANT_TYPE = _merchant_type  # "internet", "moto", or "retail"
OWNERSHIP_TYPE = _ownership_type  # For reference in scripts


# =============================================================================
# FEE SELECTION HELPERS
# =============================================================================
def generate_fee_list(fee_names: list) -> Dict[str, Dict[str, Any]]:
    """
    Generate a fee list with random amounts for each fee.
    
    Args:
        fee_names: List of fee description names
        
    Returns:
        Dict with fee_name as key and dict with 'amount' as value
    """
    fee_list = {}
    for fee_name in fee_names:
        fee_list[fee_name] = {
            "amount": generate_fee_amount()
        }
    return fee_list
