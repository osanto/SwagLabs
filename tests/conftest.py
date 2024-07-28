import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

from pages.login_page import *
from config import UserData


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    page = open_login_page(driver)
    page.login(UserData.USER_NAME, UserData.PASSWORD)
    yield page


def find_project_root(starting_directory):
    current_directory = starting_directory
    while True:
        if 'README.md' in os.listdir(current_directory) or 'requirements.txt' in os.listdir(current_directory):
            return current_directory
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            raise FileNotFoundError("Could not find the project root.")
        current_directory = parent_directory


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver', None)
        if driver:
            project_root = find_project_root(os.path.abspath(os.path.dirname(__file__)))

            # Define the reports directory path in the project root
            reports_dir = os.path.join(project_root, 'reports')
            screenshot_dir = os.path.join(reports_dir, 'failed_tests_screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)

            # Generate a safe filename for the screenshot
            screenshot_name = os.path.join(screenshot_dir, f"{item.nodeid.replace('::', '_').replace('/', '_')}.png")
            try:
                driver.save_screenshot(screenshot_name)
                print(f"Screenshot taken: {screenshot_name}")
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
        else:
            print("Driver not found for failed test.")
