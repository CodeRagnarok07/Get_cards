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
                    # Contar archivos existentes
                    total_files = len(data)
                    already_downloaded = 0
                    extension = ".ogg"
                    for index, _ in enumerate(data):
                        file_name = f"{champion['name']}_{index+1}{extension}"
                        file_path = f"{route}/{file_name}"
                        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                            already_downloaded += 1
                    
                    files_to_download = total_files - already_downloaded
                    
                    print(f"\n{Fore.CYAN}Resumen de archivos para {champion['name']}:{Style.RESET_ALL}")
                    print(f"- Total de entradas en JSON: {total_files}")
                    print(f"- Archivos ya descargados: {already_downloaded}")
                    print(f"- Archivos pendientes por descargar: {files_to_download}")
                    
                    if files_to_download > 0:
                        confirm = input(f"\n{Fore.YELLOW}¿Deseas iniciar/continuar la descarga? (s/n): {Style.RESET_ALL}").lower()
                        if confirm != 's':
                            print(f"{Fore.RED}Proceso cancelado por el usuario.{Style.RESET_ALL}")
                            break
                    else:
                        print(f"\n{Fore.GREEN}Todos los audios ya están descargados.{Style.RESET_ALL}")

                    print(f"\n{Fore.YELLOW}PASO 1: Descargando audios...{Style.RESET_ALL}")
                    new_data = downloader(champion['name'], data)

                    print(f"\n{Fore.YELLOW}PASO 2: Creando mazo de Anki...{Style.RESET_ALL}")
                    create_deck(new_data, champion['name'])
                    


                
             
                break

        print(f"\n{Fore.YELLOW}Has seleccionado: {Style.BRIGHT}{seleccion}{Style.RESET_ALL}")
        
        if seleccion == "Salir":
            print("¡Adiós!")
            sys.exit(0)
      
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit(0)
