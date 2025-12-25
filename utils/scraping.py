import os
import requests
from bs4 import BeautifulSoup
import json
import re

def scraping(champion: str, url: str) -> None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return

    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # CREAR EL DIRECTORIO
    output_dir = f'data/{champion}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Guardar el HTML original
    html_path = f'{output_dir}/page.html'
    with open(html_path, "w", encoding='utf-8') as f:
        f.write(content)

    all_data = []

    # Encontrar todas las secciones (representadas por encabezados h2, h3, h4, etc.)
    # La wiki usa h2 para categorías grandes, h3 para tipos de diálogo.
    # Buscamos los contenedores que suelen ser <ul> o <dl> después de un header.
    
    # Una estrategia robusta es buscar todos los elementos de audio y subir hasta encontrar su contenedor de línea <li>.
    # Luego, en ese <li>, buscar el texto y determinar el skin.
    
    audio_buttons = soup.select('audio.ext-audiobutton')
    
    for audio in audio_buttons:
        # Encontrar el <li> que contiene este audio
        parent_li = audio.find_parent('li')
        if not parent_li:
            continue
            
        source = audio.select_one('source')
        if not source or not source.get('src'):
            continue
            
        audio_url = source.get('src')
        
        # Encontrar el texto asociado.
        # Las frases suelen estar en un <i> después de los botones de audio.
        # Buscamos el <i> dentro del mismo <li>
        text_elem = parent_li.select_one('i')
        
        # Si no hay <i>, a veces el texto es el último nodo de texto del <li>
        if not text_elem:
            # Seleccionar texto que no esté dentro de otras etiquetas si es posible, 
            # o simplemente limpiar el texto total del li restando el de los botones.
            text = parent_li.get_text(" ", strip=True)
            # Limpieza agresiva de metadatos de la wiki
            text = re.sub(r'▶️.*?\s+', '', text) # Eliminar botones
            text = re.sub(r'\[.*?\]', '', text) # Eliminar corchetes
        else:
            text = text_elem.get_text(strip=True)
            
        text = text.strip('"').strip()
        
        if not text or len(text.split()) <= 1:
            continue

        # Determinar el skin para este audio específico.
        skin = "Original" # Default
        # El botón de audio (span que envuelve el audio) está antes de un skin-play-button
        container_span = audio.find_parent('span')
        if container_span:
            # Buscar el siguiente span con clase skin-play-button
            skin_hint = container_span.find_next_sibling('span', class_='skin-play-button')
            if skin_hint and skin_hint.get('data-skin'):
                skin = skin_hint.get('data-skin')

        # Encontrar la categoría (h3 o h2 más cercano hacia arriba)
        category = "General"
        prev = parent_li.find_previous(['h3', 'h2'])
        if prev:
            category = prev.get_text(strip=True).replace('[edit]', '').strip()

        all_data.append({
            "category": category,
            "skin": skin,
            "text": text,
            "audio_url": audio_url
        })

    # Filtrado por jerarquía y duplicados
    # 1. Agrupar por Texto (normalizado a minúsculas para comparaciones más precisas de unicidad)
    # 2. Priorizar "Original" skin.
    
    filtered_quotes = {}
    for item in all_data:
        # Normalizamos el texto para la clave de unicidad (aunque guardamos el original)
        # Eliminamos puntuación básica y espacios extra para mayor precisión en duplicados
        norm_text = re.sub(r'[^\w\s]', '', item["text"].lower()).strip()
        
        if not norm_text:
            continue

        if norm_text not in filtered_quotes:
            filtered_quotes[norm_text] = item
        else:
            # Prioridad: Si el nuevo es "Original" y el actual no, reemplazamos.
            # También comprobamos si el skin actual es "General" o similar y el nuevo es más específico.
            current_skin = filtered_quotes[norm_text]["skin"].lower()
            new_skin = item["skin"].lower()
            
            if new_skin == "original" and current_skin != "original":
                filtered_quotes[norm_text] = item
            # Si ambos son del mismo skin, mantenemos el que ya estaba (o el que sea más completo)
    
    final_list = list(filtered_quotes.values())

    # Orden final opcional por categoría para mejor visualización
    final_list.sort(key=lambda x: x["category"])

    file_path = f'{output_dir}/data.json'
    try:
        with open(file_path, "w", encoding='utf-8') as outfile:
            json.dump(final_list, outfile, indent=4, ensure_ascii=False)
        print(f"Datos guardados exitosamente en: {file_path}")
        print(f"Total de frases únicas extraídas: {len(final_list)}")
    except IOError as e:
        print(f"Error al guardar el archivo JSON: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        scraping(sys.argv[1], f"https://leagueoflegends.fandom.com/wiki/{sys.argv[1]}/LoL/Audio")
