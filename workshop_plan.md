# Workshop Mini-Me — Plan de ejecución (v2, un día)

**De datos crudos a un Data-Driven Document en un solo día.**

| Campo | Valor |
|---|---|
| Fecha | **jueves 22 de octubre de 2026** (confirmada) |
| Duración | **5 h efectivas** (rango acordado 4–6 h; ver §3.3 para recortes y extensiones) |
| Participantes | 20–30 personas, en equipos de 2–3 |
| Modalidad | Presencial, laptops propias con WSL2 preinstalado |
| Herramienta | **Mini-Me Desktop** (`mini-me-desktop`) + backend Mini-Me en WSL |
| Entregable del participante | **Data-Driven Document** (1–2 páginas, con evidencia trazable) |
| Medición | Mentimeter **pre** y **post** + score de limpieza automatizado |
| Fecha de este plan | 3 de septiembre de 2026 (T-7 semanas) |

> **Cambio respecto a la v1.** La versión anterior (3 días, dataset sintético único) queda archivada en
> `workshop_plan_v1_3dias.bak.md`. Esta v2 comprime todo a **un día con tres bloques**, cambia el dataset
> sintético por **datos reales de CIP ensuciados de forma controlada** (4 temáticas), y añade el eje de
> **medición antes/después**.

---

## 1. Concepto

Un solo hilo narrativo, tres bloques, un entregable:

```
Bloque 1  Data Lifecycle      ->  el científico entiende y arregla sus datos
Bloque 2  Asta / Allen AI     ->  el científico busca, teoriza y explora evidencia
Bloque 3  Hands-on            ->  el científico produce un documento defendible
                                   |
                                   v
                          Data-Driven Document
```

El mensaje central del día, que debe repetirse en cada bloque:

> **La IA acelera tareas; el científico mantiene la responsabilidad sobre la pregunta, los datos, la
> evidencia y la interpretación.**

### 1.1 Resultados esperados

Al terminar, cada participante debe poder:

1. Nombrar las 7 etapas del ciclo de vida del dato y el subagente que corresponde a cada una.
2. Detectar y **documentar** problemas de calidad en un dataset real de su área.
3. Distinguir exploración, diagnóstico, predicción y causalidad.
4. Usar al menos tres herramientas Asta (búsqueda académica, PDF librarian, Theorizer, DataVoyager, AutoDiscovery).
5. Verificar un resultado de IA: fuentes, código, archivos, estado de ejecución.
6. Identificar al menos **un error o límite** de la IA durante el día.
7. Entregar un Data-Driven Document con una afirmación respaldada y una afirmación que **no** puede hacerse.

---

## 2. Datos — las 4 temáticas de Vilma

Responsable de la entrega: **Vilma**. Cuatro paquetes, uno por temática:

| # | Temática | Fuente | Unidad de observación | Preguntas de investigación (1–2 por dataset) |
|---|---|---|---|---|
| 1 | **Morfología de papa** | Banco de germoplasma | Accesión × descriptor | ¿Qué descriptores morfológicos agrupan accesiones y cuáles son redundantes? |
| 2 | **Breeding** | Ensayos de rendimiento | Genotipo × sitio × bloque | ¿Qué genotipos combinan rendimiento alto y estabilidad entre ambientes? |
| 3 | **Disease** | Bactericera / punta morada | Parcela o planta × evaluación | ¿Qué variables ambientales y de manejo se asocian con la incidencia? |
| 4 | **Encuestas a agricultores** | Encuesta socioeconómica | Hogar o productor | ¿Qué factores se asocian con la adopción de una práctica o variedad? |

### 2.1 Cada paquete entregado al participante contiene

```
datasets/<tematica>/
  <tematica>_dirty.csv        <- punto de partida del participante
  <tematica>_clean.csv        <- benchmark del facilitador (NO se distribuye durante el ejercicio)
  <tematica>_dictionary.csv   <- tipo, unidad, rol analítico, rango válido, descripción
  README.md                   <- brief, pregunta(s), unidad de observación, limitación causal
  FACILITATOR.md              <- clave de defectos: familia de corrupción y filas afectadas
```

