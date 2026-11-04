"""Apply what the workshop datasets mean to the dictionaries adapt_dataset.py wrote.

The adapter infers structure, never meaning: which column is the outcome, which ones
are computed from it, what unit a field team used. Those answers come from the data
owner's own dictionaries (Crop Ontology templates for the trials, a variable list for
the survey) and live here, so re-running the adapter never loses them.

    python scripts/configurar_taller.py datasets/

Run it after adapt_dataset.py and before corrupt_dataset.py, which should read the
full dictionary so the facilitator key lists the leakage columns:

    python scripts/corrupt_dataset.py datasets/<slug>/<slug>_clean.csv --dictionary datasets/<slug>/<slug>_dictionary_completo.csv

Every role marked as a proposal in PREGUNTAS still needs the data owner's confirmation.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

# Column -> fields to overwrite in <slug>_dictionary.csv. A key ending in "*" matches
# every column with that prefix.
CONFIG: dict[str, dict[str, dict[str, str]]] = {
    "mejoramiento": {
        "country": {"role": "context", "description": "País del ensayo"},
        "adm1": {"role": "context", "description": "Región"},
        "adm2": {"role": "context", "description": "Provincia"},
        "adm3": {"role": "context", "description": "Distrito"},
        "location": {"role": "design", "description": "Localidad del ensayo (una sola en estos datos)"},
        "elevation": {"unit": "m", "role": "context", "description": "Altitud del campo"},
        "latitude": {"unit": "deg", "role": "context", "description": "Latitud del campo"},
        "longitude": {"unit": "deg", "role": "context", "description": "Longitud del campo"},
        "rep": {"role": "design", "valid_values_or_range": "1-4", "description": "Repetición (bloque)"},
        "instn": {"role": "design", "description": "Genotipo evaluado (código de accesión CIP)"},
        "ntp": {"unit": "tuber/plot", "role": "predictor", "valid_values_or_range": "0-500",
                "description": "Número de tubérculos sembrados por parcela"},
        "nph": {"unit": "plants/plot", "role": "predictor", "description": "Número de plantas cosechadas por parcela"},
        "pph": {"unit": "%", "role": "predictor", "valid_values_or_range": "0-100",
                "description": "Proporción de plantas cosechadas"},
        "tntp": {"unit": "tuber/plot", "role": "predictor", "description": "Número de tubérculos cosechados por parcela"},
        "tntpl": {"unit": "tuber/plant", "role": "predictor", "description": "Número de tubérculos por planta"},
        "ttwp": {"unit": "kg", "role": "leakage",
                 "description": "Peso de tubérculos por parcela (kg/parcela). El rendimiento se calcula a partir de él"},
        "ttwpl": {"unit": "kg", "role": "leakage", "description": "Peso de tubérculos por planta (kg/planta)"},
        "ttyna": {"unit": "t/ha", "role": "leakage", "valid_values_or_range": "0-100",
                  "description": "Rendimiento sin ajustar. Es casi el mismo dato que el resultado"},
        "ttya": {"unit": "t/ha", "role": "outcome", "valid_values_or_range": "0-100",
                 "description": "Rendimiento ajustado de tubérculos"},
        "atw": {"unit": "g", "role": "predictor", "description": "Peso medio del tubérculo"},
    },
    "morfologia": {
        "accession_number": {"role": "design", "description": "Número de accesión del banco de germoplasma"},
        "accession_name": {"role": "design", "description": "Nombre de la accesión"},
        "country_of_selection": {"role": "context", "description": "País donde se seleccionó la variedad"},
        "tuber_skin_predominant_color": {"role": "predictor", "description": "Color predominante de la piel (código)"},
        "tuber_skin_secondary_color": {"role": "predictor", "description": "Color secundario de la piel (código)"},
        "distribution_of_secondary_color": {"role": "predictor", "description": "Distribución del color secundario de la piel (código)"},
        "tuber_flesh_predominant_color": {"role": "predictor", "description": "Color predominante de la pulpa (código)"},
        "tuber_flesh_secondary_color": {"role": "predictor", "description": "Color secundario de la pulpa (código)"},
        "tuber_flesh_secondary_color_distribution": {"role": "predictor", "description": "Distribución del color secundario de la pulpa (código)"},
        "tuber_shape": {"role": "predictor", "description": "Forma general del tubérculo (código)"},
        "tuber_shape_unusual": {"role": "predictor", "description": "Forma rara del tubérculo: 0 ausente, 1 presente"},
        "tuber_shape_depth_of_eyes": {"role": "predictor", "description": "Profundidad de ojos (código)"},
    },
    "tizon_tardio": {
        "plot": {"role": "design", "description": "Parcela"},
        "rep": {"role": "design", "description": "Repetición (bloque)"},
        "treatment": {"role": "design", "description": "Tratamiento fungicida aplicado"},
        "class": {"role": "design", "description": "Tipo de tratamiento: control, convencional o fosfonato"},
        "site": {"role": "design", "description": "Localidad del ensayo en Kenia"},
        "instn": {"role": "design", "description": "Genotipo evaluado"},
        "accename": {"role": "design", "description": "Nombre de la variedad"},
        "audpc": {"role": "outcome", "valid_values_or_range": "0-6000",
                  "description": "Área bajo la curva de progreso del tizón tardío"},
        "raudpc": {"role": "leakage", "valid_values_or_range": "0-1",
                   "description": "AUDPC relativo. Se calcula a partir del AUDPC"},
        "rlb": {"role": "leakage", "description": "Resistencia al tizón, clasificada a partir del rAUDPC"},
        "ttya": {"unit": "t/ha", "role": "context", "valid_values_or_range": "0-100",
                 "description": "Rendimiento ajustado (resultado secundario)"},
    },
    "consumidores": {
        "encuesta": {"role": "design", "description": "Número de encuesta"},
        "distrito": {"role": "design", "description": "Distrito de Lima donde se encuestó"},
        "fecha": {"role": "design", "description": "Fecha de la encuesta"},
        "encuestador": {"role": "design", "description": "Código del encuestador (posible efecto encuestador)"},
        "sexo": {"role": "context", "description": "F femenino, M masculino"},
        "edad": {"unit": "years", "role": "context", "description": "Edad de la persona encuestada"},
        # Checkboxes: an empty cell meant "not ticked". Written as 0 by BLANK_AS_ZERO.
        "v1*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                "description": "Conoce y consume papas nativas de color (1 = marcado)"},
        "v2*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                "description": "Frecuencia de consumo (1 = marcado)"},
        "v3*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                "description": "Ocasión de consumo (1 = marcado)"},
        "v4*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                "description": "Cantidad que compra (1 = marcado)"},
        "v5*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                "description": "Forma de preparación (1 = marcado)"},
        "v6*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                "description": "Dónde las compra (1 = marcado)"},
        "v10*": {"data_type": "category", "valid_values_or_range": "0|1", "role": "predictor",
                 "description": "Por dónde se enteró (1 = marcado)"},
        "v7*": {"data_type": "integer", "valid_values_or_range": "1-3", "role": "predictor",
                "description": "Importancia al comprar: 1 muy importante, 2 importante, 3 poco importante"},
        "v8*": {"data_type": "integer", "valid_values_or_range": "1-3", "role": "predictor",
                "description": "Percepción de las papas nativas de color. Escala sin documentar: 1-3 en los datos"},
        "v9*": {"data_type": "integer", "valid_values_or_range": "1-5", "role": "predictor",
                "description": "Acuerdo: 1 muy de acuerdo ... 4 total desacuerdo; 5 = no sé (no es ordinal)"},
        "v9pagarpreciojustoalagricultor": {"data_type": "integer", "valid_values_or_range": "1-5", "role": "outcome",
                "description": "Pagaría un precio justo al agricultor: 1 muy de acuerdo ... 4 total desacuerdo; 5 = no sé"},
        "v11*": {"data_type": "integer", "valid_values_or_range": "1-5", "role": "predictor",
                 "description": "Acuerdo sobre la campaña en Wong: 1 muy de acuerdo ... 4 total desacuerdo; 5 = no sé"},
    },
}

# Checkbox groups whose blank cells are rewritten as 0 in <slug>_clean.csv.
BLANK_AS_ZERO = {"consumidores": ("v1", "v2", "v3", "v4", "v5", "v6", "v10")}

# Open questions for the data owner, appended to <slug>_ADAPTATION.md.
PREGUNTAS = {
    "mejoramiento": [
        "Hay una sola localidad (La Victoria, Huancayo): la pregunta de estabilidad entre ambientes del plan no se puede responder con estos datos. ¿Se cambia por '¿qué genotipos rinden más?'",
        "¿El resultado es `ttya` (rendimiento ajustado)? Si es así, `ttwp`, `ttwpl` y `ttyna` son leakage.",
        "`ttya` tiene 13 celdas vacías en el original: ¿son parcelas perdidas?",
        "El diccionario fija TNTP en 0-50, pero los datos llegan a 536 tubérculos por parcela: ¿el límite es por planta?",
    ],
    "morfologia": [
        "No hay variable de resultado: el ejercicio es agrupar accesiones por descriptores. ¿Correcto?",
        "Los colores y formas son códigos: ¿hay una tabla de códigos para el diccionario?",
    ],
    "tizon_tardio": [
        "¿El resultado es `audpc`? Si es así, `raudpc` y `rlb` son leakage (se calculan a partir de él).",
        "`rlb` usa texto (Resistant, Susceptible...) y el diccionario una escala numérica de 7 puntos: ¿cuál se usa?",
    ],
    "consumidores": [
        "Propuesta de resultado: `v9pagarpreciojustoalagricultor`. ¿Hay otra pregunta que interese más?",
        "La escala de `v8` no está en el diccionario y los datos solo tienen 1-3: ¿qué significa cada valor?",
        "En `v9` y `v11`, el 5 significa 'no sé': ¿se trata como faltante en el análisis?",
    ],
}


def apply(folder: Path, slug: str) -> list[str]:
    config = CONFIG[slug]
    dictionary = folder / f"{slug}_dictionary.csv"
    with dictionary.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]

    used: set[str] = set()
    for row in rows:
        name = row["column"]
        exact = config.get(name)
        prefix = next(
            (key for key in sorted(config, key=len, reverse=True) if key.endswith("*") and name.startswith(key[:-1])),
            None,
        )
        for key in (prefix, name if exact else None):
            if key:
                row.update(config[key])
                used.add(key)

    # The full dictionary is for facilitators and corrupt_dataset.py. The participants'
    # copy hides the leakage role: finding those columns is part of the exercise, and
    # the descriptions still say where each one comes from.
    complete = folder / f"{slug}_dictionary_completo.csv"
    hidden = [{**row, "role": "predictor"} if row.get("role") == "leakage" else row for row in rows]
    for path, content in ((complete, rows), (dictionary, hidden)):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(content)

    leaks = sum(1 for row in rows if row.get("role") == "leakage")
    notes = [
        f"- {len(used)} entradas de configuración aplicadas. Diccionario completo en `{complete.name}`; "
        f"en `{dictionary.name}` (participantes) las {leaks} columnas leakage aparecen como `predictor`."
    ]
    unused = sorted(set(config) - used)
    if unused:
        notes.append(f"- Sin columna correspondiente (revisar): {', '.join(unused)}.")

    groups = BLANK_AS_ZERO.get(slug)
    if groups:
        clean = folder / f"{slug}_clean.csv"
        with clean.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = list(reader.fieldnames or [])
            data = [dict(row) for row in reader]
        targets = [c for c in header if any(c.startswith(g) and c[len(g):][:1].isalpha() for g in groups)]
        filled = 0
        for record in data:
            for column in targets:
                if record[column] == "":
                    record[column] = "0"
                    filled += 1
        with clean.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)
        notes.append(
            f"- Casillas de marcar ({', '.join(groups)}): {filled} celdas vacías pasan a 0 en `{clean.name}`. "
            "Vacío significaba 'no marcado'; sin esto, un faltante sembrado sería indistinguible de un 'no'."
        )
    return notes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datasets", type=Path, help="folder holding one subfolder per dataset")
    args = parser.parse_args()

    for slug in CONFIG:
        folder = args.datasets / slug
        if not (folder / f"{slug}_dictionary.csv").exists():
            print(f"{slug}: no adaptado todavía, se omite")
            continue
        notes = apply(folder, slug)
        report = folder / f"{slug}_ADAPTATION.md"
        section = ["", "## Configuración del taller (`configurar_taller.py`)", "", *notes, "",
                   "Preguntas para quien produjo los datos:", ""]
        section += [f"{i}. {q}" for i, q in enumerate(PREGUNTAS[slug], 1)]
        text = report.read_text(encoding="utf-8")
        marker = "\n## Configuración del taller"
        if marker in text:
            text = text[: text.index(marker)]
        report.write_text(text.rstrip("\n") + "\n" + "\n".join(section) + "\n", encoding="utf-8")
        print(f"{slug}:")
        for note in notes:
            print(f"  {note}")


if __name__ == "__main__":
    main()
