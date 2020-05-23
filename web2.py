import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import os

# funciones de data cleaning:

# se define una funcion para quedarnos con los valores de las celdas de la tabla que solamente correspondan
# al acumulativo de infectados y muertos, es decir, sacamos las referencias de wikipedia encerradas entre corchetes
def limpiar_dato(texto):
    i = 0
    cadena = ''
    flag = True
    while i < len(texto):
        if texto[i] == '[':
            flag = False
        elif texto[i] == ']':
            flag = True
        elif flag and texto[i] != ']':
            cadena = cadena + texto[i]

        i = i + 1

    return cadena


# funcion que reemplaza las letras vocales con tildes por su correspondiente sin tilde
def quitar_acentos(texto):
    return texto.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')


# obtenemos el sitio web a traves de un request. devuelve un objeto response
result = requests.get("https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Argentina")

# se abre el texto HTML del sitio web con su correspondiente analizador
soup = BeautifulSoup(result.text, 'html.parser')

# Verificamos el codigo de estado de la respuesta. Un codigo 200 significa que el sitio responde OK
if result.status_code != 200:
    raise Exception("El sitio web no responde. código de error: " + str(result.status_code))

# se busca el primer tag table que se corresponda con la tabla de estadisticas. Se obtiene el codigo HTML correspondiente
table = soup.find('table', {'class': 'wikitable mw-collapsible'})

# Se separa en una lista todas las etiquetas TR, es decir, las filas de la tabla
rows = table.find_all('tr')

# columns0: almacena en una lista todos las etiquetas TH(header) de la primer fila de la tabla. Por cada una obtenemos el texto y quitamos saltos de linea
# columns1: almacena en una lista los nombres de todas las provincias, a traves de atributo title de la etiqueta abbr
# columns2: almacena en una lista las headers de los totales
columns0 = [v.text.replace('\n', '') for v in rows[0].find_all('th')]  # row[0] significa la primer fila, y ahi busca todos los headers
columns1 = [v.attrs['title'] for v in rows[1].find_all('abbr')[:-1]]  # aca tengo una lista con BA (C) hasta New
columns2 = [v.attrs['title'] for v in rows[2].find_all('abbr')]  # ['Total', 'D', 'NC', 'ND']

# Se añade al encabezado general de la tabla, la columna 'ID' y 'Date' en la lista llamada 'header'
header = ['ID']
header.append(columns0[0])

# proceso de construccion del encabezado
for e in columns1:
    header.append(quitar_acentos(e))

for e in columns2:
    header.append(e)



# Se construye un dataframe bidimensional solamente con el header
df = pd.DataFrame(columns=header)

#inicializo indice autoincremental para la columna ID
index=0

# Interesa almacenar estadisticas de la tabla a partir de la 4° fila hasta la última, exceptuando las notas al pie de tabla
for i in range(3, len(rows) - 1):

    # lista que almacena las estadisticas de infectados y muertos de la fila en cuestion. Contiene etiquetas TD(valor de celda)
    tds = rows[i].find_all('td')

    # lista que almacena el dia y mes de cada fila, cuyo valor se contiene en la primer columna(Date) de la tabla
    aux = rows[i].find_all('th')[0].text.replace('\n', '')

    # La lista values realiza la construccion de cada registro de la tabla según el orden del header.
    values = []
    values.append(index)

    # se añaden los elementos al registro, comenzando por la fecha y luego las estadisticas de infectados/muertos
    values.append(limpiar_dato(aux))
    #print(values)
    for td in tds:
            values.append(limpiar_dato(td.text.replace('\n', '').replace('—', '').replace(' ', '')))

    # Si el registro contiene algun valor para cualquiera de sus campos se añade al Dataframe
    if len(values) == 30:
        # Se crea una serie cuyo valor es el registro entero y el indice son todos los campos del header
        # La serie creada se añade al dataframe inicialmente vacio, ignorando el indice para que sea consecutivo
        df = df.append(pd.Series(values, index=header), ignore_index=True)
    index=index+1

# Se exporta el dataframe resultante en un archivo con formato csv.
# Se declara index=False para que no se incluya el numero de indice de linea

#ruta = 'F:\Phyton_programas\PyCharm\WebScrapping_Covid-19_Argentina_daily.csv'
path = os.getcwd()+'\\'+'WebScrapping_Covid-19_Argentina_daily.csv'
try:
    df.to_csv(path, index=False)
except PermissionError:
    print("[Errno 13] Permission denied: Revisa que hayas cerrado correctamente el archivo csv antes de ejecutar el programa.")
else:
    print("archivo csv generado correctamente.")
