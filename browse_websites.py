from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import sys
import random

# Path to GeckoDriver (replace with your actual path)
GECKO_DRIVER_PATH = "/usr/local/bin/geckodriver"
FIREFOX_BINARY_PATH = "/usr/bin/firefox"

options = Options()
options.binary_location = FIREFOX_BINARY_PATH
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Mimic real user

# Use existing Firefox profile
profile_path = "/home/dloiacono/snap/firefox/common/.mozilla/firefox/yijwrx6z.SeleniumProfile"
options.add_argument(f"--profile={profile_path}")

options.set_preference("marionette.enabled", False)

if len(sys.argv) != 2:
    print("Usage: python3 browse_websites.py <website_url>")
    sys.exit(1)

site = sys.argv[1]  # Get website URL from command-line argument

# Setup Firefox WebDriver
service = Service(GECKO_DRIVER_PATH)
driver = webdriver.Firefox(service=service, options=options)

print(f"Opening {site}...")
driver.get(site)  # Open website

# Simulate mouse movement
actions = ActionChains(driver)
for _ in range(random.randint(5, 10)):  # Move the mouse randomly 5-10 times
    x_offset = random.randint(10, 500)
    y_offset = random.randint(10, 300)
    actions.move_by_offset(x_offset, y_offset).perform()
    time.sleep(random.uniform(0.5, 1.5))  # Small delay between movements

# Simulate scrolling
for _ in range(random.randint(3, 7)):  # Scroll down randomly 3-7 times
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(random.uniform(2, 5))  # Pause randomly between scrolls

time.sleep(40)  # Keep open for 40 seconds

driver.quit()  # Close browser
print(f"Finished {site}.")
