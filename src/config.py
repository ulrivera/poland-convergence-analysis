# Configuración centralizada del proyecto de convergencia
import os

# ========== RUTAS ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

EUROSTAT_DIR = os.path.join(DATA_DIR, "eurostat")
EUROSTAT_DATA_DIR = os.path.join(EUROSTAT_DIR, "eurostat_data")
EUROSTAT_DB = os.path.join(EUROSTAT_DATA_DIR, "eurostat_convergencia.db")

NBP_DIR = os.path.join(DATA_DIR, "nbp")
NBP_DATA_DIR = os.path.join(NBP_DIR, "nbp_data")

WORLDBANK_DIR = os.path.join(DATA_DIR, "worldbank")
WORLDBANK_DATA_DIR = os.path.join(WORLDBANK_DIR, "worldbank_data")

NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
FIGURES_DIR = os.path.join(NOTEBOOKS_DIR, "v1.0", "figures")

# ========== GRUPOS DE PAÍSES ==========
UE14 = ["AT", "BE", "DK", "FI", "FR", "DE", "EL", "IE", 
        "IT", "LU", "NL", "PT", "ES", "SE"]

V4 = ["PL", "CZ", "HU", "SK"]
BALTICOS = ["EE", "LV", "LT"]
ESTE_RECIENTE = ["BG", "RO", "HR"]

# ========== CONFIGURACIÓN EUROSTAT ==========
EUROSTAT_DATASET = "nama_10_pc"
EUROSTAT_NA_ITEM = "B1GQ"  # PIB a precios de mercado
EUROSTAT_UNIT = "CP_PPS_EU27_2020_HAB"  # PPS per cápita

# ========== VISUALIZACIÓN ==========
COLORES_V4 = {
    "PL": "#e41a1c",  # Rojo
    "CZ": "#377eb8",  # Azul
    "HU": "#4daf4a",  # Verde
    "SK": "#ff7f00"   # Naranja
}

COLORES_UE = {
    "promedio": "#333333",
    "paridad": "#666666",
    "umbral_75": "#999999"
}

# Nombres legibles para gráficos
NOMBRES_PAIS = {
    "PL": "Polonia",
    "CZ": "República Checa", 
    "HU": "Hungría",
    "SK": "Eslovaquia",
    "DE": "Alemania",
    "FR": "Francia",
    "IT": "Italia",
    "ES": "España"
}

# ========== PERÍODO DE ANÁLISIS ==========
AÑO_INICIO_DEFAULT = 2004
AÑO_FIN_DEFAULT = 2023
