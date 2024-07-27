from tests.base_test import BaseTest
from pages.catalog_page import CatalogPage
from pages.main_page import MainPage
from config import Logging


logger = Logging.setup_logging()


class TestCartInteraction(BaseTest):
    def test_add_product_to_cart_via_catalog(self, driver):
        catalog_page = CatalogPage.open(driver)

        product_one = catalog_page.get_product_name_by_position(3)
        assert product_one, "Unable to retrieve product name on Catalog page."
        catalog_page.add_product_to_cart(product_one)

        product_two = catalog_page.get_product_name_by_position(1)
        assert product_one, "Unable to retrieve product name on Catalog page."
        catalog_page.add_product_to_cart(product_two)

        main_page = MainPage.open(driver)
        icon_value = main_page.get_cart_icon_value()
        assert icon_value == '2'

        cart_page = main_page.navigate_to_cart()

        assert cart_page.search_product_by_name(product_one), f"Product {product_one} not found on Cart page."
        assert cart_page.search_product_by_name(product_two), f"Product {product_two} not found on Cart page."

    def test_remove_product_from_cart_via_catalog(self, driver):
        catalog_page = CatalogPage.open(driver)

        product_one = catalog_page.get_product_name_by_position(3)
        assert product_one, "Unable to retrieve product name on Catalog page."

        catalog_page.add_product_to_cart(product_one)

        product_two = catalog_page.get_product_name_by_position(1)
        catalog_page.add_product_to_cart(product_two)

        main_page = MainPage.open(driver)
        cart_page = main_page.navigate_to_cart()

        cart_page.remove_product_by_name(product_one)
        icon_value = main_page.get_cart_icon_value()
        assert icon_value == '1'

        cart_page.remove_product_by_name(product_two)

        assert main_page.is_shopping_cart_badge_not_visible(), "Shopping cart badge still visible."
        assert cart_page.is_cart_item_class_removed(), "Removed class is not visible."

    def test_add_product_to_cart_via_product(self, driver):
        catalog_page = CatalogPage.open(driver)

        product = catalog_page.get_product_name_by_position(5)
        assert product, "Unable to retrieve product name on Catalog page."

        product_page = catalog_page.navigate_to_product_page_via_product_name_link(product)
        product_page.add_product_to_cart()

        main_page = MainPage.open(driver)
        icon_value = main_page.get_cart_icon_value()
        assert icon_value == '1'

        cart_page = main_page.navigate_to_cart()
        cart_page.search_product_by_name(product)

        assert cart_page.search_product_by_name(product),  f"Product {product} not found on Cart page."

    def test_remove_product_from_cart_via_product(self, driver):
        catalog_page = CatalogPage.open(driver)

        product = catalog_page.get_product_name_by_position(5)
        assert product, "Unable to retrieve product name."
        catalog_page.add_product_to_cart(product)

        product_page = catalog_page.navigate_to_product_page_via_product_name_link(product)

        product_page.remove_product()
        assert product_page.is_add_button_displayed(), "Add to cart button is not displayed."
