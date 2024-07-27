from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Tuple

from pages.base_page import BasePage
from config import Logging

logger = Logging.setup_logging()


class CheckoutPage(BasePage):
    FIRST_NAME: Tuple[By, str] = (By.XPATH, "//input[@id = 'first-name']")
    LAST_NAME: Tuple[By, str] = (By.XPATH, "//input[@id = 'last-name']")
    POSTAL_CODE: Tuple[By, str] = (By.XPATH, "//input[@id = 'postal-code']")
    CONTINUE_BUTTON: Tuple[By, str] = (By.XPATH, "//input[@data-test = 'continue']")
    FINISH_BUTTON: Tuple[By, str] = (By.XPATH, "//button[@data-test = 'finish']")
    COMPLETE_HEADER: Tuple[By, str] = (By.XPATH, "//h2[@class = 'complete-header']")
    CHECKOUT_ERROR: Tuple[By, str] = (By.XPATH, "//h3[contains(text(), 'Error')]")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("Navigating to Checkout Page.")

    def get_order_completion_header(self):
        return self._get_text(self.COMPLETE_HEADER)

    def get_mandatory_field_error(self):
        return self._get_text(self.CHECKOUT_ERROR)

    def click_continue(self) -> None:
        if self._click(self.CONTINUE_BUTTON, element_name="Continue button") is None:
            logger.warning("Continue button was not clicked. Checkout process aborted.")
            return None

    def click_finish(self) -> None:
        if not self._click(self.FINISH_BUTTON, element_name="Finish button"):
            logger.warning("Finish button was not clicked. Checkout process aborted.")
            return None

    def populate_all_fields(self, first_name: str, last_name: str, postal_code: str) -> None:
        logger.info(f"Populating fields: First Name, Last Name, Postal Code")
        self._populate_field(self.FIRST_NAME, first_name)
        self._populate_field(self.LAST_NAME, last_name)
        self._populate_field(self.POSTAL_CODE, postal_code)




