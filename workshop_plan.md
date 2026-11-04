# Workshop Mini-Me — Plan de ejecución (v3, un día)

**CIP Mini-Me: IA aplicada a la ciencia de datos.** De datos crudos a un Data-Driven Document en un solo día.

| Campo | Valor |
|---|---|
| Fecha | **martes 24 de noviembre de 2026** (confirmada) |
| Hora | **8:00 a.m. a 1:30 p.m.** |
| Sede | **Auditorio** del CIP |
| Organiza | **Unidad Digital & Data del CIP** (desarrolladora de Mini-Me) |
| Duración | **5 h efectivas** + 30 min de setup (ver §3.3 para recortes y extensiones) |
| Participantes | 20–30 personas, en equipos de 2–3 |
| Modalidad | Presencial, laptops propias con WSL2 preinstalado |
| Herramientas | **Mini-Me Desktop** (`mini-me-desktop`) + backend en WSL; herramientas de **Allen AI**: Asta (Paper Finder, PDF librarian), Theorizer y AutoDiscovery |
| Entregable del participante | **Data-Driven Document** (1–2 páginas, con evidencia trazable) |
| Medición | Mentimeter **pre** y **post** + score de limpieza automatizado |
| Fecha de este plan | 4 de noviembre de 2026 (T-20 días) |

> **Cambios de la v3 (4 de noviembre).** La fecha pasa del 22 de octubre al **24 de noviembre**, con inicio
> a las 8:00. El Bloque 2 deja fuera **DataVoyager**: la literatura se trabaja con Asta, Theorizer queda
> como demostración y AutoDiscovery entra cuando no se sabe por dónde empezar a analizar. Los bloques 1 y
> 2 abren con **presentaciones narrativas** en Quarto + Reveal.js (§5.7). Se agregan la nota de concepto
> y el formulario de registro (§5.8). El cronograma se rehízo para la nueva fecha (§6).
>
> **Cambios de la v2.** La v1 (3 días, dataset sintético único) queda archivada en
> `workshop_plan_v1_3dias.bak.md`. La v2 comprimió todo a **un día con tres bloques**, cambió el dataset
> sintético por **datos reales de CIP ensuciados de forma controlada** (4 temáticas) y añadió el eje de
> **medición antes/después**.

---

## 1. Concepto

Un solo hilo narrativo, tres bloques, un entregable:

```
Bloque 1  Data Lifecycle      ->  el científico entiende y arregla sus datos
Bloque 2  Allen AI            ->  el científico busca, lee y contrasta evidencia
Bloque 3  Hands-on            ->  el científico produce un documento defendible
                                   |
                                   v
                          Data-Driven Document
```

El mensaje central del día, que debe repetirse en cada bloque:

> **La IA acelera tareas; el científico mantiene la responsabilidad sobre la pregunta, los datos, la
> evidencia y la interpretación.**

El mensaje se cuenta **en positivo**: la IA es una fortaleza cuando se usa con criterio, no algo de lo
que desconfiar. Las presentaciones lo dicen con dos frases de cierre: *"La IA acelera el recorrido; Isabel
le da dirección"* (Bloque 1) y *"La IA busca, lee y propone; Isabel decide qué es evidencia"* (Bloque 2).

### 1.1 Resultados esperados

Al terminar, cada participante debe poder:

1. Nombrar las 7 etapas del ciclo de vida del dato y el subagente que corresponde a cada una.
2. Detectar y **documentar** problemas de calidad en un dataset real de su área.
3. Distinguir exploración, diagnóstico, predicción y causalidad.
4. Buscar y leer literatura con Asta (Paper Finder y PDF librarian), y reconocer cuándo usar Theorizer
   (hipótesis) y AutoDiscovery (cuando no se sabe por dónde empezar a analizar).
5. Verificar un resultado de IA: fuentes, código, archivos, estado de ejecución.
6. Identificar al menos **un error o límite** de la IA durante el día.
7. Entregar un Data-Driven Document con una afirmación respaldada y una afirmación que **no** puede hacerse.

---

## 2. Datos — las 4 temáticas de Vilma

Responsable de la entrega: **Vilma**. Los datos llegaron el **4 de noviembre** (un `.zip` con 8 archivos:
datos y diccionario por temática). Dos temáticas cambiaron respecto a lo planeado: la enfermedad es **tizón
tardío** (no Bactericera) y la encuesta es de **percepción de consumidores** (no de adopción en agricultores).

| # | Temática (slug) | Fuente | Unidad de observación | Pregunta de investigación propuesta |
|---|---|---|---|---|
| 1 | **Morfología** (`morfologia`) | Banco de germoplasma, 2014: 70 variedades de 22 países | Accesión | ¿Qué descriptores de color y forma agrupan las variedades y cuáles son redundantes? |
| 2 | **Mejoramiento** (`mejoramiento`) | Ensayo de rendimiento 2016 en La Victoria (Huancayo): 61 genotipos × 4 repeticiones | Parcela | ¿Qué genotipos rinden más? *(Hay una sola localidad: la pregunta de estabilidad entre ambientes ya no aplica)* |
| 3 | **Tizón tardío** (`tizon_tardio`) | Ensayo de fungicidas en 3 localidades de Kenia: control, convencional y fosfonatos | Parcela | ¿Los fosfonatos reducen el tizón (AUDPC) frente al control, y depende de la variedad o la localidad? |
| 4 | **Consumidores** (`consumidores`) | Encuesta 2015 en La Molina, Miraflores y San Isidro: 114 personas | Persona encuestada | ¿Qué valoran los consumidores de papas nativas de color y cómo se asocia con su disposición a pagar un precio justo al agricultor? |

Las preguntas, los resultados y los *leakage* son **propuestas** tomadas de los diccionarios de Vilma.
Confirmarlos con ella (las preguntas abiertas están al final de cada `<slug>_ADAPTATION.md`).

### 2.1 Cada paquete entregado al participante contiene

