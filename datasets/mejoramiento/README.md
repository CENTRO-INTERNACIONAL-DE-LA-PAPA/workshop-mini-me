# Mejoramiento: ¿qué genotipos rinden más, y en todas partes?

## La historia

Un equipo de mejoramiento del CIP sembró **30 genotipos de papa**, muchos de ellos variedades
nativas, en **tres localidades de la sierra central del Perú**: Ccasapata (Paucara, Huancavelica,
3766 m), Ccollpaccasa (Paucara, Huancavelica, 4068 m) y La Victoria (San Agustín, Huancayo, Junín,
3216 m). En cada localidad, cada genotipo se sembró en **3 repeticiones**, y al cosechar se
contaron y pesaron los tubérculos de cada parcela, separando los comerciales de los no comerciales.
Es un ensayo de **estabilidad** (código `PTYL200911`): busca saber no solo qué genotipo rinde más,
sino si rinde bien en todos los ambientes.

El archivo pasó por varias manos antes de llegar a ti, y trae errores. Tu trabajo es dejarlo listo
para responder la pregunta del equipo.

## Tu pregunta

> **¿Qué genotipos rinden más?** ¿Son los mismos en las tres localidades, o el mejor de un sitio
> no es el mejor en otro?

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `mejoramiento_dirty.csv` | **Tu punto de partida**: 274 filas con errores sembrados a propósito |
| `mejoramiento_dictionary.csv` | Qué significa cada columna, su unidad y su rango válido |
| `README.md` | Este documento |
| `mejoramiento_clean.csv` | La versión limpia de referencia. **No la abras hasta terminar**: es contra la que se mide tu trabajo |
| `originales/` | El archivo tal como lo entregó el equipo que produjo los datos |

Los demás archivos (`changelog`, `defect_key`, `ADAPTATION`, `dictionary_completo`) son para
facilitadores: dicen exactamente qué se rompió. Mirarlos antes de tiempo arruina el ejercicio.

**Una fila es una parcela**: un genotipo, en una repetición, en una localidad. Se identifica con
`record_id`. El número de `plot` se repite entre localidades, así que no sirve solo como
identificador.

## Columnas clave

| Grupo | Columnas | Qué son |
|---|---|---|
| Lugar | `trial`, `site_code`, `region` … `locality`, `elevation_m`, `latitude`, `longitude` | Dónde está cada campo |
| Diseño | `locality`, `rep`, `plot` | Localidad, repetición y parcela |
| Genotipo | `instn`, `variety_name` | Código CIP y nombre de la variedad |
| Siembra y cosecha | `ntp`, `nph`, `pph` | Tubérculos sembrados, plantas cosechadas y su proporción |
| Tubérculos | `tntp`, `tntpl`, `nmtp`, `nmtpl`, `nnomtp` | Número de tubérculos: totales, comerciales y no comerciales |
| Peso y rendimiento | `ttwp`, `ttwpl`, `ttyna`, `ttya`, `mtwp`, `mtwpl`, `mtyna`, `mtya`, `nomtwp` | Peso cosechado y rendimiento (t/ha), total y comercial |
| Tamaño | `atw`, `atmw` | Peso medio del tubérculo, total y comercial |

El resultado que interesa es **`ttya`, el rendimiento total ajustado (t/ha)**.

## Antes de analizar: limpia

El archivo trae los errores típicos de una base de campo: filas repetidas, celdas vacías, valores
imposibles, unidades mezcladas y nombres de lugares escritos de varias formas. Usa el diccionario
para decidir qué es posible y qué no.

- **Repara, no borres.** Eliminar una fila con un error no cuenta como arreglarla.
- **No toques lo que está bien.** Cambiar celdas sanas también se mide.
- **Anota tus decisiones.** Las necesitarás para explicar tu trabajo.

Al final, entrega tu archivo limpio: el facilitador medirá qué porcentaje de los errores reparaste.

## Ojo al modelar

Algunas columnas se calculan **a partir del mismo resultado** que quieres explicar, o son una parte
de él. Si las usas para predecir el rendimiento, el modelo parecerá excelente sin haber aprendido
nada. Identifícalas antes de modelar y explica por qué las dejas fuera.

## Lo que estos datos no pueden decir

- **Son tres localidades de una sola campaña.** Puedes comparar la estabilidad de los genotipos
  entre estos tres sitios, pero no cómo rendirán en otro año, con otro clima.
- Que un genotipo rinda más en estas localidades no prueba que sea "mejor" en general: puede estar
  adaptado a la sierra central.
- Algunas parcelas se perdieron: no todos los genotipos tienen el mismo número de datos en cada
  localidad.

*Datos reales del CIP, compartidos solo para este taller. No los redistribuyas.*
