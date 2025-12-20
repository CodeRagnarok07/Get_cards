import os
import requests
from bs4 import BeautifulSoup
import re
import json
from deep_translator import GoogleTranslator



class MakeCards:
    name = ""
    url = ""
    tags= ""
    listado = []

    def scraping(url=url, tags= tags, listado= listado):
    
        result = requests.get(url)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')

        # Obtenemos los audios y los textos en una lista
        get_tags = soup.select(tags)
        """ Extre las etiquetas que creemos que tiene el contenido importante"""
        get_data = re.compile(r'(?<=src=").*?(?=")|(?<=>").*?(?="<)')
        """ extrae la url de las etiquetas y el texto de una etiqueta"""
        resultado = get_data.findall(str(get_tags))

        # Agregamos los textos y audios a un dict
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
                    listado.insert(len(listado), objeto)
                    objeto.clear
                    objeto = {"url": False}


    def translate(card_name = name):
        # open Json
        data = []
        with open(f'cards/{card_name}/{card_name}.json') as json_file:
            data = json.load(json_file)

        # Translate Json
        es = GoogleTranslator(source='auto', target='es')
        new_object = []
        for i in data:
            i["es"] = es.translate(i["text"])
            new_object.insert(len(new_object), i)
            print(i)


        # # CREAR UN ARCHIVO CON LA INFORMACION
        with open(f'cards/{card_name}/{card_name}.json', "w") as outfile:
            json.dump(new_object, outfile)
        print("translate completed")

    def save_json(card_name, list = listado):
                # CREAR UN ARCHIVO CON LA INFORMACION
        if not os.path.exists(f'cards/{card_name}'):
            os.mkdir(f'cards/{card_name}')

        with open(f'cards/{card_name}/{card_name}.json', "w") as outfile:
            json.dump(list, outfile)


a = MakeCards


name = "Illaoi"
url = f'https://leagueoflegends.fandom.com/wiki/{name}/LoL/Audio'
get_tags = 'i, b , audio'

a.name = name
a.url = url
a.tags = get_tags

a.scraping()
print(a.listado)



