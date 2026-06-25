
# 6. data/nbp/nbp_download.py - Refactorizado
# NBP (Banco Nacional de Polonia) - Descarga de tipos de cambio y oro
# =====================================================================

# Uso:
#     python nbp_download.py --currency EUR --table A --period 30
#     python nbp_download.py --gold --period 10

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from config import NBP_DATA_DIR

import requests
import json
from datetime import datetime

BASE_URL = "https://api.nbp.pl/api"


def get_rates(table, currency, period=None, start=None, end=None, today=False):
    """Descarga tipos de cambio del NBP."""
    base = f"{BASE_URL}/exchangerates/rates/{table}/{currency}"
    
    if today:
        url = f"{base}/today/?format=json"
        suffix = "today"
    elif period:
        url = f"{base}/last/{period}/?format=json"
        suffix = f"last_{period}"
    elif start and end:
        url = f"{base}/{start}/{end}/?format=json"
        suffix = f"{start}_to_{end}"
    elif start:
        url = f"{base}/{start}/?format=json"
        suffix = start
    else:
        url = f"{base}/?format=json"
        suffix = "current"
    
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    filepath = os.path.join(NBP_DATA_DIR, f"{currency}_{table}_{suffix}.json")
    os.makedirs(NBP_DATA_DIR, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 {filepath} | {len(data['rates'])} registros")
    return data


def get_gold(period=None, start=None, end=None, today=False):
    """Descarga precios del oro del NBP."""
    base = f"{BASE_URL}/cenyzlota"
    
    if today:
        url = f"{base}/today/?format=json"
        suffix = "today"
    elif period:
        url = f"{base}/last/{period}/?format=json"
        suffix = f"last_{period}"
    elif start and end:
        url = f"{base}/{start}/{end}/?format=json"
        suffix = f"{start}_to_{end}"
    elif start:
        url = f"{base}/{start}/?format=json"
        suffix = start
    else:
        url = f"{base}/?format=json"
        suffix = "current"
    
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    filepath = os.path.join(NBP_DATA_DIR, f"gold_{suffix}.json")
    os.makedirs(NBP_DATA_DIR, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 {filepath} | {len(data)} registros")
    return data


def main():
    parser = argparse.ArgumentParser(description="Descarga datos del NBP")
    parser.add_argument("--currency", default="EUR", help="Código de moneda (default: EUR)")
    parser.add_argument("--table", default="A", choices=["A", "B", "C"], help="Tabla NBP")
    parser.add_argument("--period", type=int, help="Últimos N registros")
    parser.add_argument("--start", help="Fecha inicio YYYY-MM-DD")
    parser.add_argument("--end", help="Fecha fin YYYY-MM-DD")
    parser.add_argument("--today", action="store_true", help="Solo datos de hoy")
    parser.add_argument("--gold", action="store_true", help="Descargar oro en vez de moneda")
    
    args = parser.parse_args()
    
    if args.gold:
        get_gold(period=args.period, start=args.start, end=args.end, today=args.today)
    else:
        get_rates(args.table, args.currency, period=args.period, 
                  start=args.start, end=args.end, today=args.today)


if __name__ == "__main__":
    main()
