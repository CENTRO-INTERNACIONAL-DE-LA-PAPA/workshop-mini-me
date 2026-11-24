# Clave de defectos — mejoramiento

> No distribuir antes del ejercicio. Este archivo dice exactamente qué se rompió.

Semilla: `20261022`. Volver a correr `corrupt_dataset.py` con la misma semilla reproduce
estos archivos byte por byte.

**Total de cambios registrados: 479**

## Por familia

| Familia | Cambios | Columnas afectadas |
|---|---:|---|
| `category_variant` | 72 | district, locality, province, region, site_code, trial |
| `duplicate_row` | 7 | — |
| `impossible_value` | 48 | atmw, atw, elevation_m, latitude, longitude, mtwp, mtwpl, mtya, mtyna, nmtp, nmtpl, nnomtp, nomtwp, nph, ntp, plot, pph, rep, tntp, tntpl, ttwp, ttwpl, ttya, ttyna |
| `missing_cell` | 275 | atmw, atw, district, elevation_m, instn, latitude, locality, longitude, mtwp, mtwpl, mtya, mtyna, nmtp, nmtpl, nnomtp, nomtwp, nph, ntp, plot, pph, province, region, rep, site_code, tntp, tntpl, trial, ttwp, ttwpl, ttya, ttyna, variety_name |
| `mixed_unit` | 67 | elevation_m, mtwp, mtwpl, mtya, mtyna, nomtwp, pph, ttwp, ttwpl, ttya, ttyna |
| `whitespace_case` | 10 | instn, variety_name |

## Por columna

| Columna | Cambios | Familias |
|---|---:|---|
| `atmw` | 11 | impossible_value, missing_cell |
| `atw` | 11 | impossible_value, missing_cell |
| `district` | 21 | category_variant, missing_cell |
| `elevation_m` | 18 | impossible_value, missing_cell, mixed_unit |
| `instn` | 14 | missing_cell, whitespace_case |
| `latitude` | 11 | impossible_value, missing_cell |
| `locality` | 21 | category_variant, missing_cell |
| `longitude` | 11 | impossible_value, missing_cell |
| `mtwp` | 17 | impossible_value, missing_cell, mixed_unit |
| `mtwpl` | 16 | impossible_value, missing_cell, mixed_unit |
| `mtya` | 16 | impossible_value, missing_cell, mixed_unit |
| `mtyna` | 16 | impossible_value, missing_cell, mixed_unit |
| `nmtp` | 11 | impossible_value, missing_cell |
| `nmtpl` | 8 | impossible_value, missing_cell |
| `nnomtp` | 9 | impossible_value, missing_cell |
| `nomtwp` | 15 | impossible_value, missing_cell, mixed_unit |
| `nph` | 11 | impossible_value, missing_cell |
| `ntp` | 11 | impossible_value, missing_cell |
| `plot` | 11 | impossible_value, missing_cell |
| `pph` | 18 | impossible_value, missing_cell, mixed_unit |
| `province` | 21 | category_variant, missing_cell |
| `region` | 21 | category_variant, missing_cell |
| `rep` | 11 | impossible_value, missing_cell |
| `site_code` | 21 | category_variant, missing_cell |
| `tntp` | 10 | impossible_value, missing_cell |
| `tntpl` | 10 | impossible_value, missing_cell |
| `trial` | 21 | category_variant, missing_cell |
| `ttwp` | 17 | impossible_value, missing_cell, mixed_unit |
| `ttwpl` | 18 | impossible_value, missing_cell, mixed_unit |
| `ttya` | 14 | impossible_value, missing_cell, mixed_unit |
| `ttyna` | 17 | impossible_value, missing_cell, mixed_unit |
| `variety_name` | 14 | missing_cell, whitespace_case |

## Columnas que no son un defecto de limpieza

Están correctamente registradas: el problema es analítico, no de calidad del dato.

| Columna | Rol |
|---|---|
| `mtwp` | `leakage` |
| `mtwpl` | `leakage` |
| `mtya` | `leakage` |
| `mtyna` | `leakage` |
| `nomtwp` | `leakage` |
| `ttwp` | `leakage` |
| `ttwpl` | `leakage` |
| `ttyna` | `leakage` |

## Cómo se usa

El detalle celda a celda está en `mejoramiento_changelog.csv`: cada fila trae `record_id`,
columna, valor original y valor sucio. Ese archivo permite medir cuántos de los defectos
sembrados reparó realmente un equipo, que es una pregunta más estricta que el score global
de `score_cleanliness.py`.
