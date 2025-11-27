"""
OSC Application Data Configuration - QA ENVIRONMENT

This file contains test data for the QA environment.
Modify values here for QA-specific testing needs.

Set OSC_DATA_ENV=qa to use this data file.

Data Categories:
- Sales Representatives
- Merchant Information
- Application Settings
- Contact Information
"""

from typing import Dict, Any
from datetime import datetime, timedelta
from faker import Faker
import random
import string

faker = Faker()


# =====================================================
# DROPDOWN OPTIONS - All available values from DOM
# =====================================================
class DropdownOptions:
    """All available dropdown options across the application"""
    
    # Association dropdown options
    ASSOCIATION_OPTIONS = [
        "Big Association",
        "DEMO NET1",
        "TestWelcomeEmails"
    ]

    # Lead Source dropdown options
    LEAD_SOURCE_OPTIONS = [
        "AdvanceMe",
        "Merchant Call In",
        "Referral",
        "Rocky Gingg",
        "Yellow Pages"
    ]

    # Referral Partner dropdown options
    REFERRAL_PARTNER_OPTIONS = [
        "None",
        "Test Troy1"
    ]

    # Country dropdown options
    COUNTRY_OPTIONS = [
        "Canada",
        "United States"
    ]

    # State dropdown options (US States + Canadian Provinces)
    STATE_OPTIONS = [
        "Please select...",
        "NA",
        "Alaska",
        "Alabama",
        "Arkansas",
        "Arizona",
        "California",
        "Colorado",
        "Connecticut",
        "Dist. of Columbia",
        "Delaware",
        "Florida",
        "Georgia",
        "Guam",
        "Hawaii",
        "Iowa",
        "Idaho",
        "Illinois",
        "Indiana",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Massachusetts",
        "Maryland",
        "Maine",
        "Michigan",
        "Minnesota",
        "Missouri",
        "Mississippi",
        "Montana",
        "North Carolina",
        "North Dakota",
        "Nebraska",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "Nevada",
        "New York",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Puerto Rico",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Virginia",
        "Virgin Islands",
        "Vermont",
        "Washington",
        "Wisconsin",
        "West Virginia",
        "Wyoming",
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Nova Scotia",
        "Northwest Territories",
        "Nunavut",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Yukon"
    ]
    
    # US States only (for random selection)
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
    
    # Ownership Type dropdown options
    OWNERSHIP_TYPE_OPTIONS = [
        "C Corporation",
        "Government (Fed,St,Local)",
        "LLC- C Corp",
        "LLC- Disregarded Entity",
        "LLC- Partnership",
        "LLC- S Corp",
        "LLC- Sole Proprietor",
        "Non-Profit",
        "Non-US Entity",
        "Partnership",
        "S Corporation",
        "Sole Proprietor",
        "Trust/Estate",
        "Please select..."
    ]
    
    # Business Type dropdown options
    BUSINESS_TYPE_OPTIONS = [
        "Grocery",
        "GSA",
        "Hotel/Restaurant",
        "MOTO",
        "Retail"
    ]

    SIC_CODE_LIST = ['7311', '7321', '3030']
    
    # Return Policy dropdown options
    RETURN_POLICY_OPTIONS = [
        "30 Days Money Back Guarantee",
        "30 Days Exchange Only",
        "60 Days Money Back Guarantee",
        "60 Days Exchange Only",
        "90 Days Money Back Guarantee",
        "90 Days Exchange Only",
        "Other"
    ]
    
    # Tax Filing State dropdown options (same as STATE_OPTIONS)
    TAX_FILING_STATE_OPTIONS = STATE_OPTIONS
    
    # Owner/Officer Title options
    TITLE_OPTIONS = [
        "CEO",
        "CFO",
        "COO",
        "President",
        "Vice President",
        "Owner",
        "Partner",
        "Manager",
        "Director",
        "Secretary",
        "Treasurer"
    ]


# =====================================================
# HELPER FUNCTIONS - Phone/Fax (digits only for masked inputs)
# =====================================================
def generate_phone_digits() -> str:
    """Generate a 10-digit phone number (digits only for masked input)"""
    area_code = random.randint(200, 999)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"{area_code}{prefix}{line}"


def generate_fax_digits() -> str:
    """Generate a 10-digit fax number (digits only for masked input)"""
    return generate_phone_digits()


