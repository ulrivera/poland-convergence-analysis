# 5. data/eurostat/eurostat_convergencia_sqlite.py - Refactorizado
# Eurostat Convergencia Real - Extracción a SQLite
# =================================================

# Script maestro para descargar datos de PIB per cápita PPS de Eurostat
# y almacenarlos en SQLite sin duplicados.

# Uso:
#     python eurostat_convergencia_sqlite.py
    
#     # Con grupos personalizados:
#     python eurostat_convergencia_sqlite.py --paises PL CZ HU SK --años 2004 2023


import sys
import os
import argparse

# Añadir src/ al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from config import ( UE14, V4, EUROSTAT_DATASET, EUROSTAT_NA_ITEM, EUROSTAT_UNIT, EUROSTAT_DB, AÑO_INICIO_DEFAULT, AÑO_FIN_DEFAULT)
from db_utils import inicializar_db, get_connection

import requests
import json
from datetime import datetime


def descargar_pais_año(pais, año, dataset, na_item, unit):
    """Descarga un dato de Eurostat."""
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}"
    
    params = {
        "format": "JSON",
        "lang": "EN",
        "geo": pais,
        "time": str(año),
        "na_item": na_item,
        "unit": unit
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        valores = data.get("value", {})
        if valores:
            return {
                "pais": pais,
                "año": año,
                "valor": list(valores.values())[0],
                "status": "ok",
                "descargado": datetime.now().isoformat()
            }
        return {
            "pais": pais, "año": año, "valor": None,
            "status": "sin_datos", "descargado": datetime.now().isoformat()
        }
        
    except requests.exceptions.HTTPError:
        return {
            "pais": pais, "año": año, "valor": None,
            "status": "no_disponible", "descargado": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "pais": pais, "año": año, "valor": None,
            "status": f"error: {e}", "descargado": datetime.now().isoformat()
        }


def obtener_faltantes(db_path, paises, años, dataset, na_item, unit):
    """Identifica combinaciones país-año que faltan en la BD."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    placeholders_paises = ",".join(["?"] * len(paises))
    placeholders_años = ",".join(["?"] * len(años))
    
    query = f"""
        SELECT pais, año FROM convergencia
        WHERE pais IN ({placeholders_paises})
          AND año IN ({placeholders_años})
          AND dataset = ?
          AND na_item = ?
          AND unit = ?
    """
    
    params = paises + años + [dataset, na_item, unit]
    cursor.execute(query, params)
    existentes = set(cursor.fetchall())
    conn.close()
    
    faltantes = []
    for pais in paises:
        for año in años:
            if (pais, año) not in existentes:
                faltantes.append((pais, año))
    
    return faltantes


def guardar_registros(db_path, registros, dataset, na_item, unit):
    """Inserta registros nuevos en la BD."""
    if not registros:
        return 0
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    fecha = datetime.now().isoformat()
    insertados = 0
    
    for r in registros:
        if r.get("status") == "ok" and r.get("valor") is not None:
            try:
                cursor.execute("""
                    INSERT INTO convergencia (pais, año, valor, dataset, na_item, unit, fecha_descarga)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (r["pais"], r["año"], r["valor"], dataset, na_item, unit, fecha))
                insertados += 1
            except Exception:
                pass  # Duplicado u otro error
    
    conn.commit()
    conn.close()
    return insertados


def main():
    parser = argparse.ArgumentParser(description="Descarga datos de convergencia de Eurostat")
    parser.add_argument("--paises", nargs="+", default=UE14 + V4,
                        help="Lista de códigos de país (default: UE14 + V4)")
    parser.add_argument("--años", nargs=2, type=int, metavar=("INICIO", "FIN"),
                        default=[AÑO_INICIO_DEFAULT, AÑO_FIN_DEFAULT],
                        help="Rango de años (default: 2004 2023)")
    parser.add_argument("--db", default=EUROSTAT_DB,
                        help="Ruta a la base de datos SQLite")
    
    args = parser.parse_args()
    
    paises = args.paises
    años = list(range(args.años[0], args.años[1] + 1))
    db_path = args.db
    
    print("=" * 60)
    print("Eurostat Convergencia Real - Descarga incremental")
    print("=" * 60)
    
    # Inicializar BD
    inicializar_db(db_path)
    
    # Ver qué falta
    faltantes = obtener_faltantes(db_path, paises, años, EUROSTAT_DATASET, EUROSTAT_NA_ITEM, EUROSTAT_UNIT)
    
    print(f"\\nPaíses: {len(paises)} | Años: {años[0]}-{años[-1]}")
    print(f"Total combinaciones: {len(paises) * len(años)}")
    print(f"Ya en BD: {len(paises) * len(años) - len(faltantes)}")
    print(f"Faltantes: {len(faltantes)}")
    
    if not faltantes:
        print("\\n✅ Todos los datos ya están descargados")
        return
    
    # Descargar
    print(f"\\n🌐 Descargando {len(faltantes)} registros...")
    registros = []
    for i, (pais, año) in enumerate(faltantes):
        if (i + 1) % 10 == 0 or i == len(faltantes) - 1:
            print(f"   [{i+1}/{len(faltantes)}] {pais} {año}")
        registros.append(descargar_pais_año(pais, año, EUROSTAT_DATASET, EUROSTAT_NA_ITEM, EUROSTAT_UNIT))
    
    # Guardar
    insertados = guardar_registros(db_path, registros, EUROSTAT_DATASET, EUROSTAT_NA_ITEM, EUROSTAT_UNIT)
    print(f"\\n✅ Insertados: {insertados} registros nuevos")


if __name__ == "__main__":
    main()