Esta es exactamente la estructura que ya existe en `datasets/` para los siete paquetes sintéticos, así que
el scorer y los materiales se reutilizan sin cambios.

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
que acepte datos externos. **Se puede escribir y probar hoy** contra los siete datasets sintéticos que ya
están en `datasets/`, sin esperar a Vilma: si al corromper un `clean.csv` conocido el score cae y al
limpiarlo vuelve a subir, el pipeline funciona. Ver milestone **M3**.

**Métrica que verá el participante** (`scripts/score_cleanliness.py`, ya funciona):

```bash
python scripts/score_cleanliness.py datasets/breeding/breeding_dirty.csv
```

Ponderación: esquema 15% · integridad de registros 20% · concordancia celda a celda 65%.
Cada equipo reporta su score **antes** y **después** de limpiar. Es la métrica cuantitativa del Bloque 1.

> Advertencia que debe decirse en voz alta: **100/100 no significa que el análisis sea correcto, insesgado o
> causal.** Limpieza y validez analítica se enseñan como preguntas separadas.

### 2.4 Protección de datos — bloqueante, resolver antes de M2

Los datos de Vilma son datos reales de CIP y las **encuestas a agricultores contienen datos personales**.
La política institucional prohíbe introducir datos confidenciales o personales en herramientas de IA, y el
stack Asta procesa los datos fuera de la máquina del participante.

Por eso, antes de que cualquier archivo entre al workshop:

1. **Anonimización obligatoria** de las encuestas: eliminar nombres, DNI, teléfonos, coordenadas exactas
   (degradar a distrito), y reemplazar identificadores por códigos correlativos sin diccionario reversible
   en el paquete distribuido.
2. **Revisión y visto bueno** del responsable del dato (Vilma) y, si aplica, del punto focal de datos de CIP,
   por escrito, para las cuatro temáticas.
3. Si una temática no obtiene visto bueno a tiempo, se sustituye por su equivalente sintético de
   `datasets/` (`value_chain_adoption` para encuestas, `potato_breeding_trials` para breeding,
   `native_potato_biodiversity` para morfología, `seed_system_quality` o `climate_smart_agronomy` para
   disease). **El workshop no se detiene por un dataset.**
4. Investigación no publicada / propiedad intelectual de terceros: no se incluye nada inédito que no esté
   autorizado a salir.

---

## 3. Agenda del día

### 3.1 Bloque a bloque (versión canónica, 5 h)

| Hora | Min | Bloque | Contenido |
|---|---:|---|---|
| 08:30–09:00 | 30 | **B0 Setup** | Registro, verificación de laptops, login, API key, dataset descargado |
| 09:00–09:20 | 20 | **Apertura** | Encuadre + **Mentimeter PRE** + reglas del día |
| 09:20–10:20 | 60 | **B1 Data Lifecycle** | Intro → Limpieza → Validación → EDA → Diagnostics → Predictive → Reporting |
| 10:20–10:35 | 15 | Pausa | Café. *Se lanzan Theorizer y AutoDiscovery en background.* |
| 10:35–11:40 | 65 | **B2 Asta / Allen AI** | Academic research → PDF librarian → Theorizer → DataVoyager → AutoDiscovery |
| 11:40–11:50 | 10 | Pausa | |
| 11:50–13:20 | 90 | **B3 Hands-on** | Dos rutas (Research / Data) sobre el dataset de su temática |
| 13:20–13:45 | 25 | **Galería** | Mural con todos los Data-Driven Documents + **2 presentaciones voluntarias** + síntesis |
| 13:45–14:00 | 15 | **Cierre** | **Mentimeter POST** + próximos pasos + entrega de materiales |

**B0 no es opcional.** Es el bloque que salva el día: 30 minutos de colchón para el 10–20% de laptops que
llegarán con algo roto pese a la instalación previa.

### 3.2 Detalle de cada bloque

#### B1 — Data Lifecycle (60 min)

Todo el bloque se hace **en vivo, con el facilitador proyectando** y los participantes replicando sobre el
dataset de su temática.

