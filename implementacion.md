# Plan de Implementación - LoL Audio Scraper (ACTUALIZADO)

## 🔍 Hallazgos de Investigación

### Problema Detectado: Protección Anti-Bot de Fandom
**Resultado de pruebas:**
- ✅ Yasuo: 1075 audios, 745 transcripciones (1455 KB)
- ✅ Jinx: 471 audios, 393 transcripciones (706 KB)
- ❌ Illaoi, Ezreal, Ahri, Lux: **0 audios** (3 KB) - **Bloqueados por "Client Challenge"**

**Conclusión:** Fandom Wiki tiene protección anti-bot que bloquea ~66% de las peticiones.

### Frases a Filtrar (Detectadas)
- ❌ "Sound Effect" (no es diálogo)
- ❌ "15 seconds cooldown" (descripción técnica)
- ❌ "A stripped-down version of..." (descripción de música)
- ❌ "These lines aren't guaranteed..." (notas técnicas)
- ❌ Frases monosilábicas: "Hm", "Ah", "Ugh", etc.

---

## 📋 Objetivos CORREGIDOS

- ✅ No tocar el directorio `make_cards/`
- ✅ Crear programa modular en el root del proyecto
- ✅ Selección interactiva de campeón
- ✅ Almacenamiento en SQLite (caché)
- ✅ **SIN descarga de audios** (solo URLs)
- ✅ Generación directa de CSV para Anki
- ✅ **Manejo de protección anti-bot**
- ✅ **Filtrado de frases sin sentido**
- ✅ Ejecutable en entorno de desarrollo
- ✅ Compilable con Nuitka para Windows

---

## 🏗️ Estructura del Proyecto (ACTUALIZADA)

```
Get_cards/
├── make_cards/              # ❌ NO TOCAR
│   └── ...
├── src/                     # ✅ NUEVO - Código modular
│   ├── __init__.py
│   ├── scraper.py          # Scraping con anti-bot handling
│   ├── text_filter.py      # ✅ NUEVO - Filtrado de frases
│   ├── translator.py       # Traducción con GoogleTranslator
│   ├── database.py         # Gestión SQLite
│   ├── csv_generator.py    # Generación CSV para Anki
│   └── champion_list.py    # Obtención de lista de campeones
├── data/                    # ✅ NUEVO - Datos persistentes
│   └── champions.db        # Base de datos SQLite
├── output/                  # ✅ NUEVO - Archivos CSV generados
│   └── {champion_name}.csv
├── venv/                    # Entorno virtual
├── test_scraping.py         # ✅ Script de pruebas
├── scraping_test_results.json  # ✅ Resultados de pruebas
├── main.py                  # ✅ NUEVO - CLI principal
├── config.py                # ✅ NUEVO - Configuración
├── requirements.txt         # ✅ NUEVO - Dependencias
├── build.py                 # ✅ NUEVO - Script de compilación Nuitka
└── README.md                # ✅ NUEVO - Documentación
```

---

## 🗄️ Esquema de Base de Datos SQLite (ACTUALIZADO)

### Tabla: `champions`
```sql
CREATE TABLE champions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    title TEXT,
    scraping_attempts INTEGER DEFAULT 0,
    last_scrape_success BOOLEAN DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: `voice_lines`
```sql
CREATE TABLE voice_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    champion_id INTEGER NOT NULL,
    text_en TEXT NOT NULL,
    text_es TEXT,
    audio_url TEXT NOT NULL,
    is_filtered BOOLEAN DEFAULT 0,  -- Si fue filtrada (monosílaba/sin sentido)
    filter_reason TEXT,              -- Razón del filtro
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (champion_id) REFERENCES champions(id)
);
```

---

## 📦 Módulos y Funciones

### 1. `src/champion_list.py`
```python
def get_all_champions() -> List[str]:
    """Obtiene lista de campeones desde Data Dragon API"""
    
def search_champion(query: str) -> List[str]:
    """Busca campeones por nombre (fuzzy search)"""
```

### 2. `src/database.py`
```python
def init_db() -> None:
    """Inicializa la base de datos SQLite"""
    
