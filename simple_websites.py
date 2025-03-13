import webbrowser
import time
import sys
import pyautogui

if len(sys.argv) != 2:
    print("Usage: python3 browse_websites.py <website_url>")
    sys.exit(1)

site = sys.argv[1]  # Get website URL from command-line argument

print(f"Opening {site} in Firefox...")

# Specify Firefox as the browser to use
firefox = webbrowser.get('firefox')
firefox.open(site)  # Open the website in Firefox

# Keep the script running for 40 seconds
time.sleep(40)

# Close the Firefox tab (Ctrl + W)
pyautogui.hotkey('ctrl', 'w')

print(f"Finished {site}.")
