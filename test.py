import pandas as pd
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':

    companyNumbersDataFrame = pd.read_csv('powrot.csv')

    companyData = pd.read_csv('forbesFixed.csv', sep=';')
    companyNames = companyData["Firma"].tolist()

    occurNumber = 22
    del companyNames[0:occurNumber-1]


    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)

    service = Service('C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0.5)

    counter = 1
    numberOfCompanies = len(companyNames)
    allCompanyData = []
    for company in companyNames:

        counter += 1

        text = f'https://google.com/search?q=jaki krs krs-online.com {company}'
        driver.get(text)

        if counter == 0:
            buttonClick = driver.find_element(By.ID, 'W0wltc')
            buttonClick.click()

        soup = BeautifulSoup(driver.page_source, 'lxml')
        search = soup.find('h3', class_="LC20lb MBeuO DKV0Md").text
        print(search)
        if 'KRS' in search:
            search = soup.find('h3', class_="LC20lb MBeuO DKV0Md").findNext('h3', class_="LC20lb MBeuO DKV0Md").text
        searchResult = search.split('krs: ')
        try:
            krs = searchResult[1]
            compKRS = krs[:10]

            currentCompany = [[company, compKRS]]
            dfCompany = pd.DataFrame(currentCompany, columns=["Firma", "KRS"])
            dfCompany.set_index(['Firma'])

        except IndexError:
            buttonClick = driver.find_element(By.ID, 'W0wltc')
            buttonClick.click()

            goToSite = driver.find_element(By.TAG_NAME, 'h3')
            goToSite.click()

            siteHtml = driver.page_source
            soup = BeautifulSoup(siteHtml, 'lxml')
            tables = soup.find_all('table')

            if tables:
                compBasicInformations = tables[0]
                compBasicInformationsContent = []
                for element in compBasicInformations.find_all('td'):
                    element = element.text
                    compBasicInformationsContent.append(element)

                compKRS = compBasicInformationsContent[5]

                currentCompany = [[company, compKRS]]
                dfCompany = pd.DataFrame(currentCompany, columns=["Firma", "KRS"])


        companyNumbersDataFrame = pd.concat([companyNumbersDataFrame, dfCompany], ignore_index=True, axis=0)

        print(companyNumbersDataFrame)
        print('\t', counter, company)

        companyNumbersDataFrame.to_csv('powrot.csv', encoding='utf-8-sig', mode='w', index=False)




