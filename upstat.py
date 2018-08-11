# http://stat.dopa.go.th/stat/statnew/upstat_age.php

import requests
import bs4
# import csv
# import numpy as np
import pandas as pd

years = [
    '36',
    '37',
    '38',
    '39',
    '40',
    '41',
    '42',
    '43',
    '44',
    '45',
    '46',
    '47',
    '48',
    '49',
    '50',
    '51',
    '52',
    '53',
    '54',
    '55',
    '56',
    '57',
    '58',
    '59',
    '60'
]
# df_male = pd.DataFrame()
# df_female = pd.DataFrame()
df_male = None
df_female = None
df_total = None
url = "http://stat.dopa.go.th/stat/statnew/upstat_age_disp.php"

for year in years:
    print('fetching ' + year)
    payload = {
        'rcodecode': '',
        'send': 5000,
        'catDesc': '',
        'service': 'bsts_stat_webWS',
        'YEAR': year,
        'LEVEL': 1,
        'txtMsg': '1||||' + year + '12|'
    }

    headers = {
        'Connection': "keep-alive",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache",
        'Origin': "http://stat.dopa.go.th",
        'Upgrade-Insecure-Requests': "1",
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'Referer': "http://stat.dopa.go.th/stat/statnew/upstat_age.php",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "en-US,en;q=0.9,th;q=0.8",
        'Cookie': "TS01a5fe75_77=0803fa2a32ab28004b48defeba32a6a146b4d1c7b0b56938c7923e30014962d5eb09b1757031f0e989bb209444fbe16b086beabfe0823800aac8bd3e40759693c520fc4114ca52a6c1c9d8d522de41f4aa6ab9a2c6ddb9009e4ce6d7d51e09797603875704dc9291642c51276c2ca231; TS01a5fe75=010214bde33dded3e477fb0a4cfe99a504f47ff312589c47f0b8a6cad754dc35028b834873",
        'Postman-Token': "d95b9ddc-7ff2-4e53-b4a2-10efaeb258ac"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    # print(response.text)

    doc = bs4.BeautifulSoup(response.text, 'html.parser')

    tables = doc.find_all('table')

    table = tables[4]
    labels = []
    males = []
    females = []
    totals = []

    for row in table.find_all('tr')[1:]:
        # print(row)
        cols = row.find_all('td')
        age1 = cols[0].get_text().strip()
        male1 = int(cols[1].get_text().strip().replace(',', ''))
        female1 = int(cols[2].get_text().strip().replace(',', ''))
        total1 = int(cols[3].get_text().strip().replace(',', ''))
        labels.append(age1)
        males.append(male1)
        females.append(female1)
        totals.append(total1)

        age2 = cols[4].get_text().strip()
        male2 = int(cols[5].get_text().strip().replace(',', ''))
        female2 = int(cols[6].get_text().strip().replace(',', ''))
        total2 = int(cols[7].get_text().strip().replace(',', ''))
        labels.append(age2)
        males.append(male2)
        females.append(female2)
        totals.append(total2)

    if df_male is None:
        df_male = pd.DataFrame(columns=labels)
    if df_female is None:
        df_female = pd.DataFrame(columns=labels)
    if df_total is None:
        df_total = pd.DataFrame(columns=labels)

    df_male.loc[year] = males
    df_female.loc[year] = females
    df_total.loc[year] = totals

df_male.to_csv('male_year_age.csv')
df_female.to_csv('female_year_age.csv')
df_total.to_csv('total_year_age.csv')