| Min | Etapa | Subagente | Producto visible |
|---:|---|---|---|
| 0–8 | Introducción | — | El ciclo de vida dibujado + la pregunta científica del dataset |
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

#### B2 — Asta / Allen AI (65 min) — el bloque más intensivo

**Regla de oro operativa:** Theorizer y AutoDiscovery se **lanzan en la pausa anterior** (10:20) para que sus
resultados lleguen dentro del bloque. Además, cada uno tiene un **run terminado de respaldo** en disco.

| Min | Herramienta | Subagente | Prompt / acción |
|---:|---|---|---|
| 0–5 | Encuadre | — | Qué es Asta, qué resuelve y qué **no** |
| 5–17 | **Academic research** | `academic_researcher` | "¿Qué evidencia existe sobre \<pregunta de la temática\>?" → 5 fuentes, una frase de por qué importa cada una |
| 17–28 | **PDF librarian** | `pdf_librarian` | Indexar 2–3 PDFs **abiertos, pre-descargados** y localizar pasajes |
| 28–40 | **Theorizer** | `hypothesis_generator` | Mecanismos e hipótesis comprobables; inspeccionar el run lanzado en la pausa |
| 40–52 | **DataVoyager** | `data_voyager` | Pregunta dirigida sobre el dataset ya limpio; exigir supuestos, incertidumbre, código |
| 52–65 | **AutoDiscovery** | `autodiscovery` | Run pre-cocinado + presupuesto vivo de 3–5 experimentos |

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

**Ruta 1 — Research** (para quien viene con una pregunta, no con datos):

