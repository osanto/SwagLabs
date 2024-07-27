from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Optional, Tuple

from pages.base_page import BasePage
from config import Urls
from config import Logging

logger = Logging.setup_logging()


def open_login_page(driver: WebDriver):
    logger.info("Opening a Login Page.")
    driver.get(Urls.login_url)
    return LoginPage(driver)


class LoginPage(BasePage):
    NAME_INPUT: Tuple[By, str] = (By.XPATH, '//*[@id="user-name"]')
    PASSWORD_INPUT: Tuple[By, str] = (By.XPATH, '//*[@id="password"]')
    LOGIN_BUTTON: Tuple[By, str] = (By.XPATH, '//*[@id="login-button"]')
    ERROR_MESSAGE: Tuple[By, str] = (By.XPATH, "//h3[contains(text(), 'Epic sadface')]")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def login(self, username: str, password: str) -> None:
        self._populate_field(self.NAME_INPUT, username, field_name="Name input")
        self._populate_field(self.PASSWORD_INPUT, password, field_name="Password input")
        if self._click(self.LOGIN_BUTTON, element_name="Login button") is None:
            logger.error("Login button was not clicked. Login process aborted.")
            return None

    def get_error_message(self) -> Optional[str]:
        message = self._get_text(self.ERROR_MESSAGE)
        if message is None:
            logger.error("Error message was not found")
            return None
        return message

