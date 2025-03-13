from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import sys

# Path to GeckoDriver (replace with your actual path)
GECKO_DRIVER_PATH = "/usr/local/bin/geckodriver"

FIREFOX_BINARY_PATH = "/usr/bin/firefox"

options = Options()
options.binary_location = FIREFOX_BINARY_PATH

if len(sys.argv) != 2:
    print("Usage: python3 browse_websites.py <website_url>")
    sys.exit(1)

site = sys.argv[1]  # Get website URL from command-line argument

# Setup Firefox WebDriver
service = Service(GECKO_DRIVER_PATH)


print(f"Opening {site}...")

driver = webdriver.Firefox(service=service, options=options)
driver.get(site)  # Open website

time.sleep(40)  # Keep open for 40 seconds
driver.quit()  # Close browser

print(f"Finished {site}.")
