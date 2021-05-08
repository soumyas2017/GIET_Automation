from utilties.config import (
    login_successful_div_element,
    login_url,
    login_page_load_wait_duration,
    chrome_driver_path,
    firefox_driver_path
)
from utilties.constants import *
from utilties.helpers import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class SeleniumFactory:
    def __init__(self):
        if sys.platform == 'win32':
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        else:
            self.driver = webdriver.Firefox(executable_path=firefox_driver_path)
        self.url = login_url

    def connect(self):
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, login_page_load_wait_duration).until(EC.presence_of_element_located(
                (By.CLASS_NAME, login_successful_div_element)))
            self.driver.minimize_window()
        except TimeoutException:
            logger.exception("Unable to connect")
            sys.exit()
        else:
            return True

    def disconnect(self):
        try:
            self.driver.close()
        except Exception as e:
            logger.exception(f"Unable to close the browser instance {e}")

    def search_and_click_by_xpath(self, main_tag='select', tag_name='name', tag_value=None, tag_search_text=None, static_tag=None,):
        try:

            if not static_tag:
                if tag_value is not None:
                    if tag_search_text is not None:
                        self.driver.find_element_by_xpath(
                            f"//{main_tag}[@{tag_name}='{tag_value}']/option[text()='{tag_search_text}']").click()
                        return True
                    else:
                        self.driver.find_element_by_xpath(
                            f"//{main_tag}[@{tag_name}='{tag_value}']").click()
                        return True
                else:
                    return False
            else:
                self.driver.find_element_by_xpath(static_tag).click()
                return True

        except Exception as e:
            logger.exception(f"Exception {e}")
            return False

    def search_and_return_items_by_xpath(self, main_tag='select', tag_name='name', tag_value=None, tag_search_text=None):
        try:
            items = self.driver.find_element_by_xpath(
                f"//{main_tag}[@{tag_name}='{tag_value}']").text.split('\n')
            scrubbed_items = remove_junks(items)
            return True, scrubbed_items
        except Exception as e:
            logger.exception(f"Unable to search items - {e}")
            return False, None

    def search_and_send_keys_by_name(self, tag_value=None, tag_search_text=None):
        try:
            if tag_value is not None and tag_search_text is not None:
                self.driver.find_element_by_name(tag_value).send_keys(tag_search_text)
                return True
            else:
                print("Insufficient Data")
                return False
        except Exception as e:
            print(f"Exception as {e}")
            return False

    def search_and_send_keys_by_class_name(self, tag_value=None, tag_search_text=None):
        try:
            if tag_value is not None and tag_search_text is not None:
                self.driver.find_element_by_name(tag_value).send_keys(tag_search_text)
                return True
            else:
                print("Insufficient Data")
                return False
        except Exception as e:
            logger.exception(f"Exception as {e}")
            return False

    def click_by_class_name(self, tag_value=None):
        try:
            if tag_value is not None:
                self.driver.find_element_by_class_name(tag_value).click()
                return True
            else:
                logger.error("Insufficient Data")
                return False
        except Exception as e:
            logger.exception(f"Exception as {e}")
            return False

    def click_by_id(self, tag_value=None):
        try:
            if tag_value is not None:
                self.driver.find_element_by_id(tag_value).click()
                return True
            else:
                logger.error("Insufficient Data")
                return False
        except Exception as e:
            logger.exception(f"Exception as {e}")
            return

    def find_text_by_xpath(self, static_tag=None):
        try:
            data = tuple()
            if static_tag is not None:
                value = self.driver.find_element_by_xpath(static_tag).text.split(":")
                data = (value[0], value[1])
                return True, data
            else:
                logger.error("Insufficient Data")
                return False, data
        except Exception as e:
            logger.exception(f"Exception as {e}")
            return False

    def search_element_by_css(self, search_key):
        try:
            elements = self.driver.find_elements_by_css_selector(search_key)
            return True, elements
        except Exception as e:
            logger.exception(f'{search_key} doesn\'t exist - {e}')
            return False

    def search_element_by_name_or_id(self, main_tag='name', tag_value=None):
        status = False
        value = ''
        try:
            if main_tag == 'name':
                if tag_value is not None:
                    value = self.driver.find_element_by_name(tag_value).get_attribute('value')
                    status = True
                else:
                    logger.error("Unable to search")
                return status, value
            elif main_tag == 'id':
                if tag_value is not None:
                    value = self.driver.find_element_by_id(tag_value)
                    status = True
                else:
                    logger.error("Unable to search")
                return status, value
            else:
                options = ['M', 'F', 'O']
                for option in options:
                    if self.driver.find_element_by_xpath(f".//input[@type='radio' and @value='{option}']").is_selected():
                        value = option
                        break
                status = True
                return status, value
        except Exception as e:
            logger.exception(f"Exception while fetching values {e}")

# ob = SeleniumFactory()
# ob.connect()
# ob.disconnect()
