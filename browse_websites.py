import undetected_geckodriver as ugd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import sys
import random

if len(sys.argv) != 2:
    print("Usage: python3 browse_websites.py <website_url>")
    sys.exit(1)

site = sys.argv[1]  # Get website URL from command-line argument

# Setup Undetected Firefox WebDriver
driver = ugd.Firefox()

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
