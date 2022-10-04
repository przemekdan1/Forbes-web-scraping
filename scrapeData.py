import time

import pandas as pd

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    companyInformations = pd.DataFrame(columns=["Firma", "Na giełdzie od", "Liczba wyemitowanych akcji",
                                                 "Wartość rynkowa (mln zł)",
                                                 "Nazwa na GPW", "Skrót: 11B", "Nazwa pełna", "Adres siedziby",
                                                 "Województwo",
                                                 "Prezes Zarządu", "Numer telefonu", "Numer faksu",
                                                 "Strona www", "E-mail",
                                                 "Przynależność do indeksu", "Kurs ostatni", "Zmiana",
                                                 "Oferta kupna",
                                                 "Oferta sprzedaży", "Min. cena akcji", "Max. cena akcji",
                                                 "Wol. obrotu (szt.)",
                                                 "Wart. obrotu", "Data debiutu i kurs debiutu",
                                                 "Max historyczny (52 tyg.)",
                                                 "Min historyczny (52 tyg.)", "ISIN", "Rynek/Segment", "Sektor",
                                                 "Liczba wyemitowanych akcji", "Wartość rynkowa",
                                                 "Wartość księgowa", "C/WK", "C/Z",
                                                 "Stopa dywidendy (%)", "Akcjonariusze", "Dodatek"])
    companiesData = pd.read_csv('dane.csv')


    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)
    # options.add_argument ("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
    service = Service('C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0.5)

    driver.get("https://www.gpw.pl/spolka?isin=PLAB00000019#")

    # searchFied = driver.find_element(By.NAME,'searchText')
    # searchFied.send_keys('AB SPÓŁKA AKCYJNA')
    # searchFied.send_keys(Keys.RETURN)
    company = 'AB SPÓŁKA AKCYJNA'
    # time.sleep(10)
    # company = driver.find_element(By.CLASS_NAME,'name')
    # company.click()

    allData = []
    allData.append(company)
    for i in range(1,7):
        if i == 4 or i == 5:
            continue
        quotes = driver.find_element(By.XPATH,f'//*[@id="stateTabs"]/li[{i}]/a')
        quotes.click()
        # time.sleep(5)

        driver.get(driver.current_url)

        soup = BeautifulSoup(driver.page_source,'lxml')
        table = soup.find('table','footable table')
        if i == 6:
            tds = table.find_all('td',class_='left')
            shareholderList = ''
            for shareholder in tds:
                shareholderList += shareholder.text
                shareholderList += ', '
            allData.append(shareholderList)
        else:
            tds = table.find_all('td')

            for element in tds:
                if element != '\n':
                    element = element.text.replace('\t','').replace('\n','').replace(u'\xa0', u'').replace('    ','').strip()
                    allData.append(element)
    allData = [allData]

    companyInformations = pd.DataFrame(allData,columns=["Firma", "Na giełdzie od", "Liczba wyemitowanych akcji", "Wartość rynkowa (mln zł)",
                                                 "Nazwa na GPW", "Skrót: 11B", "Nazwa pełna", "Adres siedziby", "Województwo",
                                                 "Prezes Zarządu", "Numer telefonu", "Numer faksu", "Strona www", "E-mail",
                                                 "Przynależność do indeksu", "Kurs ostatni", "Zmiana", "Oferta kupna",
                                                 "Oferta sprzedaży", "Min. cena akcji", "Max. cena akcji", "Wol. obrotu (szt.)",
                                                 "Wart. obrotu", "Data debiutu i kurs debiutu", "Archiwalne (wg. cen zamknięcia sesji)","Max historyczny (52 tyg.)",
                                                 "Min historyczny (52 tyg.)", "ISIN", "Rynek/Segment", "Sektor",
                                                 "Liczba wyemitowanych akcji", "Wartość rynkowa", "Wartość księgowa", "C/WK", "C/Z",
                                                 "Stopa dywidendy (%)", "Akcjonariusze"],index=["Firma"])
    # companyInformations.reset_index(inplace=True, drop=True)
    # companiesData = pd.concat([companiesData, companyInformations], axis=0)
    companyInformations.to_csv('dane.csv', encoding='utf-8-sig', mode='w', index=False)
    # print(companiesData)





