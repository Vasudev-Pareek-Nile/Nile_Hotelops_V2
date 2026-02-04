from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Update if necessary

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the MakeMyTrip hotel review page
url = "https://www.makemytrip.com/hotels/citadel_sarovar_portico_bengaluru-details-bangalore.html"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll down to load more reviews if necessary
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Find all review elements
reviews = driver.find_elements(By.CSS_SELECTOR, ".reviewBox")  # Update the selector as necessary

# Loop through the reviews and print the text
if reviews:
    print(f"Found {len(reviews)} reviews.")
    for review in reviews:
        print(review.text)
        print('-' * 80)  # Separator between reviews
else:
    print("No reviews found.")

# Close the browser
driver.quit()
