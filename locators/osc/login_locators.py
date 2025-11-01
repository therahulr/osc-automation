"""Login screen locators for OSC application."""

# Login form elements
USERNAME_INPUT = "input[name='txtUsername']"
PASSWORD_INPUT = "input[name='txtPassword']"
LOGIN_BUTTON = "input[name='btnLogin']"

# Post-login indicators - Dashboard/Home page
HOME_HEADING = "h2:has-text('Home')"
APPLICATION_SUMMARY = "text=Application Summary"
DASHBOARD_LOADED = "h2:has-text('Home'), text=Application Summary"

# MFA page detection
MFA_PAGE_INDICATOR = "text=One-time Passcode, text=MFA"

# Error messages
ERROR_MESSAGE = ".error-message, .alert-danger, [role='alert']"
INVALID_CREDENTIALS = "text=/Invalid (username|password|credentials)/i"
