# Workshop Mini-Me — CIP

Materiales del workshop de un día **CIP Mini-Me: IA aplicada a la ciencia de datos**, el
**martes 24 de noviembre de 2026**.

El plan completo, con agenda, milestones y riesgos, está en
[`workshop_plan.md`](workshop_plan.md).

## Qué hay aquí

| Carpeta | Qué es |
|---|---|
| `scripts/` | El pipeline de preparación de datos |
| `presentacion/` | Las presentaciones de los bloques 1 y 2, en Quarto + Reveal.js |
| `manual/` | El manual del participante, en Quarto + Typst |
| `datasets/` | Los cuatro paquetes del taller (datos reales de CIP, públicos), con sus originales |

## El pipeline

Cuatro pasos. El primero normaliza, el segundo fija el significado, el tercero rompe con
registro y el cuarto mide.

```
archivo real  ──adapt──▶  clean.csv     ──configurar──▶  dictionary.csv  ──corrupt──▶  dirty.csv    ──score──▶  % reparado
   (de quien                dictionary.csv                (unidades, rangos,             changelog.csv
    lo produjo)             ADAPTATION.md                  roles)                        defect_key.md
```

### 1 · `adapt_dataset.py` — normalizar

Toma el archivo tal como lo entrega quien produjo los datos y devuelve el paquete canónico.
Lee CSV (probando codificaciones y detectando el delimitador) o Excel; convierte cabeceras
en español a nombres de columna manejables sin perder el original; normaliza comas decimales
y fechas; y **sintetiza un `record_id`** cuando ninguna columna sirve de identificador único.

```bash
python scripts/adapt_dataset.py "Ensayo 2025.xlsx" --slug breeding
```

Deduce estructura, nunca significado. Cuál es la variable de resultado, qué columnas se
calculan *después* de ella y qué relaciones ya se conocen no salen de un CSV: quedan como
preguntas abiertas en `<slug>_ADAPTATION.md`, para responder con quien conoce los datos.

**Ese paso intermedio es manual a propósito.** Sin saber cuál es el outcome no se puede
sembrar un *leakage* con sentido.

### 1b · `configurar_taller.py` — fijar el significado

Las respuestas a esas preguntas, para los cuatro datasets del taller, viven en este script:
unidades, rangos válidos y descripciones tomadas de los diccionarios de quien produjo los
datos, y el rol propuesto de cada columna (`outcome`, `leakage`, `design`...). Se corre después
del adaptador, así que volver a adaptar no las borra.

```bash
python scripts/configurar_taller.py datasets/
```

Agrega al final de cada `<slug>_ADAPTATION.md` las preguntas que siguen abiertas.

### 2 · `corrupt_dataset.py` — ensuciar con registro

Rompe el archivo limpio de forma **determinística** (semilla fija: la misma semilla
reproduce el mismo archivo byte por byte) y anota cada celda que toca.

```bash
python scripts/corrupt_dataset.py datasets/breeding/breeding_clean.csv
```

Siete familias de defectos —duplicados, variantes de categoría, unidades mezcladas, valores
imposibles, faltantes, espacios y mayúsculas, formatos de fecha— elegidas según lo que diga
el diccionario de cada columna, no según un plan escrito a mano.

El `changelog.csv` es la pieza clave: `record_id`, columna, valor original, valor sucio y
qué se le hizo.

### 3 · `score_recovery.py` — medir

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

Tres números, no uno: cuánto del daño sembrado se reparó, cuántas filas se **borraron** en
lugar de arreglarlas, y cuántas celdas sanas se estropearon de paso.

### Y `score_cleanliness.py` — control de esquema

El score compuesto original (esquema 15%, integridad de registros 20%, concordancia celda a
celda 65%). Se conserva como control, pero **no como métrica del taller**: un archivo
corrupto ya puntúa 98/100, así que limpiarlo entero parece una mejora de dos puntos.

```bash
python scripts/score_cleanliness.py datasets/breeding/breeding_dirty.csv
```

## Sobre los datos

Los cuatro paquetes del workshop salen de datos reales de investigación de CIP:
morfología del banco de germoplasma (`morfologia`), un ensayo de rendimiento
(`mejoramiento`), un ensayo de fungicidas contra el tizón tardío (`tizon_tardio`) y una
encuesta de percepción de consumidores sobre papas nativas de color (`consumidores`).

> **Las encuestas contienen datos de personas.** No entran a ninguna herramienta de IA sin
> anonimización y visto bueno escrito del responsable del dato. Ver §2.4 del plan.

### Datos sintéticos

`scripts/generate_datasets.py` genera siete paquetes sintéticos completos (breeding,
nutrición, biodiversidad, banco de germoplasma, sistemas de semilla, agronomía y adopción).
Se usaron para construir y probar el pipeline y ya no se versionan, porque el workshop corre
sobre datos reales. Si hacen falta:

```bash
python scripts/generate_datasets.py --output-dir .
```

La semilla es fija: reproduce los mismos archivos byte por byte.

## El manual

```bash
cd manual && quarto render manual.qmd
```

Sale en `manual/_output/manual.pdf`. Detalles y advertencias en
[`manual/README.md`](manual/README.md).

## Requisitos

- Python 3.11+. El pipeline usa solo la biblioteca estándar, salvo `openpyxl` para leer
  Excel en `adapt_dataset.py`.
- Quarto 1.8+ para el manual. Typst viene incluido.
