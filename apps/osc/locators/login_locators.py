"""Login screen locators for OSC application."""

# Login form elements
USERNAME_INPUT = "input[name='username'], input[id='username'], input[type='email']"
PASSWORD_INPUT = "input[name='password'], input[id='password'], input[type='password']"
LOGIN_BUTTON = "button[type='submit'], button:has-text('Login'), button:has-text('Sign In')"

# Post-login indicators
WELCOME_MESSAGE = ".welcome-message, .user-greeting, [data-testid='user-menu']"
DASHBOARD_HEADER = "h1:has-text('Dashboard'), [data-testid='dashboard-header']"

# Error messages
ERROR_MESSAGE = ".error-message, .alert-danger, [role='alert']"
INVALID_CREDENTIALS = "text=/Invalid (username|password|credentials)/i"
