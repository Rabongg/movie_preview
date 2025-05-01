from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
from common.constant import WEB_DRIVER_WAIT_TIME

class WebDriverManager:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_dir = os.getenv('CHROME_DIR', '')
        chrome_options.binary_location = chrome_dir
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def start_driver(self, url) -> None:
        self.driver.get(url)

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

    def get_element_by_class_name(self, class_name):
        try:
            element = WebDriverWait(self.driver, WEB_DRIVER_WAIT_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            return element
        except Exception as e:
            logging.exception(f"Error occurred: {e}")
            return None