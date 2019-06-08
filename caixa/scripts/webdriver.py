#
# Webdriver class
#
import click
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

# Selenium webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Webdriver:

    def __init__(self, cache=False, headless=False, prefs=False, type_=False):
        click.echo("Loading Webdriver...")
        self.chrome_options = webdriver.ChromeOptions()
        if headless:
            self.chrome_options.add_argument("--headless")
        if cache:
            self.chrome_options.add_argument("user-data-dir=/home/acioli/cache")
        if prefs:
            self.prefs={
                "profile.managed_default_content_settings.images": 2,
                "profile.managed_default_content_settings.stylesheet": 2,
                'disk-cache-size': 5000
                }
            self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        #self.driver.minimize_window()

    def get(self, url, element_wait=False, element_type=False):
        click.echo("Loading url: %s" % url)
        click.echo("Element definition: <%s | %s>" % (element_type, element_wait))
        self.driver.get(url)
        if element_wait and element_type:
            if element_type == "class":
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, element_wait)))
            elif element_type == "id":
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.ID, element_wait)))
        else:
            self.driver.close()
            return False
        bs4_page = BeautifulSoup(self.driver.page_source, "html.parser")
        self.driver.close()
        return bs4_page

    def close(self):
        self.driver.close()
