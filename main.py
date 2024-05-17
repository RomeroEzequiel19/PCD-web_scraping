import requests
from bs4 import BeautifulSoup
import json

# Se obtienen todos los enlaces de la url especificada
def obtener_enlaces(url):
    
    # request
    response = requests.get(url)

    # obtener texto plano y dárselo a BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    hrefs = []

    # Agrega a la lista de hrefs los links obtenidos
    for link in soup.find_all('a', class_="promotion-item__link-container"):
        hrefs.append(link.get('href'))

    print(f"Se obtuvieron {len(hrefs)} enlaces de la página")

    return hrefs

# Obtiene las etiquetas <h1> y <p> de cada enlace encontrado.
def obtener_contenido(enlaces):

    elementos = {}

    for url in enlaces[:20]:

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recopila los elementos h1 y p
            etiquetas_h1 = [str(h1) for h1 in soup.find_all('h1')]
            etiquetas_p = [str(p) for p in soup.find_all('p')]
            
            # Asigna los valores correspondientes a las claves en el diccionario
            elementos[url] = {"h1": etiquetas_h1, "p":etiquetas_p}
        
        except Exception as e:
            print(f"Error: ({e})")

    print(f"Se obtuvieron los elementos h1 y p de los enlaces")

    return elementos

# Almacena los datos en un archivo JSON
def realizar_json(elementos):

    with open('resultados.json', 'w', encoding='utf-8') as archivo:
        # Convierte la estructura de datos de Python en una cadena JSON y la guarda en el archivo
        json.dump(elementos, archivo, ensure_ascii=False, indent=4)

    print(f"Se realizó el archivo JSON con los enlaces y elementos")



# URL inicial
url_inicial = 'https://www.mercadolibre.com.ar/ofertas?domain_id=MLA-CELLPHONES&container_id=MLA779505-1#deal_print_id=8463b610-12c1-11ef-ad0e-535c6aa6c935&c_id=carouseldynamic-home&c_element_order=undefined&c_campaign=VER-MAS&c_uid=8463b610-12c1-11ef-ad0e-535c6aa6c935'

# Ejecutar la función principal
enlaces = obtener_enlaces(url_inicial)
elementos = obtener_contenido(enlaces)
realizar_json(elementos)
