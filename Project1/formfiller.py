import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class FormFiller:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def type_like_human(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Random typing speed

    def fill_form_page1(self, data, mapper,mapper2, url):
        try:
            self.driver.get(url)
            self.logger.info("Navigating to URL...")
            time.sleep(random.uniform(1, 3))
            for field, value in data.items():
                if field in mapper:
                    element_locator = mapper[field]
                    locator_type = mapper2[field]
                    match locator_type:
                        case "input_field":
                            input_field = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, element_locator))
                            )
                            self.type_like_human(input_field, value)
                            self.logger.info(f"Type: {field}")
                            self.logger.info(f"Value : {value}")
                        case "dropdown":
                            dropdown = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, element_locator))
                            )
                            dropdown.click() 
                            option_xpath = f'{element_locator}/option[text()="{value.capitalize()}"]'
                            option_element = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, option_xpath))
                            )
                            option_element.click()
                            self.logger.info(f"Type: {field}")
                            self.logger.info(f"Value : {value}")
                        case "button_element":
                            button_element = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, element_locator))
                            )
                            button_element.click()
                            self.logger.info(f"Type: {field}")
                            self.logger.info(f"Value : {value}")

            time.sleep(random.uniform(2, 5))  # Random delay before quitting
            self.logger.info("Form filling completed successfully.")

        except Exception as e:
            self.logger.error(f"Error occurred during form filling: {e}")

        finally:
            self.driver.quit()
            self.logger.info("Browser session closed.")