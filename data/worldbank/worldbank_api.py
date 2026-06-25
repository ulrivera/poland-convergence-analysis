import requests
import json
import os

OUTPUT_DIR = "worldbank_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "https://api.worldbank.org/v2"


def get_indicator_data(indicator, countries="PL", date_range=None, per_page=1000):
    """
    Descarga datos de un indicador del Banco Mundial.
    
    Args:
        indicator: Código del indicador (ej: "NY.GDP.MKTP.CD")
        countries: Código ISO2 del país o países separados por ;
                   (ej: "PL", "PL;DE;ES", "all" para todos)
        date_range: Rango de años (ej: "2010:2020") o None para todos
        per_page: Registros por página (máx recomendado: 1000)
    
    Returns:
        Lista de diccionarios con los datos
    """
    
    # Construir URL
    url = f"{BASE_URL}/country/{countries}/indicator/{indicator}"
    params = {
        "format": "json",
        "per_page": per_page,
        "page": 1
    }
    if date_range:
        params["date"] = date_range
    
    print(f"🌐 Indicador: {indicator}")
    print(f"   Países: {countries}")
    if date_range:
        print(f"   Años: {date_range}")
    
    all_records = []
    
    # Paginación automática
    while True:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # La respuesta siempre es [metadata, lista_de_registros]
        if not isinstance(data, list) or len(data) < 2:
            print("❌ Respuesta inesperada")
            return []
        
        metadata = data[0]
        records = data[1]
        
        all_records.extend(records)
        
        current_page = metadata["page"]
        total_pages = metadata["pages"]
        
        print(f"   Página {current_page}/{total_pages} | Registros: {len(records)}")
        
        if current_page >= total_pages:
            break
        
        params["page"] = current_page + 1
    
    # Filtrar valores None (datos no disponibles)
    valid_records = [r for r in all_records if r["value"] is not None]
    null_count = len(all_records) - len(valid_records)
    
    print(f"✅ Total descargado: {len(all_records)}")
    if null_count > 0:
        print(f"   ⚠️  Valores nulos (sin dato): {null_count}")
    print(f"   ✅ Válidos: {len(valid_records)}")
    
    return valid_records


def save_data(records, filename=None, indicator=None):
    """
    Guarda los datos en JSON y opcionalmente muestra resumen.
    """
    if not filename and indicator:
        filename = f"{OUTPUT_DIR}/{indicator.replace('.', '_')}.json"
    elif not filename:
        filename = f"{OUTPUT_DIR}/worldbank_data.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Guardado: {filename}")
    return filename


def show_summary(records, max_rows=10):
    """Muestra resumen de los datos descargados."""
    if not records:
        print("Sin datos para mostrar.")
        return
    
    print(f"\n{'='*60}")
    print("RESUMEN DE DATOS")
    print(f"{'='*60}")
    
    # Agrupar por país
    by_country = {}
    for r in records:
        country = r["country"]["value"]
        if country not in by_country:
            by_country[country] = []
        by_country[country].append(r)
    
    for country, country_records in by_country.items():
        print(f"\n📍 {country}")
        print(f"   Registros: {len(country_records)}")
        print(f"   Años: {country_records[-1]['date']} a {country_records[0]['date']}")
        print(f"   Últimos {max_rows} valores:")
        for r in country_records[:max_rows]:
            print(f"      {r['date']}: {r['value']:,.2f}")


# ========== EJEMPLOS DE USO ==========
if __name__ == "__main__":
    import sys
    
    # Ejemplo 1: PIB de Polonia (todos los años disponibles)
    # records = get_indicator_data("NY.GDP.MKTP.CD", countries="PL")
    # save_data(records, indicator="NY.GDP.MKTP.CD_PL")
    # show_summary(records)
    
    # Ejemplo 2: PIB per cápita de Polonia (2010-2023)
    # records = get_indicator_data("NY.GDP.PCAP.CD", countries="PL", date_range="2010:2023")
    # save_data(records, indicator="NY.GDP.PCAP.CD_PL_2010_2023")
    # show_summary(records)
    
    # Ejemplo 3: Comparar PIB de Polonia, Alemania y España (2023)
    # records = get_indicator_data("NY.GDP.MKTP.CD", countries="PL;DE;ES", date_range="2023")
    # save_data(records, indicator="NY.GDP.MKTP.CD_PL_DE_ES_2023")
    # show_summary(records)
    
    # Ejemplo 4: Inflación de Polonia
    # records = get_indicator_data("FP.CPI.TOTL.ZG", countries="PL", date_range="2015:2023")
    # save_data(records, indicator="inflation_PL")
    # show_summary(records)
    
    # Uso por argumentos
    if len(sys.argv) >= 2:
        indicator = sys.argv[1]
        country = sys.argv[2] if len(sys.argv) > 2 else "PL"
        date_range = sys.argv[3] if len(sys.argv) > 3 else None
        
        records = get_indicator_data(indicator, countries=country, date_range=date_range)
        save_data(records, indicator=f"{indicator}_{country}")
        show_summary(records)
    else:
        # Demo por defecto
        print("Uso: python worldbank_api.py <indicador> [país] [año_inicio:año_fin]")
        print("Ejemplo: python worldbank_api.py NY.GDP.MKTP.CD PL 2010:2023")
        print("\nEjecutando demo: PIB de Polonia (últimos 10 años)...")
        records = get_indicator_data("NY.GDP.MKTP.CD", countries="PL", date_range="2014:2023")
        save_data(records, indicator="NY.GDP.MKTP.CD_PL_2014_2023")
        show_summary(records)