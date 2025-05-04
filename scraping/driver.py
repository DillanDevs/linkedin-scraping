from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .config import settings
import time

def init_driver(headless: bool = True):
    opts = Options()
    opts.headless = headless
    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
    return driver


def linkedin_login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(settings.SCRAPE_DELAY)
    driver.find_element("id", "username").send_keys(settings.LINKEDIN_USER)
    driver.find_element("id", "password").send_keys(settings.LINKEDIN_PASS)
    driver.find_element("xpath", "//button[@type='submit']").click()
    time.sleep(settings.SCRAPE_DELAY)