def champion_exists(name: str) -> bool:
    """Verifica si un campeón ya está en la DB"""
    
def save_champion(name: str, title: str) -> int:
    """Guarda un campeón y retorna su ID"""
    
def update_scraping_status(champion_id: int, success: bool) -> None:
    """Actualiza el estado del scraping (para tracking de anti-bot)"""
    
def save_voice_line(champion_id: int, text_en: str, audio_url: str, is_filtered: bool = False, filter_reason: str = None) -> int:
    """Guarda una voice line con estado de filtrado"""
    
def update_translation(voice_line_id: int, text_es: str) -> None:
    """Actualiza la traducción de una voice line"""
    
def get_champion_data(champion_name: str, include_filtered: bool = False) -> Dict:
    """Obtiene todos los datos de un campeón desde la DB"""
```

### 3. `src/scraper.py`
```python
def scrape_champion_audio(champion_name: str, retry_count: int = 3) -> Tuple[List[Dict], bool]:
    """
    Scrapea la wiki de LoL para obtener audios y textos con manejo de anti-bot
    Returns: ([{"text": str, "audio_url": str}, ...], success: bool)
    """
    
def extract_audio_data(soup: BeautifulSoup) -> List[Dict]:
    """Extrae datos de audio del HTML parseado"""
    
def is_blocked_by_antibot(response: requests.Response) -> bool:
    """Detecta si la página fue bloqueada por protección anti-bot"""
    
def get_with_retry(url: str, max_retries: int = 3, delay: int = 2) -> requests.Response:
    """Realiza petición con reintentos y delay entre intentos"""
```

### 4. `src/text_filter.py` ✅ NUEVO
```python
def is_monosyllabic(text: str) -> bool:
    """Detecta si es una frase monosilábica sin sentido"""
    
def is_technical_note(text: str) -> bool:
    """Detecta si es una nota técnica (cooldown, sound effect, etc.)"""
    
def should_filter(text: str) -> Tuple[bool, str]:
    """
    Determina si una frase debe ser filtrada
    Returns: (should_filter: bool, reason: str)
    """
    
def clean_text(text: str) -> str:
    """Limpia el texto eliminando comillas extra y formateando"""
```

### 5. `src/translator.py`
```python
def translate_text(text: str, target_lang: str = 'es') -> str:
    """Traduce texto usando GoogleTranslator"""
    
def translate_batch(texts: List[str], target_lang: str = 'es') -> List[str]:
    """Traduce múltiples textos en batch"""
```

### 6. `src/csv_generator.py`
```python
def generate_anki_csv(champion_name: str, output_dir: str = "output") -> str:
    """
    Genera CSV para Anki desde la base de datos
    Formato: audio,text_en,text_es
    Returns: ruta del archivo CSV generado
    """
```

### 7. `config.py`
```python
# Configuración global
DATABASE_PATH = "data/champions.db"
AUDIO_DIR = "data/audios"
OUTPUT_DIR = "output"
WIKI_BASE_URL = "https://leagueoflegends.fandom.com/wiki"
DATA_DRAGON_URL = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json"
```

### 8. `main.py` - CLI Principal
```python
def main():
    """
    CLI interactiva con las siguientes opciones:
    1. Seleccionar campeón (búsqueda interactiva)
    2. Scrapear datos (si no están en DB)
    3. Descargar audios
    4. Traducir textos
    5. Generar CSV para Anki
    6. Ver estadísticas de la DB
    7. Salir
    """
```

---

## 🎨 Interfaz CLI (usando `rich`)

```
╔══════════════════════════════════════════════════════════╗
║         LoL Audio Scraper - Anki Card Generator          ║
╚══════════════════════════════════════════════════════════╝

Selecciona un campeón:
> Illaoi

[1/5] Verificando caché...        ✓ No encontrado en DB
[2/5] Scrapeando wiki...          ✓ 47 voice lines encontradas
[3/5] Descargando audios...       ━━━━━━━━━━━━━━━━ 100% 47/47
[4/5] Traduciendo textos...       ━━━━━━━━━━━━━━━━ 100% 47/47
[5/5] Generando CSV...            ✓ output/Illaoi.csv

