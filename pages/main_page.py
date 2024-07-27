from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import Optional, Tuple

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from config import Logging

logger = Logging.setup_logging()


class MainPage(BasePage):
    CART_ICON: Tuple[By, str] = (By.XPATH, "//span[@data-test = 'shopping-cart-badge']")
    CART_BUTTON: Tuple[By, str] = (By.XPATH, "//div[@id = 'shopping_cart_container']")
    BURGER_BUTTON: Tuple[By, str] = (By.XPATH, "//button[contains(text(), 'Open Menu')]")
    LOGOUT_BUTTON: Tuple[By, str] = (By.XPATH, "//a[@id = 'logout_sidebar_link']")
    ABOUT_BUTTON: Tuple[By, str] = (By.ID, 'about_sidebar_link')
    RESET_BUTTON: Tuple[By, str] = (By.ID, 'reset_sidebar_link')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    @staticmethod
    def open(driver: WebDriver):
        logger.info("Navigating to Main Page.")
        return MainPage(driver)

    def get_cart_icon_value(self) -> Optional[str]:
        cart_icon_value = self._get_text(self.CART_ICON)
        if cart_icon_value is None:
            logger.warning("Unable to retrieve icon value.")
            return None
        return cart_icon_value

    def navigate_to_cart(self) -> Optional[CartPage]:
        if self._click(self.CART_BUTTON, element_name="Cart button") is None:
            logger.warning("Cart button was not clicked. Unable to navigate to Cart page")
            return None
        return CartPage(self.driver)

    def is_shopping_cart_badge_not_visible(self) -> bool:
        if not self._wait_until_element_is_invisible(self.CART_ICON):
            logger.warning("Shopping cart badge is still visible.")
            return False
        return True

    def logout(self) -> LoginPage:
        if self._click(self.BURGER_BUTTON, element_name="Burger button") is False:
            logger.warning("Burger button is not visible.")
        if self._click(self.LOGOUT_BUTTON, element_name="Login button") is False:
            logger.warning("Login button is not visible.")
        return LoginPage(self.driver)

    def get_about_url(self) -> Optional[str]:
        if self._click_burger_menu() is False:
            logger.warning("Burger menu button is not visible.")
        about = self._get_visible_element(self.ABOUT_BUTTON)
        return about.get_attribute('href')

    def reset(self) -> None:
        if self._click_burger_menu() is False:
            logger.warning("Burger menu button is not visible.")
        if self._click(self.RESET_BUTTON, element_name="Reset button") is False:
            logger.warning("Reset button is not visible.")

    def _click_burger_menu(self) -> None:
        if self._click(self.BURGER_BUTTON, element_name="Burger button") is False:
            logger.warning("Burger menu button is not visible.")










