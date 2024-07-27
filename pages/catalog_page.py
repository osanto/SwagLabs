from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Optional, Tuple

from pages.base_page import BasePage
from pages.product_page import ProductPage
from config import Logging

logger = Logging.setup_logging()


def open_catalog_page(driver: WebDriver):
    logger.info("Navigating to Catalog Page.")
    return CatalogPage(driver)


class CatalogPage(BasePage):
    PRODUCTS_TITLE: Tuple[By, str] = (By.XPATH, "//span[@class='title']")
    PRODUCT_NAMES_LIST: Tuple[By, str] = (By.XPATH, "// div[@data-test = 'inventory-item-name']")
    PRODUCT_PRICES_LIST: Tuple[By, str] = (By.XPATH, "//div[@class='inventory_item_price']")
    ADD_TO_CART_BUTTON: Tuple[By, str] = (By.XPATH,"//div[text()='{}']"
                                                   "/ancestor::div[@class='inventory_item_description']//button")
    TITLE_LINK: Tuple[By, str] = (By.XPATH, "//div[text()='{}']/ancestor::a[@href='#']")
    IMAGE_LINK: Tuple[By, str] = (By.XPATH, "//img[@alt='{}']")
    PRODUCT_NAME: Tuple[By, str] = (By.XPATH,
                                    "//div[@data-test='inventory-item'][{}]//div[@data-test='inventory-item-name']")
    SORT_BUTTON = (By.CLASS_NAME, "product_sort_container")

    def __init__(self, driver: WebDriver) -> None:
        logger.info("Navigating to Catalog Page.")
        super().__init__(driver)

    @staticmethod
    def open(driver: WebDriver):
        logger.info("Opening a Catalog Page.")
        return CatalogPage(driver)

    def sort_products(self, text: str) -> None:
        if self._select_from_dropdown(self.SORT_BUTTON, text) is None:
            logger.warning(f"Error while sorting products.")
        return None

    def get_products_names(self) -> list:
        product_names_list = self.PRODUCT_NAMES_LIST
        elements_list = self._get_visible_elements(product_names_list)
        if not elements_list:
            logger.warning("No product elements found.")
            return []

        product_names = [element.text for element in elements_list]
        if not product_names:
            logger.warning("No text found in the product elements.")

        logger.info(f"Retrieved {len(product_names)} product names: {product_names}")
        return product_names

    def get_products_prices(self) -> list:
        product_prices_list = self.PRODUCT_PRICES_LIST
        elements_list = self._get_visible_elements(product_prices_list)
        actual_product_prices = [element.text for element in elements_list]
        try:
            actual_prices = [float(price.replace('$', '').replace(',', '')) for price in actual_product_prices]
        except ValueError as e:
            logger.error(f"Error converting price to float: {e}")
            return []

        logger.info(f"Retrieved product prices list:  {actual_prices}")
        return actual_prices

    def get_product_name_by_position(self, position: int) -> Optional[str]:
        product_name_xpath = self._build_dynamic_locator(self.PRODUCT_NAME, position)
        product_name_text = self._get_text(product_name_xpath)
        if product_name_text is None:
            logger.warning(f"Unable to retrieve product number: {position}")
            return None
        logger.warning(f"Retrieved product: {product_name_text}")
        return product_name_text

    def add_product_to_cart(self, product_name: str) -> None:
        add_to_cart_button = self._build_dynamic_locator(self.ADD_TO_CART_BUTTON, product_name)
        logger.info(f"Adding product '{product_name}' to cart.")
        if self._click(add_to_cart_button, element_name="Add to Cart button") is None:
            logger.warning("Product title was not clicked. Navigating process aborted.")
            return None

    def navigate_to_product_page_via_product_name_link(self, product_name: str) -> Optional[ProductPage]:
        name_link = self._build_dynamic_locator(self.TITLE_LINK, product_name)
        if self._click(name_link, element_name="Product name") is None:
            logger.warning("Product name was not clicked. Navigating process aborted.")
            return None
        logger.info(f"Product name {product_name} clicked")
        return ProductPage(self.driver)

    def navigate_to_product_page_via_product_image(self, product_name: str) -> Optional[ProductPage]:
        image = self._build_dynamic_locator(self.IMAGE_LINK, product_name)
        if self._click(image, element_name="Product image") is None:
            logger.warning("Product image was not clicked. Navigating process aborted.")
            return None
        return ProductPage(self.driver)