```
datasets/<tematica>/
  <tematica>_dirty.csv        <- punto de partida del participante
  <tematica>_clean.csv        <- benchmark del facilitador (NO se distribuye durante el ejercicio)
  <tematica>_dictionary.csv   <- tipo, unidad, rol analítico, rango válido, descripción
  README.md                   <- brief, pregunta(s), unidad de observación, limitación causal
  FACILITATOR.md              <- clave de defectos: familia de corrupción y filas afectadas
```

Esta es la estructura canónica que produce el pipeline (§2.2 y §2.3), y sobre la que ya funcionan el
scorer y los materiales del manual.

### 2.2 Normalización — Vilma entrega en su estructura, nosotros adaptamos

**Vilma manda sus datos y sus diccionarios con la estructura que ya usa.** No le pedimos que se adapte a un
formato nuestro: sus archivos son su trabajo y reformatearlos es nuestro problema, no el suyo. Lo que
recibiremos son CSV o Excel con nombres de columna en español, diccionarios con campos distintos a los
nuestros, y probablemente sin una columna identificadora única.

El puente lo pone **`scripts/adapt_dataset.py`** (nuevo, ver M3), que toma lo que ella mande y produce el
paquete canónico de §2.1:

| Lo que llega | Lo que hace el adaptador |
|---|---|
| Excel o CSV, cualquier codificación | Normaliza a CSV UTF-8 |
| Nombres de columna en español, con espacios o tildes | Conserva el nombre original en el diccionario y genera un slug estable |
| Sin identificador único de fila | **Sintetiza `record_id` correlativo** — así desaparece la dependencia dura |
| Diccionario de Vilma en su propio formato | Mapea sus campos a `column, data_type, unit, role, valid_values_or_range, description` |
| Sin roles analíticos declarados | **Propone** roles (`primary_key`, `design`, `predictor`, `outcome`) para que nosotros los confirmemos |

**Lo que el adaptador no puede deducir lo fija `scripts/configurar_taller.py`.** Toma de los diccionarios
de Vilma (plantillas de Crop Ontology para los ensayos y la lista de variables de la encuesta) las unidades,
los rangos válidos y las descripciones, y propone el resultado y los *leakage* de cada temática. Se corre
entre el adaptador y `corrupt_dataset.py`, y vive en el repositorio para que volver a adaptar no borre esas
decisiones. En la encuesta, además, convierte en 0 las casillas vacías ("no marcado"), para que un faltante
sembrado se distinga de un "no".

Esto importa por una razón concreta: `score_cleanliness.py:50` exige exactamente una columna con
`role=primary_key` y falla si no la encuentra. Sintetizar el identificador en el adaptador resuelve ese
requisito sin pedirle nada a nadie.

**Lo único que sí necesitamos preguntarle a Vilma** — y son preguntas de significado, no de formato, que se
responden en un correo o en 20 minutos de llamada por temática:

1. ¿Cuál es la unidad de observación? (¿una fila es una parcela, una planta, una accesión, un hogar?)
2. ¿Cuál es la variable de resultado que interesa? (rendimiento, incidencia, adopción...)
3. ¿Qué columnas se calculan **después** de conocer ese resultado? (son el *leakage* del ejercicio)
4. ¿Qué columnas describen el **diseño**? (sitio, bloque, campaña, lote)
5. ¿Qué unidad tiene cada variable numérica y qué rango es imposible? (para sembrar valores fuera de rango)
6. ¿Hay alguna relación que ella ya sepa que existe, y alguna que sepa que **no** existe?

Las respuestas 3 y 6 son las que permiten sembrar leakage y confusores con sentido agronómico en lugar de
inventados. Si no llegan, el ejercicio funciona igual pero pierde el valor de usar datos reales.

### 2.3 "Ensuciar la data" — cómo y por qué

Partimos del dato **real y ya limpio** de Vilma, y generamos la versión sucia de forma **determinística y
registrada**. Como conocemos el original, el score de limpieza es una métrica objetiva, no una opinión.

Familias de corrupción a sembrar (8–10 por dataset), reutilizando `corrupt_rows()` de
`scripts/generate_datasets.py`:

| Familia | Ejemplo |
|---|---|
| Duplicados exactos | ~3% de filas repetidas |
| Variantes de categoría | `Huánuco` / `Huanuco` / `HUANUCO` |
| Unidades mezcladas | altitud en m y en pies; severidad 0–1 y 0–100 |
| Valores imposibles | `soil_ph = 14.9`, rendimiento negativo |
| Faltantes no aleatorios | ausencias concentradas en un sitio o campaña |
| Formatos de fecha incompatibles | `2024-03-01` vs `01/03/24` |
| Espacios y tipografía | ` GEN-014`, `gen-014` |
| Leakage | una variable derivada del outcome que debe excluirse del modelo |

**Trabajo de ingeniería requerido (nuevo):** `scripts/corrupt_dataset.py` — toma el CSV canónico que sale
del adaptador (§2.2) y produce `dirty.csv` + `FACILITATOR.md` con la clave de defectos. Hoy la lógica de
corrupción vive acoplada al generador sintético (`generate_datasets.py:938`); hay que extraerla a un script
que acepte datos externos. **Ya está escrito y probado** (M3 cumplido): se construyó y validó contra los
paquetes sintéticos de `scripts/generate_datasets.py`, sin esperar a los datos reales. Falta únicamente
aplicarlo cuando lleguen.

**Nada se rompe al azar.** `corrupt_dataset.py` usa un RNG con semilla fija (`--seed`, por defecto
`20261022`): la misma semilla reproduce el archivo sucio byte por byte. Y cada celda modificada queda
registrada en un **changelog**:

| change_id | family | record_id | column | original_value | new_value | detail |
|---|---|---|---|---|---|---|
| C00042 | `mixed_unit` | PBT-0024 | altitude_m | 236.1 | 774.606 | m -> ft |
| C00118 | `category_variant` | PBT-0003 | site | La Molina | La  Molina | double inner space |

**La métrica que verá el participante** sale de ese log (`scripts/score_recovery.py`):

```bash
python scripts/score_recovery.py mi_archivo_limpio.csv
```

