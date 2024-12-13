import json
import time
import pyperclip  # To handle clipboard operations
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# Set the correct path to your geckodriver and Firefox binary
gecko_path = "./drivers/geckodriver.exe"
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Adjust to your actual path

# Setup Firefox options and driver
options = Options()
options.binary_location = firefox_binary_path
service = Service(gecko_path)
driver = webdriver.Firefox(service=service, options=options)

# API URLs
cs2_url = 'https://api.prizepicks.com/projections?league_id=265'  # CS2 API URL
lol_url = 'https://api.prizepicks.com/projections?league_id=121'  # LoL API URL

# Function to fetch JSON data using the Copy button
def fetch_api_data(url, filename):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    try:
        # Locate the Copy button (adjust the selector based on the actual HTML structure)
        copy_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Copy')]")  # Adjust as necessary
        copy_button.click()  # Click the button to copy data to clipboard
        
        time.sleep(1)  # Wait a moment for the data to be copied

        # Retrieve the copied data from the clipboard
        raw_json = pyperclip.paste()

        # Clear the content of the file before saving new data
        with open(filename, 'w', encoding='utf-8') as json_file:
            json_file.seek(0)  # Move to the start of the file
            json_file.truncate()  # Clear the file content
            print("Data Cleared")
            json_file.write(raw_json)  # Write the new JSON data
        print(f"[🟢] Successfully pulled and saved raw JSON data to {filename}\n")

    except Exception as e:
        print(f"[🔴] Error fetching data from {url}: {e}")

# Fetch and save CS2 data
fetch_api_data(cs2_url, 'json/cs2_data.json')

# Fetch and save LoL data
fetch_api_data(lol_url, 'json/lol_data.json')

# Close the driver
driver.quit()
