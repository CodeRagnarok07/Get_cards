import os
import requests
from bs4 import BeautifulSoup
import re
import json

""" Obtiene una url y extrae los audios y los texto de las etiquetas que creemos que contienen los audios
    Crea un archivo Json a partir de esto
"""

name = "Illaoi"
url = f'https://leagueoflegends.fandom.com/wiki/{name}/LoL/Audio'
get_tags = 'i, b , audio'


def scraping(card_name, url, get_tags):
    # leer cualquier web
    website = url
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Obtenemos los audios y los textos en una lista
    tags = soup.select(get_tags)
    """ Extre las etiquetas que creemos que tiene el contenido importante"""
    get_data = re.compile(r'(?<=src=").*?(?=")|(?<=>").*?(?="<)')
    """ extrae la url de las etiquetas y el texto de una etiqueta"""
    resultado = get_data.findall(str(tags))

    # Agregamos los textos y audios a un dict
    lista = []
    objeto = {
        "url": False
    }
    for i in resultado:
        """ si es una url agrega 1 elemento a un dic luego agrega ese dict a la lista"""
        if i.startswith("http") == True:
            if objeto["url"]:
                pass
            else:
                objeto["url"] = i
        else:
            if i.endswith(".ogg") == True:
                pass
            else:
                objeto["text"] = i
                lista.insert(len(lista), objeto)
                objeto.clear
                objeto = {"url": False}

    # CREAR UN ARCHIVO CON LA INFORMACION
    if not os.path.exists(f'cards/{card_name}'):
        os.mkdir(f'cards/{card_name}')

    with open(f'cards/{card_name}/{card_name}.json', "w") as outfile:
        json.dump(lista, outfile)


scraping(name, url, get_tags)
