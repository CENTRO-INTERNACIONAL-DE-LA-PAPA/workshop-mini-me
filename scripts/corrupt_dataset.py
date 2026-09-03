"""Corrupt a clean workshop dataset and record every change.

The corruption is driven by the data dictionary, not by a hand-written plan, so the
script works on any dataset that ships the canonical dictionary columns. Nothing is
decided at random in the colloquial sense: a seeded RNG makes every run reproducible,
and every single modified cell is written to a changelog.

    python scripts/corrupt_dataset.py datasets/potato_breeding_trials/potato_breeding_trials_clean.csv

Outputs, next to the input unless --output-dir says otherwise:

    <slug>_dirty.csv        the participant starting point
    <slug>_changelog.csv    one row per atomic change: what it was, what it became
    <slug>_defect_key.md    facilitator summary derived from the changelog

The changelog is the ground truth for measuring how much of the damage a participant
actually repaired, which is a stricter question than overall cell agreement.
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
import unicodedata
from pathlib import Path
from typing import Any, Callable

CHANGELOG_FIELDS = [
    "change_id",
    "family",
    "record_id",
    "column",
    "original_value",
    "new_value",
    "detail",
]

DEFAULT_SEED = 20261022  # the workshop date; nothing meaningful, just fixed

DEFAULT_RATES = {
    "missing": 0.035,
    "category": 0.045,
    "unit": 0.025,
    "whitespace": 0.020,
    "date": 0.030,
    "duplicate": 0.025,
}

# Unit pairs a field scientist would plausibly mix in the same column. Anything not
# listed is left alone: an implausible conversion teaches nothing.
UNIT_CONVERTERS: dict[str, tuple[str, Callable[[float], float]]] = {
    "m": ("ft", lambda v: v * 3.28084),
    "cm": ("mm", lambda v: v * 10.0),
    "mm": ("in", lambda v: v / 25.4),
    "mm/season": ("in/season", lambda v: v / 25.4),
    "t/ha": ("kg/ha", lambda v: v * 1000.0),
    "kg/ha": ("t/ha", lambda v: v / 1000.0),
    "kg": ("lb", lambda v: v * 2.20462),
    "ha": ("ac", lambda v: v * 2.47105),
    "%": ("fraction 0-1", lambda v: v / 100.0),
    "pct": ("fraction 0-1", lambda v: v / 100.0),
    "deg c": ("deg F", lambda v: v * 9.0 / 5.0 + 32.0),
}


# --------------------------------------------------------------------------- io


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def discover_dictionary(clean: Path) -> Path:
    """Mirror score_cleanliness.discover_companions so the three scripts agree."""
    name = clean.name
    for suffix in ("_clean.csv", "_dirty.csv"):
        if name.endswith(suffix):
            return clean.with_name(f"{name[: -len(suffix)]}_dictionary.csv")
    return clean.with_name(f"{clean.parent.name}_dictionary.csv")


def slug_for(clean: Path) -> str:
    name = clean.name
    for suffix in ("_clean.csv", "_dirty.csv"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return clean.stem


# --------------------------------------------------------- dictionary handling


class Spec:
    """What the dictionary says about one column."""

    def __init__(self, row: dict[str, str]) -> None:
        self.name = (row.get("column") or "").strip()
        self.data_type = (row.get("data_type") or "string").strip().lower()
        self.unit = (row.get("unit") or "none").strip()
        self.role = (row.get("role") or "").strip().lower()
        self.valid = (row.get("valid_values_or_range") or "").strip()

    @property
    def numeric(self) -> bool:
        return self.data_type in {"number", "integer"}

    @property
    def integer(self) -> bool:
        return self.data_type == "integer"

    def categories(self) -> list[str]:
        if self.data_type != "category" or "|" not in self.valid:
            return []
        return [item.strip() for item in self.valid.split("|") if item.strip()]

    def bounds(self) -> tuple[float, float] | None:
        """Parse '0-100', '3.0-9.0' or '>=0' into usable bounds."""
        text = self.valid
        if text.startswith(">="):
            try:
                return (float(text[2:].strip()), float(text[2:].strip()) + 100.0)
            except ValueError:
                return None
        # A leading minus would be a negative lower bound, not a separator.
        body = text[1:] if text.startswith("-") else text
        if "-" not in body or ".." in text:
            return None
        left, _, right = body.partition("-")
        prefix = "-" if text.startswith("-") else ""
        try:
            return (float(prefix + left.strip()), float(right.strip()))
        except ValueError:
            return None

    def converter(self) -> tuple[str, Callable[[float], float]] | None:
        return UNIT_CONVERTERS.get(self.unit.strip().lower())


def load_specs(path: Path) -> tuple[dict[str, Spec], str]:
    _, rows = read_csv(path)
    specs = {}
    primary = ""
    for row in rows:
        spec = Spec(row)
        if not spec.name:
            continue
        specs[spec.name] = spec
        if spec.role == "primary_key":
            primary = spec.name
    if not primary:
        raise SystemExit(
            f"{path}: no column has role=primary_key. Run adapt_dataset.py first so the "
            "dataset gets a synthetic record_id."
        )
    return specs, primary


# ------------------------------------------------------------------ formatting


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def format_number(value: float, integer: bool) -> str:
    if integer:
        return str(int(round(value)))
    rounded = round(value, 3)
    return str(int(rounded)) if rounded == int(rounded) else str(rounded)


def category_variant(value: str, rng: random.Random) -> tuple[str, str] | None:
    """A variant a human would actually type. Returns (new_value, what_changed)."""
    options: list[tuple[str, str]] = [
        (value.upper(), "uppercase"),
        (value.lower(), "lowercase"),
        (f" {value}", "leading space"),
        (f"{value} ", "trailing space"),
        (value.replace(" ", "  "), "double inner space") if " " in value else (value, ""),
    ]
    stripped = strip_accents(value)
    if stripped != value:
        options.append((stripped, "accents removed"))
    usable = [item for item in options if item[0] != value and item[1]]
    return rng.choice(usable) if usable else None


def date_variant(value: str, rng: random.Random) -> tuple[str, str] | None:
    """Re-render an ISO date in a format that will not parse the same way."""
    parts = value.split("-")
    if len(parts) != 3 or len(parts[0]) != 4:
        return None
    year, month, day = parts
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return None
    options = [
        (f"{int(day):02d}/{int(month):02d}/{year[2:]}", "DD/MM/YY"),
        (f"{int(month):02d}-{int(day):02d}-{year}", "MM-DD-YYYY"),
        (f"{int(day)}/{int(month)}/{year}", "D/M/YYYY"),
    ]
    return rng.choice(options)


def whitespace_variant(value: str, rng: random.Random) -> tuple[str, str] | None:
    options = [(f" {value}", "leading space"), (f"{value} ", "trailing space")]
    if value.lower() != value:
        options.append((value.lower(), "lowercase"))
    usable = [item for item in options if item[0] != value]
    return rng.choice(usable) if usable else None


# ------------------------------------------------------------------ corruption


class Corruptor:
    def __init__(
        self,
        rows: list[dict[str, str]],
        specs: dict[str, Spec],
        primary: str,
        rates: dict[str, float],
        seed: int,
    ) -> None:
        self.rows = [dict(row) for row in rows]
        self.specs = specs
        self.primary = primary
        self.rates = rates
        self.rng = random.Random(seed)
        self.changes: list[dict[str, str]] = []
        self.touched: set[tuple[int, str]] = set()

    # Sorting every candidate list keeps the seed meaningful across Python versions.
    def _eligible(self, predicate: Callable[[Spec], bool]) -> list[str]:
        return sorted(
            name
            for name, spec in self.specs.items()
            if name != self.primary and name in self.rows[0] and predicate(spec)
        )

    def _count(self, rate: float, minimum: int = 2) -> int:
        return max(minimum, round(len(self.rows) * rate))

    def _pick_rows(self, column: str, count: int) -> list[int]:
        free = [i for i in range(len(self.rows)) if (i, column) not in self.touched]
        return sorted(self.rng.sample(free, min(count, len(free))))

    def _record(self, family: str, index: int, column: str, original: str, new: str, detail: str) -> None:
        self.rows[index][column] = new
        self.touched.add((index, column))
        self.changes.append(
            {
                "change_id": f"C{len(self.changes) + 1:05d}",
                "family": family,
                "record_id": self.rows[index].get(self.primary, ""),
                "column": column,
                "original_value": original,
                "new_value": new,
                "detail": detail,
            }
        )

    # -- families ----------------------------------------------------------

    def missing_cells(self) -> None:
        for column in self._eligible(lambda _s: True):
            for index in self._pick_rows(column, self._count(self.rates["missing"])):
                original = self.rows[index][column]
                if original == "":
                    continue
                self._record("missing_cell", index, column, original, "", "value blanked")

    def category_variants(self) -> None:
        for column in self._eligible(lambda s: bool(s.categories())):
            for index in self._pick_rows(column, self._count(self.rates["category"])):
                original = self.rows[index][column]
                variant = category_variant(original, self.rng) if original else None
                if variant:
                    self._record("category_variant", index, column, original, variant[0], variant[1])

    def mixed_units(self) -> None:
        for column in self._eligible(lambda s: s.numeric and s.converter() is not None):
            spec = self.specs[column]
            target_unit, convert = spec.converter()  # type: ignore[misc]
            for index in self._pick_rows(column, self._count(self.rates["unit"])):
                original = self.rows[index][column]
                try:
                    converted = convert(float(original))
                except ValueError:
                    continue
                formatted = format_number(converted, spec.integer)
                if formatted == original:
                    continue  # e.g. converting a zero changes nothing: not a defect
                self._record(
                    "mixed_unit",
                    index,
                    column,
                    original,
                    formatted,
                    f"{spec.unit} -> {target_unit}",
                )

    def impossible_values(self) -> None:
        for column in self._eligible(lambda s: s.numeric and s.bounds() is not None):
            spec = self.specs[column]
            low, high = spec.bounds()  # type: ignore[misc]
            span = (high - low) or 1.0
            candidates = [
                (high + span * 0.5, "above the valid maximum"),
                (low - span * 0.2, "below the valid minimum"),
            ]
            for (value, detail), index in zip(candidates, self._pick_rows(column, 2)):
                original = self.rows[index][column]
                self._record(
                    "impossible_value",
                    index,
                    column,
                    original,
                    format_number(value, spec.integer),
                    detail,
                )

    def whitespace_case(self) -> None:
        for column in self._eligible(lambda s: s.data_type == "string" and not s.categories()):
            for index in self._pick_rows(column, self._count(self.rates["whitespace"])):
                original = self.rows[index][column]
                variant = whitespace_variant(original, self.rng) if original else None
                if variant:
                    self._record("whitespace_case", index, column, original, variant[0], variant[1])

    def date_formats(self) -> None:
        for column in self._eligible(lambda s: s.data_type == "date"):
            for index in self._pick_rows(column, self._count(self.rates["date"])):
                original = self.rows[index][column]
                variant = date_variant(original, self.rng) if original else None
                if variant:
                    self._record("date_format", index, column, original, variant[0], variant[1])

    def duplicate_rows(self) -> None:
        """Runs last: duplicates carry whatever corruption their source row received."""
        count = self._count(self.rates["duplicate"])
        for index in sorted(self.rng.sample(range(len(self.rows)), min(count, len(self.rows)))):
            source = self.rows[index]
            self.rows.append(dict(source))
            self.changes.append(
                {
                    "change_id": f"C{len(self.changes) + 1:05d}",
                    "family": "duplicate_row",
                    "record_id": source.get(self.primary, ""),
                    "column": "",
                    "original_value": "",
                    "new_value": "",
                    "detail": "whole row appended a second time",
                }
            )

    def run(self) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        self.category_variants()
        self.mixed_units()
        self.impossible_values()
        self.whitespace_case()
        self.date_formats()
        self.missing_cells()  # last of the cell families, so it can blank a corrupted cell
        self.duplicate_rows()
        self.rng.shuffle(self.rows)
        return self.rows, self.changes


# ------------------------------------------------------------------ reporting


def defect_key(slug: str, specs: dict[str, Spec], changes: list[dict[str, str]], seed: int) -> str:
    by_family: dict[str, list[dict[str, str]]] = {}
    for change in changes:
        by_family.setdefault(change["family"], []).append(change)

    lines = [
        f"# Clave de defectos — {slug}",
        "",
        "> No distribuir antes del ejercicio. Este archivo dice exactamente qué se rompió.",
        "",
        f"Semilla: `{seed}`. Volver a correr `corrupt_dataset.py` con la misma semilla reproduce",
        "estos archivos byte por byte.",
        "",
        f"**Total de cambios registrados: {len(changes)}**",
        "",
        "## Por familia",
        "",
        "| Familia | Cambios | Columnas afectadas |",
        "|---|---:|---|",
    ]
    for family in sorted(by_family):
        items = by_family[family]
        columns = sorted({item["column"] for item in items if item["column"]})
        lines.append(f"| `{family}` | {len(items)} | {', '.join(columns) if columns else '—'} |")

    lines += ["", "## Por columna", "", "| Columna | Cambios | Familias |", "|---|---:|---|"]
    by_column: dict[str, list[dict[str, str]]] = {}
    for change in changes:
        if change["column"]:
            by_column.setdefault(change["column"], []).append(change)
    for column in sorted(by_column):
        items = by_column[column]
        families = sorted({item["family"] for item in items})
        lines.append(f"| `{column}` | {len(items)} | {', '.join(families)} |")

    flagged = [(name, spec.role) for name, spec in sorted(specs.items()) if spec.role in {"leakage", "null", "confounded_exposure"}]
    if flagged:
        lines += [
            "",
            "## Columnas que no son un defecto de limpieza",
            "",
            "Están correctamente registradas: el problema es analítico, no de calidad del dato.",
            "",
            "| Columna | Rol |",
            "|---|---|",
        ]
        lines += [f"| `{name}` | `{role}` |" for name, role in flagged]

    lines += [
        "",
        "## Cómo se usa",
        "",
        f"El detalle celda a celda está en `{slug}_changelog.csv`: cada fila trae `record_id`,",
        "columna, valor original y valor sucio. Ese archivo permite medir cuántos de los defectos",
        "sembrados reparó realmente un equipo, que es una pregunta más estricta que el score global",
        "de `score_cleanliness.py`.",
        "",
    ]
    return "\n".join(lines)


# ----------------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("clean", type=Path, help="clean CSV to corrupt")
    parser.add_argument("--dictionary", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    for name, value in DEFAULT_RATES.items():
        parser.add_argument(f"--{name}-rate", type=float, default=value)
    args = parser.parse_args()

    clean_path: Path = args.clean
    if not clean_path.exists():
        raise SystemExit(f"{clean_path}: not found")

    dictionary_path = args.dictionary or discover_dictionary(clean_path)
    if not dictionary_path.exists():
        raise SystemExit(f"{dictionary_path}: dictionary not found")

    fieldnames, rows = read_csv(clean_path)
    if not rows:
        raise SystemExit(f"{clean_path}: no rows")
    specs, primary = load_specs(dictionary_path)

    unknown = sorted(set(fieldnames) - set(specs))
    if unknown:
        print(f"warning: not in the dictionary, left untouched: {', '.join(unknown)}", file=sys.stderr)

    rates = {name: getattr(args, f"{name}_rate") for name in DEFAULT_RATES}
    dirty, changes = Corruptor(rows, specs, primary, rates, args.seed).run()

    slug = slug_for(clean_path)
    out_dir = args.output_dir or clean_path.parent
    dirty_path = out_dir / f"{slug}_dirty.csv"
    changelog_path = out_dir / f"{slug}_changelog.csv"
    key_path = out_dir / f"{slug}_defect_key.md"

    write_csv(dirty_path, fieldnames, dirty)
    write_csv(changelog_path, CHANGELOG_FIELDS, changes)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(defect_key(slug, specs, changes, args.seed), encoding="utf-8")

    families: dict[str, int] = {}
    for change in changes:
        families[change["family"]] = families.get(change["family"], 0) + 1

    print(f"{slug}: {len(rows)} filas limpias -> {len(dirty)} filas sucias, semilla {args.seed}")
    for family in sorted(families):
        print(f"  {family:<20} {families[family]:>4}")
    print(f"  {'TOTAL':<20} {len(changes):>4}")
    print(f"\n  {dirty_path}\n  {changelog_path}\n  {key_path}")


if __name__ == "__main__":
    main()
