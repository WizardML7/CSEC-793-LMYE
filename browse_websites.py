from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time
import sys

# Path to GeckoDriver (replace with your actual path)
GECKO_DRIVER_PATH = "/usr/local/bin/geckodriver"

if len(sys.argv) != 2:
    print("Usage: python3 browse_websites.py <website_url>")
    sys.exit(1)

site = sys.argv[1]  # Get website URL from command-line argument

# Setup Firefox WebDriver
service = Service(GECKO_DRIVER_PATH)
options = webdriver.FirefoxOptions()
#options.add_argument("--headless")  # Run without opening a visible browser window

print(f"Opening {site}...")

driver = webdriver.Firefox(service=service, options=options)
driver.get(site)  # Open website

time.sleep(40)  # Keep open for 40 seconds
driver.quit()  # Close browser

print(f"Finished {site}.")
