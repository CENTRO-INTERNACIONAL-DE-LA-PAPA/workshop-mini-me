# Adaptacion — morfologia

Origen: `02_Datos_morfologicos_2014.xlsx`  ·  70 filas  ·  13 columnas

Este archivo deja por escrito todo lo que el adaptador dedujo. **La estructura se puede
inferir; el significado no.** Lo de abajo hay que confirmarlo con quien conoce los datos.

## Lo que se hizo

- `Number` -> `number`
- `Accession Number` -> `accession_number`
- `Accession Name` -> `accession_name`
- `Country of selection` -> `country_of_selection`
- `Tuber Skin Predominant Color` -> `tuber_skin_predominant_color`
- `Tuber Skin Secondary Color` -> `tuber_skin_secondary_color`
- `Distribution of Secondary Color` -> `distribution_of_secondary_color`
- `Tuber Flesh Predominant Color` -> `tuber_flesh_predominant_color`
- `Tuber Flesh Secondary Color` -> `tuber_flesh_secondary_color`
- `Tuber Flesh secondary color distribution` -> `tuber_flesh_secondary_color_distribution`
- `Tuber Shape` -> `tuber_shape`
- `Tuber shape unusual` -> `tuber_shape_unusual`
- `Tuber Shape Depth of Eyes` -> `tuber_shape_depth_of_eyes`
- Identificador unico encontrado: `number`.

## Tipos y unidades deducidos

| Columna | Original | Tipo | Unidad | Rol propuesto | Rango observado |
|---|---|---|---|---|---|
| `number` | Number | integer | none | `primary_key` | unique |
| `accession_number` | Accession Number | string | none | `design` |  |
| `accession_name` | Accession Name | string | none | `design` |  |
| `country_of_selection` | Country of selection | string | none | `context` |  |
| `tuber_skin_predominant_color` | Tuber Skin Predominant Color | integer | none | `context` | 0-10 |
| `tuber_skin_secondary_color` | Tuber Skin Secondary Color | integer | none | `context` | 0-9 |
| `distribution_of_secondary_color` | Distribution of Secondary Color | integer | none | `context` | 0-8 |
| `tuber_flesh_predominant_color` | Tuber Flesh Predominant Color | integer | none | `context` | 0-5 |
| `tuber_flesh_secondary_color` | Tuber Flesh Secondary Color | integer | none | `context` | 0-9 |
| `tuber_flesh_secondary_color_distribution` | Tuber Flesh secondary color distribution | integer | none | `context` | 0-4 |
| `tuber_shape` | Tuber Shape | integer | none | `context` | 0-8 |
| `tuber_shape_unusual` | Tuber shape unusual | integer | none | `context` | 0-1 |
| `tuber_shape_depth_of_eyes` | Tuber Shape Depth of Eyes | integer | none | `context` | 0-8 |

## Confirmar antes de usar

1. **Unidad de observacion**: ¿que representa una fila?
2. **Variable de resultado**: ¿cual es el `outcome`? Ahora todas figuran como `context`.
3. **Columnas calculadas despues del resultado**: son el `leakage` del ejercicio.
4. **Columnas de diseño**: revisar las marcadas `design` abajo, y agregar las que falten.
5. **Unidades**: las deducidas del nombre de la columna estan sin verificar.
6. **Relaciones conocidas**: ¿alguna que exista de verdad, y alguna que se sepa que no?

Los roles validos son: `primary_key`, `design`, `context`, `predictor`, `outcome`,
`outcome_secondary`, `confounded_exposure`, `leakage`, `null`.

Marcadas como `design` por el nombre: `accession_number`, `accession_name`.

## Siguiente paso

Editar `morfologia_dictionary.csv` con las respuestas de arriba y despues:

```bash
python scripts/corrupt_dataset.py datasets/morfologia/morfologia_clean.csv
```

## Configuración del taller (`configurar_taller.py`)

- 12 entradas de configuración aplicadas. Diccionario completo en `morfologia_dictionary_completo.csv`; en `morfologia_dictionary.csv` (participantes) las 0 columnas leakage aparecen como `predictor`.

Preguntas para quien produjo los datos:

1. No hay variable de resultado: el ejercicio es agrupar accesiones por descriptores. ¿Correcto?
2. Los colores y formas son códigos: ¿hay una tabla de códigos para el diccionario?
