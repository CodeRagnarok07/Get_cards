import os
import requests
from bs4 import BeautifulSoup
import re
import json

def downloader(champion:str,data:list):

    extension = ".ogg"
    new_data = []
    
    with requests.Session() as req:
        "! se abre una secion para hacer multiples descargas"
        
        for index, item in enumerate(data):
            name = f'{champion}_{index+1}{extension}'
            if os.path.exists(f'data/{champion}/{name}'):
                pass
            else:

                print(f"Downloading File {name}")
                download = req.get(item["audio_url"])

                if download.status_code == 200: # si el status es 200 comienza la descarga
                    file_path = f'data/{champion}/{name}'
                    with open(file_path, 'wb') as f:
                        f.write(download.content)
                        print(f"Success Download File {name}")
                        item["file_path"] = file_path
                        new_data.insert(len(new_data), item)
                else:
                    print(f"Download Failed For File {name}")


    return new_data



