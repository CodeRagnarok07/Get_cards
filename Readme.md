# League of Legends - Audio to Anki Trainer 🎧🃏

Este programa de línea de comandos (CLI) permite extraer las frases y audios de los campeones de League of Legends desde la wiki oficial y convertirlos automáticamente en mazos de Anki para practicar audición y vocabulario.

## ✨ Características

- **Menú Interactivo**: Selección de campeones con buscador en tiempo real.
- **Scraping Inteligente**: Extrae frases organizadas por categorías (Moverse, Ataque, etc.) y prioriza audios de la **Skin Original**.
- **Deduplicación Automática**: Evita frases repetidas y normaliza textos para un mazo limpio.
- **Descarga Robusta**: Sistema de descarga con cabeceras que imitan navegador y tiempos de espera para evitar bloqueos.
- **Generación de Anki**: Crea archivos `.apkg` listos para importar con audio incluido.

## 📋 Requisitos Previos

- **Python 3.10 o superior**
- Un navegador web instalado (Chrome, Firefox, etc.)
- **Anki** (para usar los mazos generados)

## 🚀 Instalación y Configuración

Sigue estos pasos para preparar el entorno:

1. **Clonar o descargar el proyecto** en una carpeta local.
2. **Crear un entorno virtual** (recomendado):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # o
   .venv\Scripts\activate     # Windows
   ```
3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencias Principales:
- `requests`: Para peticiones a la API y descarga de archivos.
- `beautifulsoup4` & `lxml`: Para procesar el HTML de la wiki.
- `colorama`: Para una interfaz de terminal colorida.
- `genanki`: Para la creación técnica de los mazos de Anki.

## 🛠️ Guía de Uso

Ejecuta el programa principal con:
```bash
python3 main.py
```

### Flujo de Trabajo:

1. **Búsqueda**: Escribe el nombre del campeón en el menú. Usa las flechas `↑` y `↓` para navegar.
2. **Primera Vez (Scraping)**: Si es la primera vez que eliges a ese campeón, el programa abrirá automáticamente tu navegador en la página de la wiki. Esto es necesario para asegurar que el contenido esté disponible.
   - El programa descargará el HTML y generará un archivo `data.json` en `data/[Campeon]/`.
3. **Confirmación de Descarga**: Antes de bajar los archivos de audio (que pueden ser cientos), el programa mostrará un resumen:
   - Cuántas frases se encontraron.
   - Cuántas ya han sido descargadas previamente.
   - Cuántas faltan.
   - Presiona `s` para continuar.
4. **Creación del Mazo**: Una vez descargados los audios, se generará un archivo `.apkg`.

### ¿Dónde están mis archivos?
Todo se organiza en la carpeta `data/`:
- `data/[Campeon]/page.html`: Copia del sitio web.
- `data/[Campeon]/data.json`: Lista de frases y URLs procesadas.
- `data/[Campeon]/*.ogg`: Los archivos de audio.
- **`data/[Campeon]/[Campeon].apkg`**: ¡Este es tu mazo de Anki!

## ⚠️ Notas Importantes

- **Bloqueos de Conexión**: Si ves errores de "Read timeout" o "Connection reset", es normal si el servidor de la wiki está saturado. El programa saltará los fallidos y podrás reintentar después; no descargará lo que ya bajaste con éxito.
- **Deduplicación**: El programa normaliza los textos (ignora mayúsculas y signos de puntuación) para no crear tarjetas duplicadas si una frase aparece en varias skins.

---
*Desarrollado como herramienta educativa para el aprendizaje de idiomas a través del gaming.*
