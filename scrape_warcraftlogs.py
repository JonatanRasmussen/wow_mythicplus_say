import os
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
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
            print("Error: get_attribute('innerHTML') returned None")
            return ""

        return html_content

    @staticmethod
    def locate_html_with_bs4(html: str, id_to_locate: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        table_element = soup.find(id=id_to_locate)

        if not table_element:
            print(f"Error: Could not locate element with id '{id_to_locate}'.")
            return ""
        return str(table_element)

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
            print(f"Error: The file {file_path} does not exist.")
            return ""
        except Exception as e:
            print(f"Error: An error occurred while reading the file {file_path}. Error: {e}")
            return ""

    @staticmethod
    def write_file(content: str, file_path: str, file_name: str) -> None:
        file_path_and_name = os.path.join(file_path, file_name)
        with open(file_path_and_name, 'w', encoding='utf-8') as file:
            if content:
                file.write(content)
            else:
                print(f"Error: Content to write to {file_path_and_name} is empty.")

    @staticmethod
    def write_pandas_df(df: pd.DataFrame, file_path: str, file_name: str) -> None:
        try:
            file_path_and_name = os.path.join(file_path, file_name)
            df.to_csv(file_path_and_name, index=False)
            print(f"DataFrame successfully written to {file_path_and_name}")
        except Exception as e:
            print(f"Error: An error occurred while writing the DataFrame to {file_path_and_name}. Error: {e}")

    @staticmethod
    def html_table_to_pandas_df(html_table: str) -> pd.DataFrame:
        # Parse the HTML content
        soup = BeautifulSoup(html_table, 'lxml')

        # Find the table
        table = soup.find('table', id='reports-table')

        if not table:
            print("Error: Could not locate table with id 'reports-table'.")
            return pd.DataFrame()
        if isinstance(table, NavigableString):
            print("Error: Table cannot .find_all() due to being a NavigableString")
            return pd.DataFrame()

        # Extract headers
        headers = []
        for th in table.find_all('th'):
            headers.append(th.get_text(strip=True))

        # Extract rows
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip the header row
            cells = tr.find_all('td')
            row = [cell.get_text(strip=True) for cell in cells]
            rows.append(row)

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=headers)
        return df

# Example usage
if __name__ == "__main__":
    utils = Utils()
    my_driver = utils.create_selenium_webdriver()
    try:
        my_url = "https://www.warcraftlogs.com/zone/reports?zone=39&boss=61822&page=2"
        my_html = utils.scrape_url_with_selenium(my_url, 10, my_driver)
        if my_html:
            my_table_html = utils.locate_html_with_bs4(my_html, "reports-table")
            utils.write_file(my_table_html, ".", "table.html")
            # Read the HTML file
            my_html_content = utils.read_file('table.html')
            if my_html_content:
                my_df = utils.html_table_to_pandas_df(my_html_content)
                utils.write_pandas_df(my_df, ".", "table.csv")
                print(my_df.head())
    finally:
        utils.quit_selenium_webdriver(my_driver)
