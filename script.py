import os
import time
import base64
import requests
import argparse
import random
from unidecode import unidecode #pip install unidecode
from dotenv import load_dotenv #pip install python-dotenv
from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By

load_dotenv() # Load environment variables from .env file

# Get LIMIT value from cmd
parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=1000, help='Number of images to download per keyword')
args = parser.parse_args()
LIMIT = args.limit

# Constants
IMG_EXTS = ['jpg', 'jpeg', 'png']
FOLDER_PATH = os.getenv('FOLDER_PATH')

# Create folder if it doesn't exist
if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)

def check_url_extension(url):
    for ext in IMG_EXTS:
        if ext in url:
            return ext
    return None

def download_image(url, img_name, folder_path):
    if url.startswith('data:image'):
        # If it's a base64 data URI
        img_data = url.split(',')[1]
        img_data = base64.b64decode(img_data)
        with open(os.path.join(folder_path, img_name), 'wb') as f:
            f.write(img_data)
    else:
        # If it's a regular URL
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, img_name), 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download image: {img_name}")

def get_driver():
    opts = webdriver.ChromeOptions() 
    opts.add_argument('--headless') # Run Chrome in headless mode
    driver = webdriver.Chrome(options=opts) # Open Chrome
    return driver

print("Starting script...")

driver = get_driver()



# Read keywords from keywords.txt file
with open('keywords.txt', 'r', encoding='utf8') as f:
    keywords = f.readlines()
    keywords = [x.strip() for x in keywords]
    keywords = [unidecode(x).lower() for x in keywords]

print(keywords)
download_queue = [] # List of tuples (url, img_name)

print("Loading....")
for keyword in keywords:

    img_tags = set() # Using a set to avoid duplicate tags
    urls_batch = set() # Using a set to avoid duplicate URLs

    url = f"https://www.google.com/search?tbm=isch&q={keyword}"

    driver.get(url) # Open URL

    time.sleep(2) # Wait for page to load
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) # Wait for more images to load

    img_tags.update(driver.find_elements(By.CSS_SELECTOR, '[class="YQ4gaf"]:not([class~=" "])')) # Get all img tags which have only "YQ4gaf" class
    print(len(img_tags))
    for idx, tag in enumerate(img_tags):
        img_url = tag.get_attribute('src') # Get image URL in "src" attribute
        if img_url:
            # ext = check_url_extension(img_url)
            # if ext:
            img_name = f"{keyword}_{idx}_{random.randint(1, 1000)}.jpg"
            # img_name = f"{keyword}_{len(urls_batch)}.jpg"
            urls_batch.add((img_url, img_name))

    if len(urls_batch) > LIMIT:
        urls_batch = list(urls_batch)[:LIMIT] # Convert to list and limit to LIMIT
    download_queue.extend(urls_batch)

print("Downloading images...")
for idx, (url, img_name) in enumerate(download_queue):
    download_image(url, img_name, FOLDER_PATH)
    print(f"Downloaded {idx+1}/{len(download_queue)} images.")

driver.quit() # Close Chrome

print("Script finished!")
print(len(os.listdir(FOLDER_PATH)), "images downloaded.") # The number of images downloaded should now match the LIMIT value as expected.
