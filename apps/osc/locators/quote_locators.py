"""Quote creation screen locators for OSC application."""

# Quote form sections
CUSTOMER_SECTION = "#customer-section, [data-testid='customer-section']"
PRODUCT_SECTION = "#product-section, [data-testid='product-section']"
PRICING_SECTION = "#pricing-section, [data-testid='pricing-section']"

# Customer fields
CUSTOMER_NAME_INPUT = "input[name='customerName'], #customer-name"
CUSTOMER_EMAIL_INPUT = "input[name='customerEmail'], #customer-email"
CUSTOMER_PHONE_INPUT = "input[name='customerPhone'], #customer-phone"

# Product fields
PRODUCT_SELECT = "select[name='product'], #product-select"
QUANTITY_INPUT = "input[name='quantity'], #quantity"
ADD_PRODUCT_BUTTON = "button:has-text('Add Product')"

# Pricing fields
DISCOUNT_INPUT = "input[name='discount'], #discount"
TAX_RATE_SELECT = "select[name='taxRate'], #tax-rate"
TOTAL_AMOUNT = ".total-amount, [data-testid='total-amount']"

# Form actions
SAVE_QUOTE_BUTTON = "button:has-text('Save Quote'), button[type='submit']"
CANCEL_BUTTON = "button:has-text('Cancel')"
SUCCESS_MESSAGE = ".success-message, .alert-success, text=/Quote (created|saved) successfully/i"
