#!/usr/bin/env python3
"""
Script de prueba para explorar el formato de las páginas de audio de campeones
y determinar patrones de scraping
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import json

# Lista de campeones para probar
TEST_CHAMPIONS = [
    "Illaoi",
    "Ezreal", 
    "Ahri",
    "Yasuo",
    "Lux",
    "Jinx"
]

def test_champion_page(champion_name: str) -> Dict:
    """Prueba scrapear una página de campeón y analiza su estructura"""
    url = f'https://leagueoflegends.fandom.com/wiki/{champion_name}/LoL/Audio'
    
    print(f"\n{'='*60}")
    print(f"Probando: {champion_name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        # Headers para evitar bloqueos
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        result = requests.get(url, headers=headers, timeout=10)
        result.raise_for_status()
        
        soup = BeautifulSoup(result.text, 'lxml')
        
        # Buscar diferentes patrones de etiquetas
        audio_tags = soup.find_all('audio')
        i_tags = soup.find_all('i')
        b_tags = soup.find_all('b')
        
        # Buscar URLs de audio
        audio_urls = []
        for tag in soup.find_all(['audio', 'source']):
            src = tag.get('src')
            if src and '.ogg' in src:
                audio_urls.append(src)
        
        # Buscar textos en itálica (probablemente transcripciones)
        transcriptions = []
        for tag in i_tags:
            text = tag.get_text(strip=True)
            if text and len(text) > 1:  # Filtrar monosílabos
                transcriptions.append(text)
        
        # Estadísticas
        stats = {
            'champion': champion_name,
            'status_code': result.status_code,
            'audio_tags': len(audio_tags),
            'i_tags': len(i_tags),
            'b_tags': len(b_tags),
            'audio_urls_found': len(audio_urls),
            'transcriptions_found': len(transcriptions),
            'sample_audio_urls': audio_urls[:3] if audio_urls else [],
            'sample_transcriptions': transcriptions[:5] if transcriptions else [],
            'page_size_kb': len(result.content) / 1024
        }
        
        print(f"✓ Status: {stats['status_code']}")
        print(f"✓ Tamaño página: {stats['page_size_kb']:.2f} KB")
        print(f"✓ Tags <audio>: {stats['audio_tags']}")
        print(f"✓ Tags <i>: {stats['i_tags']}")
        print(f"✓ Tags <b>: {stats['b_tags']}")
        print(f"✓ URLs de audio encontradas: {stats['audio_urls_found']}")
        print(f"✓ Transcripciones encontradas: {stats['transcriptions_found']}")
        
        if stats['sample_audio_urls']:
            print(f"\n📁 Muestra de URLs:")
            for url in stats['sample_audio_urls']:
                print(f"   - {url[:80]}...")
        
        if stats['sample_transcriptions']:
            print(f"\n📝 Muestra de transcripciones:")
            for text in stats['sample_transcriptions']:
                print(f"   - \"{text}\"")
        
        # Detectar frases monosilábicas o sin sentido
        monosyllabic = [t for t in transcriptions if len(t.split()) == 1 and len(t) <= 3]
        if monosyllabic:
            print(f"\n⚠️  Frases monosilábicas detectadas ({len(monosyllabic)}):")
            for text in monosyllabic[:10]:
                print(f"   - \"{text}\"")
        
        return stats
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return {'champion': champion_name, 'error': str(e)}
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return {'champion': champion_name, 'error': str(e)}


def analyze_pattern_consistency(all_stats: List[Dict]):
    """Analiza si el formato es consistente entre campeones"""
    print(f"\n\n{'='*60}")
    print("ANÁLISIS DE CONSISTENCIA")
    print(f"{'='*60}\n")
    
    successful = [s for s in all_stats if 'error' not in s]
    failed = [s for s in all_stats if 'error' in s]
    
    print(f"✓ Exitosos: {len(successful)}/{len(all_stats)}")
    print(f"❌ Fallidos: {len(failed)}/{len(all_stats)}")
    
    if successful:
        avg_audio_tags = sum(s['audio_tags'] for s in successful) / len(successful)
        avg_transcriptions = sum(s['transcriptions_found'] for s in successful) / len(successful)
        
        print(f"\n📊 Promedios:")
        print(f"   - Tags <audio>: {avg_audio_tags:.1f}")
        print(f"   - Transcripciones: {avg_transcriptions:.1f}")
        
        # Verificar consistencia
        has_audio = all(s['audio_tags'] > 0 for s in successful)
        has_transcriptions = all(s['transcriptions_found'] > 0 for s in successful)
        
        print(f"\n✓ Formato consistente:")
        print(f"   - Todos tienen <audio>: {'SÍ' if has_audio else 'NO'}")
        print(f"   - Todos tienen transcripciones: {'SÍ' if has_transcriptions else 'NO'}")
    
    if failed:
        print(f"\n⚠️  Campeones fallidos:")
        for s in failed:
            print(f"   - {s['champion']}: {s.get('error', 'Unknown')}")


def main():
    """Función principal"""
    print("="*60)
    print("EXPLORADOR DE PÁGINAS DE AUDIO - LEAGUE OF LEGENDS")
    print("="*60)
    print(f"\nProbando {len(TEST_CHAMPIONS)} campeones...\n")
    
    all_stats = []
    
    for champion in TEST_CHAMPIONS:
        stats = test_champion_page(champion)
        all_stats.append(stats)
    
    # Análisis final
    analyze_pattern_consistency(all_stats)
    
    # Guardar resultados
    output_file = 'scraping_test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n✓ Resultados guardados en: {output_file}")
    
    print("\n" + "="*60)
    print("RECOMENDACIONES:")
    print("="*60)
    print("""
1. Revisar los resultados en scraping_test_results.json
2. Identificar patrones comunes en las transcripciones
3. Definir filtros para frases monosilábicas
4. Verificar si hay API de Fandom disponible
    """)


if __name__ == "__main__":
    main()
