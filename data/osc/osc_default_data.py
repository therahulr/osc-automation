# =====================================================
# DROPDOWN OPTIONS - All available values
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
    
    # Country dropdown options
    COUNTRY_OPTIONS = [
        "Canada",
        "United States"
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
    
    # Tax Filing State dropdown options (same as STATE_OPTIONS)
    TAX_FILING_STATE_OPTIONS = STATE_OPTIONS
    
    # Business Type dropdown options
    BUSINESS_TYPE_OPTIONS = [
        "Select business type",
        "Grocery",
        "GSA",
        "Hotel/Restaurant",
        "MOTO",
        "Retail"
    ]
    
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

    # Business Type dropdown options
    BUSINESS_TYPE_OPTIONS = [
        "Select business type",
        "Grocery",
        "GSA",
        "Hotel/Restaurant",
        "MOTO",
        "Retail"
    ]


class CorporateInfoTestData:
    # ---- Positive Test Data ----
    legal_name = "Tech Solutions LLC"
    address_1 = "123 Elm Street"
    city = "New York"
    state = "NY"
    zip = "12345"
    country = "United States"
    phone = "7038529999"
    fax = "7038529998"
    email = "info@testcompany.com"
    dunns = "123456789"
    contact_title = "Manager"
    contact_first_name = "John"
    contact_last_name = "Doe"

    # ---- Negative Test Data ----
    invalid_email = "abc@"
    invalid_phone = "123ABC"
    invalid_zip = "ABCDE"


class LocationInfoTestData:
    dba = "Best Coffee Shop"
    address_1 = "456 Market Street"
    city = "San Francisco"
    state = "CA"
    zip_code = "94103"
    country = "United States"
    phone = "9876543210"
    fax = "9876543211"
    customer_service_phone = "9876543000"
    website = "https://bestcoffee.com"
    email = "info@bestcoffee.com"
    chargeback_email = "chargeback@bestcoffee.com"
    business_open_date = "2020-01-01"
    existing_mid = "MID12345"
    general_comment = "This is a test comment."

    # Negative / edge test data
    email_wrong = "test@"
    phone_wrong = "ABC123"
    zip_wrong = "ZZZZZ"
    website_wrong = "abc"
    business_open_date_future = "2050-01-01"



class TaxInfoTestData:
    federal_tax_id = "123456789"
    tax_filing_corp_name = "Tech Holdings Inc"
    ownership_type = "Corporation"
    tax_filing_state = "NY"

    # Checkboxes
    is_corp_headquarters = True
    is_foreign_entity = False
    is_authorizing_1099 = True

    # Negative cases
    federal_tax_id_short = "12345"
    federal_tax_id_alpha = "12AB56789"
    tax_filing_corp_name_empty = ""
    ownership_type_not_selected = ""
    tax_filing_state_not_selected = ""


class OwnerOfficerTestData:
    # Shared for Owner 1 and Owner 2 (with different values)
    title = "CEO"
    first_name = "John"
    last_name = "Doe"
    address_1 = "221B Baker Street"
    address_2 = "Floor 2"
    city = "New York"
    state = "NY"
    zip_code = "10001"
    country = "United States"
    phone = "7038529999"
    fax = "7038528888"
    email = "john.doe@example.com"
    date_of_birth = "1988-03-15"
    ssn = "123-45-6789"
    date_of_ownership = "2020-05-10"
    equity_percent = "50"

    # Owner 2 variation
    title_2 = "CFO"
    first_name_2 = "Jane"
    last_name_2 = "Smith"
    phone_2 = "7038527777"
    email_2 = "jane.smith@example.com"
    equity_percent_2 = "50"

    # Negative Data
    email_bad = "abc@"
    phone_alpha = "123ABC9999"
    ssn_wrong_format = "123456789"
    zip_alpha = "ABCDE"
    equity_overflow = "150"    # More than 100%
    dob_future = "2050-01-01"


class CreditCardAuthorizationTestData:
    authorization_network_in_house = "In-House"
    authorization_network_nuvei = "Nuvei"
    authorization_network_visanet_tsys = "Visanet/TSYS"

class CreditCardSettlementBankTestData:
    settlement_bank_citizens_na = "Citizens Bank, N.A."

class CreditCardSettlementNetworkTestData:
    settlement_network_vital = "Vital"

class CreditCardDiscountPaidTestData:
    discount_paid_monthly = "Monthly"
    discount_paid_daily = "Daily"

class CreditCardUserBankTestData:
    user_bank_3948 = "3948"



