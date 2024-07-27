from tests.base_test import BaseTest
from pages.login_page import *


class TestLogin:
    def test_login_positive(self, driver):
        login_page = open_login_page(driver)
        login_page.login("standard_user", "secret_sauce")

        actual_title = login_page.get_title()
        assert actual_title, f"Title was not found: {actual_title}."

        expected_title = "Swag Labs"
        assert actual_title == expected_title, (f"Actual text does not match to expected."
                                                f"Actual: {actual_title},  "f"Expected : {expected_title}.")

    def test_login_negative(self, driver):
        login_page = open_login_page(driver)
        login_page.login("user'", "user")

        actual_error = login_page.get_error_message()
        assert actual_error, f"Error message was not found: {actual_error}"

        expected_error = "Epic sadface: Username and password do not match any user in this service"
        assert actual_error == expected_error, (f"Actual error does not match to expected."
                                                f"Actual: {actual_error}, Expected: {expected_error}.")




