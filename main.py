import os
import sys
import json
from colorama import Fore, Style

from utils import downloader, scraping, menu_interactivo, filter_quotes

# seleccion de campeones
with open("data/champions.json", "r") as f:
    champions = json.load(f)

champions_names = [champion["name"] for champion in champions]

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

        seleccion = menu_interactivo(champions_names)

        for champion in champions:
            if champion["name"] == seleccion:

                # check if data exist 
                route = f"data/{champion['name']}"
                
                data = load_champion_data(f"{route}/data.json")

                if data:
                    # new_data = Downlader.block_download(champion['name'],data)
                    # pasos
                    print("PASO 1 limpiar duplicados")

                    print(f"Total de quotes: {len(data)}")
                    new_data = filter_quotes(data)
                    print(f"Total de quotes sin duplicados: {len(new_data)}")

                    print("PASO 2 descargar audios")
                    new_data = downloader(champion['name'],new_data)


                    print("pasos 3 create ankie deck")
                    


                
             
                break

        print(f"\n{Fore.YELLOW}Has seleccionado: {Style.BRIGHT}{seleccion}{Style.RESET_ALL}")
        
        if seleccion == "Salir":
            print("¡Adiós!")
            sys.exit(0)
        
        # Aquí puedes añadir la lógica para cada opción
        print(f"Ejecutando {seleccion}...")
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit(0)
