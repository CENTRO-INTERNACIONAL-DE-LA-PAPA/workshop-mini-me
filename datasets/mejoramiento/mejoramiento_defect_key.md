# Clave de defectos — mejoramiento

> No distribuir antes del ejercicio. Este archivo dice exactamente qué se rompió.

Semilla: `20261022`. Volver a correr `corrupt_dataset.py` con la misma semilla reproduce
estos archivos byte por byte.

**Total de cambios registrados: 247**

## Por familia

| Familia | Cambios | Columnas afectadas |
|---|---:|---|
| `duplicate_row` | 6 | — |
| `impossible_value` | 28 | atw, elevation, latitude, longitude, nph, ntp, pph, rep, tntp, tntpl, ttwp, ttwpl, ttya, ttyna |
| `missing_cell` | 174 | adm1, adm2, adm3, atw, country, elevation, instn, latitude, location, longitude, nph, ntp, pph, rep, tntp, tntpl, ttwp, ttwpl, ttya, ttyna |
| `mixed_unit` | 34 | elevation, pph, ttwp, ttwpl, ttya, ttyna |
| `whitespace_case` | 5 | instn |

## Por columna

| Columna | Cambios | Familias |
|---|---:|---|
| `adm1` | 9 | missing_cell |
| `adm2` | 9 | missing_cell |
| `adm3` | 9 | missing_cell |
| `atw` | 11 | impossible_value, missing_cell |
| `country` | 9 | missing_cell |
| `elevation` | 17 | impossible_value, missing_cell, mixed_unit |
| `instn` | 14 | missing_cell, whitespace_case |
| `latitude` | 11 | impossible_value, missing_cell |
| `location` | 9 | missing_cell |
| `longitude` | 11 | impossible_value, missing_cell |
| `nph` | 11 | impossible_value, missing_cell |
| `ntp` | 11 | impossible_value, missing_cell |
| `pph` | 17 | impossible_value, missing_cell, mixed_unit |
| `rep` | 11 | impossible_value, missing_cell |
| `tntp` | 10 | impossible_value, missing_cell |
| `tntpl` | 10 | impossible_value, missing_cell |
| `ttwp` | 15 | impossible_value, missing_cell, mixed_unit |
| `ttwpl` | 16 | impossible_value, missing_cell, mixed_unit |
| `ttya` | 15 | impossible_value, missing_cell, mixed_unit |
| `ttyna` | 16 | impossible_value, missing_cell, mixed_unit |

## Columnas que no son un defecto de limpieza

Están correctamente registradas: el problema es analítico, no de calidad del dato.

| Columna | Rol |
|---|---|
| `ttwp` | `leakage` |
| `ttwpl` | `leakage` |
| `ttyna` | `leakage` |

## Cómo se usa

El detalle celda a celda está en `mejoramiento_changelog.csv`: cada fila trae `record_id`,
columna, valor original y valor sucio. Ese archivo permite medir cuántos de los defectos
sembrados reparó realmente un equipo, que es una pregunta más estricta que el score global
de `score_cleanliness.py`.
