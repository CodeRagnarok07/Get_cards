
import genanki
import os
import random
from .config import TEMPLATE, CSS   



def create_deck(data, path):
    # ============================================
    # 1. DEFINIR EL MODELO (TEMPLATE)
    # ============================================

    # IDs únicos (genera una vez y mantén fijos)
    MODEL_ID = random.randrange(1 << 30, 1 << 31)
    DECK_ID = random.randrange(1 << 30, 1 << 31)

    # Modelo para listening con input
    listening_model = genanki.Model(
        MODEL_ID,
        'Listening Trainer',
        fields=[
            {'name': 'phrase'},
            {'name': 'translate'},
            {'name': 'url_file'},
        ],
        templates=[ TEMPLATE ],
        css=CSS
    )

    # ============================================
    # 2. CREAR EL DECK
    # ============================================

    deck = genanki.Deck(
        DECK_ID,
        f'English::Gaming_Listening_Trainer::{path}'
    )


    # Lista para almacenar rutas de archivos media
    media_files = []

    for item in data:
        print(item)

        file_path = item['file_path']
        if not file_path:
            print('archivo no existe')
            print(item)
            continue
        
        # Verificar que el archivo existe
        if os.path.exists(file_path):
            media_files.append(file_path)
            
            # Crear nota
            note = genanki.Note(
                model=listening_model,
                fields=[
                    item['text'],
                    '',
                    f"[sound:{os.path.basename(file_path)}]",  # Formato Anki para audio
                ],
                # tags=[item['Tag'], item['Skin']]
            )
            deck.add_note(note)
            print(f"✅ Añadido: {item['file_path']}")
        else:
            print(f"⚠️ Audio no encontrado: {file_path}")

    # ============================================
    # 4. CREAR EL PACKAGE (.apkg)
    # ============================================

    package = genanki.Package(deck)
    package.media_files = media_files  # Incluir los audios

    output_file = f'data/{path}/{path}.apkg'
    package.write_to_file(output_file)

    print(f"\n🎉 Mazo creado: {output_file}")
    print(f"📊 Total de tarjetas: {len(deck.notes)}")
    print(f"🎵 Archivos de audio incluidos: {len(media_files)}")