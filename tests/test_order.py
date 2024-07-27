import pytest

from tests.base_test import BaseTest
from pages.catalog_page import *
from pages.main_page import MainPage


class TestOrder(BaseTest):
    def test_order_with_valid_credentials(self, driver):
        catalog_page = CatalogPage.open(driver)

        product = catalog_page.get_product_name_by_position(2)
        assert product, "Unable to retrieve product name."

        catalog_page.add_product_to_cart(product)

        main_page = MainPage.open(driver)
        cart_page = main_page.navigate_to_cart()
        checkout_page = cart_page.checkout()

        checkout_page.populate_all_fields("First", "Last", "66012")
        checkout_page.click_continue()
        checkout_page.click_finish()

        actual_header = checkout_page.get_order_completion_header()
        assert actual_header, "'Thank you for your order!' was not found."

        expected_header = 'Thank you for your order!'
        assert expected_header == actual_header, (f"Actual header does not match to expected."
                                                  f"Actual: {actual_header}, Expected: {expected_header}.")

    data = [
            ["", "LastName ", "55556", "Error: First Name is required"],
            ["First Name", "", "20231", "Error: Last Name is required"],
            ["First Name", "Last Name", "", "Error: Postal Code is required"]
        ]

    @pytest.mark.parametrize("user_data", data)
    def test_order_with_invalid_credentials(self, driver, user_data):
        catalog_page = CatalogPage.open(driver)

        product = catalog_page.get_product_name_by_position(2)
        assert product, "Unable to retrieve product name."

        catalog_page.add_product_to_cart(product)

        main_page = MainPage.open(driver)
        cart_page = main_page.navigate_to_cart()
        checkout_page = cart_page.checkout()

        checkout_page.populate_all_fields(user_data[0], user_data[1], user_data[2])
        checkout_page.click_continue()

        actual_error = checkout_page.get_mandatory_field_error()
        assert actual_error, "Failed to retrieve an error"
        assert user_data[3] == actual_error,  (f"Actual error does not match to expected."
                                               f" Actual: {actual_error}, Expected: {user_data[3]}.")
