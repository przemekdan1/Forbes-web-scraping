import time

import pandas as pd

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)
    options.add_argument ("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    service = Service('C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0.5)

    driver.get("https://newconnect.pl/spolki")

    counter = 1
    companyNames = []
    while True:
        counter += 1
        print('\n','-'*10,' #',counter,'-'*10)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        currentNames = soup.find_all('strong', class_='name')

        try:
            showMoreButton = driver.find_element(By.CLASS_NAME,'more')
            showMoreButton.click()
        except:
            for name in soup.find_all('strong', class_='name'):
                name = name.text
                name = name.strip()
                name = name.replace('\n', '')
                print(name)
            break

        for name in soup.find_all('strong', class_='name'):
            name = name.text
            name = name.strip()
            name = name.replace('\n', '')
            print(name)
        time.sleep(5)



        # currentNamesAfterClick = soup.find_all('strong',class_='name')
        # print("Po",len(currentNamesAfterClick))
        #
        # print('\n',currentNamesBeforeClick,currentNamesAfterClick)

        # currentNames = list(set(currentNamesBeforeClick) & set(currentNamesAfterClick))
        # print("Roznica",len(currentNames))


        time.sleep(1)
