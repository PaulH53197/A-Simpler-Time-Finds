import traceback
import selenium.webdriver as webdriver
import time
import base64
import logging
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def getChrome():
    options = webdriver.ChromeOptions()
    # options.headless = True

    # options.add_argument('--headless=new')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1960,1080')

    # chrome = webdriver.Chrome(executable_path=r'D:\\chromedriver\\chromedriver.exe', options=options)
    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return chrome