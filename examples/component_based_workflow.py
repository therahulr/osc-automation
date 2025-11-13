"""Component-based workflow example.

This example demonstrates:
1. Creating reusable page components
2. Building workflows by composing components
3. Advanced component features (forms, tables, etc.)
4. How to organize app-specific pages
"""

from core import UIAutomationCore, BaseComponent, FormComponent, log_step, log_success


# ==================== Define Reusable Components ====================

class GoogleSearchComponent(BaseComponent):
    """Reusable Google search component."""

    def search(self, query: str):
        """Perform a Google search.

        Args:
            query: Search query
        """
        log_step(f"Searching for: {query}")

        self.input("textarea[name='q']", query)
        self.press("textarea[name='q']", "Enter")
        self.wait_for_navigation()

        log_success("Search completed")

    def get_result_count(self) -> int:
        """Get number of search results.

        Returns:
            Number of results found
        """
        self.wait_visible("#search")
        return self.get_count("#search .g")

    def get_first_result_title(self) -> str:
        """Get the title of the first search result.

        Returns:
            Title text
        """
        return self.get_text("#search .g:first-child h3")


class GithubLoginComponent(FormComponent):
    """Reusable GitHub login component."""

    def __init__(self, page):
        # Initialize with the login form selector
        super().__init__(page, form_selector="form[action='/session']")

    def login(self, username: str, password: str):
        """Perform GitHub login.

        Args:
            username: GitHub username or email
            password: GitHub password
        """
        log_step("Logging into GitHub")

        # Navigate to login page
        self.goto("https://github.com/login")

        # Fill login form (inherited from FormComponent)
        self.fill_form({
            "#login_field": username,
            "#password": password
        })

        # Submit form
        self.click("input[type='submit'][name='commit']")

        log_success("Login completed")


# ==================== Workflow Composition ====================

def google_search_workflow():
    """Workflow composed of reusable components."""

    with UIAutomationCore(
        app_name="google_example",
        script_name="component_search",
        headless=False
    ) as core:

        # Navigate to Google
        core.page.goto("https://www.google.com")

        # Create search component
        search = GoogleSearchComponent(core.page, logger=core.logger)

        # Perform multiple searches
        searches = [
            "Python automation framework",
            "Playwright testing",
            "Web scraping best practices"
        ]

        for query in searches:
            search.search(query)

            # Get results
            result_count = search.get_result_count()
            first_result = search.get_first_result_title()

            log_success(f"Query: {query}")
            core.logger.info(f"  Results: {result_count}")
            core.logger.info(f"  Top result: {first_result}")

            # Go back to continue searching
            core.page.goto("https://www.google.com")


def form_submission_workflow():
    """Example showing form component usage."""

    with UIAutomationCore(
        app_name="form_example",
        script_name="contact_form",
        headless=False
    ) as core:

        # Example: Contact form submission
        log_step("Navigating to contact form")
        core.page.goto("https://www.example.com/contact")  # Replace with actual URL

        # Create form component
        contact_form = FormComponent(core.page, form_selector="#contact-form")

        # Fill and submit form in one call
        log_step("Filling contact form")
        contact_form.fill_and_submit({
            "#name": "John Doe",
            "#email": "john@example.com",
            "#subject": "Inquiry",
            "#message": "This is an automated test message"
        }, wait_for_navigation=True)

        log_success("Form submitted successfully")


# ==================== Advanced Component Pattern ====================

class CustomApplicationForm(BaseComponent):
    """Custom component for your specific application.

    This shows how to create app-specific components with
    domain logic encapsulated.
    """

    def __init__(self, page):
        super().__init__(page)
        self.form_data = {}

    def fill_personal_info(self, name: str, email: str, phone: str):
        """Fill personal information section.

        Args:
            name: Full name
            email: Email address
            phone: Phone number
        """
        log_step("Filling personal information")

        self.input("#full_name", name)
        self.input("#email", email)
        self.input("#phone", phone)

        self.form_data.update({
            "name": name,
            "email": email,
            "phone": phone
        })

    def fill_address(self, street: str, city: str, state: str, zip_code: str):
        """Fill address section.

        Args:
            street: Street address
            city: City
            state: State
            zip_code: ZIP code
        """
        log_step("Filling address information")

        self.input("#street", street)
        self.input("#city", city)
        self.select("#state", state)
        self.input("#zip", zip_code)

        self.form_data.update({
            "street": street,
            "city": city,
            "state": state,
            "zip": zip_code
        })

    def accept_terms(self):
        """Accept terms and conditions."""
        log_step("Accepting terms and conditions")
        self.check("#terms_checkbox")

    def submit(self):
        """Submit the application form."""
        log_step("Submitting application")

        self.click("#submit_button")
        self.wait_for_text("#confirmation", "Application submitted")

        log_success("Application submitted successfully")

    def verify_summary(self) -> bool:
        """Verify the summary page shows correct information.

        Returns:
            True if all information matches
        """
        log_step("Verifying application summary")

        # Check if submitted data matches
        summary_name = self.get_text("#summary_name")
        summary_email = self.get_text("#summary_email")

        if summary_name != self.form_data.get("name"):
            self.logger.error(f"Name mismatch: {summary_name} != {self.form_data.get('name')}")
            return False

        if summary_email != self.form_data.get("email"):
            self.logger.error(f"Email mismatch: {summary_email} != {self.form_data.get('email')}")
            return False

        log_success("Summary verification passed")
        return True


def advanced_application_workflow():
    """Advanced workflow using custom component."""

    with UIAutomationCore(
        app_name="application_example",
        script_name="job_application",
        headless=False
    ) as core:

        # Navigate to application page
        core.page.goto("https://www.example.com/apply")  # Replace with actual URL

        # Create custom application component
        app_form = CustomApplicationForm(core.page)

        # Fill application step by step
        app_form.fill_personal_info(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="555-0123"
        )

        app_form.fill_address(
            street="123 Main St",
            city="Springfield",
            state="IL",
            zip_code="62701"
        )

        app_form.accept_terms()

        # Take screenshot before submission
        core.take_screenshot("before_submit")

        app_form.submit()

        # Verify submission
        if app_form.verify_summary():
            log_success("Application workflow completed successfully")
        else:
            core.logger.error("Application verification failed")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("COMPONENT-BASED WORKFLOW EXAMPLES")
    print("="*80 + "\n")

    print("1. Google Search with Components")
    google_search_workflow()

    print("\n2. Form Submission Example")
    # form_submission_workflow()  # Uncomment when you have a real form URL

    print("\n3. Advanced Application Workflow")
    # advanced_application_workflow()  # Uncomment when you have a real application URL

    print("\n" + "="*80)
    print("Examples completed! Check the performance reports above.")
    print("="*80 + "\n")
