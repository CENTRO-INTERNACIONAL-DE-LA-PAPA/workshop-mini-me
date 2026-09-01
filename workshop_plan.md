La estructura de tres días es buena. Mi recomendación principal es usar un solo caso científico que evolucione durante todo el workshop: datos sucios → análisis → evidencia científica → hipótesis → investigación asistida por agentes. Así los participantes aprenden un flujo, no una colección de botones.

## Concepto del workshop

**Título sugerido:**  
**From Dirty Data to Scientific Discovery: Research Workflows with Mini-Me**

**Caso conductor:**  
“Resiliencia de papas nativas frente al clima y al tizón tardío en ensayos multiambiente”.

Es relevante para CIP, permite trabajar con rendimiento, sanidad, clima, diversidad y predicción, y se alinea con los dominios que CIP está FAIRificando: mejoramiento, agronomía, tizón tardío y diversidad in situ. [CIP: FAIRification of legacy datasets](https://cipotato.org/publication/fairification-of-cip-legacy-datasets/)

**Resultados esperados al finalizar:**

- Elegir el subagente adecuado para cada etapa.
- Detectar y documentar problemas de calidad de datos.
- Diferenciar exploración, diagnóstico, predicción y causalidad.
- Verificar fuentes, código, archivos y estados de ejecución.
- Formular hipótesis científicas comprobables.
- Identificar al menos un error o limitación de la IA.
- Entregar un pequeño paquete reproducible de investigación.

---

# Día 1 — The Data Lifecycle

**Objetivo:** transformar un dataset deliberadamente sucio en resultados analizables y comunicables.

| Tiempo | Actividad | Subagente |
|---|---|---|
| 0–15 min | Introducción: ciclo de vida y pregunta científica | — |
| 15–35 min | Diagnóstico y limpieza del dataset | `data_cleaning` |
| 35–55 min | EDA: distribuciones, faltantes, relaciones y anomalías | `exploratory_data_analysis` |
| 55–75 min | ¿Por qué ocurrió? Variables explicativas y confusión | `diagnostic_analytics` |
| 75–95 min | Modelo predictivo, validación y leakage | `predictive_analytics` |
| 95–110 min | Informe de una página con resultados y limitaciones | `report_writer` |
| 110–120 min | Discusión: ¿qué hizo la IA y qué decidió el científico? | — |

## Dataset recomendado

**`native_potato_trials_dirty.csv`**

Base sintética de aproximadamente 360 observaciones:

- 30 genotipos o variedades.
- 4 localidades.
- 3 bloques.
- Una campaña agrícola.
- Diferentes altitudes, temperaturas y niveles de presión de tizón.

Variables sugeridas:

- `trial_id`
- `site`
- `season`
- `block`
- `genotype`
- `potato_group`
- `flesh_color`
- `altitude_m`
- `rainfall_mm`
- `mean_temperature_c`
- `relative_humidity_pct`
- `soil_ph`
- `nitrogen_kg_ha`
- `fungicide_treatment`
- `late_blight_severity_pct`
- `yield_t_ha`
- `marketable_yield_pct`
- `dry_matter_pct`
- `tuber_count`

## Problemas sembrados deliberadamente

Prepararía entre ocho y diez errores conocidos:

- Registros duplicados.
- `Huánuco`, `Huanuco` y `HUANUCO` como categorías diferentes.
- Rendimientos negativos o extremadamente altos.
- Severidad expresada unas veces de 0–1 y otras de 0–100.
- Altitud en metros y algunos registros en pies.
- Fechas con formatos incompatibles.
- Valores faltantes no aleatorios.
- Un `soil_ph` imposible.
- Una variable derivada del rendimiento que provoque *target leakage*.
- Genotipos presentes solamente en una localidad.

El facilitador debe tener una “clave de defectos” para comparar lo encontrado por los grupos. Esto refuerza la recomendación institucional de que los datos estén limpios, verificados, estructurados y documentados antes de su publicación. [CIP: Publishing Research Data](https://cipotato.org/open-access/publishing-research-data/)

## Pregunta científica

> ¿Qué genotipos mantienen buen rendimiento bajo alta presión de tizón y qué variables ambientales están asociadas con esa respuesta?

La palabra importante es **asociadas**. El objetivo del día es que los participantes no conviertan automáticamente una correlación en causalidad.

---

# Día 2 — The Research Point of View

**Objetivo:** pasar de “qué patrones hay” a “qué sabemos, qué hipótesis tenemos y qué deberíamos investigar”.

Asta debe presentarse como el ecosistema; dentro del flujo se utilizan búsqueda académica, Theorizer, DataVoyager y AutoDiscovery. Asta combina búsqueda, síntesis y análisis científico, mientras que DataVoyager trabaja con datos estructurados mediante preguntas en lenguaje natural y produce código, visualizaciones y explicaciones. [Asta Agents](https://allenai.org/asta/agents), [Asta DataVoyager](https://allenai.org/blog/asta-datavoyager)

| Tiempo | Actividad | Subagente |
|---|---|---|
| 0–15 min | Diferencia entre evidencia, hipótesis y descubrimiento exploratorio | — |
| 15–35 min | Buscar evidencia sobre clima, tizón y rendimiento | `academic_researcher` |
| 35–50 min | Descargar/indexar 2–3 artículos y consultar sus textos | `pdf_librarian` |
| 50–65 min | Lanzar Theorizer e inspeccionar un resultado preparado | `hypothesis_generator` |
| 65–85 min | Probar una hipótesis dirigida sobre el dataset limpio | `data_voyager` |
| 85–110 min | AutoDiscovery: presupuesto, aprobación, árbol y resultados | `autodiscovery` |
| 110–120 min | Construir la cadena evidencia → hipótesis → prueba → conclusión | — |

## Flujo científico sugerido

1. **Academic Researcher**

   Pregunta:

   > ¿Qué evidencia existe sobre la interacción entre temperatura, humedad, resistencia genética y severidad de tizón tardío en papa?

   Producto: cinco fuentes relevantes, con una frase explicando por qué cada una importa.

2. **PDF Librarian**

   Entregar previamente dos o tres PDFs abiertos. Pedir:

   > Indexa estos documentos y encuentra los pasajes que expliquen cómo temperatura y humedad modifican el desarrollo del tizón.

   No dependería de una descarga en vivo: los PDF deberían estar preparados localmente como respaldo.

3. **Hypothesis Generator / Theorizer**

   Pregunta:

   > Genera mecanismos e hipótesis comprobables sobre por qué ciertos genotipos conservan rendimiento bajo alta presión de tizón.

   Como puede tardar varios minutos, conviene iniciarlo temprano y tener un resultado terminado de respaldo.

4. **DataVoyager**

   Pregunta dirigida:

   > Evalúa si la asociación entre humedad y rendimiento está mediada o modificada por severidad de tizón y genotipo. Reporta supuestos, incertidumbre, visualizaciones y código.

5. **AutoDiscovery**

   Usar un presupuesto pequeño —idealmente 3–5 experimentos en vivo— y mostrar un run terminado previamente. AutoDiscovery puede tardar horas; Ai2 recomienda comenzar con menos de diez hipótesis y cada experimento consume un crédito. [Ai2: AutoDiscovery](https://allenai.org/blog/autodiscovery)

   Los participantes deben inspeccionar:

   - La hipótesis.
   - El prior y posterior.
   - El valor firmado de `surprise`.
   - El código ejecutado.
   - El método estadístico.
   - Las limitaciones.
   - Si el resultado merece validación independiente.

AutoDiscovery propone direcciones de investigación; no convierte automáticamente una relación encontrada en una conclusión científica.

---

# Día 3 — Hands-on Research Challenge

**Objetivo:** que cada equipo resuelva una tarea concreta y defienda sus decisiones.

## Organización

- Equipos de 2–3 personas.
- Idealmente máximo seis equipos.
- Cada equipo utiliza como máximo tres subagentes.
- No gana quien usa más herramientas: gana quien construye el argumento más verificable.

| Tiempo | Actividad |
|---|---|
| 0–10 min | Explicación del reto y rúbrica |
| 10–20 min | Elegir pregunta, roles y subagentes |
| 20–65 min | Investigación |
| 65–80 min | Auditoría cruzada entre equipos |
| 80–105 min | Presentaciones o galería de resultados |
| 105–115 min | Retroalimentación |
| 115–120 min | Evaluación final y próximos pasos |

## Cuatro retos posibles

### Reto A — Resistencia a tizón

> Identifiquen genotipos que combinen bajo nivel de enfermedad, rendimiento alto y estabilidad entre ambientes.

Subagentes sugeridos: EDA → Diagnostic Analytics → Report Writer.

### Reto B — Predicción de rendimiento

> Construyan un modelo para predecir rendimiento comercial antes de la cosecha. Detecten leakage y expliquen dónde falla el modelo.

Subagentes sugeridos: Data Cleaning → Predictive Analytics → Report Writer.

### Reto C — Clima y mecanismos

> Propongan y evalúen una hipótesis sobre cómo altitud, temperatura y humedad afectan indirectamente el rendimiento mediante la presión de tizón.

Subagentes sugeridos: Academic Researcher → Hypothesis Generator → DataVoyager.

### Reto D — Descubrimiento abierto

> Examinen un resultado preparado de AutoDiscovery, reproduzcan el análisis más sorprendente y decidan si merece un experimento de seguimiento.

Subagentes sugeridos: AutoDiscovery → Academic Researcher → Report Writer.

Este último debe usar un run terminado previamente; intentar completar AutoDiscovery durante la sesión sería arriesgado.

## Entregable de cada equipo

Una carpeta que contenga:

- Pregunta científica.
- Dataset utilizado.
- Registro de limpieza o decisiones.
- Una visualización principal.
- Un resultado cuantitativo.
- Dos o tres fuentes.
- Una afirmación respaldada.
- Una afirmación que **no** puede hacerse con esos datos.
- Próximo experimento recomendado.
- Informe de máximo una página.

## Rúbrica

| Criterio | Peso |
|---|---:|
| Pregunta científica clara | 15% |
| Calidad y trazabilidad de datos | 20% |
| Método apropiado | 20% |
| Evidencia y reproducibilidad | 20% |
| Interpretación y limitaciones | 15% |
| Comunicación | 10% |

Añadiría una regla: **cada equipo debe encontrar al menos un error, omisión o afirmación demasiado fuerte hecha por la IA**. Eso transforma a los participantes de usuarios pasivos en revisores científicos.

---

# Preparación indispensable

## Dos semanas antes

- Congelar la versión de Mini-Me que se utilizará.
- Probar la instalación en las mismas laptops Windows.
- Crear una conversación y carpeta separada por equipo.
- Preinstalar credenciales y comprobar acceso a Asta.
- Confirmar créditos disponibles; no asumir que una promoción anterior sigue activa.
- Preparar resultados terminados de Theorizer, DataVoyager y AutoDiscovery.
- Descargar los PDFs abiertos.
- Crear versiones `dirty`, `clean` y una clave del facilitador.
- Probar todos los prompts exactamente como aparecerán en las tarjetas.

## Respaldo ante fallos

Cada actividad en línea debería tener:

- Captura o JSON de un resultado real.
- Archivos producidos previamente.
- Informe de ejemplo.
- Código generado.
- Una tarjeta que permita continuar el análisis sin conexión.

## Precauciones por los defectos actuales

Antes del workshop corregiría, o mitigaría en la guía, tres hallazgos de la auditoría:

- Un mensaje de herramienta fallido puede abrir el camino a un artefacto con apariencia exitosa. Los participantes deben comprobar `status`, identificador de tarea y archivos reales.
- `diagnostic_analytics` puede aceptar el formulario de contexto completamente vacío. Conviene entregar una plantilla obligatoria con pregunta, outcome, drivers, unidad de análisis, periodo y confusores.
- El Research Planner actualmente no incluye AutoDiscovery entre sus acciones permitidas. No lo usaría para generar automáticamente el flujo del Día 2.

## Recomendación final

No intentaría enseñar todos los detalles estadísticos ni todos los agentes en seis horas. El aprendizaje central debería ser:

> **La IA acelera tareas; el científico mantiene la responsabilidad sobre la pregunta, los datos, la evidencia y la interpretación.**

El siguiente entregable práctico debería ser un paquete del workshop con:

- Un dataset maestro sintético.
- Versiones limpia y sucia.
- Diccionario de variables.
- Cuatro tarjetas de retos.
- Prompts iniciales.
- Respuestas esperadas para el facilitador.
- Rúbrica y encuesta pre/post.