```
Reparacion: 21.5%  (59/274 defectos sembrados)

Familia               Reparados       %   Filas borradas
category_variant          26/26  100.0%                0
duplicate_row               7/7  100.0%                0
impossible_value          26/26  100.0%                0
missing_cell              0/160    0.0%                0
mixed_unit                 0/55    0.0%                0

Dano colateral: 1 celdas que no eran defecto y ahora difieren del original.
```

**Por qué esta métrica y no el score global.** Medimos `score_cleanliness.py` sobre los siete datasets del
repo: un archivo sucio ya puntúa **98.2–98.5 sobre 100**, así que limpiarlo entero se ve como una mejora de
dos puntos y no motiva a nadie. El porcentaje de reparación va de 0% a 100%, se desglosa por familia de
defecto y delata dos comportamientos que el score global esconde: **borrar filas** en lugar de arreglarlas, y
el **daño colateral** de modificar celdas que estaban bien.

`score_cleanliness.py` se sigue usando como control de esquema e integridad, con su ponderación de
esquema 15% · registros 20% · celdas 65%.

> Advertencia que debe decirse en voz alta: **100/100 no significa que el análisis sea correcto, insesgado o
> causal.** Limpieza y validez analítica se enseñan como preguntas separadas.

### 2.4 Protección de datos — bloqueante, resolver antes de M2

Los datos de Vilma son datos reales de CIP y las **encuestas a agricultores contienen datos personales**.
La política institucional prohíbe introducir datos confidenciales o personales en herramientas de IA, y el
stack Asta procesa los datos fuera de la máquina del participante.

**Estado (4 de noviembre):** la encuesta de consumidores llegó anonimizada y con visto bueno (confirmado por
Piero). Las columnas `encuestador` y `encuestado` son códigos, no nombres, y la ubicación está a nivel de
distrito. Los datos son públicos y tienen visto bueno, así que los paquetes completos se publican en
`datasets/` de este repositorio, junto con los originales, y se distribuyen por GitHub. El diccionario
de los participantes oculta el rol *leakage*; el completo queda en `<slug>_dictionary_completo.csv`.

Por eso, antes de que cualquier archivo entre al workshop:

1. **Anonimización obligatoria** de las encuestas: eliminar nombres, DNI, teléfonos, coordenadas exactas
   (degradar a distrito), y reemplazar identificadores por códigos correlativos sin diccionario reversible
   en el paquete distribuido.
2. **Revisión y visto bueno** del responsable del dato (Vilma) y, si aplica, del punto focal de datos de CIP,
   por escrito, para las cuatro temáticas.
3. Si una temática no obtiene visto bueno a tiempo, se sustituye por su equivalente sintético, que se
   regenera en un comando (`python scripts/generate_datasets.py --output-dir .`): `value_chain_adoption`
   para la encuesta, `potato_breeding_trials` para mejoramiento, `native_potato_biodiversity` para morfología,
   `climate_smart_agronomy` para tizón tardío. **El workshop no se detiene por un
   dataset.**
4. Investigación no publicada / propiedad intelectual de terceros: no se incluye nada inédito que no esté
   autorizado a salir.

---

## 3. Agenda del día

### 3.1 Bloque a bloque (versión canónica, 5 h)

| Hora | Min | Bloque | Contenido |
|---|---:|---|---|
| 08:00–08:30 | 30 | **B0 Setup** | Registro, verificación de laptops, login, API key, dataset descargado |
| 08:30–08:50 | 20 | **Apertura** | Encuadre + **Mentimeter PRE** + reglas del día |
| 08:50–09:50 | 60 | **B1 Data Lifecycle** | Presentación *El viaje de los datos* → demo en vivo: limpieza → validación → EDA → diagnóstico → predicción → reporte |
| 09:50–10:05 | 15 | Pausa | Café. *Se lanzan Theorizer y AutoDiscovery en background.* |
| 10:05–11:10 | 65 | **B2 Allen AI** | Presentación *De la pregunta al conocimiento* → Asta Paper Finder → PDF librarian → Theorizer (demo) → AutoDiscovery |
| 11:10–11:20 | 10 | Pausa | |
| 11:20–12:50 | 90 | **B3 Hands-on** | Dos rutas (Research / Data) sobre el dataset de su temática |
| 12:50–13:15 | 25 | **Galería** | Mural con todos los Data-Driven Documents + **2 presentaciones voluntarias** + síntesis |
| 13:15–13:30 | 15 | **Cierre** | **Mentimeter POST** + próximos pasos + entrega de materiales |

**B0 no es opcional.** Es el bloque que salva el día: 30 minutos de colchón para el 10–20% de laptops que
llegarán con algo roto pese a la instalación previa.

### 3.2 Detalle de cada bloque

#### B1 — Data Lifecycle (60 min)

Todo el bloque se hace **en vivo, con el facilitador proyectando** y los participantes replicando sobre el
dataset de su temática.

| Min | Etapa | Subagente | Producto visible |
|---:|---|---|---|
| 0–8 | Introducción | — | Presentación *El viaje de los datos* (§5.7): el ciclo dibujado paso a paso con la historia de Isabel |
| 8–20 | **Limpieza** | `data_cleaning` | `dirty` → `clean`, con log de decisiones |
| 20–28 | **Validación** | `data_cleaning` + diccionario | Score de limpieza antes/después |
| 28–40 | **EDA** | `exploratory_data_analysis` | Distribuciones, faltantes, relaciones, anomalías |
| 40–48 | **Diagnostics** | `diagnostic_analytics` | Variables explicativas, confusor, "¿por qué ocurrió?" |
| 48–55 | **Predictive** | `predictive_analytics` | Modelo + detección de *leakage* (demo, no ejercicio) |
| 55–60 | **Reporting** | `report_writer` | Informe de una página en PDF |

Dos trampas que el facilitador debe provocar a propósito:

- El **confusor**: alguien va a decir "la humedad causa el rendimiento". Corregir en el momento.
- El **leakage**: el modelo predictivo dará un R² sospechosamente alto. Que lo encuentren ellos.

> Nota de la auditoría vigente: `diagnostic_analytics` acepta el formulario de contexto vacío. Entregar
> plantilla obligatoria (pregunta, outcome, drivers, unidad de análisis, periodo, confusores) en la tarjeta.

