"""Measure how much of the seeded damage a participant actually repaired.

`score_cleanliness.py` answers "how close is this file to the benchmark?" and its
answer is compressed: a corrupted file already scores around 96-98/100, so cleaning it
looks like a two-point gain. This script answers the question participants care about,
using the changelog written by `corrupt_dataset.py`:

    of the defects we planted, how many did you fix?

That runs 0-100% and is readable without explaining the weighting of a composite score.

    python scripts/score_recovery.py my_cleaned.csv --changelog <slug>_changelog.csv

Cell equality uses the same rules as score_cleanliness.py, imported rather than
reimplemented, so the two scripts can never drift apart on what counts as equal.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_cleanliness import (  # noqa: E402
    dictionary_types,
    discover_companions,
    read_csv,
    values_equal,
)

CELL_FAMILIES = {
    "category_variant",
    "date_format",
    "impossible_value",
    "missing_cell",
    "mixed_unit",
    "whitespace_case",
}


def discover_changelog(reference: Path) -> Path:
    """The changelog sits beside the clean reference it was generated from."""
    name = reference.name
    slug = name[: -len("_clean.csv")] if name.endswith("_clean.csv") else reference.stem
    return reference.with_name(f"{slug}_changelog.csv")


def index_rows(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    index: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        index.setdefault((row.get(key) or "").strip(), []).append(row)
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("candidate", type=Path, help="the participant's cleaned CSV")
    parser.add_argument("--changelog", type=Path, default=None)
    parser.add_argument("--reference", type=Path, default=None)
    parser.add_argument("--dictionary", type=Path, default=None)
    parser.add_argument("--show", type=int, default=8, help="unrepaired defects to list")
    args = parser.parse_args()

    if not args.candidate.exists():
        raise SystemExit(f"{args.candidate}: not found")

    found_reference, found_dictionary = discover_companions(args.candidate)
    reference = args.reference or found_reference
    dictionary = args.dictionary or found_dictionary
    changelog = args.changelog or discover_changelog(reference)

    for path, label in ((reference, "clean reference"), (dictionary, "dictionary"), (changelog, "changelog")):
        if not path.exists():
            raise SystemExit(f"{path}: {label} not found")

    primary, types = dictionary_types(dictionary)
    _, candidate_rows = read_csv(args.candidate)
    _, changes = read_csv(changelog)

    if primary not in (candidate_rows[0] if candidate_rows else {}):
        raise SystemExit(f"{args.candidate}: no column named '{primary}' to match rows by")

    index = index_rows(candidate_rows, primary)

    repaired: dict[str, int] = {}
    total: dict[str, int] = {}
    dropped: dict[str, int] = {}
    unrepaired: list[str] = []

    for change in changes:
        family = change["family"]
        record_id = change["record_id"].strip()
        total[family] = total.get(family, 0) + 1
        rows = index.get(record_id, [])

        if not rows:
            # The row is gone. Deleting data is not repairing it.
            dropped[family] = dropped.get(family, 0) + 1
            if len(unrepaired) < args.show:
                unrepaired.append(f"  {record_id} / {family}: fila eliminada del archivo")
            continue

        if family == "duplicate_row":
            if len(rows) == 1:
                repaired[family] = repaired.get(family, 0) + 1
            elif len(unrepaired) < args.show:
                unrepaired.append(f"  {record_id}: sigue duplicada ({len(rows)} copias)")
            continue

        column = change["column"]
        original = change["original_value"]
        data_type = types.get(column, "string")
        # Every surviving copy has to be right, otherwise the duplicate hides a defect.
        if all(values_equal(row.get(column), original, data_type) for row in rows):
            repaired[family] = repaired.get(family, 0) + 1
        elif len(unrepaired) < args.show:
            got = rows[0].get(column)
            unrepaired.append(f"  {record_id} / {column}: '{got}' deberia ser '{original}' ({family})")

    total_all = sum(total.values())
    repaired_all = sum(repaired.values())
    if not total_all:
        raise SystemExit(f"{changelog}: no changes recorded")

    print(f"Reparacion: {repaired_all / total_all * 100:.1f}%  ({repaired_all}/{total_all} defectos sembrados)")
    print()
    print(f"{'Familia':<20}{'Reparados':>11}{'%':>8}{'Filas borradas':>17}")
    for family in sorted(total):
        count = total[family]
        fixed = repaired.get(family, 0)
        print(f"{family:<20}{f'{fixed}/{count}':>11}{fixed / count * 100:>7.1f}%{dropped.get(family, 0):>17}")

    # Cells the participant changed that were never a defect: over-cleaning.
    _, reference_rows = read_csv(reference)
    reference_index = {(row.get(primary) or "").strip(): row for row in reference_rows}
    seeded = {(c["record_id"].strip(), c["column"]) for c in changes if c["family"] in CELL_FAMILIES}
    collateral = 0
    for record_id, rows in index.items():
        benchmark = reference_index.get(record_id)
        if not benchmark:
            continue
        for column, expected in benchmark.items():
            if (record_id, column) in seeded:
                continue
            if any(not values_equal(row.get(column), expected, types.get(column, "string")) for row in rows):
                collateral += 1

    print()
    if collateral:
        print(f"Dano colateral: {collateral} celdas que no eran defecto y ahora difieren del original.")
    else:
        print("Dano colateral: ninguno. No se modifico nada que no estuviera roto.")

    if unrepaired:
        print(f"\nSin reparar (muestra de {len(unrepaired)}):")
        for line in unrepaired:
            print(line)


if __name__ == "__main__":
    main()