def generate_random_date_past(years_back: int = 10) -> str:
    """Generate a random date in the past as digits only (mmddyyyy for masked input)"""
    days_back = random.randint(365, years_back * 365)
    past_date = datetime.now() - timedelta(days=days_back)
    # Return digits only for masked input fields (mm/dd/yyyy mask)
    return past_date.strftime("%m%d%Y")


def generate_dunns_number() -> str:
    """Generate a random 9-digit D&B number"""
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])


def generate_federal_tax_id() -> str:
    """Generate a 9-digit Federal Tax ID (EIN) as digits only for masked input"""
    # EIN format: XX-XXXXXXX, but for masked input we send digits only
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])


def generate_ssn_digits() -> str:
    """Generate a 9-digit SSN as digits only for masked input"""
    # SSN format: XXX-XX-XXXX, but for masked input we send digits only
    # Avoid invalid SSN patterns (000, 666, 900-999 for first group)
    first = random.randint(100, 665)
    if first == 666:
        first = 667
    second = random.randint(1, 99)
    third = random.randint(1, 9999)
    return f"{first:03d}{second:02d}{third:04d}"


def generate_dob_digits(min_age: int = 25, max_age: int = 65) -> str:
    """Generate date of birth as digits only (ddmmyyyy for masked input)"""
    dob = faker.date_of_birth(minimum_age=min_age, maximum_age=max_age)
    # Return digits only for masked input fields (dd/mm/yyyy mask)
    return dob.strftime("%d%m%Y")


def generate_date_of_ownership_digits(years_back: int = 10) -> str:
    """Generate date of ownership as digits only (ddmmyyyy for masked input)"""
    days_back = random.randint(365, years_back * 365)
    ownership_date = datetime.now() - timedelta(days=days_back)
    # Return digits only for masked input fields (dd/mm/yyyy mask)
    return ownership_date.strftime("%d%m%Y")


# =====================================================
# CORPORATE INFORMATION DATA
# =====================================================
CORPORATE_INFO = {
    "legal_business_name": faker.company(),
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
    "use_different_location": True,  # Always use different location address
}


# =====================================================
# LOCATION INFORMATION DATA
# =====================================================
LOCATION_INFO = {
    "dba": faker.company() + " " + random.choice(["Store", "Shop", "Center", "Outlet"]),
    "address": faker.street_address(),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    "fax": generate_fax_digits(),
    "customer_service_phone": generate_phone_digits(),
    "website": "https://www." + faker.domain_name(),
    "email": faker.email(),
    "chargeback_email": "rahul.raj@nuvei.com",
    "business_open_date": generate_random_date_past(years_back=15),
    "existing_sage_mid": "",  # Optional - leave empty for new merchants
    "general_comments": faker.sentence(nb_words=10),
}


# =====================================================
# TAX INFORMATION DATA
# =====================================================
TAX_INFO = {
    "federal_tax_id": generate_federal_tax_id(),
    "tax_filing_corp_name": faker.company() + " Holdings Inc",
    "ownership_type": random.choice([
        "C Corporation",
        "S Corporation",
        "LLC- C Corp",
        "LLC- S Corp",
        "Sole Proprietor"
    ]),
    "tax_filing_state": "Georgia",
    # Checkboxes
    "is_corp_headquarters": True,
    "is_foreign_entity": False,
    "authorize_1099": True,
}


# =====================================================
# OWNER EQUITY CALCULATION (Must sum to 100)
# =====================================================
# Generate Owner1 equity between 20-90, Owner2 gets the remainder
_owner1_equity = random.randint(20, 90)
_owner2_equity = 100 - _owner1_equity


# =====================================================
# OWNER/OFFICER 1 INFORMATION DATA
# =====================================================
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
    "equity": str(_owner1_equity),  # Owner1 equity (20-90)
}


# =====================================================
# OWNER/OFFICER 2 INFORMATION DATA
# =====================================================
# Generate Owner2 name first, then use for email
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
    "equity": str(_owner2_equity),  # Owner2 equity (100 - Owner1)
}


# =====================================================
# TRADE REFERENCE INFORMATION DATA
# =====================================================
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


