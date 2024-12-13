import time
import csv
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

# Function to scrape player stats from an individual page
def scrape_player_stats(player_url):
    driver.get(player_url)
    
    try:
        # Wait for the statistics section to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'statistics')))

        # Extract player name
        player_name = driver.find_element(By.CSS_SELECTOR, 'h1.player-nick').text

        # Extract statistics from both columns on the page
        stats = {}

        # First column of stats
        stats['Total kills'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Total kills']/span[2]").text
        stats['Headshot %'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Headshot %']/span[2]").text
        stats['Total deaths'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Total deaths']/span[2]").text
        stats['K/D Ratio'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='K/D Ratio']/span[2]").text
        stats['Damage / Round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Damage / Round']/span[2]").text
        stats['Grenade dmg / Round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Grenade dmg / Round']/span[2]").text
        stats['Maps played'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Maps played']/span[2]").text

        # Second column of stats
        stats['Rounds played'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Rounds played']/span[2]").text
        stats['Kills / round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Kills / round']/span[2]").text
        stats['Assists / round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Assists / round']/span[2]").text
        stats['Deaths / round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Deaths / round']/span[2]").text
        stats['Saved by teammate / round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Saved by teammate / round']/span[2]").text
        stats['Saved teammates / round'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Saved teammates / round']/span[2]").text
        stats['Rating 2.0'] = driver.find_element(By.XPATH, "//div[@class='stats-row'][span='Rating 2.0']/span[2]").text
        
        # Add player name to the stats
        stats['Player Name'] = player_name
        
        return stats

    except Exception as e:
        print(f"Error scraping data from {player_url}: {e}")
        return None

# Function to read player URLs from the text file
def read_urls_from_file(filename="player_urls.txt"):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to write player stats to a CSV file
def write_stats_to_csv(player_stats_list, filename="player_stats.csv"):
    # Specify the CSV headers
    headers = [
        'Player Name', 'Total kills', 'Headshot %', 'Total deaths', 'K/D Ratio', 
        'Damage / Round', 'Grenade dmg / Round', 'Maps played', 
        'Rounds played', 'Kills / round', 'Assists / round', 'Deaths / round',
        'Saved by teammate / round', 'Saved teammates / round', 'Rating 2.0'
    ]
    
    # Open CSV file and write data
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:  # Use 'a' mode to append
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        for player_stats in player_stats_list:
            writer.writerow(player_stats)

# Main script to scrape all players from the URLs and save to CSV sequentially
if __name__ == "__main__":
    player_urls = read_urls_from_file()

    # Open an initial tab
    driver.get('about:blank')

    all_player_stats = []
    
    for i, url in enumerate(player_urls):
        if i > 0:
            # Open a new tab for the next URL
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
        
        player_stats = scrape_player_stats(url)
        if player_stats:
            write_stats_to_csv([player_stats])  # Write each player's stats to CSV right after scraping
            print(f"Successfully scraped data for {player_stats['Player Name']}")
        
        # Close the previous tab (except the first)
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # Close the browser after scraping
    driver.quit()

    print("All player stats saved to 'player_stats.csv'.")
