# Resumen de Investigación y Próximos Pasos

## 🔍 Hallazgos Clave

### 1. Protección Anti-Bot de Fandom Wiki
**Problema:** ~66% de las peticiones son bloqueadas por "Client Challenge"

**Evidencia:**
- ✅ Yasuo: 1075 audios exitosos
- ✅ Jinx: 471 audios exitosos  
- ❌ Illaoi, Ezreal, Ahri, Lux: Bloqueados (3KB vs 700-1400KB)

**Solución Propuesta:**
1. Implementar User-Agent rotación
2. Agregar delays entre peticiones (2-5 segundos)
3. Sistema de reintentos con backoff exponencial
4. Tracking de intentos fallidos en DB

---

### 2. Frases a Filtrar

#### Categorías Detectadas:

**A. Efectos de Sonido (NO son diálogos)**
- "Sound Effect"
- Ejemplo: Tags `<audio>` sin transcripción útil

**B. Notas Técnicas**
- "15 seconds cooldown"
- "A stripped-down version of..."
- "These lines aren't guaranteed to play..."

**C. Monosílabos sin Sentido**
- "Hm", "Ah", "Ugh", "Mm"
- Criterio: ≤3 caracteres Y 1 palabra

**D. Descripciones de Música**
- "plays" en el texto
- Referencias a canciones

#### Filtros Implementar:
```python
FILTER_PATTERNS = [
    r"Sound Effect",
    r"\d+ seconds? cooldown",
    r"A .* version of .* plays",
    r"aren't guaranteed to play",
    r"^[A-Za-z]{1,3}[!?.]?$",  # Monosílabos
]
```

---

### 3. Formato de URLs de Audio

**Patrón Detectado:**
```
https://static.wikia.nocookie.net/leagueoflegends/images/{hash}/{filename}.ogg/revision/latest?cb={timestamp}
```

**Ejemplo:**
```
https://static.wikia.nocookie.net/leagueoflegends/images/0/0b/Yasuo_Select.ogg/revision/latest?cb=20200709161222
```

**Conclusión:** URLs directas, no requieren descarga previa para Anki

---

## 📊 Estadísticas de Prueba

| Campeón | Status | Audios | Transcripciones | Tamaño |
|---------|--------|--------|-----------------|--------|
| Yasuo   | ✅     | 1075   | 745             | 1455 KB |
| Jinx    | ✅     | 471    | 393             | 706 KB  |
| Illaoi  | ❌     | 0      | 0               | 3 KB    |
| Ezreal  | ❌     | 0      | 0               | 3 KB    |
| Ahri    | ❌     | 0      | 0               | 3 KB    |
| Lux     | ❌     | 0      | 0               | 3 KB    |

**Tasa de Éxito:** 33% (2/6)

---

## 🎯 Próximos Pasos

### Fase 1: Scraper Robusto ✅ PRIORITARIO
1. [ ] Crear `src/scraper.py` con:
   - Detección de anti-bot
   - Sistema de reintentos
   - User-Agent rotation
   - Delays configurables

2. [ ] Crear `src/text_filter.py` con:
   - Filtros de monosílabos
   - Filtros de notas técnicas
   - Limpieza de texto

### Fase 2: Base de Datos
3. [ ] Crear `src/database.py`
   - Esquema actualizado (sin descarga)
   - Tracking de intentos de scraping
   - Estado de filtrado

### Fase 3: Procesamiento
4. [ ] Crear `src/translator.py`
   - Traducción en batch
   - Manejo de errores

5. [ ] Crear `src/csv_generator.py`
   - Formato Anki correcto
   - Exclusión de frases filtradas

### Fase 4: CLI
6. [ ] Crear `main.py`
   - Menú interactivo
   - Selección de campeón
   - Progreso visual

### Fase 5: Testing
7. [ ] Probar con 10+ campeones
8. [ ] Validar CSV en Anki
9. [ ] Ajustar filtros según resultados

---

## 🔧 Configuración Recomendada

### `config.py`
```python
# Anti-bot handling
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    # ... más user agents
]

REQUEST_DELAY_MIN = 2  # segundos
REQUEST_DELAY_MAX = 5  # segundos
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # multiplicador

# Filtros
MIN_TEXT_LENGTH = 4  # caracteres
MAX_MONOSYLLABLE_LENGTH = 3
FILTER_PATTERNS = [...]

# Paths
DATABASE_PATH = "data/champions.db"
OUTPUT_DIR = "output"
```

---

## ⚠️ Consideraciones Importantes

### 1. Tasa de Bloqueo Alta
- **Problema:** 66% de bloqueo es muy alto
- **Opciones:**
  - A. Implementar delays más largos (5-10s)
  - B. Usar proxies rotativos (costo adicional)
  - C. Scraping manual asistido (fallback)

### 2. No Descargar Audios
- **Ventaja:** Más rápido, menos espacio
- **Desventaja:** Dependencia de URLs de Fandom
- **Riesgo:** URLs pueden cambiar/expirar
- **Mitigación:** Guardar URLs en DB para re-scraping

### 3. Formato CSV para Anki
```csv
audio,text_en,text_es
[sound:https://static.wikia.nocookie.net/.../Yasuo_Select.ogg],"death is like the wind","la muerte es como el viento"
```

**Nota:** Anki soporta URLs directas en el campo `[sound:]`

---

## 📝 Decisiones Pendientes

1. **¿Implementar sistema de proxies?**
   - Costo: ~$10-20/mes
   - Beneficio: Tasa de éxito 90%+

2. **¿Scraping paralelo o secuencial?**
   - Paralelo: Más rápido, mayor riesgo de bloqueo
   - Secuencial: Más lento, menor riesgo

3. **¿Incluir skins alternativas?**
   - Algunos campeones tienen voicelines de skins
   - Ejemplo: Yasuo tiene ~1075 audios (incluye skins)

---

## ✅ Recomendación Final

**Enfoque Híbrido:**
1. Scraping secuencial con delays (2-5s)
2. Sistema de reintentos inteligente
3. Fallback manual para campeones bloqueados
4. Caché agresivo en SQLite
5. Filtrado estricto de frases

**Tiempo Estimado:**
- Scraping 1 campeón exitoso: ~30-60 segundos
- Scraping 160 campeones: ~2-3 horas (con bloqueos)
- Desarrollo completo: ~2-3 días

---

## 🚀 ¿Comenzamos la Implementación?

Siguiente paso sugerido:
1. Crear `src/scraper.py` con anti-bot handling
2. Crear `src/text_filter.py` con filtros
3. Probar con 5 campeones más

¿Procedemos? 🎯
