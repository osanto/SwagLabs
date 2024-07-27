from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Optional, Tuple

from pages.base_page import BasePage
from config import Logging

logger = Logging.setup_logging()


class ProductPage(BasePage):
    ADD_TO_CART_BUTTON: Tuple[By, str] = (By.XPATH, "//button[@data-test = 'add-to-cart']")
    REMOVE_BUTTON: Tuple[By, str] = (By.XPATH, "//button[@data-test='remove']")
    PRODUCT_NAME: Tuple[By, str] = (By.XPATH, "//div[@data-test='inventory-item-name']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        logger.info("Navigating to Product Page.")

    def get_product_name(self) -> Optional[str]:
        name = self._get_text(self.PRODUCT_NAME)
        if name is None:
            logger.error("Unable to retrieve Product name.")
            return None
        return name

    def is_add_button_displayed(self) -> bool:
        add_to_cart_button = self._get_visible_element(self.ADD_TO_CART_BUTTON)
        if add_to_cart_button is None:
            logger.warning(f"Add to cart button is not visible or does not exist.")
            return False
        return True

    def add_product_to_cart(self) -> None:
        if self._click(self.ADD_TO_CART_BUTTON, element_name="Add to cart button") is None:
            logger.warning("Add to cart button could not be clicked.")

    def remove_product(self) -> None:
        if self._click(self.REMOVE_BUTTON, element_name="Remove button") is None:
            logger.warning("Remove button could not be clicked.")





