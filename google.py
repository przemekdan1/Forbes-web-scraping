from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


if __name__ == '__main__':

    # data = ["DREWPAL WIESŁAW MAJTAS KRZYSZTOF DRYGAŁA GRZEGORZ DRYGAŁA SPÓŁKA JAWNA","ABILE SP Z O O"]
    companyNumbersDataFrame = pd.read_csv('dane.csv')

    companyData = pd.read_csv(r"C:\Users\jange\PycharmProjects\Staz\Forbes\forbesFixed.csv", sep=';')
    companyNames = companyData["Firma"].tolist()

    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36'
    opts = Options()
    opts.add_argument(f"user-agent={user_agent}")
    # opts.headless = True
    service = Service('C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(options=opts,service=service)

    startFromPosition = 245
    del companyNames[0:startFromPosition - 1]

    compPos = startFromPosition
    for company in companyNames:
        compPos += 1
        if compPos%20 == 0:
            time.sleep(10)
        elif compPos%33 == 0:
            time.sleep(15)
        elif compPos%17 == 0:
            time.sleep(3)


        search = company + 'site:krs-online.com.pl'
        results = 1
        driver.get("https://www.google.com/search?q={}&num={}".format(search, results))
        if compPos == startFromPosition+1:
            buttonClick = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/form[1]/input[10]')
            buttonClick.click()
        if compPos == startFromPosition+1:
            time.sleep(15)
        soup = BeautifulSoup(driver.page_source, "lxml")
        metaDescription = soup.find('div',class_='BNeawe s3v9rd AP7Wnd').text

        if 'KRS ' in metaDescription:
            searchResult = metaDescription.split('KRS ')
            krs = searchResult[1]
            compKRS = krs[:10]
            print(compPos,company,compKRS)
        else:
            compKRS = ''

        if len(compKRS) == 10:
            currentCompany = [[company, str(compKRS)]]
            dfCompany = pd.DataFrame(currentCompany, columns=["Firma", "KRS"])
            dfCompany.set_index(['Firma'])

            companyNumbersDataFrame = pd.concat([companyNumbersDataFrame, dfCompany], ignore_index=True, axis=0)
            companyNumbersDataFrame.to_csv('dane.csv', encoding='utf-8-sig', mode='w', index=False)
        time.sleep(1)
        # driver.quit()
