import os
import requests
import sys
import json
from colorama import Fore, Style

from utils import downloader, scraping, menu_interactivo, create_deck
from urllib.parse import quote

# seleccion de campeones
url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json"
response = requests.get(url)
data = response.json()


champions = list(data["data"].values())
champions_names = sorted([champion["name"] for champion in champions])

opciones = [
    # 'descargar',
    'process',
    'Salir'
]

def load_champion_data(route:str):
    


    if os.path.exists(route):
        with open(route, "r") as f:
            data = json.load(f)
        return data
    else:
        return None



if __name__ == "__main__":
    try:

        print(f"{Fore.GREEN}{Style.BRIGHT}--- MENÚ DE NAVEGACIÓN ---{Style.RESET_ALL}")

        seleccion = menu_interactivo(champions_names, buscador=True)

        for champion in champions:
            if champion["name"] == seleccion:

                # check if data exist 
                route = f"data/{champion['name']}"

                if not os.path.exists(route):
                    champion_url = f'https://leagueoflegends.fandom.com/wiki/{quote(champion["name"])}/LoL/Audio'
                    print(f"{Fore.CYAN}Abriendo el navegador y descargando datos para {champion['name']}...{Style.RESET_ALL}")
                    
                    # 1. Abrir el navegador
                    import webbrowser
                    webbrowser.open(champion_url)
                    
                    # 2. Descargar todo el html y procesar
                    scraping(champion["name"], champion_url)
                    
                
                data = load_champion_data(f"{route}/data.json")

                if data:
                    print("PASO 1 descargar audios")
                    new_data = downloader(champion['name'], data)

                    print("PASO 2 create ankie deck")
                    create_deck(new_data, champion['name'])
                    


                
             
                break

        print(f"\n{Fore.YELLOW}Has seleccionado: {Style.BRIGHT}{seleccion}{Style.RESET_ALL}")
        
        if seleccion == "Salir":
            print("¡Adiós!")
            sys.exit(0)
      
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit(0)
