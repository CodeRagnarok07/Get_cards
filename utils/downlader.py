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
            file_name = f'{champion}_{index+1}{extension}'
            file_path = f'data/{champion}/{file_name}'
            if os.path.exists(file_path):
                item["file_path"] = file_path
            else:

                print(f"Downloading File {file_name}")
                download = req.get(item["audio_url"])

                if download.status_code == 200: # si el status es 200 comienza la descarga
                    with open(file_path, 'wb') as f:
                        f.write(download.content)
                        print(f"Success Download File {file_name}")
                        item["file_path"] = file_path
                else:
                    print(f"Download Failed For File {file_name}")

            new_data.insert(len(new_data), item)

    return new_data



