# Análisis de Convergencia Real: Polonia vs V4 vs UE-14

## Descripción

Este proyecto analiza la convergencia real del PIB per cápita (PPS) de Polonia y el Grupo de Visegrado (V4) respecto al promedio de la UE-14 desde 2004 (adhesión a la UE) hasta 2023.

## Estructura

```
tu-proyecto-convergencia/
├── data/
│   ├── eurostat/
│   │   ├── eurostat_convergencia_sqlite.py   ← Script de extracción
│   │   └── eurostat_data/
│   │       └── eurostat_convergencia.db      ← Base de datos SQLite
│   ├── nbp/
│   │   └── nbp_download.py                   ← Script NBP
│   └── worldbank/                            ← Reservado para v2.0
│
├── src/                                      ← Módulos compartidos
│   ├── __init__.py
│   ├── config.py                             ← Constantes (UE14, V4, colores)
│   ├── db_utils.py                           ← Leer/escribir SQLite
│   └── plotting_utils.py                     ← Funciones de graficación
│
├── notebooks/v1.0/                           ← Análisis
│   ├── 01_carga_y_exploracion.ipynb
│   ├── 02_indice_convergencia.ipynb
│   ├── 03_convergencia_beta.ipynb
│   ├── 04_convergencia_sigma.ipynb
│   ├── 05_visualizaciones_comparativas.ipynb
│   └── 06_conclusiones.ipynb                 ← Con limitaciones y roadmap v2.0
│
├── docs/
│   ├── README.md
│   └── metodologia.md
│
├── requirements.txt
└── .gitignore
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### 1. Extraer datos

```bash
cd data/eurostat
python eurostat_convergencia_sqlite.py
```

### 2. Analizar

```bash
cd notebooks/v1.0
jupyter notebook
```

Abre los notebooks numerados en orden.

## Metodología

Ver [docs/metodologia.md](docs/metodologia.md)

## Fuentes

- **Eurostat**: `nama_10_pc` (PIB per cápita PPS)
- **NBP**: `api.nbp.pl` (tipos de cambio y oro)

## Autor
