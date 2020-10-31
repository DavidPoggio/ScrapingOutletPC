# Importamos las librerías necesarias para el trabajo
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuramos Pandas para mostrar adecuadamente los datos del dataframe

#pd.set_option('display.max_rows', 200)
#pd.set_option('display.max_columns', 200)
#pd.set_option('display.width', 1000)


# Preparamos los headers de la llamada
headers={
    "User-Agent": "PostmanRuntime/7.26.1",
    "Accept": "/*/",
    }

# Creamos un array en el que iremos volcando los datos
datos = []

# Iteramos por las primeras 20 páginas de productos
for page in range(1, 20):
    # URL contra la que realizaremos el scrapeo
    url = "https://www.pccomponentes.com/outlet/ajax?page="+str(page)+"&order=relevance"

    # Realizamos la request con la url y los headers definidos antes
    resp = requests.get(url, headers)

    # Parseamos la respuesta de la solicitud
    parseado = BeautifulSoup(resp.text, 'html.parser')

    # Buscamos todas las ocurrencias del tag article, forzando la existencia de data-name
    hits=parseado.find_all('article', {"data-name": True})

    # Iteramos por todas las ocurrencias de las búsqueda anterior añadiendo valores al array
    for hit in hits:
        nombre = hit['data-name']
        precio_rebajado = float(hit['data-price'])
        marca = hit['data-brand']
        categoria = hit['data-category']
        stock = hit['data-stock-web']
        identificador = hit['data-sku']
        precio_original = float(hit.find("div", class_="c-product-card__prices-pvp cy-product-price-normal").find("span").text.replace("€","").replace(",","."))
        porcentaje_descuento = 100-(precio_rebajado*100/precio_original)
        registro = [nombre, precio_rebajado, precio_original, porcentaje_descuento, marca, categoria, int(stock), identificador]
        datos += [registro]

# Creamos el dataframe en base a los datos
set_datos = pd.DataFrame(datos, columns=['Nombre', 'Precio', 'Precio_Original', 'Descuento', 'Marca', 'Cateogoría', 'Stock', 'Identificador'])

# Mostramos por pantalla los 5 primeros registros para validar
print(set_datos.head(5))

# Por último, exportamos el csv con los datos
set_datos.to_csv("D:\\Dataset.csv",encoding='utf-8-sig')

