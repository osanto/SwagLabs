from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (TimeoutException,  ElementClickInterceptedException,
                                        StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from typing import Optional, Union

from config import Logging

logger = Logging.setup_logging()


class BasePage:
    Locator = tuple[str, str]

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=10)

    def get_title(self) -> Optional[str]:
        try:
            title = self.driver.title
            logger.info(f"Retrieved title: {title}")
            return title
        except WebDriverException as e:
            logger.error(f"Failed to get title: {e}")
            return None

    def get_current_url(self) -> Optional[str]:
        try:
            url = self.driver.current_url
            logger.info(f"Retrieved current URL: {url}")
            return url
        except WebDriverException as e:
            logger.error(f"Failed to get current URL: {e}")
            return None

    def _get_text(self, locator: Locator) -> Optional[str]:
        element = self._get_visible_element(locator)
        if element is None:
            logger.warning(f"Element with locator {locator} is not visible or does not exist.")
            return None
        text = element.text
        logger.info(f"Retrieved text from element: '{text}'")
        return text

    def _get_clickable_element(self, locator: Locator) -> Optional[WebElement]:
        try:
            return self.wait.until(ec.element_to_be_clickable(locator))
        except TimeoutException:
            logger.warning(f"Element with locator {locator} is not clickable after waiting.")
            return None

    def _get_visible_element(self, locator: Locator) -> Optional[WebElement]:
        try:
            return self.wait.until(ec.visibility_of_element_located(locator))
        except TimeoutException:
            logger.warning(f"Element with locator {locator} is not visible after waiting.")
            return None

    def _get_visible_elements(self, locator: Locator) -> list[WebElement]:
        try:
            return self.wait.until(ec.visibility_of_all_elements_located(locator))
        except TimeoutException:
            logger.warning(f"Elements with locator {locator} are not visible after waiting.")
            return []

    def _get_present_element(self, locator: Locator) -> Optional[WebElement]:
        try:
            return self.wait.until(ec.presence_of_element_located(locator))
        except TimeoutException:
            logger.warning(f"Element with locator {locator} is not present after waiting.")
            return None

    def _wait_until_element_is_invisible(self, locator: Locator) -> Optional[WebElement]:
        try:
            return self.wait.until(ec.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.warning(f"Element with locator {locator} is still visible after waiting.")
            return None

    def _click(self, locator: Locator, element_name: str = "Element") -> bool:
        try:
            element = self._get_clickable_element(locator)
            if element is None:
                logger.warning(f"{element_name} is not clickable.")
                return False
            element.click()
            return True
        except (ElementClickInterceptedException, StaleElementReferenceException) as e:
            logger.error(f"{element_name} could not be clicked: {e}")
            return False

    def _populate_field(self, locator: Locator, content: str,  field_name: str = "Field") -> None:
        element = self._get_visible_element(locator)
        if element is None:
            logger.warning(f"Field with locator {locator} is not visible.")
            return None
        element.send_keys(content)

    def _select_from_dropdown(self, locator: Locator, option: str) -> None:
        dropdown_element = self._find_dropdown_element(locator)
        if dropdown_element is None:
            logger.warning(f"Dropdown with locator {locator} is not visible.")
            return None
        dropdown_element.select_by_visible_text(option)

    def _find_dropdown_element(self, locator: Locator) -> Optional[Select]:
        element = self._get_visible_element(locator)
        if element is None:
            logger.warning(f"Element with locator {locator} is not visible.")
            return None
        return Select(element)

    @staticmethod
    def _build_dynamic_locator(locator: Locator, value: Union[str, int]) -> Locator:
        by, path = locator
        return by, path.format(value)

