# Adaptacion — mejoramiento

Origen: `01_Datos_mejoramiento_rendimiento_2016.xlsx`  ·  244 filas  ·  21 columnas

Este archivo deja por escrito todo lo que el adaptador dedujo. **La estructura se puede
inferir; el significado no.** Lo de abajo hay que confirmarlo con quien conoce los datos.

## Lo que se hizo

- `PLOT` -> `plot`
- `REP` -> `rep`
- `INSTN` -> `instn`
- `NTP` -> `ntp`
- `NPH` -> `nph`
- `PPH` -> `pph`
- `TNTP` -> `tntp`
- `TNTPL` -> `tntpl`
- `TTWP` -> `ttwp`
- `TTWPL` -> `ttwpl`
- `TTYNA` -> `ttyna`
- `TTYA` -> `ttya`
- `ATW` -> `atw`
- Identificador unico encontrado: `plot`.

## Tipos y unidades deducidos

| Columna | Original | Tipo | Unidad | Rol propuesto | Rango observado |
|---|---|---|---|---|---|
| `country` | country | category | none | `context` | Peru |
| `adm1` | adm1 | category | none | `context` | Junin |
| `adm2` | adm2 | category | none | `context` | Huancayo |
| `adm3` | adm3 | category | none | `context` | San Agustin |
| `location` | location | category | none | `context` | La Victoria |
| `elevation` | elevation | integer | none | `context` | 3055-3377 |
| `latitude` | latitude | number | none | `context` | -12.6277--11.4251 |
| `longitude` | longitude | number | none | `context` | -79.0071--71.4827 |
| `plot` | PLOT | integer | none | `primary_key` | unique |
| `rep` | REP | integer | none | `context` | 0-5 |
| `instn` | INSTN | string | none | `context` |  |
| `ntp` | NTP | integer | none | `context` | 4-11 |
| `nph` | NPH | integer | none | `context` | 2-11 |
| `pph` | PPH | integer | none | `context` | 22-188 |
| `tntp` | TNTP | integer | none | `context` | 0-536 |
| `tntpl` | TNTPL | number | none | `context` | 0-53.4833 |
| `ttwp` | TTWP | number | none | `context` | 0-10.475 |
| `ttwpl` | TTWPL | number | none | `context` | 0-1.0466 |
| `ttyna` | TTYNA | number | none | `context` | 0-38.7963 |
| `ttya` | TTYA | number | none | `context` | 0-38.7618 |
| `atw` | ATW | number | none | `context` | 1.2821-86.4233 |

## Confirmar antes de usar

1. **Unidad de observacion**: ¿que representa una fila?
2. **Variable de resultado**: ¿cual es el `outcome`? Ahora todas figuran como `context`.
3. **Columnas calculadas despues del resultado**: son el `leakage` del ejercicio.
4. **Columnas de diseño**: revisar las marcadas `design` abajo, y agregar las que falten.
5. **Unidades**: las deducidas del nombre de la columna estan sin verificar.
6. **Relaciones conocidas**: ¿alguna que exista de verdad, y alguna que se sepa que no?

Los roles validos son: `primary_key`, `design`, `context`, `predictor`, `outcome`,
`outcome_secondary`, `confounded_exposure`, `leakage`, `null`.

## Siguiente paso

Editar `mejoramiento_dictionary.csv` con las respuestas de arriba y despues:

```bash
python scripts/corrupt_dataset.py datasets/mejoramiento/mejoramiento_clean.csv
```

## Configuración del taller (`configurar_taller.py`)

- 20 entradas de configuración aplicadas. Diccionario completo en `mejoramiento_dictionary_completo.csv`; en `mejoramiento_dictionary.csv` (participantes) las 3 columnas leakage aparecen como `predictor`.

Preguntas para quien produjo los datos:

1. Hay una sola localidad (La Victoria, Huancayo): la pregunta de estabilidad entre ambientes del plan no se puede responder con estos datos. ¿Se cambia por '¿qué genotipos rinden más?'
2. ¿El resultado es `ttya` (rendimiento ajustado)? Si es así, `ttwp`, `ttwpl` y `ttyna` son leakage.
3. `ttya` tiene 13 celdas vacías en el original: ¿son parcelas perdidas?
4. El diccionario fija TNTP en 0-50, pero los datos llegan a 536 tubérculos por parcela: ¿el límite es por planta?
