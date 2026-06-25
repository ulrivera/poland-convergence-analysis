import requests
import json
import os
from datetime import datetime

# ========== CONFIGURACIÓN DE RUTAS ==========
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "nbp_data")
os.makedirs(DATA_DIR, exist_ok=True)

BASE_URL = "https://api.nbp.pl/api"


def get_rates(table, currency, period=None, start=None, end=None):
    """
    Descarga tipos de cambio del NBP.
    
    Args:
        table: "A", "B" o "C"
        currency: Código ISO 4217 (EUR, USD, GBP...)
        period: "current", "today", o número (últimos N días)
        start, end: Fechas YYYY-MM-DD (máx 93 días de diferencia)
    
    Returns:
        dict con los datos
    """
    
    # Construir URL
    if period == "current":
        url = f"{BASE_URL}/exchangerates/rates/{table}/{currency}/?format=json"
        suffix = "current"
    elif period == "today":
        url = f"{BASE_URL}/exchangerates/rates/{table}/{currency}/today/?format=json"
        suffix = "today"
    elif isinstance(period, int):
        url = f"{BASE_URL}/exchangerates/rates/{table}/{currency}/last/{period}/?format=json"
        suffix = f"last_{period}"
    elif start and end:
        d_start = datetime.strptime(start, "%Y-%m-%d")
        d_end = datetime.strptime(end, "%Y-%m-%d")
        days = (d_end - d_start).days + 1
        if days > 93:
            raise ValueError(f"Rango de {days} días excede el límite de 93. Usa period=int en su lugar.")
        
        url = f"{BASE_URL}/exchangerates/rates/{table}/{currency}/{start}/{end}/?format=json"
        suffix = f"{start}_to_{end}"
    else:
        raise ValueError("Especifica period o start+end")
    
    print(f"🌐 {currency} (tabla {table}) - {suffix}")
    
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    # Guardar
    filepath = os.path.join(DATA_DIR, f"{currency}_{table}_{suffix}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 {filepath} | {len(data['rates'])} registros")
    return data


def get_gold(period=None, start=None, end=None):
    """Descarga precios del oro. Misma lógica de parámetros."""
    
    if period == "current":
        url = f"{BASE_URL}/cenyzlota/?format=json"
        suffix = "current"
    elif period == "today":
        url = f"{BASE_URL}/cenyzlota/today/?format=json"
        suffix = "today"
    elif isinstance(period, int):
        url = f"{BASE_URL}/cenyzlota/last/{period}/?format=json"
        suffix = f"last_{period}"
    elif start and end:
        d_start = datetime.strptime(start, "%Y-%m-%d")
        d_end = datetime.strptime(end, "%Y-%m-%d")
        days = (d_end - d_start).days + 1
        if days > 93:
            raise ValueError(f"Rango de {days} días excede el límite de 93.")
        
        url = f"{BASE_URL}/cenyzlota/{start}/{end}/?format=json"
        suffix = f"{start}_to_{end}"
    else:
        raise ValueError("Especifica period o start+end")
    
    print(f"🌐 Oro - {suffix}")
    
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    filepath = os.path.join(DATA_DIR, f"gold_{suffix}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 {filepath} | {len(data)} registros")
    return data


# ========== EJEMPLOS ==========
if __name__ == "__main__":
    
    # Ejemplos:
    # get_rates("A", "EUR", period="current")
    # get_rates("A", "EUR", period=30)
    # get_rates("A", "EUR", start="2026-04-01", end="2026-06-23")
    # get_gold(period=10)
    
    print("Ejecutando demos...")
    get_rates("A", "EUR", period=10)
    get_gold(period=5)