#### B2 — Allen AI (65 min) — el bloque más intensivo

Todas las herramientas del bloque son de **Allen AI (Ai2)**. La literatura se trabaja con **Asta** (Paper
Finder y PDF librarian), las hipótesis con **Theorizer** y el análisis automatizado con **AutoDiscovery**.
**DataVoyager queda fuera del taller.**

**Regla de oro operativa:** Theorizer y AutoDiscovery se **lanzan en la pausa anterior** (09:50) para que sus
resultados lleguen dentro del bloque. Además, cada uno tiene un **run terminado de respaldo** en disco.

| Min | Herramienta | Subagente | Prompt / acción |
|---:|---|---|---|
| 0–7 | Encuadre | — | Presentación *De la pregunta al conocimiento* (§5.7): el gancho de las cifras y el bucle de investigación |
| 7–20 | **Asta · Paper Finder** | `academic_researcher` | "¿Qué evidencia existe sobre \<pregunta de la temática\>?" → 5 fuentes, una frase de por qué importa cada una |
| 20–32 | **Asta · PDF librarian** | `pdf_librarian` | Indexar 2–3 PDFs **abiertos, pre-descargados** y localizar pasajes |
| 32–42 | **Theorizer** (solo demo) | `hypothesis_generator` | El facilitador muestra el run lanzado en la pausa: hipótesis como propuestas para probar, no conclusiones |
| 42–65 | **AutoDiscovery** | `autodiscovery` | Para cuando no se sabe por dónde empezar: run pre-cocinado + presupuesto vivo de 3–5 experimentos (formato por confirmar, ver §8) |

Lo que los participantes **deben inspeccionar** en AutoDiscovery (esto es la lección, no el resultado):
hipótesis · prior y posterior · valor firmado de `surprise` · código ejecutado · método estadístico ·
limitaciones · si merece validación independiente.

Precauciones ya conocidas:

- No usar `research_planner` para armar el flujo del bloque: hoy no incluye `autodiscovery` entre sus
  acciones permitidas.
- Un mensaje de herramienta fallido puede producir un artefacto con apariencia exitosa. Enseñar a comprobar
  `status`, identificador de tarea y archivos reales en el panel de outputs.
- PDFs siempre locales; nunca depender de una descarga en vivo.

#### B3 — Hands-on (90 min)

Equipos de 2–3, cada equipo con **una** temática. Máximo tres subagentes por equipo: no gana quien usa más
herramientas, gana quien construye el argumento más verificable.

**Ruta 1 — Research** (para quien viene con una pregunta, no con datos). Sigue el bucle de la presentación
del Bloque 2:

```
Pregunta -> Paper Finder -> PDF librarian -> Analizar datos -> Report -> Data-Driven Document
                                             (AutoDiscovery si no sabes por dónde empezar;
                                              si no, el ciclo de datos de Mini-Me)
```

**Ruta 2 — Data** (para quien viene con un dataset):

```
Limpieza/Validación -> EDA -> Report
EDA -> Diagnostics -> Report
EDA -> Diagnostics -> Predictive -> Report
```

Ambas rutas convergen en el mismo entregable. Los equipos eligen ruta en los primeros 10 minutos.

| Min | Actividad |
|---:|---|
| 0–10 | Elegir ruta, pregunta, roles y subagentes |
| 10–70 | Trabajo con Mini-Me Desktop |
| 70–90 | Redacción del Data-Driven Document |

**Plantilla del Data-Driven Document** (1–2 páginas, es la tarjeta que se entrega impresa):

> Es un **ejercicio del workshop**: el registro de lo que el equipo hizo, encontró y no puede afirmar
> con sus datos en 90 minutos. No es una nota conceptual, una propuesta ni un insumo para financiamiento.

1. Pregunta científica.
2. Dataset y unidad de observación.
3. Score de limpieza antes → después, y 3 decisiones de limpieza documentadas.
4. Una visualización principal.
5. Un resultado cuantitativo con su incertidumbre.
6. 2–3 fuentes de la literatura.
7. **Una afirmación respaldada.**
8. **Una afirmación que NO puede hacerse con estos datos** (y por qué).
9. **Un error, omisión o exageración cometido por la IA durante la sesión.**
10. Próximo experimento recomendado.

#### Galería (25 min) — voluntaria

Con 10 equipos no alcanza el tiempo para que todos presenten, y forzarlo convierte el cierre en una fila de
turnos apurados. Formato:

| Min | Actividad |
|---:|---|
| 0–5 | **Mural**: los 10 Data-Driven Documents quedan pegados en la pared / subidos a la carpeta compartida |
| 5–13 | **Auditoría cruzada**: cada equipo lee el Data-Driven Document de otro y le deja una pregunta escrita |
| 13–23 | **Máximo 2 presentaciones voluntarias**, 5 min cada una |
| 23–25 | Síntesis del facilitador: los 3 patrones que aparecieron en el mural |

Los 2 grupos se ofrecen durante el hands-on, no en el momento; si nadie se ofrece, el facilitador presenta
uno del mural. **Todos los equipos entregan** su Data-Driven Document aunque no presenten — la entrega es el
requisito, la presentación es opcional.

Rúbrica (se aplica a **todos** los Data-Driven Documents entregados, no solo a los presentados): pregunta clara 15% · calidad y trazabilidad del dato 20% · método apropiado 20% ·
evidencia y reproducibilidad 20% · interpretación y límites 15% · comunicación 10%.

### 3.3 Cómo se recorta a 4 h y cómo se estira a 6 h

| Bloque | 4 h (mínimo viable) | 5 h (canónico) | 6 h (extendido) |
|---|---:|---:|---:|
| Apertura + Menti PRE | 15 | 20 | 20 |
| B1 Data Lifecycle | 45 | 60 | 60 |
| B2 Asta | 55 | 65 | 75 |
| B3 Hands-on | 60 | 90 | 120 |
| Galería | 15 | 25 | 35 |
| Cierre + Menti POST | 10 | 15 | 20 |
| Pausas | 20 | 25 | 30 |
| **Total** | **3 h 40** | **5 h 00** | **6 h 00** |

