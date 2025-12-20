

def filter_quotes(data, priority_skin="Original"):
    """
    Filtra lista eliminando:
    - Textos de una sola palabra
    - Duplicados (priorizando el skin especificado)
    """
    # Eliminar textos de una palabra
    filtered = [item for item in data if len(item["Text"].split()) > 1]
    
    # Ordenar priorizando el skin deseado
    sorted_data = sorted(filtered, key=lambda x: (0 if x["Skin"] == priority_skin else 1))
    
    # Eliminar duplicados
    seen = {}
    for item in sorted_data:
        if item["Text"] not in seen:
            seen[item["Text"]] = item
    
    return list(seen.values())