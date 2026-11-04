# Mejoramiento: ¿qué genotipos rinden más?

## La historia

En 2016, un equipo de mejoramiento del CIP sembró **61 genotipos de papa** en La Victoria (San
Agustín, Huancayo, Junín), a más de 3 000 m de altitud. Cada genotipo se sembró en **4 repeticiones**,
y al cosechar se contaron y pesaron los tubérculos de cada parcela.

El archivo pasó por varias manos antes de llegar a ti, y trae errores. Tu trabajo es dejarlo listo
para responder la pregunta del equipo.

## Tu pregunta

> **¿Qué genotipos rinden más?** ¿Las diferencias entre ellos son claras o se confunden con la
> variación entre repeticiones?

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `mejoramiento_dirty.csv` | **Tu punto de partida**: 250 filas con errores sembrados a propósito |
| `mejoramiento_dictionary.csv` | Qué significa cada columna, su unidad y su rango válido |
| `README.md` | Este documento |
| `mejoramiento_clean.csv` | La versión limpia de referencia. **No la abras hasta terminar**: es contra la que se mide tu trabajo |
| `originales/` | Los archivos tal como los entregó el equipo que produjo los datos |

Los demás archivos (`changelog`, `defect_key`, `ADAPTATION`, `dictionary_completo`) son para
facilitadores: dicen exactamente qué se rompió. Mirarlos antes de tiempo arruina el ejercicio.

**Una fila es una parcela**: un genotipo en una repetición. Se identifica con `plot`.

## Columnas clave

| Grupo | Columnas | Qué son |
|---|---|---|
| Diseño | `instn`, `rep`, `plot` | Genotipo, repetición y parcela |
| Lugar | `country` … `adm3`, `location`, `elevation`, `latitude`, `longitude` | Dónde está el campo |
| Siembra y cosecha | `ntp`, `nph`, `pph` | Tubérculos sembrados, plantas cosechadas y su proporción |
| Tubérculos | `tntp`, `tntpl`, `atw` | Número de tubérculos por parcela y por planta, y peso medio |
| Peso y rendimiento | `ttwp`, `ttwpl`, `ttyna`, `ttya` | Peso cosechado y rendimiento en t/ha |

El resultado que interesa es **`ttya`, el rendimiento ajustado (t/ha)**.

## Antes de analizar: limpia

El archivo trae los errores típicos de una base de campo: filas repetidas, celdas vacías, valores
imposibles y unidades mezcladas. Usa el diccionario para decidir qué es posible y qué no.

- **Repara, no borres.** Eliminar una fila con un error no cuenta como arreglarla.
- **No toques lo que está bien.** Cambiar celdas sanas también se mide.
- **Anota tus decisiones.** Necesitarás tres para tu Data-Driven Document.

Al final, entrega tu archivo limpio: el facilitador medirá qué porcentaje de los errores reparaste.

## Ojo al modelar

Algunas columnas se calculan **a partir del mismo resultado** que quieres explicar. Si las usas para
predecir el rendimiento, el modelo parecerá excelente sin haber aprendido nada. Identifícalas antes
de modelar y explica por qué las dejas fuera.

## Lo que estos datos no pueden decir

- **Hay una sola localidad y un solo año.** Puedes comparar genotipos en La Victoria en 2016, pero no
  decir cuál es más estable entre ambientes ni cómo rendirá en otro lugar.
- Que un genotipo rinda más aquí no prueba que sea "mejor" en general: puede estar adaptado a este
  sitio en particular.

## Para tu Data-Driven Document

Una pregunta, los datos con sus decisiones de limpieza, una visualización, un resultado con su
incertidumbre, dos o tres fuentes de la literatura, **una afirmación respaldada**, **una afirmación
que no puedes hacer** y cómo verificaste el trabajo de la IA.

*Datos reales del CIP, compartidos solo para este taller. No los redistribuyas.*