# =====================================================
# GENERAL UNDERWRITING INFORMATION DATA
# =====================================================
GENERAL_UNDERWRITING_INFO = {
    # "business_type": random.choice(DropdownOptions.BUSINESS_TYPE_OPTIONS[1:]),  # Skip "Select business type"
    "business_type": "Retail",  # Hardcoded for BET mapping implementation
    "sic_code": random.choice(DropdownOptions.SIC_CODE_LIST),
    "products_sold": faker.sentence(nb_words=20),
    "return_policy": random.choice(DropdownOptions.RETURN_POLICY_OPTIONS),
    "days_until_delivery": str(random.randint(1, 30)),
    # Seasonal months - list of months to check (empty list = no seasonal business)
    "seasonal_months": [],  # e.g., ["january", "february", "december"]
}


# =====================================================
# BILLING QUESTIONNAIRE DATA
# =====================================================
BILLING_QUESTIONNAIRE_INFO = {
    # Type of Merchant (radio button): "internet", "moto", or "retail"
    "merchant_type": random.choice(["internet", "moto", "retail"]),
    
    # Billing/Delivery Policy options
    "full_payment_upfront": True,
    "full_payment_days": str(random.randint(1, 30)),
    
    "partial_payment_upfront": True,
    "partial_payment_percentage":str(random.randint(10, 90)),
    "partial_payment_days": str(random.randint(1, 30)),
    
    "payment_after_delivery": True,
    
    # Recurring Billing Options (checkboxes)
    "billing_monthly": False,
    "billing_quarterly": True,
    "billing_semi_annually": False,
    "billing_annually": False,
    
    # Outsourced to Third Party
    "outsourced_to_third_party": True,  # True = YES, False = NO
    "outsourced_explanation": "Outsourced billing to third party provider for efficiency.",  # Only required if outsourced_to_third_party is True
}


# Bank Information Section
BANK_INFORMATION = {
    # Bank Basic Details
    "bank_name": "Test Bank " + faker.company_suffix(),
    "address1": faker.street_address(),
    "address2": "Suite " + str(random.randint(100, 999)),
    "city": "Atlanta",
    "state": "Georgia",
    "zip_code": "30309",
    "country": "United States",
    "phone": generate_phone_digits(),
    
    # Depository Account (Credit) - Routing and Account Numbers
    "routing_number": "061000052",
    "account_number": "61000543270",
}


# Credit Card Information Section
CREDIT_CARD_INFORMATION = {
    # Authorization Network options: "In-House", "Nuvei", "Visanet/TSYS"
    "authorization_network": "Visanet/TSYS",
    
    # Settlement Bank options: "Citizens Bank, N.A."
    "settlement_bank": "Citizens Bank, N.A.",
    
    # Settlement Network options: "Vital"
    "settlement_network": "Vital",
    
    # Discount Paid options: "Monthly", "Daily"
    "discount_paid": "Monthly",
    
    # User Bank options: "3948"
    "user_bank": "3948",
}


