# Clave de defectos — morfologia

> No distribuir antes del ejercicio. Este archivo dice exactamente qué se rompió.

Semilla: `20261022`. Volver a correr `corrupt_dataset.py` con la misma semilla reproduce
estos archivos byte por byte.

**Total de cambios registrados: 50**

## Por familia

| Familia | Cambios | Columnas afectadas |
|---|---:|---|
| `duplicate_row` | 2 | — |
| `impossible_value` | 18 | distribution_of_secondary_color, tuber_flesh_predominant_color, tuber_flesh_secondary_color, tuber_flesh_secondary_color_distribution, tuber_shape, tuber_shape_depth_of_eyes, tuber_shape_unusual, tuber_skin_predominant_color, tuber_skin_secondary_color |
| `missing_cell` | 24 | accession_name, accession_number, country_of_selection, distribution_of_secondary_color, tuber_flesh_predominant_color, tuber_flesh_secondary_color, tuber_flesh_secondary_color_distribution, tuber_shape, tuber_shape_depth_of_eyes, tuber_shape_unusual, tuber_skin_predominant_color, tuber_skin_secondary_color |
| `whitespace_case` | 6 | accession_name, accession_number, country_of_selection |

## Por columna

| Columna | Cambios | Familias |
|---|---:|---|
| `accession_name` | 4 | missing_cell, whitespace_case |
| `accession_number` | 4 | missing_cell, whitespace_case |
| `country_of_selection` | 4 | missing_cell, whitespace_case |
| `distribution_of_secondary_color` | 4 | impossible_value, missing_cell |
| `tuber_flesh_predominant_color` | 4 | impossible_value, missing_cell |
| `tuber_flesh_secondary_color` | 4 | impossible_value, missing_cell |
| `tuber_flesh_secondary_color_distribution` | 4 | impossible_value, missing_cell |
| `tuber_shape` | 4 | impossible_value, missing_cell |
| `tuber_shape_depth_of_eyes` | 4 | impossible_value, missing_cell |
| `tuber_shape_unusual` | 4 | impossible_value, missing_cell |
| `tuber_skin_predominant_color` | 4 | impossible_value, missing_cell |
| `tuber_skin_secondary_color` | 4 | impossible_value, missing_cell |

## Cómo se usa

El detalle celda a celda está en `morfologia_changelog.csv`: cada fila trae `record_id`,
columna, valor original y valor sucio. Ese archivo permite medir cuántos de los defectos
sembrados reparó realmente un equipo, que es una pregunta más estricta que el score global
de `score_cleanliness.py`.
