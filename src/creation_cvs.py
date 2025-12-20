import json
import re
import csv

name = "Illaoi"
def make_cvs(card_name):
    # open Json
    data = []
    with open(f'cards/{card_name}/{card_name}.json') as json_file:
        data = json.load(json_file)

    # Borra la url y formatea el texto español
    for i in data:
        i["text"] = re.sub('\W+', ' ', i["text"]).lstrip().lower()
        i["audio"] = f'[sound:{i["audio"]}]'
        del i["url"]
    """Falta agregar los nombres de los archivos de audio"""


    #Crea el archivo CSV
    csv_file = f'cards/{card_name}/{card_name}.csv'
    csv_columns = ['audio', 'text', 'es']
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in data:
                writer.writerow(data)
    except IOError:
        print("I/O error")

make_cvs(name)