# Clave de defectos — tizon_tardio

> No distribuir antes del ejercicio. Este archivo dice exactamente qué se rompió.

Semilla: `20261022`. Volver a correr `corrupt_dataset.py` con la misma semilla reproduce
estos archivos byte por byte.

**Total de cambios registrados: 151**

## Por familia

| Familia | Cambios | Columnas afectadas |
|---|---:|---|
| `category_variant` | 54 | accename, class, instn, rlb, site, treatment |
| `duplicate_row` | 5 | — |
| `impossible_value` | 10 | audpc, plot, raudpc, rep, ttya |
| `missing_cell` | 77 | accename, audpc, class, instn, plot, raudpc, rep, rlb, site, treatment, ttya |
| `mixed_unit` | 5 | ttya |

## Por columna

| Columna | Cambios | Familias |
|---|---:|---|
| `accename` | 16 | category_variant, missing_cell |
| `audpc` | 9 | impossible_value, missing_cell |
| `class` | 16 | category_variant, missing_cell |
| `instn` | 16 | category_variant, missing_cell |
| `plot` | 9 | impossible_value, missing_cell |
| `raudpc` | 9 | impossible_value, missing_cell |
| `rep` | 9 | impossible_value, missing_cell |
| `rlb` | 16 | category_variant, missing_cell |
| `site` | 16 | category_variant, missing_cell |
| `treatment` | 16 | category_variant, missing_cell |
| `ttya` | 14 | impossible_value, missing_cell, mixed_unit |

## Columnas que no son un defecto de limpieza

Están correctamente registradas: el problema es analítico, no de calidad del dato.

| Columna | Rol |
|---|---|
| `raudpc` | `leakage` |
| `rlb` | `leakage` |

## Cómo se usa

El detalle celda a celda está en `tizon_tardio_changelog.csv`: cada fila trae `record_id`,
columna, valor original y valor sucio. Ese archivo permite medir cuántos de los defectos
sembrados reparó realmente un equipo, que es una pregunta más estricta que el score global
de `score_cleanliness.py`.
