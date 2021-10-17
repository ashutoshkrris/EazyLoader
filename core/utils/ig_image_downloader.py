import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os

class IgImage:
    def __init__(self, path, link, chrome_driver_path, chrome_path):
        self.link = link
        self.chromedriver = chrome_driver_path
        self.chrome = chrome_path
        self.filepath = os.path.join(path, "ig_image.png")

    def save_image(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get(self.chrome)
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=chrome_options)
            driver.get(self.link)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            img = soup.find('img', class_='FFVAD')
            img_url = img['src']

            r = requests.get(img_url)

            with open(self.filepath, 'wb') as f:
                f.write(r.content)

            print(self.filepath)
            
            return "Image is downloaded"
        except:
            return "Try again Later"

    def delete_image(self):
        os.remove(self.filepath)
