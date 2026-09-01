# Data Quality Report v1

- Archivo fuente preservado: `/mnt/c/Users/LENOVO/Documents/workshop mini-me/datasets/native_potato_biodiversity/native_potato_biodiversity_dirty.csv`
- Archivo limpio completo: `/mnt/c/Users/LENOVO/Documents/workshop mini-me/datasets/native_potato_biodiversity/native_potato_biodiversity_cleaned_v1.csv`
- Archivo limpio apto para análisis (sin leakage): `/mnt/c/Users/LENOVO/Documents/workshop mini-me/datasets/native_potato_biodiversity/native_potato_biodiversity_cleaned_v1_analysis.csv`

## Acciones aplicadas
- Eliminación de duplicados exactos y duplicados por llave primaria `record_id` conservando la primera ocurrencia.
- Recorte de espacios en columnas de texto.
- Estandarización de categorías en `region`, `altitude_band` y `skin_primary_color` según diccionario.
- Conversión de unidades en `altitude_m` (ft→m) y `market_distance_km` (miles→km).
- Coerción de tipos numéricos.
- Valores fuera de rango convertidos a faltantes cuando no podían corregirse justificadamente.
- La columna `next_season_observed_copy` se conserva en el archivo limpio completo por trazabilidad, pero se excluye en la versión `analysis` por leakage.

## Conteos de cambios
duplicados_exactos_eliminados                  7
duplicados_record_id_residuales_eliminados     0
espacios_recortados                            3
region_estandarizada                          10
altitude_band_estandarizada                   13
skin_primary_color_estandarizada              13
altitude_ft_a_m                                7
altitude_coercion_a_numerico                   7
market_distance_millas_a_km                    7
coercion_numerica_columnas                    10

## Issues de validación detectados
sampling_visit_fuera_de_rango                 0
households_interviewed_fuera_de_rango         1
altitude_m_fuera_de_rango                     0
market_distance_km_fuera_de_rango             1
seed_exchange_events_year_fuera_de_rango      1
number_of_reported_uses_fuera_de_rango        0
years_reported_in_community_fuera_de_rango    0
observed_next_season_fuera_de_rango           0
interviewer_badge_number_fuera_de_rango       0
next_season_observed_copy_fuera_de_rango      0

## Faltantes persistentes por columna
record_id                       0
community_code                  0
region                          0
survey_round                    0
sampling_visit                  0
households_interviewed         11
altitude_band                   0
altitude_m                      0
market_distance_km              1
morphotype_id                   0
local_variety_name             10
skin_primary_color             10
main_use                        0
seed_exchange_events_year       1
number_of_reported_uses         0
years_reported_in_community    10
observed_next_season            0
interviewer_badge_number        0
next_season_observed_copy       0

## Resultado
- Filas finales: 288
- Columnas en archivo limpio completo: 19
- Faltantes totales persistentes: 43
- Apto para EDA: sí, con faltantes remanentes manejables y la columna de leakage excluida en la versión analysis.
