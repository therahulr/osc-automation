"""Quote page object for OSC application."""

from playwright.sync_api import Page

from apps.osc.locators.quote_locators import (
    CUSTOMER_EMAIL_INPUT,
    CUSTOMER_NAME_INPUT,
    CUSTOMER_PHONE_INPUT,
    PRODUCT_SELECT,
    QUANTITY_INPUT,
    SAVE_QUOTE_BUTTON,
    SUCCESS_MESSAGE,
)
from apps.osc.pages.base_page import OSCBasePage


class QuotePage(OSCBasePage):
    """Quote creation page object for OSC application.

    Handles quote creation workflow.
    """

    def __init__(self, page: Page) -> None:
        """Initialize quote page.

        Args:
            page: Playwright Page instance
        """
        super().__init__(page)

    def open(self) -> None:
        """Navigate to OSC quote creation page."""
        self.logger.info(f"Opening quote page | url={self.settings.quote_url}")
        self.ui.goto(self.settings.quote_url)

    def fill_customer_info(self, name: str, email: str, phone: str) -> None:
        """Fill customer information section.

        Args:
            name: Customer name
            email: Customer email
            phone: Customer phone number

        Raises:
            RuntimeError: If form filling fails
        """
        self.logger.info(f"Filling customer info | name={name}, email={email}")

        try:
            self.ui.input_text(CUSTOMER_NAME_INPUT, name)
            self.ui.input_text(CUSTOMER_EMAIL_INPUT, email)
            self.ui.input_text(CUSTOMER_PHONE_INPUT, phone)

            self.logger.debug("Customer info filled successfully")

        except Exception as e:
            self.logger.error(f"Failed to fill customer info | error={e}")
            raise RuntimeError(f"Failed to fill customer info: {e}") from e

    def select_product(self, product_value: str, quantity: int) -> None:
        """Select product and quantity.

        Args:
            product_value: Product option value
            quantity: Product quantity

        Raises:
            RuntimeError: If product selection fails
        """
        self.logger.info(f"Selecting product | product={product_value}, quantity={quantity}")

        try:
            self.ui.select_option(PRODUCT_SELECT, product_value)
            self.ui.input_text(QUANTITY_INPUT, str(quantity))

            self.logger.debug("Product selected successfully")

        except Exception as e:
            self.logger.error(f"Failed to select product | error={e}")
            raise RuntimeError(f"Failed to select product: {e}") from e

    def save_quote(self) -> None:
        """Submit quote form and verify success.

        Raises:
            RuntimeError: If save fails
        """
        self.logger.info("Saving quote")

        try:
            self.ui.click(SAVE_QUOTE_BUTTON, name="Save Quote button")
            self.ui.wait_visible(SUCCESS_MESSAGE, timeout_ms=10000)

            self.logger.info("Quote saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save quote | error={e}")
            raise RuntimeError(f"Failed to save quote: {e}") from e

    def create_quote(
        self,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        product: str,
        quantity: int,
    ) -> None:
        """Complete quote creation workflow.

        Args:
            customer_name: Customer name
            customer_email: Customer email
            customer_phone: Customer phone
            product: Product selection value
            quantity: Product quantity

        Raises:
            RuntimeError: If quote creation fails
        """
        self.logger.info(f"Creating quote | customer={customer_name}, product={product}")

        self.fill_customer_info(customer_name, customer_email, customer_phone)
        self.select_product(product, quantity)
        self.save_quote()

        self.logger.info("Quote creation workflow completed")
