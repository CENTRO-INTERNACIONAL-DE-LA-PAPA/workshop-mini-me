# Tizón tardío: ¿funcionan los fosfonatos?

## La historia

El tizón tardío es una de las enfermedades más destructivas de la papa. En **tres localidades de
Kenia** (Limuru, Njabini y la Universidad de Nairobi), un ensayo comparó cómo avanzaba la enfermedad
en varias variedades bajo tres tipos de manejo: **sin fungicida (control)**, **fungicida
convencional** y **fosfonatos**, una alternativa con distintas dosis.

Para medir la enfermedad se usa el **AUDPC**: el área bajo la curva de progreso del tizón a lo largo
de la temporada. **Más AUDPC significa más enfermedad.**

El archivo trae errores. Tu trabajo es dejarlo listo para responder la pregunta del ensayo.

## Tu pregunta

> **¿Los fosfonatos reducen el tizón tardío frente al control? ¿El efecto depende de la variedad o de
> la localidad?**

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `tizon_tardio_dirty.csv` | **Tu punto de partida**: 194 filas con errores sembrados a propósito |
| `tizon_tardio_dictionary.csv` | Qué significa cada columna, su unidad y su rango válido |
| `README.md` | Este documento |
| `tizon_tardio_clean.csv` | La versión limpia de referencia. **No la abras hasta terminar**: es contra la que se mide tu trabajo |
| `originales/` | Los archivos tal como los entregó el equipo que produjo los datos |

Los demás archivos (`changelog`, `defect_key`, `ADAPTATION`, `dictionary_completo`) son para
facilitadores: dicen exactamente qué se rompió. Mirarlos antes de tiempo arruina el ejercicio.

**Una fila es una parcela**: una variedad, con un tratamiento, en una repetición y una localidad. Se
identifica con `record_id`.

## Columnas clave

| Grupo | Columnas | Qué son |
|---|---|---|
| Diseño | `site`, `rep`, `plot` | Localidad, repetición y parcela |
| Tratamiento | `class`, `treatment` | Tipo de manejo (control, convencional, fosfonato) y producto o dosis |
| Variedad | `instn`, `accename` | Código y nombre de la variedad |
| Enfermedad | `audpc`, `raudpc`, `rlb` | Avance del tizón y clasificación de resistencia |
| Rendimiento | `ttya` | Rendimiento ajustado (t/ha), un resultado secundario |

El resultado que interesa es **`audpc`**.

## Antes de analizar: limpia

El archivo trae filas repetidas, celdas vacías, valores imposibles, unidades mezcladas y categorías
escritas de varias formas (mayúsculas, espacios de más). Usa el diccionario para saber qué valores
son válidos.

- **Repara, no borres.** Eliminar una fila con un error no cuenta como arreglarla.
- **No toques lo que está bien.** Cambiar celdas sanas también se mide.
- **Anota tus decisiones.** Necesitarás tres para tu Data-Driven Document.

Al final, entrega tu archivo limpio: el facilitador medirá qué porcentaje de los errores reparaste.

## Ojo al modelar

Algunas columnas se calculan **a partir del mismo resultado** que quieres explicar. Si las usas para
predecir el AUDPC, el modelo parecerá excelente sin haber aprendido nada. Identifícalas antes de
modelar y explica por qué las dejas fuera.

## Lo que estos datos sí y no pueden decir

- **Es un experimento**: los tratamientos se asignaron a propósito. Por eso aquí sí puedes hablar del
  *efecto* del tratamiento sobre la enfermedad, siempre que compares dentro de la misma localidad y
  repetición.
- Ese efecto vale **para estas variedades y estas tres localidades**. No dice cómo funcionarán los
  fosfonatos en otra región, con otro clima o en otro año.
- No todas las combinaciones de localidad, variedad y tratamiento tienen el mismo número de parcelas:
  revísalo antes de comparar.

## Para tu Data-Driven Document

Una pregunta, los datos con sus decisiones de limpieza, una visualización, un resultado con su
incertidumbre, dos o tres fuentes de la literatura, **una afirmación respaldada**, **una afirmación
que no puedes hacer** y cómo verificaste el trabajo de la IA.

*Datos reales del CIP, compartidos solo para este taller. No los redistribuyas.*
