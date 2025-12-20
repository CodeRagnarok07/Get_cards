# Traduccion de textos
from deep_translator import GoogleTranslator
import json


def translate(path):
    # open Json
    data = []
    with open(f'{path}.json') as json_file:
        data = json.load(json_file)

    # Translate Json
    es = GoogleTranslator(source='auto', target='es')
    new_object = []
    for i in data:
        i["es"] = es.translate(i["text"])
        new_object.insert(len(new_object), i)
        print(i)

    return new_object


translate(path)