- **Para llegar a 4 h:** en B1 se elimina el ejercicio de `predictive_analytics` (queda solo como demo de
  2 min sobre leakage) y la galería queda solo como mural + auditoría cruzada, sin presentaciones.
- **Para llegar a 6 h:** se añade el módulo opcional **Bring Your Own Data** (45 min) — el participante trae
  su propio dataset y llena un **Data Passport** (propiedad, confidencialidad, unidad de observación, diseño,
  outcome, códigos de faltantes, herramientas permitidas, límites causales) antes de subir nada. Los datos
  sintéticos siguen siendo el respaldo para que nadie quede bloqueado ni presionado a subir datos sensibles.

---

## 4. Medición — Mentimeter pre/post

Mismo instrumento antes y después, para poder graficar el delta en vivo en el cierre.

### 4.1 Encuesta PRE (08:30, 5 min, 6 preguntas)

| # | Tipo | Pregunta |
|---|---|---|
| 1 | Escala 1–5 | ¿Qué tan cómodo/a te sientes limpiando y validando un dataset antes de analizarlo? |
| 2 | Escala 1–5 | ¿Qué tan cómodo/a te sientes distinguiendo correlación de causalidad en tu propio análisis? |
| 3 | Opción múltiple | ¿Cuánto tiempo te toma hoy pasar de datos crudos a un primer informe? (<1 día / 1–3 días / 1–2 semanas / >2 semanas) |
| 4 | Escala 1–5 | ¿Qué tanto confías hoy en un resultado producido por una IA sin verificarlo? |
| 5 | Multi-selección | ¿Cuáles de estas herramientas has usado? (Paper Finder / PDF librarian / Theorizer / AutoDiscovery / ninguna) |
| 6 | Nube de palabras | En una palabra: ¿qué esperas llevarte de hoy? |

### 4.2 Encuesta POST (13:15, 8 min)

Preguntas 1–5 **idénticas** (ese es el delta medible), más:

| # | Tipo | Pregunta |
|---|---|---|
| 7 | Sí/No | ¿Encontraste al menos un error o límite de la IA hoy? |
| 8 | Abierta | ¿Cuál fue? |
| 9 | Escala 1–5 | ¿Usarías Mini-Me en tu trabajo el próximo mes? |
| 10 | Abierta | ¿Qué te faltó / qué sobró? |
| 11 | Nube de palabras | En una palabra: ¿qué te llevas? |

### 4.3 Métricas objetivas (no autoreportadas)

| Métrica | Fuente | Meta |
|---|---|---|
| **% de defectos reparados** por equipo | `score_recovery.py` + changelog | mediana ≥ 70% |
| Daño colateral (celdas sanas modificadas) | `score_recovery.py` | ≤ 5 celdas por equipo |
| Filas borradas en vez de reparadas | `score_recovery.py` | 0 |
| Equipos que entregan Data-Driven Document completo | Carpeta de entregas (no la galería) | ≥ 80% |
| Equipos que identifican el leakage sembrado | Clave del facilitador | ≥ 60% |
| Equipos que identifican el confusor sembrado | Clave del facilitador | ≥ 50% |
| Equipos que documentan un error de la IA | Data-Driven Document, punto 9 | 100% |
| Laptops operativas al inicio de B1 | Checklist B0 | ≥ 95% |

---

## 5. Preparación técnica

### 5.1 Instalación previa de WSL2 + Ubuntu

El backend de Mini-Me **corre dentro de WSL2** (el stack necesita `bash`/`python3`/`asta`, que no se comportan
bajo `cmd.exe`); el cliente corre nativo en Windows. Instalar WSL requiere **permisos de administrador y un
reinicio**, así que no puede improvisarse la mañana del workshop.

**Recomendación: dos semanas antes, no una.** Una sola ventana deja fuera a quien esté de viaje, de campo o
con la laptop bloqueada por políticas de TI; la segunda semana es la ventana de recuperación.

| Cuándo | Qué | Quién |
|---|---|---|
| 9–13 nov | Sesión con IT: instalación de WSL2 + Ubuntu en laptops de participantes confirmados | IT + Piero |
| 9–13 nov | Instalación de Mini-Me Desktop y provisión del backend desde `vendor/` (sin GitHub) | IT |
| 16–19 nov | **Ventana de recuperación** para rezagados + verificación 1:1 | IT |
| hasta 19 nov | Cada laptop corre `--preflight` y entrega captura verde | Participante |

Comando de verificación que se pide a cada participante (una línea, sin ventana gráfica):

```bash
cargo run -p mini-me-desktop-app -- --preflight
```

Para quien solo usa la app: el panel **Setup** se abre solo, dice qué falta y trae un botón por cada cosa que
puede resolver (instalar WSL, instalar Mini-Me, instalar los paquetes de Python), mostrando la salida en vivo.
Nada se escribe en una terminal y nada se edita a mano.

### 5.2 API keys

- Las claves **no** van en el `.env` del checkout: viven en el **llavero del sistema operativo** y viajan con
  cada request, así que no queda ningún secreto en disco.
- Se configuran en **Settings** de la app, pegando la clave. Se hace en B0, con la clave entregada en una
  tarjeta por participante — nunca proyectada en pantalla.
- **Pendiente de decisión (ver §8):** ¿una clave por participante o una clave compartida de taller? Afecta al
  presupuesto de créditos y a la trazabilidad de consumo.
- Confirmar créditos de Asta disponibles **antes** del 9 de noviembre. No asumir que una promoción anterior sigue
  activa. AutoDiscovery consume un crédito por experimento; con 10 equipos × 5 experimentos son ~50 créditos
  solo en el Bloque 3, más el uso en B2.

### 5.3 Bundle del backend (una sola vez, antes de todo)

Mini-Me es un repositorio **privado**: un `git clone` pediría un personal access token a cada participante,
que es exactamente el muro que queremos evitar. En una máquina con acceso a GitHub, ejecutar una vez:

```bash
bash scripts/bundle-backend.sh
```

Eso deja una copia fijada y sin modificar en `vendor/`, y cada instalación posterior provisiona desde ahí sin
volver a contactar GitHub. **Esto tiene que estar hecho antes de la sesión con IT (M5).**

