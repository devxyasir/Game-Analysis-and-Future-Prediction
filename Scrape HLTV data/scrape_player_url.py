import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the correct path to your geckodriver and Firefox binary
gecko_path = "./drivers/geckodriver.exe"
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Adjust to your actual path

# Setup Firefox options and driver
options = Options()
options.binary_location = firefox_binary_path
service = Service(gecko_path)
driver = webdriver.Firefox(service=service, options=options)

BASE_URL = "https://www.hltv.org"

# Function to get player URLs from the main players page
def get_player_urls():
    url = "/stats/players"
    driver.get(url)

    try:
        # Wait until the player table is loaded (waiting for a specific element in the table)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td.playerCol a')))
        
        print("Page fully loaded, extracting player URLs...")

        player_urls = []
        
        # Find all player columns after the page is fully loaded
        player_columns = driver.find_elements(By.CSS_SELECTOR, 'td.playerCol a')
        
        for player_column in player_columns:
            player_url = BASE_URL + player_column.get_attribute('href')
            player_urls.append(player_url)

        return player_urls

    except Exception as e:
        print(f"Error while waiting for the page to load: {e}")
        return []

# Function to save the player URLs to a text file
def save_urls_to_file(player_urls, filename="player_urls.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        for url in player_urls:
            file.write(f"{url}\n")

# Main script execution
if __name__ == "__main__":
    # Get all player URLs from the main players page
    player_urls = get_player_urls()

    if player_urls:
        # Save the player URLs to a text file
        save_urls_to_file(player_urls)
        print("Player URLs saved to 'player_urls.txt'")
    else:
        print("No player URLs found.")

    # Close the browser after scraping
    driver.quit()
