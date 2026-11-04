# Morfología: ¿qué hace parecidas a dos variedades?

## La historia

En 2014, el banco de germoplasma del CIP describió **70 variedades de papa seleccionadas en 22
países**, de Perú a Bangladesh. A cada una se le registró el color de la piel y de la pulpa, cómo se
distribuye el color secundario, la forma del tubérculo y la profundidad de sus ojos, siguiendo la guía
de caracterización morfológica de papas nativas.

El archivo trae errores. Tu trabajo es dejarlo listo para encontrar patrones entre las variedades.

## Tu pregunta

> **¿Qué descriptores de color y forma agrupan a las variedades, y cuáles dicen casi lo mismo
> (son redundantes)?**

Aquí no hay una variable de resultado: el ejercicio es **descubrir grupos**.

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `morfologia_dirty.csv` | **Tu punto de partida**: 72 filas con errores sembrados a propósito |
| `morfologia_dictionary.csv` | Qué significa cada columna, su unidad y su rango válido |
| `README.md` | Este documento |
| `morfologia_clean.csv` | La versión limpia de referencia. **No la abras hasta terminar**: es contra la que se mide tu trabajo |
| `originales/` | Los archivos tal como los entregó el equipo que produjo los datos |

Los demás archivos (`changelog`, `defect_key`, `ADAPTATION`, `dictionary_completo`) son para
facilitadores: dicen exactamente qué se rompió. Mirarlos antes de tiempo arruina el ejercicio.

**Una fila es una variedad (accesión)**. Se identifica con `number`.

## Columnas clave

| Grupo | Columnas | Qué son |
|---|---|---|
| Identidad | `number`, `accession_number`, `accession_name`, `country_of_selection` | Qué variedad es y de dónde viene |
| Piel | `tuber_skin_predominant_color`, `tuber_skin_secondary_color`, `distribution_of_secondary_color` | Colores de la piel y cómo se reparte el secundario |
| Pulpa | `tuber_flesh_predominant_color`, `tuber_flesh_secondary_color`, `tuber_flesh_secondary_color_distribution` | Colores de la pulpa |
| Forma | `tuber_shape`, `tuber_shape_unusual`, `tuber_shape_depth_of_eyes` | Forma general, formas raras y profundidad de ojos |

## Antes de analizar: limpia

El archivo trae filas repetidas, celdas vacías, códigos fuera de rango y nombres con espacios o
mayúsculas de más. Usa el diccionario para saber qué códigos son válidos.

- **Repara, no borres.** Eliminar una fila con un error no cuenta como arreglarla.
- **No toques lo que está bien.** Cambiar celdas sanas también se mide.
- **Anota tus decisiones.** Necesitarás tres para tu Data-Driven Document.

Al final, entrega tu archivo limpio: el facilitador medirá qué porcentaje de los errores reparaste.

## Ojo al analizar

Los colores y las formas son **códigos, no cantidades**. El color 6 no es "el doble" del color 3, y
promediarlos no tiene sentido. Trátalos como categorías al buscar grupos.

## Lo que estos datos no pueden decir

- **Parecerse no es estar emparentado.** Dos variedades con el mismo color y forma pueden tener
  orígenes genéticos muy distintos.
- **La muestra no está equilibrada**: 26 de las 70 variedades son de Perú, y varios países tienen una
  sola. No sirve para comparar la diversidad entre países.

## Para tu Data-Driven Document

Una pregunta, los datos con sus decisiones de limpieza, una visualización, un resultado con su
incertidumbre, dos o tres fuentes de la literatura, **una afirmación respaldada**, **una afirmación
que no puedes hacer** y cómo verificaste el trabajo de la IA.

*Datos reales del CIP, compartidos solo para este taller. No los redistribuyas.*
