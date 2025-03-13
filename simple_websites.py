import webbrowser
import time
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python3 browse_websites.py <website_url>")
    sys.exit(1)

site = sys.argv[1]  # Get website URL from command-line argument

print(f"Opening {site} in the default web browser...")

# Open the website in the system's default web browser
browser = webbrowser.get()  
browser.open(site)

# Keep the script running for 40 seconds
time.sleep(40)

# Attempt to close the browser (may depend on OS and browser behavior)
os.system("pkill -f 'chrome|firefox|brave|edge'")  # Kill common browsers on Linux/macOS
os.system("taskkill /IM chrome.exe /F")  # Kill Chrome on Windows
os.system("taskkill /IM msedge.exe /F")  # Kill Edge on Windows
os.system("taskkill /IM firefox.exe /F")  # Kill Firefox on Windows

print(f"Finished {site}.")
