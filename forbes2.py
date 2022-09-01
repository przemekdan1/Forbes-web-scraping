from bs4 import BeautifulSoup
from itertools import chain
from functools import reduce
import pandas as pd
import numpy as np
import requests


def remove_items(test_list, item):
    res = [i for i in test_list if i != item]
    return res

def flatten(list_of_lists):
    return list(chain.from_iterable(list_of_lists))

def which_year_url(url):
    year = 2016
    while str(year) not in url:
        year += 1
    return year


if __name__ == '__main__':

    #creating df for all data from sites
    dataForbes = pd.DataFrame(
        columns=["Firma", "Miejsce na liście regionalnej", "Miejsce na liście ogólnopolskiej","Rok", "Siedziba", "Opis",
                 "Przychody","Zysk","Skala","Waluta","Link"])
    # dataForbes.to_csv("test.csv", encoding="utf-8")




    with open("forbes.txt") as file:
        for url in file:
            url = url.strip()

            # YEAR
            year = which_year_url(url)
            print(year, url)

            if year == 2022:
                html_text = requests.get(url).text
                soup = BeautifulSoup(html_text, 'lxml')

                # FINDING TABLE OF ALL DATA
                rankings = soup.find_all('div', class_='pulsembed_embed')

                links = []
                for ranking in rankings:
                    links.append(ranking.a.get('href'))

                if links:
                    dataToPandas = []
                    for link in links:

                        html_text = requests.get(link).text

                        soup = BeautifulSoup(html_text, 'lxml')
                        rankings = soup.find_all('table', class_='rankTable tableWithBorder')
                        # print(rankings)

                        data = []
                        for ranking in rankings:
                            all_data = ranking.find_all('td')
                            headersOfYear = all_data[1:9]
                            for i, header in enumerate(headersOfYear):
                                header = header.text
                                headersOfYear[i] = header

                            # filling scale
                            moneyData = headersOfYear[-2]
                            if 'mln' in moneyData:
                                scale = 'mln'
                            else:
                                scale = '---'

                            # delete title and headers of ranking
                            del all_data[0:9]
                            for data_storage in all_data:
                                data_storage = data_storage.text.strip().splitlines()
                                if len(data_storage) > 1:
                                    data_storage = reduce(lambda a, b: a + b, data_storage)
                                    data_storage = [data_storage]
                                data.append(data_storage)
                        data = flatten(data)

                        numberOfColumns = len(headersOfYear)
                        counter = 1
                        dataRow = []
                        for element in data:
                            if counter < numberOfColumns:
                                dataRow.append(element)
                                counter += 1
                            else:
                                dataRow.append(element)
                                dataToPandas.append(dataRow)
                                dataRow = []
                                counter = 1
            else:
                html_text = requests.get(url).text
                soup = BeautifulSoup(html_text, 'lxml')
                rankings = soup.find_all('table', class_='rankTable tableWithBorder')

                #if site does contain company rankings
                if rankings:

                    # HEADERS OF THE YEAR
                    headersOfYear = []
                    ranking = rankings[0]
                    headers = ranking.find_all('th')
                    for header in headers:
                        header = header.text.strip().replace('\n', '')
                        headersOfYear.append(header)

                    #filling scale
                    moneyData = headersOfYear[-2]
                    if 'mln' in moneyData:
                        scale = 'mln'
                    else:
                        scale = '---'
                    numberOfColumns = len(headersOfYear)



                    data = []
                    for ranking in rankings:
                        all_data = ranking.find_all('td')
                        for data_storage in all_data:
                            data_storage = data_storage.text.strip().splitlines()
                            if len(data_storage) > 1:
                                data_storage = reduce(lambda a, b: a + b, data_storage)
                                data_storage = [data_storage]
                            data.append(data_storage)
                    data = flatten(data)

                    counter = 1
                    dataToPandas = []
                    dataRow = []
                    for element in data:
                        if counter < numberOfColumns:
                            dataRow.append(element)
                            counter += 1
                        else:
                            dataRow.append(element)
                            dataToPandas.append(dataRow)
                            dataRow = []
                            counter = 1


            #changing headers name
            headers = {
                'miejsce na liście regionalnej' : 'Miejsce na liście regionalnej',
                'miejsce na liście ogólnopolskiej' : 'Miejsce na liście ogólnopolskiej',
                'nazwa' : 'Firma',
                'miasto' :  'Siedziba',
                'przychody ze sprzedaży w 2014 r. (PLN)' : 'Przychody',
                'zysk netto w 2014 r. (PLN)' : 'Zysk',
                'przec. wzrost wartości 2012-2014 (proc.)' : 'Średnia ważona',
                'przec. wzrost wartości 2012-2014' : 'Średnia ważona',
                'przychody ze sprzedaży w 2015 r. (PLN)': 'Przychody',
                'zysk netto w 2015 r. (PLN)': 'Zysk',
                'zysk netto w 2015 r. (PLN)	': 'Zysk',
                'przec. wzrost wartości 2013-2015 (proc.)': 'Średnia ważona',
                'Miejsce na liście regionalnej': 'Miejsce na liście regionalnej',
                'Miejsce na liście ogólnopolskiej': 'Miejsce na liście ogólnopolskiej',
                'Firma' : 'Firma',
                'Miasto': 'Siedziba',
                'Branża/Sektor' : 'Opis',
                'SPRZEDAŻ 2016 (mln zł)': 'Przychody',
                'Zysk Netto 2016 (mln zł)': 'Zysk',
                'Średnia ważona wzrostu (proc.)': 'Średnia ważona',
                'Siedziba': 'Siedziba',
                'Sprzedaż 2017 (mln zł)': 'Przychody',
                'Zysk netto 2017 (mln zł)': 'Zysk',
                'Sprzedaż 2018 (mln zł)': 'Przychody',
                'Sprzedaż 2018  (mln zł)': 'Przychody',
                'Zysk netto 2018 (mln zł)': 'Zysk',
                'Zysk netto 2018  (mln zł)': 'Zysk',
                'Średnia ważona wzrostu  (proc.)': 'Średnia ważona',
                'Miejsce  na liście regionalnej': 'Miejsce na liście regionalnej',
                'Miejsce  na liście ogólnopolskiej': 'Miejsce na liście ogólnopolskiej',
                'Sprzedaż 2019 (mln zł)': 'Przychody',
                'Sprzedaż 2019  (mln zł)': 'Przychody',
                'Zysk netto 2019 (mln zł)': 'Zysk',
                'Zysk netto 2019  (mln zł)': 'Zysk',
                'opis': 'Opis',
                'Sprzedaż 2020 (mln zł)': 'Przychody',
                'Zysk netto 2020 (mln zł)': 'Zysk',
                'średnia ważona': 'Średnia ważona'
                }


            data = pd.DataFrame(dataToPandas, columns=headersOfYear)
            data.rename(columns = headers,inplace=True)
            data['Średnia ważona'] = data['Średnia ważona'].str.replace(',', '.')
            data['Przychody'] = data['Przychody'].str.replace(',', '.')
            data['Zysk'] = data['Zysk'].str.replace(',', '.')
            data["Rok"] = year
            data["Link"] = url
            data["Skala"] = scale
            data["Waluta"] = 'zł'


            dataForbes = dataForbes.append(data)
            print(dataForbes.info())

    dataForbes.set_index(["Firma"],inplace=True)
    dataForbes.to_csv('forbes.csv', encoding='utf-8-sig')
    print(dataForbes.info())

