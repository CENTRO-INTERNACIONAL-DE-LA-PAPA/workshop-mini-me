# Adaptacion — mejoramiento

Origen: `PTYL200911_Estabilidad_30genotipos.xlsx`  ·  267 filas  ·  33 columnas

Este archivo deja por escrito todo lo que el adaptador dedujo. **La estructura se puede
inferir; el significado no.** Lo de abajo hay que confirmarlo con quien conoce los datos.

## Lo que se hizo

- `PLOT` -> `plot`
- `REP` -> `rep`
- `INSTN` -> `instn`
- `NTP` -> `ntp`
- `NPH` -> `nph`
- `PPH` -> `pph`
- `NNoMTP` -> `nnomtp`
- `TNTP` -> `tntp`
- `TNTPL` -> `tntpl`
- `NMTP` -> `nmtp`
- `NMTPL` -> `nmtpl`
- `NoMTWP` -> `nomtwp`
- `TTWP` -> `ttwp`
- `TTWPL` -> `ttwpl`
- `TTYNA` -> `ttyna`
- `TTYA` -> `ttya`
- `MTWP` -> `mtwp`
- `MTWPL` -> `mtwpl`
- `MTYNA` -> `mtyna`
- `MTYA` -> `mtya`
- `ATW` -> `atw`
- `ATMW` -> `atmw`
- Ninguna columna era unica y no vacia: se sintetizo `record_id` (MEJ-0001...).

## Tipos y unidades deducidos

| Columna | Original | Tipo | Unidad | Rol propuesto | Rango observado |
|---|---|---|---|---|---|
| `record_id` | (sintetizado) | string | none | `primary_key` | unique |
| `trial` | trial | category | none | `context` | PTYL200911_CCASAP_Stability_Field|PTYL200911_CCOLL_Stability |
| `site_code` | site_code | category | none | `design` | CCASAP|CCOLL|LAVICT |
| `region` | region | category | none | `context` | Huancavelica|Junin |
| `province` | province | category | none | `context` | Acobamba|Huancayo |
| `district` | district | category | none | `context` | Paucara|San agustin |
| `locality` | locality | category | none | `context` | Ccasapata|Ccollpaccasa|La Victoria |
| `elevation_m` | elevation_m | integer | none | `context` | 3173-4111 |
| `latitude` | latitude | number | none | `context` | -12.8116--11.989 |
| `longitude` | longitude | number | none | `context` | -75.2695--74.7283 |
| `plot` | PLOT | integer | none | `design` | 0-124 |
| `rep` | REP | integer | none | `context` | 0-4 |
| `instn` | INSTN | string | none | `context` |  |
| `variety_name` | variety_name | string | none | `context` |  |
| `ntp` | NTP | integer | none | `context` | 9-11 |
| `nph` | NPH | integer | none | `context` | 2-11 |
| `pph` | PPH | integer | none | `context` | 26-104 |
| `nnomtp` | NNoMTP | integer | none | `context` | 0-451 |
| `tntp` | TNTP | number | none | `context` | 0-607.4 |
| `tntpl` | TNTPL | number | none | `context` | 0.255-60.645 |
| `nmtp` | NMTP | number | none | `context` | 0-248.85 |
| `nmtpl` | NMTPL | number | none | `context` | 0-24.885 |
| `nomtwp` | NoMTWP | number | none | `context` | 0-11.125 |
| `ttwp` | TTWP | number | none | `context` | 0-17.1805 |
| `ttwpl` | TTWPL | number | none | `context` | 0-1.718 |
| `ttyna` | TTYNA | number | none | `context` | 0-63.6315 |
| `ttya` | TTYA | number | none | `context` | 0-63.6315 |
| `mtwp` | MTWP | number | none | `context` | 0-10.689 |
| `mtwpl` | MTWPL | number | none | `context` | 0-1.0689 |
| `mtyna` | MTYNA | number | none | `context` | 0-39.5889 |
| `mtya` | MTYA | number | none | `context` | 0-39.5889 |
| `atw` | ATW | number | none | `context` | 0-182.6545 |
| `atmw` | ATMW | number | none | `context` | 0-3198.9764 |

## Confirmar antes de usar

1. **Unidad de observacion**: ¿que representa una fila?
2. **Variable de resultado**: ¿cual es el `outcome`? Ahora todas figuran como `context`.
3. **Columnas calculadas despues del resultado**: son el `leakage` del ejercicio.
4. **Columnas de diseño**: revisar las marcadas `design` abajo, y agregar las que falten.
5. **Unidades**: las deducidas del nombre de la columna estan sin verificar.
6. **Relaciones conocidas**: ¿alguna que exista de verdad, y alguna que se sepa que no?

Los roles validos son: `primary_key`, `design`, `context`, `predictor`, `outcome`,
`outcome_secondary`, `confounded_exposure`, `leakage`, `null`.

Marcadas como `design` por el nombre: `site_code`, `plot`.

## Siguiente paso

Editar `mejoramiento_dictionary.csv` con las respuestas de arriba y despues:

```bash
python scripts/corrupt_dataset.py datasets/mejoramiento/mejoramiento_clean.csv
```

## Configuración del taller (`configurar_taller.py`)

- 32 entradas de configuración aplicadas. Diccionario completo en `mejoramiento_dictionary_completo.csv`; en `mejoramiento_dictionary.csv` (participantes) las 8 columnas leakage aparecen como `predictor`.
- Texto mal codificado en el original, corregido en `mejoramiento_clean.csv` (9 celdas): `variety_name`: 'A±il Papa' → 'Añil Papa'.

Preguntas para quien produjo los datos:

1. Ensayo de estabilidad: 30 genotipos en 3 localidades (Ccasapata, Ccollpaccasa, La Victoria) con 3 repeticiones. ¿Es de 2009 (PTYL200911)?
2. ¿El resultado es `ttya` (rendimiento total ajustado)? Si es así, los pesos y rendimientos totales y comerciales (`ttwp`, `ttwpl`, `ttyna`, `nomtwp`, `mtwp`, `mtwpl`, `mtyna`, `mtya`) son leakage.
3. `ttya` tiene 31 celdas vacías en el original, casi siempre junto con `nph` vacío: ¿son parcelas perdidas?
4. `atmw` llega a 3047 g (La Victoria, CIP702363) y 912 g (Ccollpaccasa, CIP704327). En el primer caso `nmtp` vale 1,91, que no es un conteo: ¿error de digitación en el original?
5. Faltan 3 parcelas: el diseño completo serían 270 (30 × 3 × 3). ¿Se perdieron?
6. Dos genotipos (CIP703274 y CIP703280) figuran como `Unknown` en `variety_name`.
