# Metodología

## Versión 1.0

### Definición de convergencia real

> Acercamiento del PIB per cápita (PPS) al promedio de la UE-14.

### Promedio UE-14

**Simple**: cada país pesa igual, sin importar población o tamaño de economía.

```
Promedio_UE14 = (1/14) × Σ PIBpc_i
```

**Limitación**: Luxemburgo (0.7M hab., 75k PPS) pesa igual que Alemania (84.5M hab., 40.5k PPS).

### Dataset

| Parámetro | Valor |
|-----------|-------|
| Dataset | `nama_10_pc` |
| Indicador | `B1GQ` (PIB a precios de mercado) |
| Unidad | `CP_PPS_EU27_2020_HAB` (PPS per cápita) |
| Período | 2004-2023 |
| Países | UE-14 + V4 |

### Técnicas de análisis

1. **Índice de convergencia**: `(PIBpc país / PIBpc promedio UE-14) × 100`
2. **Convergencia beta (β)**: Regresión CAGR vs ln(PIBpc inicial)
3. **Convergencia sigma (σ)**: Desviación estándar del log(PIBpc)
4. **Proyección lineal**: Año estimado para alcanzar paridad

### Grupos de países

- **UE-14**: AT, BE, DK, FI, FR, DE, EL, IE, IT, LU, NL, PT, ES, SE
- **V4**: PL, CZ, HU, SK

### Nota sobre UE-15

El Reino Unido (GB) no está disponible en `nama_10_pc` post-Brexit. Por tanto, usamos UE-14 como aproximación de UE-15.

## Versión 2.0 (planeada)

- Promedio ponderado por población
- Comparación PPS vs PPP
- Productividad por hora trabajada
- Estructura productiva (VAB sectorial)