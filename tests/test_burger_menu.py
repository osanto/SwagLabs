from tests.base_test import BaseTest
from config import Urls
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage


class TestBurgerMenu(BaseTest):

    def test_logout(self, driver):
        main_page = MainPage.open(driver)
        login_page = main_page.logout()

        actual_url = login_page.get_current_url()
        assert actual_url, "Failed to retrieve Login page url."

        expected_url = Urls.login_url
        assert actual_url == expected_url, (f"Actual url does not match to expected."
                                            f"Actual: {actual_url}, Expected: {expected_url}.")

    def test_about_button(self, driver):
        main_page = MainPage.open(driver)

        actual_url = main_page.get_about_url()
        assert actual_url, "Failed to retrieve 'about' url."

        expected_url = Urls.about_url
        assert actual_url == expected_url,  (f"Actual url does not match to expected."
                                             f"Actual: {actual_url}, Expected: {expected_url}.")

    def test_menu_reset(self, driver):
        product_catalog_page = CatalogPage.open(driver)

        first_product = product_catalog_page.get_product_name_by_position(1)
        assert first_product, "Unable to retrieve product name."

        second_product = product_catalog_page.get_product_name_by_position(2)
        assert second_product, "Unable to retrieve product name."

        product_catalog_page.add_product_to_cart(first_product)
        product_catalog_page.add_product_to_cart(second_product)

        main_page = MainPage.open(driver)
        main_page.reset()

        assert main_page.is_shopping_cart_badge_not_visible(), "Shopping cart badge still visible."

        cart_page = main_page.navigate_to_cart()
        assert cart_page.is_cart_item_class_removed(), "Removed class is not visible."
