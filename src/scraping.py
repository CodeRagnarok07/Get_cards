import os
import requests
from bs4 import BeautifulSoup
import re
import json

"""
Módulo para el scraping de audios y diálogos de League of Legends.

Este módulo proporciona funciones para extraer URLs de audio (.ogg) y sus
correspondientes transcripciones desde la wiki de Fandom de League of Legends,
almacenando los resultados en archivos JSON estructurados.
"""

def scraping(champion: str, url: str, get_tags: str) -> None:
    """
    Extrae audios y textos de una página de la wiki y los guarda en un JSON.

    Busca etiquetas específicas en el HTML, extrae las URLs de los archivos de audio
    y el texto asociado, y organiza esta información en una lista de objetos
    que se guarda en el directorio 'cards/'.

    Args:
        champion (str): Nombre del campeón o categoría para organizar los archivos.
        url (str): Dirección URL de la página de audio de la wiki.
        get_tags (str): Selectores CSS (separados por comas) para identificar
                         las etiquetas que contienen la información deseada.

    Returns:
        None
    """
    # Realiza la petición a la web
    website = url
    try:
        result = requests.get(website)
        result.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return

    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Obtenemos las etiquetas que contienen audios y textos
    tags = soup.select(get_tags)
    
    # Expresión regular para extraer src="..." o contenido entre etiquetas simple
    # Nota: El regex original se mantiene pero se documenta su propósito
    get_data = re.compile(r'(?<=src=").*?(?=")|(?<=>").*?(?="<)')
    resultado = get_data.findall(str(tags))

    # Estructura la información en una lista de diccionarios
    lista = []
    objeto = {
        "url": False
    }
    
    for i in resultado:
        # Si el elemento parece una URL (comienza con http)
        if i.startswith("http"):
            if not objeto["url"]:
                objeto["url"] = i
        else:
            # Si no es una URL y no es un nombre de archivo .ogg, se asume que es el texto
            if not i.endswith(".ogg"):
                objeto["text"] = i
                lista.append(objeto)
                objeto = {"url": False}

    # CREAR EL DIRECTORIO Y EL ARCHIVO CON LA INFORMACIÓN
    output_dir = f'data/{champion}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    file_path = f'{output_dir}/{champion}.json'
    try:
        with open(file_path, "w", encoding='utf-8') as outfile:
            json.dump(lista, outfile, indent=4, ensure_ascii=False)
        print(f"\n")
        # Mensaje de resultados
        print(f"Datos guardados exitosamente en: {file_path}")
        print(f"\n")
    except IOError as e:
        print(f"Error al guardar el archivo JSON: {e}")

if __name__ == "__main__":
    # Configuración por defecto para ejecución directa
    CHAMPION_NAME = "Illaoi"
    TARGET_URL = f'https://leagueoflegends.fandom.com/wiki/{CHAMPION_NAME}/LoL/Audio'
    SELECTORS = 'i, b, audio'
    
    scraping(CHAMPION_NAME, TARGET_URL, SELECTORS)
