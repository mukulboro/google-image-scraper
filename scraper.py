from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
import requests
import base64
from PIL import Image
from io import BytesIO
import os

MAX_SCROLLS = 5 # Magic Number to guarantee you reach the end of the page
DOWNLOAD_DIR_NAME = "images"

class Scraper:
    def __init__(self, term, screenshot = False):
        self.term = term
        self.URL = "https://www.google.com/imghp?hl=en"
        self.opt = webdriver.ChromeOptions()
        ch 
        self.opt.add_argument("--no-sandbox")
        # self.opt.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.opt)
        self.start = time.time()
        self.ss = screenshot
        try:
            print("Creating images directory...")
            os.mkdir(DOWNLOAD_DIR_NAME)
        except FileExistsError:
            print("Download directory already exists")

    def save_http_image(self, image_source, image_index):
        response = requests.get(image_source)
        print("     Downloading HTTP image...")
        if response.status_code == 200:
            with open(f"image{image_index}.jpg", "wb") as file:
                file.write(response.content)
                print("     Image downloaded successfully")
        else:
            print("     Failed to download image")

    def save_base64_image(self, image_source, image_index):
        print("     Creating image from base64...")
        image_data = base64.b64decode(image_source.split(",")[1])
        image = Image.open(BytesIO(image_data))
        image.save(f"image{image_index}.jpg")
        print("     Image created successfully")

    def scrape(self):
        self.driver.get(self.URL)
        search_box = self.driver.find_element(By.ID, "APjFqb")
        search_box.send_keys(self.term)
        search_box.send_keys(Keys.RETURN)
        print(f"Searching for {self.term} images...")
        os.chdir(DOWNLOAD_DIR_NAME)
        time.sleep(5)
        scroll_count = 0
        while scroll_count < MAX_SCROLLS:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Scrolling... {scroll_count+1}/{MAX_SCROLLS}")
            scroll_count += 1
            time.sleep(2)

        print("Reached the end of the page")
        self.driver.execute_script("window.scrollTo(0, 0);")
        print("Scrolled to top of page")
        images = self.driver.find_elements(By.CLASS_NAME, "Q4LuWd")
        print(f"Found {len(images)} images")
        for image in images:
            time.sleep(1)
            image_index = images.index(image)
            try:
                image.click()
                print(f"Clicked image {image_index+1}/{len(images)}")
                time.sleep(1)
                image_element = self.driver.find_element(By.CLASS_NAME, "sFlh5c")
                image_source = image_element.get_attribute("src")
                if self.ss:
                    image.screenshot(f"image{image_index}.png")
                    print(f"Screenshot taken for image {image_index}")
                    continue
                try:
                    self.save_http_image(image_source, image_index)
                except:    
                    try:
                        self.save_base64_image(image_source, image_index)
                    except Exception as e:
                        print(f"    Failed to create image: {str(e)}")
                
            except ElementClickInterceptedException:
                print(f"ElementClickInterceptedException on image {image_index+1}/{len(images)}")
                continue
        self.driver.quit()
        print(f"Scraping completed in {time.time()-self.start} seconds")