### 5.4 Congelar la versión

Se congela un commit de `mini-me-desktop` el **viernes 6 de noviembre** y todo lo demás (manual PDF, capturas, tarjetas,
runs pre-cocinados) se produce contra ese commit. Cualquier cambio posterior obliga a repetir el ensayo.

Estado actual conocido: la app renderiza nativa en Windows/DirectX, lanza el sidecar Python y transmite turnos
reales del coordinador; muestra project spine, outputs, provisión de sandbox, traza de actividad de agentes y
paleta de comandos (`ctrl-p`). **Riesgo abierto:** el markdown aún no se renderiza — las respuestas muestran
sus `**asteriscos**`, y los informes y citas son el entregable. Ver riesgo R6.

### 5.5 Manual del workshop — Quarto + Typst

**Se escribe en Quarto con motor Typst**, no en Word ni en LaTeX. Tres razones: el formato Typst permite
definir la paleta institucional de CIP y una maqueta propia sin pelear con plantillas; el contenido vive en
Markdown y por tanto en git, junto a los scripts que documenta; y los bloques de código y las tablas se
generan desde el propio repositorio, así que el manual no se desactualiza respecto a lo que hacen los
scripts.

La paleta vive en `manual/_brand.typ` y **hoy son colores provisionales**: hay que pedir el manual de
marca a Comunicaciones y reemplazar seis líneas. El objetivo declarado es que **no quede como un PDF más**: colores de CIP, tipografía legible, cajas de
"prueba esto" y "ojo con esto", diagramas, y una página por subagente que se pueda leer de pie mientras la
laptop hace lo suyo. Denso en información, ligero de leer.

Contenido:

- El diagrama del ciclo de vida y del flujo de agentes (el de la pizarra, redibujado).
- Una página por subagente: qué hace, qué le tienes que dar, qué te devuelve, cómo verificarlo.
- **Los prompts exactos** de cada actividad, copiables.
- La plantilla del Data-Driven Document.
- El Data Passport (para BYOD).
- Troubleshooting: 8–10 fallas conocidas y su solución en una línea.
- Enlaces y cómo pedir ayuda después del workshop.

### 5.6 Plan de respaldo — cada actividad en línea necesita

Captura o JSON de un resultado real · archivos producidos previamente · informe de ejemplo · código generado ·
una tarjeta que permita continuar el análisis **sin conexión**. Sin excepciones para Theorizer y AutoDiscovery.

### 5.7 Presentaciones de los bloques 1 y 2 — Quarto + Reveal.js

Los bloques 1 y 2 abren con una presentación narrativa corta en lugar de diapositivas de viñetas. Viven en
`presentacion/` y comparten estilo (trazo de pizarra, letra Kalam, paleta provisional de `manual/_brand.typ`):

| Bloque | Archivo | Título | Duración |
|---|---|---|---|
| B1 | `data_lifecycle.qmd` | *El viaje de los datos* | ~9 min |
| B2 | `investigacion.qmd` | *De la pregunta al conocimiento* | ~7 min |

Archivos comunes: `estilo.scss` (estilos) y `boceto.html` (puntas de flecha, etiquetas y contadores). Los
HTML se generan con `quarto render presentacion/<archivo>.qmd`, no se versionan, y llevan todo incrustado:
funcionan **sin internet** con doble clic. Se avanza con flecha o barra espaciadora; la tecla **S** abre las
notas del orador, que traen el guion de cada clic.

**Hilo narrativo.** Una investigadora ficticia, **Isabel**, mejoradora de papa, vuelve del campo con un
ensayo (30 genotipos × 3 localidades × 3 bloques) y una pregunta: ¿qué genotipos rinden más y lo hacen en
todas partes? En el B1 limpia y analiza sus datos, y en el diagnóstico descubre que la localidad pesa
tanto como el genotipo. Esa duda abre el B2. La tabla desordenada de la slide 4 del B1 son **datos de
ejemplo**; conviene cambiarla por filas reales cuando lleguen los datos de Vilma.

**Estructura** (según las notas de presentación de Simone, MIT Global Teaching Labs):

| Momento | B1 · El viaje de los datos | B2 · De la pregunta al conocimiento |
|---|---|---|
| Gancho | Pregunta a la sala: ¿qué parte de tu tiempo se va en preparar datos? | Pregunta a la sala: ¿cuántos artículos leíste el mes pasado? Luego, las cifras reales |
| Mensaje en una frase + mapa | Mini-Me te acompaña de los datos crudos a un reporte defendible. Preparar → Analizar → Comunicar | Las herramientas de Allen AI leen contigo miles de artículos. Buscar → Leer → Proponer y probar |
| Cuerpo | Isabel, sus datos desordenados y el ciclo dibujado en 18 clics: el prescriptivo aparece y estalla (fuera de alcance) y Comunicar queda en manos de las personas | El ciclo de datos se encoge y aparece el bucle Pregunta → Paper Finder → PDF librarian → Theorizer (demo) → Analizar datos (AutoDiscovery si no se sabe por dónde empezar), que sube al ciclo de Mini-Me y termina en Generación de conocimiento |
| Pico de atención a mitad | Votación a mano alzada en el Diagnóstico: ¿genotipo o localidad? | El momento en que los dos viajes se encuentran |
| Cierre | Repaso de las 3 paradas + llamada a la acción (demo en vivo) + lo que se llevan | Igual |
| Notas del orador | Frase de apertura de memoria y preguntas probables con respuesta corta | Igual |

**Cifras del gancho del B2.** Son conteos reales de la API de búsqueda masiva de Semantic Scholar (título y
resumen), consultados el **4 de noviembre de 2026**:

| Consulta | Artículos | Leyendo uno por hora, 8 h al día |
|---|---:|---|
| `("genotype by environment" \| "genotype x environment" \| "genotype-by-environment") + potato` | 224 | casi 6 semanas |
| `potato + yield` | 35,419 | casi 18 años |
| `potato + yield`, año 2025 | 1,836 | casi un año laboral |

Repetir las consultas la semana del ensayo y actualizar la slide si cambian (la slide muestra la fecha).

