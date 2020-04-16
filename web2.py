import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd


result = requests.get("https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Argentina")

soup = BeautifulSoup(result.text, 'html.parser')

print("Codigo de estado: " + str(result.status_code))
result.raise_for_status()
print("excepcion: " + str(result.raise_for_status()))

#print(soup)

table = soup.find('table', {'class':'wikitable mw-collapsible'})

#print(table)


rows = table.find_all('tr')
#columns0 = [v.text.replace('\n','') for v in rows[0].find_all('th')]
columns1 = [v.text.replace('\n','')  for v in rows[1].find_all('th')]
columns2 = [v.text.replace('\n','')  for v in rows[2].find_all('th')]
columns3 = [v.text.replace('\n','')  for v in rows[3].find_all('th')]
print(columns3) #aca esta el 3 Mar

#header = [columns0[0]]
header=[]

for e in columns1[:-2]:
    header.append(e)

for e in columns2:
    header.append(e)

#print(header)

df = pd.DataFrame(columns=header)

for i in range(1,len(rows)):
    tds = rows[i].find_all('td')
    values=[td.text.replace('\n','') for td in tds]
    #print(values)
    if len(values) != 0:
        df = df.append(pd.Series(values,index=header),ignore_index=True)
        #print(df)


df.to_csv(r'F:\Phyton_programas\PyCharm\WebScrapping'+ 'ejemplo2.csv',index=False)