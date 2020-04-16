import requests
from bs4 import BeautifulSoup
import re
import csv


result = requests.get("https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Argentina")


soup = BeautifulSoup(result.text, 'html.parser')

print(result.status_code)
result.raise_for_status()
print(result.raise_for_status())

#elem = soup.select('#mw-content-text > div > div:nth-child(62) > table > tbody > tr:nth-child(42)') #10-abrl
elem = soup.select('#mw-content-text > div > div:nth-child(65) > table > tbody > tr:nth-child(42)')

print(elem)

elemtext = elem[0].text.split("\n")
print(elemtext)

listita=[["Date","BA","BA","CA","CH","CB","CD","CR","ER","FO","JY","LP","LR","MD","MI",
          "NE","RN","SA","SJ","SL","SC","SF","SE","TF","TU","Total","D","NC","ND"]]

aux=[]
for lista in elemtext:
    if lista != '':
        aux.append(lista)

print("\nlista aux")
print(aux)
listita.append(aux)
print("\nlista nueva")
print(listita)

mifile = open("ejemplo.csv","w")
with mifile:
    writer = csv.writer(mifile)
    writer.writerows(listita)



