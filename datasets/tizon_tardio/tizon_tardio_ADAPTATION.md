# Adaptacion — tizon_tardio

Origen: `03_Tizon tardio datos.xlsx`  ·  189 filas  ·  12 columnas

Este archivo deja por escrito todo lo que el adaptador dedujo. **La estructura se puede
inferir; el significado no.** Lo de abajo hay que confirmarlo con quien conoce los datos.

## Lo que se hizo

- 7 columna(s) sin encabezado descartada(s).
- `PLOT` -> `plot`
- `REP` -> `rep`
- `TREATMENT` -> `treatment`
- `CLASS` -> `class`
- `SITE` -> `site`
- `INSTN` -> `instn`
- `ACCENAME` -> `accename`
- `AUDPC` -> `audpc`
- `rAUDPC` -> `raudpc`
- `TTYA` -> `ttya`
- `RLB` -> `rlb`
- Ninguna columna era unica y no vacia: se sintetizo `record_id` (TIZ-0001...).

## Tipos y unidades deducidos

| Columna | Original | Tipo | Unidad | Rol propuesto | Rango observado |
|---|---|---|---|---|---|
| `record_id` | (sintetizado) | string | none | `primary_key` | unique |
| `plot` | PLOT | integer | none | `design` | 0-12 |
| `rep` | REP | integer | none | `context` | 0-4 |
| `treatment` | TREATMENT | category | none | `design` | Agrifos|Agrifos 110 ml|Agrifos 400|Agrifos 65 ml|Agriphite 6 |
| `class` | CLASS | category | none | `context` | Control|Conventional|Phosphonate |
| `site` | SITE | category | none | `design` | Limuru|Njabini|UoN |
| `instn` | INSTN | category | none | `context` | CIP381381.13|CIP381381.20|CIP800048|Dutch Robyjn|Kenya Karib |
| `accename` | ACCENAME | category | none | `context` | Asante|Desiree|Dutch Robyjn|Kenya Karibu|Kenya Mavuno|Kenya  |
| `audpc` | AUDPC | number | none | `context` | 0-3181.5 |
| `raudpc` | rAUDPC | number | none | `context` | 0-0.9975 |
| `ttya` | TTYA | number | none | `context` | 0-45.845 |
| `rlb` | RLB | category | none | `context` | Moderately Resistant|Resistant|Susceptible |

## Confirmar antes de usar

1. **Unidad de observacion**: ¿que representa una fila?
2. **Variable de resultado**: ¿cual es el `outcome`? Ahora todas figuran como `context`.
3. **Columnas calculadas despues del resultado**: son el `leakage` del ejercicio.
4. **Columnas de diseño**: revisar las marcadas `design` abajo, y agregar las que falten.
5. **Unidades**: las deducidas del nombre de la columna estan sin verificar.
6. **Relaciones conocidas**: ¿alguna que exista de verdad, y alguna que se sepa que no?

Los roles validos son: `primary_key`, `design`, `context`, `predictor`, `outcome`,
`outcome_secondary`, `confounded_exposure`, `leakage`, `null`.

Marcadas como `design` por el nombre: `plot`, `treatment`, `site`.

## Siguiente paso

Editar `tizon_tardio_dictionary.csv` con las respuestas de arriba y despues:

```bash
python scripts/corrupt_dataset.py datasets/tizon_tardio/tizon_tardio_clean.csv
```

## Configuración del taller (`configurar_taller.py`)

- 11 entradas de configuración aplicadas. Diccionario completo en `tizon_tardio_dictionary_completo.csv`; en `tizon_tardio_dictionary.csv` (participantes) las 2 columnas leakage aparecen como `predictor`.

Preguntas para quien produjo los datos:

1. ¿El resultado es `audpc`? Si es así, `raudpc` y `rlb` son leakage (se calculan a partir de él).
2. `rlb` usa texto (Resistant, Susceptible...) y el diccionario una escala numérica de 7 puntos: ¿cuál se usa?
