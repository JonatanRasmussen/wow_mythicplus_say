import os

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

class Utils:

    @staticmethod
    def create_selenium_webdriver() -> webdriver.Chrome:
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument('--disable-logging')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    @staticmethod
    def quit_selenium_webdriver(driver: webdriver.Chrome) -> None:
        driver.quit()

    @staticmethod
    def scrape_url_with_selenium(url: str, timeout_in_sec: int, driver: webdriver.Chrome) -> str:
        driver.get(url)

        # Ensure the page loads within the specified timeout
        try:
            WebDriverWait(driver, timeout_in_sec).until(
                EC.presence_of_element_located((By.TAG_NAME, 'html'))
            )
        except TimeoutException:
            print(f"Timeout after {timeout_in_sec} seconds waiting for page to load.")
            return ""

        # Get the inner HTML of the <html> element
        html_element = driver.find_element(By.TAG_NAME, 'html')
        html_content = html_element.get_attribute('innerHTML')

        # Ensure html_content is not None
        if not html_content:
            print("BudoError: get_attribute('innerHTML') returned None")
            return ""

        return html_content

    @staticmethod
    def locate_html_with_bs4(html: str, id_to_locate: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        element_to_locate = soup.find(id=id_to_locate)

        if not element_to_locate:
            print(f"BudoError: Could not locate element with id '{id_to_locate}'.")
            return ""
        return str(element_to_locate)

    @staticmethod
    def remove_irrelevant_html_content(html: str, start: str, end: str) -> str:
        start_index = html.find(start)
        end_index = html.find(end, start_index)
        if start_index == -1 or end_index == -1:
            return ""  # Return empty string if start or end string is not found
        return html[start_index:end_index + len(end)]

    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"BudoWarning: The file {file_path} does not exist.")
            return ""
        except Exception as e:
            print(f"BudoError: An error occurred while reading the file {file_path}. Error: {e}")
            return ""

    @staticmethod
    def write_file(content: str, file_path: str) -> None:
        Utils.ensure_dir_exists(file_path)
        with open(file_path, 'w', encoding='utf-8') as file:
            if content:
                file.write(content)
            else:
                print(f"BudoError: len(content) is 0 for {file_path}")

    @staticmethod
    def write_pandas_df(df: pd.DataFrame, file_path: str) -> None:
        Utils.ensure_dir_exists(file_path)
        try:
            df.to_csv(file_path, index=False)
            print(f"DataFrame successfully written to {file_path}")
        except Exception as e:
            print(f"BudoError: An error occurred while writing the DataFrame to {file_path}. Error: {e}")

    @staticmethod
    def ensure_dir_exists(file_path: str) -> None:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)