**Mantenimiento.** La primera slide del bucle del B2 usa una **copia fija** del diagrama del B1. Si se
cambia el ciclo en `data_lifecycle.qmd`, hay que actualizar también la copia en `investigacion.qmd`.

**Pendientes en las notas del orador:** cómo se accede a Mini-Me después del taller, y si Semantic Scholar
cubre bien la literatura en español (ver §8).

### 5.8 Nota de concepto y registro

- **Nota de concepto** redactada con la plantilla institucional (antecedentes, justificación, objetivos,
  organizadores, actividades, público, resultados, presupuesto y comunicación), en tono narrativo y con la
  IA presentada como fortaleza. **Actualizar la fecha a martes 24/11/2026.**
- **Formulario de registro en Microsoft Forms** (~3 min). Pide lo mínimo necesario para organizar el taller:
  nombre, correo institucional, programa o unidad y cargo; datos de la laptop (propia o institucional,
  sistema operativo, fecha disponible para la instalación con IT); temática preferida, comodidad analizando
  datos (1–5) y uso previo de IA, para armar equipos mixtos; restricciones alimentarias, accesibilidad y
  consentimiento de fotos. **No** pide DNI, teléfono ni fecha de nacimiento, y el encabezado aclara que los
  datos se eliminan después del evento. A quien responda Mac o Linux se le contacta antes, porque la
  instalación solo contempla Windows.

---

## 6. Cronograma y milestones

Hoy es **4 de noviembre de 2026**. Al martes 24 de noviembre quedan **20 días**.

### 6.1 Milestones

| ID | Milestone | Fecha límite | Responsable | Definición de "hecho" |
|---|---|---|---|---|
| **M1** | Alcance y fecha confirmados | — | Piero | ✅ Fecha (24 nov), hora (8:00–13:30), sede (Auditorio) y duración (5 h). **Falta la lista de participantes**, que sale del formulario de registro |
| **M2** | Datos crudos de las 4 temáticas entregados | **vie 6 nov** | Vilma | ✅ Datos y diccionarios recibidos el 4 nov; encuesta anonimizada y aprobada. **Falta** confirmar las preguntas de significado (§2.2), que quedaron como propuestas |
| **M3** | Pipeline `adapt` → `configurar` → `corrupt` → `score` | — | Piero | ✅ Aplicado a los 4 datasets reales el 4 nov: 247, 50, 151 y 496 defectos; 0% / 100% en los extremos y sin daño colateral |
| **M4** | Paquete didáctico v1 | **vie 13 nov** | Piero + facilitadores | ✅ Presentaciones B1 y B2 (§5.7) y nota de concepto. Pendiente: manual PDF v1, tarjetas de las 2 rutas, prompts exactos, plantilla del Data-Driven Document, Mentimeter PRE/POST |
| **M5** | Build congelado + bundle + preflight verde | **vie 6 nov** | Piero | Commit congelado, `bundle-backend.sh` ejecutado, `--preflight` verde en 2 laptops de prueba, créditos Asta confirmados |
| **M6** | Instalación en laptops de participantes | **jue 19 nov** | IT + Piero | ≥ 90% de laptops confirmadas con WSL2 + app + preflight verde (sesión 9–13 nov, recuperación 16–19 nov) |
| **M7** | Ensayo general completo | **vie 20 nov** | Equipo completo | Los 3 bloques corridos de punta a punta con los datos reales, cronometrados, incluidas las presentaciones; runs pre-cocinados guardados; respaldos offline listos |
| **M8** | **Workshop** | **mar 24 nov** | Todos | Ejecutado |
| **M9** | Cierre y reporte | **vie 4 dic** | Piero | Deltas de Mentimeter, métricas objetivas, Data-Driven Documents recopilados, lecciones y decisión de repetición |

### 6.2 Semana a semana

| Semana | Fechas | Foco | Entregable |
|---|---|---|---|
| Antes | sep–oct | Pipeline de ensuciado y scorers; esqueleto del manual | M3 ✅ |
| **T-3** | 2–6 nov | ✅ Presentaciones B1/B2 y nota de concepto. Publicar el formulario de registro; ✅ datos de Vilma recibidos y procesados; congelar build; bundle del backend; confirmar créditos | M2, M5 |
| **T-2** | 9–13 nov | **Sesión de instalación con IT**; runs pre-cocinados y respaldos offline; manual, tarjetas y Mentimeter | M4, M6 (inicio) |
| **T-1** | 16–20 nov | Ventana de recuperación (16–19); **ensayo general** (vie 20); impresión de materiales | M6, M7 |
| **T-0** | 23–24 nov | Gate final (lun 23) y workshop (mar 24) | M8 |
| **T+1** | 25 nov – 4 dic | Análisis de resultados y reporte | M9 |

### 6.3 Puntos de Go / No-Go

| Gate | Fecha | Criterio | Si no se cumple |
|---|---|---|---|
| **G1** | mié 11 nov | Datos reales listos y aprobados para las 4 temáticas | Regenerar el equivalente sintético con `generate_datasets.py` y sustituir solo la(s) temática(s) faltante(s) |
| **G2** | vie 6 nov | Build congelado con preflight verde + créditos confirmados | Bloque 2 pasa a modo demostración proyectada con runs pre-cocinados |
| **G3** | jue 19 nov | ≥ 90% de laptops instaladas | 70–90%: trabajo en parejas obligatorio. < 70%: **posponer una semana** (fecha por acordar) o mover a laboratorio con máquinas preparadas |
| **G4** | lun 23 nov | Ensayo general completo, respaldos offline en disco | Recortar a la versión de 4 h y eliminar AutoDiscovery en vivo |

### 6.4 Tracking

- Revisión semanal de 30 min, **jueves**, contra esta tabla de milestones.
- Cada milestone tiene un único responsable nombrado. Sin responsable, no hay milestone.
- Un milestone atrasado más de 3 días escala inmediatamente al gate siguiente para decidir recorte, no para
  negociar la fecha. Con 20 días por delante, cualquier atraso en M2 o M5 se decide en el gate, no se espera.

---

## 7. Riesgos

