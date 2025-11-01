"""Dashboard screen locators for OSC application."""

# Main navigation
NAV_MENU = "nav, [role='navigation']"
NAV_DASHBOARD = "a:has-text('Dashboard')"
NAV_QUOTES = "a:has-text('Quotes'), a:has-text('Create Quote')"
NAV_CUSTOMERS = "a:has-text('Customers')"
NAV_REPORTS = "a:has-text('Reports')"

# Dashboard widgets
DASHBOARD_SUMMARY = ".dashboard-summary, [data-testid='dashboard-summary']"
RECENT_QUOTES = ".recent-quotes, [data-testid='recent-quotes']"
PENDING_APPROVALS = ".pending-approvals, [data-testid='pending-approvals']"

# Quick actions
CREATE_QUOTE_BUTTON = "button:has-text('Create Quote'), a:has-text('New Quote')"
SEARCH_INPUT = "input[type='search'], input[placeholder*='Search']"
