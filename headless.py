from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)

    service = Service('C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(2)

    driver.get('https://ekrs.ms.gov.pl/krsrdf/krs/wyszukiwaniepodmiotu?')

    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    print(soup.prettify())