| ID | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | Los datos de Vilma llegan tarde o sin autorización de uso | Media | Alto | G1 con sustitución sintética ya lista; el pedido sale en T-7, no en T-5; el pipeline se construye y prueba sin sus datos |
| R1b | La estructura de Vilma resulta más irregular de lo previsto (jerárquica, una hoja por sitio, celdas combinadas) | Media | Medio | El adaptador se escribe tolerante; presupuestar 1 día por temática para el mapeo manual en T-5 |
| R2 | Datos personales en las encuestas | **Alta** | **Muy alto** | Anonimización obligatoria en M2 + visto bueno escrito; si no, se usa el sintético |
| R3 | Laptops sin WSL la mañana del workshop | Alta | Alto | B0 de 30 min + dos ventanas de instalación + trabajo en parejas como plan B |
| R4 | AutoDiscovery/Theorizer no terminan a tiempo | **Alta** | Medio | Lanzarlos en la pausa previa + runs pre-cocinados obligatorios |
| R5 | Créditos de Asta agotados a media sesión | Media | Alto | Presupuesto contado por equipo (3–5 experimentos), confirmado en M5; modo demo como respaldo |
| R6 | El markdown sin renderizar hace ilegibles informes y citas | Media | Medio | Verificar en el ensayo (M7); si sigue abierto, exportar a PDF vía `report_writer` y leer ahí |
| R7 | Un fallo de herramienta produce un artefacto con apariencia exitosa | Media | Alto | Enseñarlo como contenido: verificar `status`, task id y archivos reales |
| R8 | Red del venue insuficiente para 30 clientes concurrentes | Media | Alto | Prueba de carga en el ensayo; hotspot de respaldo; respaldos offline |
| R9 | Heterogeneidad de nivel entre 20–30 participantes | Alta | Medio | Equipos mixtos de 2–3; facilitador de apoyo por cada 8–10 personas |
| R10 | Las cifras del gancho del B2 cambian o la API de Semantic Scholar limita las consultas | Media | Bajo | Repetir las consultas la semana del ensayo (§5.7); la slide muestra la fecha de consulta |
| R11 | Calendario comprimido: 20 días entre esta versión y el taller | Alta | Alto | Gates G1–G4 sin negociación de fechas; materiales ya listos (presentaciones, pipeline) liberan tiempo para datos e instalación |

**Equipo mínimo el día del workshop:** 1 facilitador principal + 2 facilitadores de apoyo + 1 persona de IT
de guardia. Con 30 participantes, 3 facilitadores es el piso, no el ideal.

---

## 8. Decisiones pendientes

Para cerrar antes de la sesión de instalación (lunes 9 de noviembre):

1. **API keys:** ¿una por participante o una compartida del taller? Afecta presupuesto y trazabilidad.
2. **Presupuesto de créditos Asta** disponible y confirmado.
3. **Significado de los datos con Vilma:** confirmar resultado, *leakage* y pregunta de cada temática (las
   preguntas abiertas están en cada `<slug>_ADAPTATION.md`).
4. **Equipamiento del Auditorio:** mesas, tomas de corriente para 30 laptops, proyector y red probada para 30
   conexiones simultáneas.
5. **Lista de participantes confirmados**, a partir del formulario de registro. La instalación con IT depende
   de tener nombres, no estimados.
6. **AutoDiscovery:** ¿ejercicio en vivo con presupuesto de experimentos, o demostración con el run
   pre-cocinado?
7. **Acceso a Mini-Me después del taller:** definir la respuesta para el Q&A de las presentaciones.
8. **Literatura en español:** verificar la cobertura de Semantic Scholar para el Q&A del B2.

**Ya cerrado:** fecha **martes 24 de noviembre de 2026**, de 8:00 a 13:30, en el **Auditorio**; duración
canónica de **5 h**; galería **voluntaria, máximo 2 grupos** presentando; B2 con Asta (Paper Finder, PDF
librarian), Theorizer **solo como demo** y AutoDiscovery, **sin DataVoyager**; encuesta de consumidores
anonimizada y aprobada.

---

## 9. Entregables del paquete de workshop

- [x] 4 paquetes de datos en `datasets/`, publicados en GitHub con sus originales y el brief de cada temática
  (`README.md`). Las preguntas siguen siendo propuestas hasta que Vilma las confirme — M3
- [x] `scripts/configurar_taller.py` (unidades, rangos, roles y descripciones de los diccionarios de Vilma) — **hecho**
- [x] `scripts/adapt_dataset.py` (normaliza la estructura de Vilma a la nuestra) — **hecho**
- [x] `scripts/corrupt_dataset.py` (corrupción determinística + changelog celda a celda) — **hecho**
- [x] `scripts/score_recovery.py` (% de defectos reparados, daño colateral, filas borradas) — **hecho**
- [x] Presentaciones de los bloques 1 y 2 en Quarto + Reveal.js (§5.7) — **hecho**
- [x] Nota de concepto — **redactada**; falta actualizar la fecha a 24/11
- [ ] Formulario de registro en Microsoft Forms (§5.8) — preguntas definidas, falta publicarlo
- [~] Manual del workshop en Quarto + Typst — **compila, 15 páginas, con una página por temática real** (§7 del manual) y el Bloque 2 de Allen AI; falta la paleta oficial de CIP — M4
- [ ] Tarjetas impresas: ruta Research, ruta Data, plantilla del Data-Driven Document, Data Passport — M4
- [ ] Prompts exactos por actividad — M4
- [ ] Mentimeter PRE y POST configurados — M4
- [ ] Runs pre-cocinados de Theorizer y AutoDiscovery (4 temáticas) — M7
- [ ] PDFs abiertos pre-descargados para `pdf_librarian` (2–3 por temática) — M7
- [ ] Respuestas esperadas y claves de defectos para facilitadores — M3/M7
- [ ] Rúbrica de la galería — M4
- [ ] Reporte post-workshop con deltas y métricas — M9

---

*Documento elaborado con asistencia de IA (Claude Code) y revisado por el equipo. El contenido técnico debe
validarse con los responsables de cada dato y del stack antes de su ejecución.*