```
AutoDiscovery -> Report -> Academic search -> (PDF librarian) -> Data-Driven Document
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

### 4.1 Encuesta PRE (09:00, 5 min, 6 preguntas)

| # | Tipo | Pregunta |
|---|---|---|
| 1 | Escala 1–5 | ¿Qué tan cómodo/a te sientes limpiando y validando un dataset antes de analizarlo? |
| 2 | Escala 1–5 | ¿Qué tan cómodo/a te sientes distinguiendo correlación de causalidad en tu propio análisis? |
| 3 | Opción múltiple | ¿Cuánto tiempo te toma hoy pasar de datos crudos a un primer informe? (<1 día / 1–3 días / 1–2 semanas / >2 semanas) |
| 4 | Escala 1–5 | ¿Qué tanto confías hoy en un resultado producido por una IA sin verificarlo? |
| 5 | Multi-selección | ¿Cuáles de estas herramientas has usado? (Academic search / PDF librarian / Theorizer / DataVoyager / AutoDiscovery / ninguna) |
| 6 | Nube de palabras | En una palabra: ¿qué esperas llevarte de hoy? |

### 4.2 Encuesta POST (13:45, 8 min)

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
| Δ score de limpieza por equipo | `score_cleanliness.py` | mediana ≥ +40 puntos |
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
| T-2 sem (8–14 oct) | Sesión con IT: instalación de WSL2 + Ubuntu en laptops de participantes confirmados | IT + Piero |
| T-2 sem | Instalación de Mini-Me Desktop y provisión del backend desde `vendor/` (sin GitHub) | IT |
| T-1 sem (15–21 oct) | **Ventana de recuperación** para rezagados + verificación 1:1 | IT |
| T-1 sem | Cada laptop corre `--preflight` y entrega captura verde | Participante |

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
- Confirmar créditos de Asta disponibles **antes** de T-2 sem. No asumir que una promoción anterior sigue
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

Se congela un commit de `mini-me-desktop` en **T-3 semanas** y todo lo demás (manual PDF, capturas, tarjetas,
runs pre-cocinados) se produce contra ese commit. Cualquier cambio posterior obliga a repetir el ensayo.

Estado actual conocido: la app renderiza nativa en Windows/DirectX, lanza el sidecar Python y transmite turnos
reales del coordinador; muestra project spine, outputs, provisión de sandbox, traza de actividad de agentes y
paleta de comandos (`ctrl-p`). **Riesgo abierto:** el markdown aún no se renderiza — las respuestas muestran
sus `**asteriscos**`, y los informes y citas son el entregable. Ver riesgo R6.

### 5.5 Manual PDF del workshop

Un PDF, entregado impreso y digital, con:

- El diagrama del ciclo de vida y del flujo de agentes (el de la pizarra, redibujado).
- Una página por subagente: qué hace, qué le tienes que dar, qué te devuelve, cómo verificarlo.
- **Los prompts exactos** de cada actividad, copiables.
- La plantilla del Data-Driven Document.
- El Data Passport (para BYOD).
- Troubleshooting: 8–10 fallas conocidas y su solución en una línea.
- Enlaces y cómo pedir ayuda después del workshop.

### 5.6 Plan de respaldo — cada actividad en línea necesita

Captura o JSON de un resultado real · archivos producidos previamente · informe de ejemplo · código generado ·
una tarjeta que permita continuar el análisis **sin conexión**. Sin excepciones para Theorizer, DataVoyager y
AutoDiscovery.

---

## 6. Cronograma y milestones

Hoy es **3 de septiembre de 2026**. Al 22 de octubre quedan **7 semanas**.

### 6.1 Milestones

| ID | Milestone | Fecha límite | Responsable | Definición de "hecho" |
|---|---|---|---|---|
| **M1** | Alcance y fecha confirmados | **vie 11 sep** | Piero | Fecha, sede, duración (4/5/6 h) y lista de invitados cerradas; agenda aprobada |
| **M2** | Datos crudos de las 4 temáticas entregados | **vie 18 sep** | Vilma | Los 4 datasets **en la estructura que ella use**, más las 6 respuestas de significado (§2.2); **anonimización de encuestas hecha y aprobada** (§2.4) |
| **M3** | Pipeline `adapt` → `corrupt` → `score` | **vie 25 sep** | Piero | `adapt_dataset.py` y `corrupt_dataset.py` escritos y probados **contra los datasets sintéticos actuales**; `dirty.csv`, `dictionary.csv` y `FACILITATOR.md` reproducibles para las 4 temáticas; `score_cleanliness.py --all` corre limpio |
| **M4** | Paquete didáctico v1 | **vie 2 oct** | Piero + facilitadores | Manual PDF v1, tarjetas de las 2 rutas, prompts exactos, plantilla del Data-Driven Document, Mentimeter PRE/POST creados |
| **M5** | Build congelado + bundle + preflight verde | **mié 7 oct** | Piero | Commit congelado, `bundle-backend.sh` ejecutado, `--preflight` verde en 2 laptops de prueba, créditos Asta confirmados |
| **M6** | Instalación en laptops de participantes | **vie 16 oct** | IT + Piero | ≥ 90% de laptops confirmadas con WSL2 + app + preflight verde |
| **M7** | Ensayo general completo | **mar 20 oct** | Equipo completo | Los 3 bloques corridos de punta a punta con los datos reales, cronometrados; runs pre-cocinados guardados; respaldos offline listos |
| **M8** | **Workshop** | **jue 22 oct** | Todos | Ejecutado |
| **M9** | Cierre y reporte | **vie 30 oct** | Piero | Deltas de Mentimeter, métricas objetivas, Data-Driven Documents recopilados, lecciones y decisión de repetición |

### 6.2 Semana a semana

| Semana | Fechas | Foco | Entregable |
|---|---|---|---|
| **T-7** | 3–9 sep | Decisiones de alcance; pedido formal de datos a Vilma; reserva de sala | M1 |
| **T-6** | 10–16 sep | Recepción y revisión de datos; anonimización; visto bueno de protección de datos | M2 |
| **T-5** | 17–23 sep | Pipeline de ensuciado; diccionarios; claves de facilitador | M3 (inicio) |
| **T-4** | 24–30 sep | Cierre del pipeline; redacción del manual; diseño de Mentimeter | M3, M4 (inicio) |
| **T-3** | 1–7 oct | Congelar build; bundle del backend; confirmar créditos; **dry-run técnico interno** | M4, M5 |
| **T-2** | 8–14 oct | **Sesión de instalación con IT**; producción de runs pre-cocinados y respaldos offline | M6 (inicio) |
| **T-1** | 15–21 oct | Ventana de recuperación de instalaciones; **ensayo general**; impresión de materiales | M6, M7 |
| **T-0** | 22 oct | Workshop | M8 |
| **T+1** | 23–30 oct | Análisis de resultados y reporte | M9 |

### 6.3 Puntos de Go / No-Go

| Gate | Fecha | Criterio | Si no se cumple |
|---|---|---|---|
| **G1** | 30 sep | Datos reales listos y aprobados para las 4 temáticas | Sustituir la(s) temática(s) faltante(s) por su equivalente sintético de `datasets/` |
| **G2** | 7 oct | Build congelado con preflight verde + créditos confirmados | Bloque 2 pasa a modo demostración proyectada con runs pre-cocinados |
| **G3** | 16 oct | ≥ 90% de laptops instaladas | 70–90%: trabajo en parejas obligatorio. < 70%: **posponer al 29 de octubre** o mover a laboratorio con máquinas preparadas |
| **G4** | 21 oct | Ensayo general completo, respaldos offline en disco | Recortar a la versión de 4 h y eliminar AutoDiscovery en vivo |

### 6.4 Tracking

- Revisión semanal de 30 min, **jueves**, contra esta tabla de milestones.
- Cada milestone tiene un único responsable nombrado. Sin responsable, no hay milestone.
- Un milestone atrasado más de 3 días escala inmediatamente al gate siguiente para decidir recorte, no para
  negociar la fecha.

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

**Equipo mínimo el día del workshop:** 1 facilitador principal + 2 facilitadores de apoyo + 1 persona de IT
de guardia. Con 30 participantes, 3 facilitadores es el piso, no el ideal.

---

## 8. Decisiones pendientes

Necesito confirmación en estos puntos para cerrar M1 (11 de septiembre):

1. **Duración final:** ¿4, 5 o 6 horas? Recomiendo 5 h; con 4 h el hands-on queda apretado para producir un
   Data-Driven Document decente.
2. **API keys:** ¿una por participante o una compartida del taller? Afecta presupuesto y trazabilidad.
3. **Presupuesto de créditos Asta** disponible y confirmado.
4. **Encuestas a agricultores:** ¿existe ya una versión anonimizada o hay que producirla? ¿Quién firma el
   visto bueno de uso?
5. **Sede y equipamiento:** ¿sala con proyector, tomas de corriente para 30 laptops y red probada?
6. **Lista de participantes confirmados** — la instalación con IT depende de tener nombres, no estimados.

**Ya cerrado:** fecha **jueves 22 de octubre de 2026**; galería **voluntaria, máximo 2 grupos** presentando.

---

## 9. Entregables del paquete de workshop

- [ ] 4 paquetes de datos (`dirty` / `clean` / `dictionary` / `README` / `FACILITATOR`) — M3
- [ ] `scripts/adapt_dataset.py` (normaliza la estructura de Vilma a la nuestra) — M3
- [ ] `scripts/corrupt_dataset.py` — M3
- [ ] Manual PDF del workshop — M4
- [ ] Tarjetas impresas: ruta Research, ruta Data, plantilla del Data-Driven Document, Data Passport — M4
- [ ] Prompts exactos por actividad — M4
- [ ] Mentimeter PRE y POST configurados — M4
- [ ] Runs pre-cocinados de Theorizer, DataVoyager y AutoDiscovery (4 temáticas) — M7
- [ ] PDFs abiertos pre-descargados para `pdf_librarian` (2–3 por temática) — M7
- [ ] Respuestas esperadas y claves de defectos para facilitadores — M3/M7
- [ ] Rúbrica de la galería — M4
- [ ] Reporte post-workshop con deltas y métricas — M9

---

*Documento elaborado con asistencia de IA (Claude Code) y revisado por el equipo. El contenido técnico debe
validarse con los responsables de cada dato y del stack antes de su ejecución.*
