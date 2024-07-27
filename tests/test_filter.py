from tests.base_test import BaseTest
from pages.catalog_page import CatalogPage


class TestFilter(BaseTest):
    def test_filter_products_a_z(self, driver):
        catalog_page = CatalogPage.open(driver)
        catalog_page.sort_products("Name (A to Z)")

        actual_product_names = catalog_page.get_products_names()
        assert actual_product_names, "Product names list is empty."

        expected_product_names = sorted(actual_product_names)
        assert actual_product_names == expected_product_names, (f"Actual names list does not match to expected."
                                                                f"Actual: {actual_product_names}, "
                                                                f"Expected: {expected_product_names}.")

    def test_filter_products_z_a(self, driver):
        catalog_page = CatalogPage.open(driver)
        catalog_page.sort_products("Name (Z to A)")

        actual_product_names = catalog_page.get_products_names()
        assert actual_product_names, "Product names list is empty."

        expected_product_names = sorted(actual_product_names, reverse=True)
        assert actual_product_names == expected_product_names, (f"Actual names list does not match to expected."
                                                                f"Actual: {actual_product_names}, "
                                                                f"Expected: {expected_product_names}.")

    def test_filter_products_prices_asc(self, driver):
        catalog_page = CatalogPage.open(driver)
        catalog_page.sort_products("Price (low to high)")

        actual_product_prices = catalog_page.get_products_prices()
        assert actual_product_prices, "Product prices list is empty."

        expected_product_prices = sorted(actual_product_prices)
        assert actual_product_prices == expected_product_prices, (f"Actual prices list does not match the expected.\n"
                                                                  f"Actual: {actual_product_prices},\n"
                                                                  f"Expected: {expected_product_prices}."
                                                                  )

    def test_filter_products_prices_desc(self, driver):
        catalog_page = CatalogPage.open(driver)
        catalog_page.sort_products("Price (high to low)")

        actual_product_prices = catalog_page.get_products_prices()
        assert actual_product_prices, "Product prices list is empty."

        expected_product_prices = sorted(actual_product_prices, reverse=True)
        assert actual_product_prices == expected_product_prices, (f"Actual names list does not match to expected."
                                                                  f"Actual: {actual_product_prices}, "
                                                                  f"Expected: {expected_product_prices}.")

