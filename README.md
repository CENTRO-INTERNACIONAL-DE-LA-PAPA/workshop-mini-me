# Workshop Mini-Me — CIP

Materiales del workshop de un día **De datos crudos a un Data-Driven Document**, el
**jueves 22 de octubre de 2026**.

El plan completo, con agenda, milestones y riesgos, está en
[`workshop_plan.md`](workshop_plan.md).

## Qué hay aquí

| Carpeta | Qué es |
|---|---|
| `scripts/` | El pipeline de preparación de datos |
| `manual/` | El manual del participante, en Quarto + Typst |
| `datasets/` | Los paquetes por temática. **Vacío hasta que lleguen los datos** |

## El pipeline

Tres pasos. El primero normaliza, el segundo rompe con registro, el tercero mide.

```
archivo real  ──adapt──▶  clean.csv     ──corrupt──▶  dirty.csv    ──score──▶  % reparado
   (de quien                dictionary.csv             changelog.csv
    lo produjo)             ADAPTATION.md              defect_key.md
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

Los cuatro paquetes del workshop salen de datos reales de investigación de CIP —morfología
de papa del banco de germoplasma, breeding, enfermedad y encuestas a agricultores—
anonimizados antes de entrar aquí.

> **Las encuestas a agricultores contienen datos personales.** No entran a ninguna
> herramienta de IA sin anonimización y visto bueno escrito del responsable del dato. Ver
> §2.4 del plan.

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
