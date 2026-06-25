#Utilidades para interactuar con la base de datos SQLite de Eurostat.

import sqlite3
import pandas as pd
import os
from config import EUROSTAT_DB


def get_connection(db_path=None):
    """Retorna conexión a la base de datos.
    
    Args:
        db_path: Ruta alternativa a la BD. Si es None, usa la default.
    """
    path = db_path or EUROSTAT_DB
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return sqlite3.connect(path)


def inicializar_db(db_path=None):
    """Crea las tablas si no existen.
    
    Args:
        db_path: Ruta alternativa a la BD.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS convergencia (
            pais TEXT NOT NULL,
            año INTEGER NOT NULL,
            valor REAL,
            dataset TEXT,
            na_item TEXT,
            unit TEXT,
            fecha_descarga TEXT,
            PRIMARY KEY (pais, año, dataset, na_item, unit)
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_pais_año 
        ON convergencia(pais, año)
    """)
    
    conn.commit()
    conn.close()


def load_convergencia_data(paises=None, años=None, db_path=None):
    """Carga datos de convergencia desde SQLite.
    
    Args:
        paises: Lista de códigos de país (None = todos)
        años: Lista de años (None = todos)
        db_path: Ruta alternativa a la BD
    
    Returns:
        DataFrame con columnas [pais, año, valor]
    """
    conn = get_connection(db_path)
    
    query = "SELECT pais, año, valor FROM convergencia WHERE 1=1"
    params = []
    
    if paises:
        placeholders = ",".join(["?"] * len(paises))
        query += f" AND pais IN ({placeholders})"
        params.extend(paises)
    
    if años:
        placeholders = ",".join(["?"] * len(años))
        query += f" AND año IN ({placeholders})"
        params.extend(años)
    
    query += " ORDER BY pais, año"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    return df


def get_available_paises(db_path=None):
    """Retorna lista de países disponibles en la BD."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT DISTINCT pais FROM convergencia", conn)
    conn.close()
    return df["pais"].tolist()


def get_available_años(db_path=None):
    """Retorna lista de años disponibles en la BD."""
    conn = get_connection(db_path)
    df = pd.read_sql_query("SELECT DISTINCT año FROM convergencia ORDER BY año", conn)
    conn.close()
    return df["año"].tolist()


def get_estadisticas(db_path=None):
    """Retorna estadísticas de la base de datos."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM convergencia")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT pais) FROM convergencia")
    n_paises = cursor.fetchone()[0]
    
    cursor.execute("SELECT MIN(año), MAX(año) FROM convergencia")
    rango = cursor.fetchone()
    
    cursor.execute("SELECT pais, COUNT(*) as n FROM convergencia GROUP BY pais ORDER BY n DESC")
    por_pais = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_registros": total,
        "total_paises": n_paises,
        "año_inicio": rango[0],
        "año_fin": rango[1],
        "por_pais": por_pais
    }