✨ Completado! CSV listo para importar en Anki
📁 Archivo: /home/user/Get_cards/output/Illaoi.csv
```

---

## 📄 Formato CSV para Anki

```csv
audio,text_en,text_es
[sound:Illaoi_1.ogg],"i will build a vessel worthy of my god","construiré un recipiente digno de mi dios"
[sound:Illaoi_2.ogg],"motion is the soul's breath","el movimiento es el aliento del alma"
```

**Notas:**
- Columna `audio`: Formato Anki `[sound:filename.ogg]`
- Columna `text_en`: Texto en inglés (lowercase)
- Columna `text_es`: Traducción al español

---

## 🔧 Dependencias (`requirements.txt`)

```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
deep-translator>=1.11.0
rich>=13.7.0
click>=8.1.0
```

---

## 🚀 Flujo de Ejecución

### Modo Desarrollo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar programa
python main.py
```

### Compilación con Nuitka (Windows)
```bash
# Ejecutar script de compilación
python build.py
```

**`build.py`:**
```python
import subprocess
import sys

def build_exe():
    """Compila el proyecto con Nuitka"""
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=anti-bloat",
        "--include-data-dir=src=src",
        "--output-dir=dist",
        "--output-filename=lol-audio-scraper.exe",
        "main.py"
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    build_exe()
```

---

## 🎯 Casos de Uso

### Caso 1: Primera vez con un campeón
```
Usuario selecciona "Ahri"
→ No existe en DB
→ Scrapea wiki
→ Guarda en DB
→ Descarga audios
→ Traduce textos
→ Genera CSV
```

### Caso 2: Campeón ya procesado
```
Usuario selecciona "Ahri" (segunda vez)
→ Existe en DB
→ Pregunta: "¿Regenerar CSV? (s/n)"
→ Si sí: genera CSV desde DB (instantáneo)
→ Si no: sale
```

### Caso 3: Actualizar campeón
```
Usuario selecciona "Ahri"
→ Existe en DB
→ Opción: "¿Re-scrapear? (s/n)"
→ Si sí: elimina datos viejos y re-scrapea
```

---

## ✅ Checklist de Implementación

### Fase 1: Estructura Base
- [ ] Crear estructura de directorios
- [ ] Crear `config.py`
- [ ] Crear `requirements.txt`
- [ ] Inicializar módulos en `src/`

### Fase 2: Base de Datos
- [ ] Implementar `database.py`
- [ ] Crear esquema SQLite
- [ ] Funciones CRUD básicas

### Fase 3: Módulos Core
- [ ] Implementar `champion_list.py`
- [ ] Implementar `scraper.py`
- [ ] Implementar `downloader.py`
- [ ] Implementar `translator.py`

### Fase 4: Generación CSV
- [ ] Implementar `csv_generator.py`
- [ ] Validar formato Anki

### Fase 5: CLI
- [ ] Implementar `main.py`
- [ ] Menú interactivo con `rich`
- [ ] Manejo de errores

### Fase 6: Build
- [ ] Crear `build.py`
- [ ] Probar compilación Nuitka
- [ ] Documentar en README

### Fase 7: Testing
- [ ] Probar flujo completo
- [ ] Validar CSV en Anki
- [ ] Probar .exe en Windows

---

## 🎓 Notas Técnicas

### Caché Inteligente
- Si un campeón ya está en DB, no re-scrapea
- Opción manual para forzar actualización
- Timestamp de última actualización

### Manejo de Errores
- Retry automático en descargas (3 intentos)
- Logging de errores en `logs/error.log`
- Validación de URLs antes de descargar

### Optimizaciones
- Descargas paralelas (ThreadPoolExecutor, max 5 workers)
- Traducción en batch (reduce llamadas API)
- Progreso visual con `rich.progress`

---

## 📚 Recursos

- [Data Dragon API](https://developer.riotgames.com/docs/lol#data-dragon)
- [Nuitka Documentation](https://nuitka.net/doc/user-manual.html)
- [Anki CSV Import](https://docs.ankiweb.net/importing.html)
- [Rich Library](https://rich.readthedocs.io/)
