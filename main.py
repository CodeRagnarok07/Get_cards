from src.cli.menu import menu_interactivo
import sys
from colorama import Fore, Style
from src.scraping import scraping
import json

with open("data/champions.json", "r") as f:
    champions = json.load(f)

opciones = [champion["name"] for champion in champions]



if __name__ == "__main__":
    try:

        print(f"{Fore.GREEN}{Style.BRIGHT}--- MENÚ DE NAVEGACIÓN ---{Style.RESET_ALL}")

        seleccion = menu_interactivo(opciones)

        for champion in champions:
            if champion["name"] == seleccion:
                scraping(champion["name"], champion["url"], champion["get_tags"])
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
