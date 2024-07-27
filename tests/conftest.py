import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    yield login