def generate_credit_card_underwriting_data(business_type: str = "Retail") -> Dict[str, Any]:
    """
    Generate random Credit Card Underwriting data with proper business logic.
    
    Rules:
    - Card Present Swiped + Card Present Keyed + Card Not Present = 100%
    - For Grocery/Retail: Card Not Present max 30%
    - Consumer Sales + Business Sales + Government Sales = 100%
    - Monthly Volume must be > Average Ticket (and 3-5 digits with 2 decimals)
    - Dropdown options are in format: '0 %', '5 %', '10 %', ... '100 %'
    
    Args:
        business_type: Business type (Grocery, Retail, MOTO, etc.)
    
    Returns:
        Dict with all Credit Card Underwriting data
    """
    # Percentage options available in dropdowns (0, 5, 10, 15, ... 100)
    percentage_options = list(range(0, 101, 5))  # [0, 5, 10, 15, ..., 100]
    
    # ===== Card Present Distribution (must sum to 100%) =====
    # For Grocery/Retail: Card Not Present max 30%
    is_retail_or_grocery = business_type.lower() in ["retail", "grocery"]
    
    if is_retail_or_grocery:
        # Card Not Present: 0-30% (max 30%)
        card_not_present_options = [p for p in percentage_options if p <= 30]
        card_not_present = random.choice(card_not_present_options)
    else:
        # For MOTO/other types, can go higher
        card_not_present = random.choice(percentage_options)
    
    # Remaining percentage to distribute between Swiped and Keyed
    remaining = 100 - card_not_present
    
    # Find valid combinations that sum to remaining and are multiples of 5
    valid_swiped_options = [p for p in percentage_options if p <= remaining]
    card_present_swiped = random.choice(valid_swiped_options)
    card_present_keyed = remaining - card_present_swiped
    
    # Ensure keyed is a valid dropdown option (multiple of 5)
    # If not, adjust swiped
    if card_present_keyed not in percentage_options:
        # Find the nearest valid value
        card_present_keyed = min(percentage_options, key=lambda x: abs(x - card_present_keyed))
        card_present_swiped = remaining - card_present_keyed
        if card_present_swiped < 0:
            card_present_swiped = 0
            card_present_keyed = remaining
    
    # ===== Sales Distribution (must sum to 100%) =====
    # No max limit on any category
    consumer_sales = random.choice(percentage_options)
    remaining_sales = 100 - consumer_sales
    
    valid_business_options = [p for p in percentage_options if p <= remaining_sales]
    business_sales = random.choice(valid_business_options) if valid_business_options else 0
    government_sales = remaining_sales - business_sales
    
    # Ensure government is a valid dropdown option
    if government_sales not in percentage_options:
        government_sales = min(percentage_options, key=lambda x: abs(x - government_sales))
        business_sales = remaining_sales - government_sales
        if business_sales < 0:
            business_sales = 0
            government_sales = remaining_sales
    
    # ===== Volume and Ticket Values =====
    # Monthly Volume: 3-5 digits with 2 decimals, must be > Average Ticket
    # Generate average ticket first (smaller value)
    average_ticket = round(random.uniform(10.00, 999.99), 2)
    
    # Monthly Volume must be greater than Average Ticket
    # Generate 3-5 digit value that's greater than average_ticket
    min_volume = max(average_ticket + 1, 100.00)  # At least 3 digits and > average_ticket
    max_volume = 99999.99  # Max 5 digits
    monthly_volume = round(random.uniform(min_volume, max_volume), 2)
    
    # Highest Ticket: should be >= Average Ticket but <= Monthly Volume
    highest_ticket = round(random.uniform(average_ticket, min(monthly_volume, average_ticket * 10)), 2)
    
    # Format percentage for dropdown (e.g., "95 %")
    def format_percent(value: int) -> str:
        return f"{value} %"
    
    return {
        # Volume fields (2 decimal precision)
        "monthly_volume": f"{monthly_volume:.2f}",
        "average_ticket": f"{average_ticket:.2f}",
        "highest_ticket": f"{highest_ticket:.2f}",
        
        # Card Present Distribution (sum = 100%)
        "card_present_swiped": format_percent(card_present_swiped),
        "card_present_keyed": format_percent(card_present_keyed),
        "card_not_present": format_percent(card_not_present),
        
        # Sales Distribution (sum = 100%)
        "consumer_sales": format_percent(consumer_sales),
        "business_sales": format_percent(business_sales),
        "government_sales": format_percent(government_sales),
        
        # Business type used for rules
        "_business_type": business_type,
        "_card_total": card_present_swiped + card_present_keyed + card_not_present,
        "_sales_total": consumer_sales + business_sales + government_sales,
    }


# Credit Card Underwriting - Generated with business rules
# Card Present Swiped + Card Present Keyed + Card Not Present = 100%
# Consumer Sales + Business Sales + Government Sales = 100%
# Monthly Volume > Average Ticket
CREDIT_CARD_UNDERWRITING = generate_credit_card_underwriting_data("Retail")


def generate_rate_value() -> str:
    """
    Generate a random rate value with format X.XXX (1 digit before decimal, 3 after).
    Example: 8.479, 2.156, 0.342
    
    Returns:
        String formatted rate value
    """
    whole = random.randint(0, 9)
    decimal = random.randint(0, 999)
    return f"{whole}.{decimal:03d}"


def generate_annual_volume() -> str:
    """
    Generate a random annual volume with 2 decimal places.
    Example: 12500.45, 8750.00
    
    Returns:
        String formatted annual volume
    """
    volume = round(random.uniform(1000.00, 99999.99), 2)
    return f"{volume:.2f}"


