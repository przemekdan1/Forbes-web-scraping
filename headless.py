import pandas as pd

from selenium import webdriver
from fake_useragent import UserAgent

import time
import os

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

if __name__ == '__main__':

    pd.set_option('display.max_columns', None)

    companyInformations = pd.DataFrame(columns=["Firma","Nazwa","Rejestr","Województwo","Numer KRS","Powiat","NIP","Gmina","REGON",
                                                "Miejscowość","Forma prawna","Adres","Data wpisu do Rejestru Przedsiębiorców","Kod pocztowy",
                                                "Data wpisu do Rejestru Stowarzyszeń","Adres WWW","Data wykreślenia z Rejestru Przedsiębiorców",
                                                "Email","Data wykreślenia z Rejestru Stowarzyszeń","Data uprawomocnienia wykreślenia z KRS",
                                                "Status OPP","Data przyznania statusu OPP","Data zawieszenia działalności",
                                                "Data wznowienia działalności","Wpisy dot. postępowania upadłościowego",
                                                "Nazwa organu wydającego akt prawny","Sygnatura aktu prawnego",
                                                "Data wydania aktu prawnego", "Określenie sposobu prowadzenia postępowania upadłościowego",
                                                "Data zakończenia postępowania upadłościowego",
                                                "Sposób zakończenia postępowania upadłościowego","Nazwa organu reprezentacji",
                                                "Sposób reprezentacji", "Członkowie reprezentacji"])

    members = pd.read_csv('czlonkowie.csv')


    # krsNumber = '0000057567'
    # company = 'ILHO PL S.A'
    companyData = pd.read_csv('forbesFixed.csv', sep=';')
    companyNames = companyData["Firma"].tolist()
    # companyNames = ["WABCO POLSKA SP Z O O","WORK SERVICE S A","SCA HYGIENE PRODUCTS SP Z O O","VIBRACOUSTIC POLSKA SP Z O O","HP GLOBAL BUSINESS CENTER SP Z O O"]


    startFromPosition = 128
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

        members = pd.read_csv('czlonkowie.csv')
        allCompaniesInfo = pd.read_csv('sprawdzam.csv')



        options = webdriver.ChromeOptions()
        # options.headless = True
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_experimental_option("detach", True)

        ua = UserAgent()
        user_agent = str(ua.chrome)
        options.add_argument(f'user-agent={user_agent}')

        service = Service('C:\Program Files (x86)\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(0.5)


        driver.get('https://ekrs.ms.gov.pl/krsrdf/krs/wyszukiwaniepodmiotu?')



        print('\n','='*10,company,'='*10)
        print("Postion:",compPos)
        time.sleep(0.6)
        entrepreneurRegisterButton = driver.find_element(By.ID,'rejestrPrzedsiebiorcy')
        if entrepreneurRegisterButton.is_selected():
            entrepreneurRegisterButton.click()
        entrepreneurRegisterButton.click()

        # print("guzik 1")
        # time.sleep(1)
        associationsRegisterButton = driver.find_element(By.ID, 'rejestrStowarzyszenia')
        if associationsRegisterButton.is_selected():
            associationsRegisterButton.click()
        associationsRegisterButton.click()

        # print("guzik 2")

        searchByCompName = driver.find_element(By.ID,'nazwa')
        searchByCompName.clear()
        searchByCompName.send_keys(company)

        confirmButton = driver.find_element(By.ID, 'szukaj')
        confirmButton.click()

        # time.sleep(1)

        howManyResults = len(driver.find_elements(By.XPATH,'//*[text()="Wyświetl"]'))
        # print(howManyResults)

        if howManyResults == 1:
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            OPPstatus = soup.find('td', class_='czyOppAsString').text
            bankruptcyProceedingStatus = soup.find('td', class_='czyWupadlosciAsString').text

            toCompanyData = driver.find_element(By.XPATH,'//*[text()="Wyświetl"]')
            toCompanyData.click()

            html = driver.page_source
            soup = BeautifulSoup(html,'lxml')

            allTr = soup.find_all('tr')
            bankruptcyInfo1 = allTr[15].text.replace("Nazwa organu wydającego akt prawny ", "")
            bankruptcyInfo2 = allTr[16].text.replace("Sygnatura aktu prawnego", "")
            bankruptcyInfo3 = allTr[17].text.replace("Data wydania aktu prawnego", "")
            bankruptcyInfo4 = allTr[18].text.replace("Określenie sposobu prowadzenia postępowania upadłościowego", "")
            bankruptcyInfo5 = allTr[19].text.replace("Data zakończenia postępowania upadłościowego", "")
            bankruptcyInfo6 = allTr[20].text.replace("Sposób zakończenia postępowania upadłościowego", "")

            allData = soup.find_all('td',class_='big')

            data = []
            data.append(company)
            counter = 0
            for element in allData:
                data.append(element.text)
                # print(counter, element.text)
                counter += 1

            data.append(OPPstatus)
            data.append(bankruptcyProceedingStatus)

            data.append(bankruptcyInfo1)
            data.append(bankruptcyInfo2)
            data.append(bankruptcyInfo3)
            data.append(bankruptcyInfo4)
            data.append(bankruptcyInfo5)
            data.append(bankruptcyInfo6)

            data = [data]

            companyInformations = pd.DataFrame(data, columns=["Firma", "Nazwa", "Rejestr", "Województwo", "Numer KRS", "Powiat", "NIP", "Gmina", "REGON",
                                                             "Miejscowość", "Forma prawna", "Adres", "Data wpisu do Rejestru Przedsiębiorców", "Kod pocztowy",
                                                             "Data wpisu do Rejestru Stowarzyszeń", "Adres WWW", "Data wykreślenia z Rejestru Przedsiębiorców",
                                                             "Email", "Data wykreślenia z Rejestru Stowarzyszeń", "Data uprawomocnienia wykreślenia z KRS",
                                                             "Data przyznania statusu OPP", "Data zawieszenia działalności",
                                                             "Data wznowienia działalności", "Nazwa organu reprezentacji","Sposób reprezentacji",
                                                             "Status OPP","Wpisy dot. postępowania upadłościowego","Nazwa organu wydającego akt prawny",
                                                             "Sygnatura aktu prawnego","Data wydania aktu prawnego","Określenie sposobu prowadzenia postępowania upadłościowego",
                                                             "Data zakończenia postępowania upadłościowego","Sposób zakończenia postępowania upadłościowego"])
            # print(companyInformations)
            allCompaniesInfo = pd.concat([allCompaniesInfo,companyInformations], ignore_index=True, axis=0)
            allCompaniesInfo.to_csv('sprawdzam.csv', encoding='utf-8-sig',mode='w',index=False)





            membersSurname = soup.find_all('td',class_='nazwanazwiskoLubNazwa')
            membersSecondSurname = soup.find_all('td',class_='nazwanazwiskoDrugie')
            membersFirstName = soup.find_all('td',class_='nazwaimiePierwsze')
            membersSecondName = soup.find_all('td',class_='nazwaimieDrugie')
            membersFunction = soup.find_all('td',class_='funkcja')

            membersNumber = len(membersSurname)
            allMembers = []
            for i in range(0,membersNumber):
                member = []
                member.append(company)
                member.append(membersSurname[i].text)
                member.append(membersSecondSurname[i].text)
                member.append(membersFirstName[i].text)
                member.append(membersSecondName[i].text)
                member.append(membersFunction[i].text)
                allMembers.append(member)


            companyMembers = pd.DataFrame(allMembers,columns=["Firma","Nazwisko lub nazwa","Nazwisko drugi człon","Imię pierwsze",
                                                              "Imię drugie","Funkcja"])
            companyMembers.replace(' ','',inplace=True)
            members = pd.concat([members, companyMembers], ignore_index=True, axis=0)
            members.to_csv('czlonkowie.csv', encoding='utf-8-sig', mode='w',index=False)

            print("Result: Done robota")
        elif howManyResults == 0:
            with open('noInfoCompany.txt', 'a', encoding='utf-8') as file:
                company = str(company)
                file.write(company + '\n')
            print("Result: brak danych")
        else:
            with open('companyToCheck.txt', 'a', encoding='utf-8') as file:
                company = str(company)
                file.write(company + '\n')
            print("Result: do wybrania")

        time.sleep(1)
        driver.quit()