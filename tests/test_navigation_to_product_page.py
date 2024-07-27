from tests.base_test import BaseTest
from pages.catalog_page import CatalogPage


class TestProductPage(BaseTest):
    def test_navigate_to_product_via_name(self, driver):
        catalog_page = CatalogPage.open(driver)

        product = catalog_page.get_product_name_by_position(2)
        assert product, "Unable to retrieve product name."

        product_page = catalog_page.navigate_to_product_page_via_product_name_link(product)
        assert product_page, f"Unable to navigate to Product Page via '{product}' title link"

        product_name_on_product_page = product_page.get_product_name()
        assert product == product_page.get_product_name(), (
            f"Title on catalog page does not match to title on product page."
            f"Catalog Page: {product}, "f"Product Page: {product_name_on_product_page}.")

    def test_navigate_to_product_via_product_card(self, driver):
        catalog_page = CatalogPage.open(driver)
        product = catalog_page.get_product_name_by_position(6)
        assert product, "Unable to retrieve product name."

        product_page = catalog_page.navigate_to_product_page_via_product_image(product)
        assert product_page, f"Unable to navigate to Product Page via '{product}' image"

        product_name_on_product_page = product_page.get_product_name()
        assert product == product_name_on_product_page, (
            f"Title on catalog page does not match to title on product page."
            f"Catalog Page: {product}, "f"Product Page: {product_name_on_product_page}.")

