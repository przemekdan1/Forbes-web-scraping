import pandas as pd
import time
import winsound

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

if __name__ == '__main__':

    companyNumbersDataFrame = pd.read_csv('powrot.csv')

    companyData = pd.read_csv('forbesFixed.csv', sep=';')
    companyNames = companyData["Firma"].tolist()

    # companyNames = ["WABCO POLSKA SP Z O O","WORK SERVICE S A","SCA HYGIENE PRODUCTS SP Z O O","VIBRACOUSTIC POLSKA SP Z O O","HP GLOBAL BUSINESS CENTER SP Z O O"]
    startFromPosition = 59
    del companyNames[0:startFromPosition-1]


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
    # try:
    #     pass
    # except:
    #     winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    #     myElem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'LC20lb MBeuO DKV0Md')))


    for company in companyNames:

        counter += 1

        text = f'https://google.com/search?q={company} site:krs-online.com.pl'
        driver.get(text)

        if counter == 2:
            buttonClick = driver.find_element(By.ID, 'W0wltc')
            buttonClick.click()

        soup = BeautifulSoup(driver.page_source, 'lxml')
        search = soup.find('h3', class_="LC20lb MBeuO DKV0Md").text
        if '(krs:' in search:
            searchResult = search.split('krs: ')
            krs = searchResult[1]
            compKRS = krs[:10]

            if len(compKRS) == 10:
                # currentCompany = [[company, str(compKRS)]]
                # dfCompany = pd.DataFrame(currentCompany, columns=["Firma", "KRS"])
                # dfCompany.set_index(['Firma'])
                #
                # companyNumbersDataFrame = pd.concat([companyNumbersDataFrame, dfCompany], ignore_index=True, axis=0)
                # companyNumbersDataFrame.to_csv('powrot.csv', encoding='utf-8-sig', mode='w', index=False)

                print(counter, company, compKRS)
        #     else:
        #         with open('noInfoCompany.txt', 'a', encoding='utf-8') as file:
        #             company = str(company)
        #             file.write(company + '\n')
        # else:
        #     with open('noInfoCompany.txt', 'a', encoding='utf-8') as file:
        #         company = str(company)
        #         file.write(company + '\n')



        # time.sleep(0.5)
