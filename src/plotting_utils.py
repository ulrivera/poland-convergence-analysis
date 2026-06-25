# Utilidades de visualización para análisis de convergencia.

import matplotlib.pyplot as plt
import numpy as np
import os
from config import COLORES_V4, COLORES_UE, NOMBRES_PAIS, FIGURES_DIR


def setup_plot_style():
    """Configura estilo global de matplotlib."""
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


def get_color(pais):
    """Retorna color asignado a un país."""
    return COLORES_V4.get(pais, "gray")


def get_nombre(pais):
    """Retorna nombre legible de un país."""
    return NOMBRES_PAIS.get(pais, pais)


def save_figure(fig, filename, dpi=150):
    """Guarda figura en la carpeta de figuras.
    
    Args:
        fig: Objeto Figure de matplotlib
        filename: Nombre del archivo (sin ruta)
        dpi: Resolución
    
    Returns:
        Ruta completa del archivo guardado
    """
    os.makedirs(FIGURES_DIR, exist_ok=True)
    filepath = os.path.join(FIGURES_DIR, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
    return filepath


def plot_evolucion_absoluta(df, paises, promedio_ue, ax=None):
    """Grafica evolución absoluta de PIBpc para varios países.
    
    Args:
        df: DataFrame con columnas [pais, año, valor]
        paises: Lista de países a graficar
        promedio_ue: Serie con promedio UE por año
        ax: Eje de matplotlib (opcional)
    
    Returns:
        Objeto Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    for pais in paises:
        pais_data = df[df["pais"] == pais].sort_values("año")
        ax.plot(pais_data["año"], pais_data["valor"], 
                color=get_color(pais), linewidth=2.5, 
                label=get_nombre(pais), marker="o", markersize=3)
    
    ax.plot(promedio_ue.index, promedio_ue.values, 
            color=COLORES_UE["promedio"], linewidth=2, 
            linestyle="--", label="Promedio UE-14", alpha=0.7)
    
    ax.set_title("PIB per cápita PPS (evolución absoluta)")
    ax.set_xlabel("Año")
    ax.set_ylabel("PPS per cápita")
    ax.legend()
    
    return ax


def plot_indice_convergencia(convergencia_df, ax=None):
    """Grafica índice de convergencia (% del promedio UE).
    
    Args:
        convergencia_df: DataFrame con índices de convergencia por país/año
        ax: Eje de matplotlib (opcional)
    
    Returns:
        Objeto Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    for pais in convergencia_df.columns:
        ax.plot(convergencia_df.index, convergencia_df[pais], 
                color=get_color(pais), linewidth=2.5, 
                label=get_nombre(pais), marker="o", markersize=3)
    
    ax.axhline(y=100, color=COLORES_UE["paridad"], 
               linestyle="--", alpha=0.7, label="Paridad UE-14 (100%)")
    ax.axhline(y=75, color=COLORES_UE["umbral_75"], 
               linestyle=":", alpha=0.5, label="Umbral 75%")
    ax.fill_between(convergencia_df.index, 0, 100, alpha=0.1, color="green")
    
    ax.set_title("Índice de convergencia (% del promedio UE-14)")
    ax.set_xlabel("Año")
    ax.set_ylabel("% del promedio UE-14")
    ax.legend()
    ax.set_ylim(0, 110)
    
    return ax


def plot_convergencia_beta(ln_y0s, cagrs, slope, intercept, r2, ax=None):
    """Grafica convergencia beta (scatter + regresión).
    
    Args:
        ln_y0s: Lista de ln(PIBpc inicial)
        cagrs: Lista de CAGR (%)
        slope: Pendiente de la regresión
        intercept: Intercepto de la regresión
        r2: R² de la regresión
        ax: Eje de matplotlib (opcional)
    
    Returns:
        Objeto Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    paises = ["PL", "CZ", "HU", "SK"]
    
    for i, pais in enumerate(paises):
        ax.scatter(ln_y0s[i], cagrs[i], 
                   color=get_color(pais), s=200, 
                   label=get_nombre(pais), zorder=5, edgecolors='black')
    
    # Línea de tendencia
    x_line = np.linspace(min(ln_y0s) - 0.05, max(ln_y0s) + 0.05, 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, "k--", alpha=0.7, linewidth=2,
            label=f"Tendencia (β={slope:.3f}, R²={r2:.2f})")
    
    # Anotaciones
    for i, pais in enumerate(paises):
        ax.annotate(f"{pais}\\nCAGR: {cagrs[i]:.2f}%", 
                    xy=(ln_y0s[i], cagrs[i]),
                    xytext=(15, 15), textcoords='offset points',
                    fontsize=10, color=get_color(pais),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax.set_title("Convergencia Beta (β): ¿Crecen más rápido los más pobres?")
    ax.set_xlabel("ln(PIB per cápita 2004)")
    ax.set_ylabel("CAGR 2004-2023 (%)")
    ax.legend()
    
    if slope < 0:
        ax.text(0.05, 0.95, "✅ β < 0: Convergencia confirmada", 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    return ax


def plot_convergencia_sigma(sigma_df, ax=None):
    """Grafica convergencia sigma (dispersión temporal).
    
    Args:
        sigma_df: DataFrame con columnas [año, sigma]
        ax: Eje de matplotlib (opcional)
    
    Returns:
        Objeto Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(sigma_df["año"], sigma_df["sigma"], 
            color="purple", linewidth=2, marker="o", markersize=3)
    ax.axhline(y=sigma_df["sigma"].iloc[0], color="red", 
               linestyle="--", alpha=0.5, label=f"σ inicial ({sigma_df['sigma'].iloc[0]:.3f})")
    ax.axhline(y=sigma_df["sigma"].iloc[-1], color="green", 
               linestyle="--", alpha=0.5, label=f"σ final ({sigma_df['sigma'].iloc[-1]:.3f})")
    ax.fill_between(sigma_df["año"], sigma_df["sigma"], sigma_df["sigma"].iloc[0],
                    where=(sigma_df["sigma"] < sigma_df["sigma"].iloc[0]), 
                    alpha=0.3, color="green", label="Convergencia")
    
    ax.set_title("Convergencia Sigma (σ): Dispersión entre países")
    ax.set_xlabel("Año")
    ax.set_ylabel("σ (desv. estándar del log)")
    ax.legend()
    
    return ax
