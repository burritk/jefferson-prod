import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def get_headless_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    current_path = os.path.dirname(__file__)
    filename = os.path.join(current_path, 'chromedriver')
    driver = webdriver.Chrome(filename, chrome_options=chrome_options)
    return driver

def get_selenium_xpath_if_exists(driver, xpath):
    if len(driver.find_elements_by_xpath(xpath)) < 1:
        return ''
    text = driver.find_element_by_xpath(xpath) if 'text' in xpath else driver.find_element_by_xpath(xpath).text
    return text.strip() if text else ''
