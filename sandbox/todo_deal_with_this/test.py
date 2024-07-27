import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--log-level=3")
options.add_argument('--disable-logging')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# Access the URL
url = "https://www.warcraftlogs.com/reports/g8QK7Nk2vGx1B9jb#fight=last&type=casts&hostility=1"
driver.get(url)

# Wait for the page to load
time.sleep(10)  # Adjust the sleep time if necessary, or use WebDriverWait for better practice

# Get the inner HTML of the <html> element
html_element = driver.find_element(By.TAG_NAME, 'html')
html_content = html_element.get_attribute('innerHTML')

# Save the HTML content to a file
with open('output.txt', 'w', encoding='utf-8') as file:
    if html_content:
        file.write(html_content)
    else:
        print("BudoError: html_content is null")

# Clean up and close the WebDriver
driver.quit()