# =====================================================
# BET NUMBER MAPPING BY BUSINESS TYPE
# =====================================================
BET_NUMBERS_BY_BUSINESS_TYPE = {
    "Retail": {
        "visa": "7291",
        "mastercard": "5291",
        "discover": "3191",
        "amex": "4128",
    },
    # Add other business types as needed
    # "Restaurant": {
    #     "visa": "XXXX",
    #     "mastercard": "XXXX",
    #     "discover": "XXXX",
    #     "amex": "XXXX",
    # },
}

# Default BET numbers (fallback if business type not mapped)
DEFAULT_BET_NUMBERS = {
    "visa": "8693",
    "mastercard": "6693",
    "discover": "3192",
    "amex": "4884",
}


def generate_credit_card_interchange_data(business_type: str = "Retail") -> Dict[str, Any]:
    """
    Generate Credit Card Interchange data with random rates and discounts.
    BET numbers are mapped based on the business type.
    
    Args:
        business_type: The business type from General Underwriting (e.g., "Retail", "Restaurant")
    
    Returns:
        Dict with all Credit Card Interchange configuration
    """
    # Get BET numbers based on business type, fallback to defaults if not mapped
    bet_numbers = BET_NUMBERS_BY_BUSINESS_TYPE.get(business_type, DEFAULT_BET_NUMBERS)
    
    return {
        # Interchange Type dropdown options: "Tiered", "Interchange Plus", etc.
        "interchange_type": "Tiered",
        
        # Chargeback dropdown options: "0.00", "0.01", etc.
        "chargeback": "0.00",
        
        # FANF dropdown options: "FANF CP/CNP (Varies*)", etc.
        "fanf_type": "FANF CP/CNP (Varies*)",
        
        # BET Numbers for each card network (mapped by business type)
        "visa_bet_number": bet_numbers["visa"],
        "mastercard_bet_number": bet_numbers["mastercard"],
        "discover_bet_number": bet_numbers["discover"],
        "amex_bet_number": bet_numbers["amex"],
        
        # ===== Visa Rates and Discounts =====
        "visa_qualified_rate": generate_rate_value(),
        "visa_discount_per_item": generate_rate_value(),
        "visa_signature_rate": generate_rate_value(),
        "visa_signature_discount": generate_rate_value(),
        
        # ===== MasterCard Rates and Discounts =====
        "mc_qualified_rate": generate_rate_value(),
        "mc_discount_per_item": generate_rate_value(),
        "mc_signature_rate": generate_rate_value(),
        "mc_signature_discount": generate_rate_value(),
        
        # ===== Discover Rates and Discounts =====
        "discover_qualified_rate": generate_rate_value(),
        "discover_discount_per_item": generate_rate_value(),
        "discover_signature_rate": generate_rate_value(),
        "discover_signature_discount": generate_rate_value(),
        
        # ===== AMEX Rates and Discounts =====
        "amex_qualified_rate": generate_rate_value(),
        "amex_discount_per_item": generate_rate_value(),
        
        # AMEX Options
        # If True, merchant does not accept AMEX cards (checkbox will be selected)
        # If False, merchant accepts AMEX cards (checkbox will not be selected)
        "does_not_accept_amex": False,
        
        # If True, merchant opts out of AMEX marketing materials
        "amex_optout_marketing": False,
        
        # Annual AMEX Volume (random 2 decimal value)
        "amex_annual_volume": generate_annual_volume(),
    }


# Credit Card Interchange Configuration - Generated with random rates and BET mapping
CREDIT_CARD_INTERCHANGE = generate_credit_card_interchange_data(GENERAL_UNDERWRITING_INFO["business_type"])


# Credit Card Services - List of services to enable
# Each service selection causes a page reload
CREDIT_CARD_SERVICES = [
    "Mobile Merchant",
    "Interchange Advantage Program"
]


# Sales Representative Configuration
SALES_REPRESENTATIVE = {
    "name": "DEMONET1",
}

MERCHANT_PRODUCTS = [
    "Credit"
]

# Application Information Section
APPLICATION_INFO = {
    "office": "DEMO NET1",
    "phone": "7038529999",
    "contractor": "DEMONET1",
    "association": "TestWelcomeEmails",
    "lead_source": "Yellow Pages",
    "referral_partner": "None",
    "promo_code": "",  # Optional field
    "corporate_atlas_id": ""  # Optional field
}

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
