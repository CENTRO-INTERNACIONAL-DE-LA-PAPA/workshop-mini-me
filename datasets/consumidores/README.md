# Consumidores: ¿quién pagaría un precio justo por las papas nativas de color?

## La historia

En junio de 2015, tres encuestadores entrevistaron a **114 personas en La Molina, Miraflores y San
Isidro** (Lima) sobre las papas nativas de color: si las conocen, con qué frecuencia las comen, cómo
las preparan, dónde las compran, qué valoran de ellas y qué piensan de una campaña para promoverlas
en supermercados.

La encuesta está **anonimizada**: cada persona y cada encuestador aparecen solo con un código. El
archivo trae errores. Tu trabajo es dejarlo listo para entender qué mueve a estos consumidores.

## Tu pregunta

> **¿Qué valoran los consumidores de las papas nativas de color, y cómo se relaciona con su
> disposición a pagar un precio justo al agricultor?**

## Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `consumidores_dirty.csv` | **Tu punto de partida**: 117 filas con errores sembrados a propósito |
| `consumidores_dictionary.csv` | Qué significa cada columna, su unidad y su rango válido |
| `README.md` | Este documento |
| `consumidores_clean.csv` | La versión limpia de referencia. **No la abras hasta terminar**: es contra la que se mide tu trabajo |
| `originales/` | Los archivos tal como los entregó el equipo que produjo los datos |

Los demás archivos (`changelog`, `defect_key`, `ADAPTATION`, `dictionary_completo`) son para
facilitadores: dicen exactamente qué se rompió. Mirarlos antes de tiempo arruina el ejercicio.

**Una fila es una persona encuestada.** Se identifica con `encuestado`.

## Columnas clave

| Grupo | Columnas | Tipo de respuesta |
|---|---|---|
| Encuesta | `encuesta`, `distrito`, `fecha`, `encuestador` | Quién, dónde y cuándo se encuestó |
| Persona | `sexo`, `edad` | F/M y años |
| Conocimiento y consumo | `v1…` a `v6…` | Casillas: 1 = marcó la opción, 0 = no la marcó |
| Qué valora al comprar | `v7…` | 1 muy importante, 2 importante, 3 poco importante |
| Qué opina de ellas | `v8…` | Escala de 1 a 3 (ver diccionario) |
| Acuerdo con afirmaciones | `v9…`, `v11…` | 1 muy de acuerdo … 4 total desacuerdo; **5 = no sé** |
| Por dónde se enteró | `v10…` | Casillas: 1 = marcó la opción, 0 = no la marcó |

El resultado que interesa es **`v9pagarpreciojustoalagricultor`**: qué tan de acuerdo está la persona
con pagar un precio justo al agricultor.

## Antes de analizar: limpia

El archivo trae filas repetidas, celdas vacías, respuestas fuera de escala, fechas en varios formatos
y categorías escritas de varias formas. Usa el diccionario para saber qué respuestas son posibles.

- **Repara, no borres.** Eliminar una fila con un error no cuenta como arreglarla.
- **No toques lo que está bien.** Cambiar celdas sanas también se mide.
- **Anota tus decisiones.** Necesitarás tres para tu Data-Driven Document.

Al final, entrega tu archivo limpio: el facilitador medirá qué porcentaje de los errores reparaste.

## Ojo al analizar

- En `v9` y `v11`, **el 5 significa "no sé"**: no es "más en desacuerdo que el 4". Decide cómo
  tratarlo y explícalo.
- Hubo **tres encuestadores**. Si las respuestas cambian mucho según quién preguntó, eso también es un
  hallazgo.

## Lo que estos datos no pueden decir

- **No representan a Lima ni al Perú**: son 114 personas de solo tres distritos.
- **Es una encuesta, no un experimento.** Si quienes valoran la nutrición también están más
  dispuestos a pagar un precio justo, eso es una asociación: no prueba que una cosa cause la otra.
- Decir que pagarías un precio justo no es lo mismo que pagarlo: la encuesta mide intención, no
  compras.

## Para tu Data-Driven Document

Una pregunta, los datos con sus decisiones de limpieza, una visualización, un resultado con su
incertidumbre, dos o tres fuentes de la literatura, **una afirmación respaldada**, **una afirmación
que no puedes hacer** y cómo verificaste el trabajo de la IA.

*Datos reales del CIP, compartidos solo para este taller. No los redistribuyas.*
