from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Optional, Tuple

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from config import Logging

logger = Logging.setup_logging()


class CartPage(BasePage):
    REMOVE_FROM_CART_BUTTON: Tuple[By, str] = (By.XPATH, "//div[text()='{}']"
                                                         "/ancestor::div[@class='cart_item_label']//button")
    REMOVED_FROM_CARD_CLASS: Tuple[By, str] = (By.XPATH, "//div[@data-test ='inventory-item']")
    CHECKOUT_BUTTON: Tuple[By, str] = (By.XPATH, "//button[@data-test = 'checkout']")
    PRODUCT_NAME: Tuple[By, str] = (By.XPATH, "//div[text()='{}']")

    def __init__(self, driver: WebDriver) -> None:
        logger.info("Navigating to Cart Page.")
        super().__init__(driver)

    def checkout(self) -> Optional[CheckoutPage]:
        if self._click(self.CHECKOUT_BUTTON, element_name="Checkout button") is None:
            logger.warning("Checkout button was not clicked. Checkout process aborted.")
            return None
        return CheckoutPage(self.driver)

    def search_product_by_name(self, product_name: str) -> bool:
        product_name_locator = self._build_dynamic_locator(self.PRODUCT_NAME, product_name)
        product_name_text = self._get_text(product_name_locator)
        if product_name_text is None:
            logger.warning(f"Product '{product_name}' not found.")
            return False
        logger.info(f"Retrieved product: '{product_name_text}'")
        return True

    def remove_product_by_name(self, product_name: str) -> None:
        remove_from_cart_button = self._build_dynamic_locator(self.REMOVE_FROM_CART_BUTTON, product_name)
        logger.info(f"Removing product '{product_name}' from cart.")
        if self._click(remove_from_cart_button, element_name="Remove button") is None:
            logger.warning(f"Remove button was not clicked. Checkout process aborted.")
            return None

    def is_cart_item_class_removed(self) -> bool:
        if not self._wait_until_element_is_invisible(self.REMOVED_FROM_CARD_CLASS):
            logger.warning("Removed class element is still present.")
            return False
        return True
