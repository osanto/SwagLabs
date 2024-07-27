from dotenv import load_dotenv
import os
import logging

# Load environment variables from the .env file
load_dotenv()


class UserData:
    USER_NAME = os.getenv('USER_NAME')
    PASSWORD = os.getenv('PASSWORD')


class Urls:
    base_url = "https://www.saucedemo.com"
    login_url = base_url + "/"
    about_url = "https://saucelabs.com/"


class Logging:
    def setup_logging(level=logging.INFO):
        logging.basicConfig(level=level)
        logger = logging.getLogger(__name__)
        return logger
