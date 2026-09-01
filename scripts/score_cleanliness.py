#!/usr/bin/env python3
"""Score a participant-cleaned CSV against its synthetic workshop reference.

The score is a reproducible benchmark, not a universal measure of scientific
quality.  It combines schema agreement (15%), record integrity (20%) and cell
accuracy (65%).  Row order is ignored.  A score of 100 means the candidate has
the expected columns, exactly one copy of every reference record, no extra
records, and matching values after numeric parsing.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


WEIGHTS = {"schema": 0.15, "records": 0.20, "cells": 0.65}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path}: the CSV has no header")
        return list(reader.fieldnames), [dict(row) for row in reader]


def discover_companions(candidate: Path) -> tuple[Path, Path]:
    name = candidate.name
    for suffix in ("_dirty.csv", "_clean.csv"):
        if name.endswith(suffix):
            slug = name[: -len(suffix)]
            return (
                candidate.with_name(f"{slug}_clean.csv"),
                candidate.with_name(f"{slug}_dictionary.csv"),
            )
    slug = candidate.parent.name
    return (
        candidate.with_name(f"{slug}_clean.csv"),
        candidate.with_name(f"{slug}_dictionary.csv"),
    )


def dictionary_types(path: Path) -> tuple[str, dict[str, str]]:
    _, rows = read_csv(path)
    types = {row.get("column", ""): row.get("data_type", "string") for row in rows}
    keys = [row.get("column", "") for row in rows if row.get("role") == "primary_key"]
    if len(keys) != 1:
        raise ValueError(f"{path}: expected exactly one dictionary row with role=primary_key")
    return keys[0], types


def numeric_equal(left: str, right: str, integer: bool) -> bool:
    try:
        a = float(left)
        b = float(right)
    except (TypeError, ValueError):
        return False
    if not (math.isfinite(a) and math.isfinite(b)):
        return False
    if integer:
        return a.is_integer() and b.is_integer() and int(a) == int(b)
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def values_equal(candidate: str | None, reference: str | None, data_type: str) -> bool:
    left = "" if candidate is None else candidate
    right = "" if reference is None else reference
    if data_type in {"number", "integer"}:
        return numeric_equal(left, right, data_type == "integer")
    # Whitespace and capitalization are data in categorical/string columns.  A
    # trim here would give full credit to exactly the inconsistencies being taught.
    return left == right


def score_file(candidate: Path, reference: Path, dictionary: Path) -> dict[str, Any]:
    candidate_columns, candidate_rows = read_csv(candidate)
    reference_columns, reference_rows = read_csv(reference)
    primary_key, types = dictionary_types(dictionary)

    expected_columns = set(reference_columns)
    actual_columns = set(candidate_columns)
    union = expected_columns | actual_columns
    schema_fraction = len(expected_columns & actual_columns) / len(union) if union else 1.0

    if primary_key not in actual_columns:
        candidate_ids: list[str] = []
    else:
        candidate_ids = [row.get(primary_key, "") for row in candidate_rows]
    reference_ids = [row.get(primary_key, "") for row in reference_rows]
    candidate_counts = Counter(candidate_ids)
    reference_set = set(reference_ids)
    candidate_set = set(candidate_ids)
    duplicate_count = sum(max(0, count - 1) for identifier, count in candidate_counts.items() if identifier)
    missing_ids = sorted(reference_set - candidate_set)
    extra_ids = sorted(identifier for identifier in candidate_set - reference_set if identifier)
    blank_key_rows = candidate_counts.get("", 0)
    expected_record_count = max(1, len(reference_rows))
    structural_errors = len(missing_ids) + len(extra_ids) + duplicate_count + blank_key_rows
    record_fraction = max(0.0, 1.0 - structural_errors / expected_record_count)

    # The first copy is used for cell comparison; any additional copies are
    # penalized by record integrity, so duplicates cannot hide cell defects.
    candidate_by_id: dict[str, dict[str, str]] = {}
    for row in candidate_rows:
        identifier = row.get(primary_key, "")
        if identifier and identifier not in candidate_by_id:
            candidate_by_id[identifier] = row

    mismatches: list[dict[str, str]] = []
    matched_cells = 0
    total_cells = len(reference_rows) * len(reference_columns)
    for reference_row in reference_rows:
        identifier = reference_row[primary_key]
        candidate_row = candidate_by_id.get(identifier)
        for name in reference_columns:
            if candidate_row is not None and name in actual_columns and values_equal(
                candidate_row.get(name), reference_row.get(name), types.get(name, "string")
            ):
                matched_cells += 1
            elif len(mismatches) < 12:
                mismatches.append(
                    {
                        "record_id": identifier,
                        "column": name,
                        "candidate": "<missing row>" if candidate_row is None else str(candidate_row.get(name, "<missing column>")),
                        "reference": str(reference_row.get(name, "")),
                    }
                )
    cell_fraction = matched_cells / total_cells if total_cells else 1.0
    score = 100 * (
        WEIGHTS["schema"] * schema_fraction
        + WEIGHTS["records"] * record_fraction
        + WEIGHTS["cells"] * cell_fraction
    )

    return {
        "candidate": str(candidate.resolve()),
        "reference": str(reference.resolve()),
        "score": round(score, 2),
        "components": {
            "schema": round(schema_fraction * 100, 2),
            "record_integrity": round(record_fraction * 100, 2),
            "cell_accuracy": round(cell_fraction * 100, 2),
        },
        "counts": {
            "candidate_rows": len(candidate_rows),
            "reference_rows": len(reference_rows),
            "duplicate_rows": duplicate_count,
            "blank_primary_keys": blank_key_rows,
            "missing_record_ids": len(missing_ids),
            "extra_record_ids": len(extra_ids),
            "mismatched_cells": total_cells - matched_cells,
            "reference_cells": total_cells,
        },
        "missing_columns": sorted(expected_columns - actual_columns),
        "extra_columns": sorted(actual_columns - expected_columns),
        "sample_missing_ids": missing_ids[:10],
        "sample_extra_ids": extra_ids[:10],
        "sample_cell_mismatches": mismatches,
    }


def print_human(result: dict[str, Any]) -> None:
    components = result["components"]
    counts = result["counts"]
    print(f"Cleanliness score: {result['score']:.2f}/100")
    print(
        "Components: "
        f"schema {components['schema']:.2f}, "
        f"records {components['record_integrity']:.2f}, "
        f"cells {components['cell_accuracy']:.2f}"
    )
    print(
        "Rows: "
        f"candidate {counts['candidate_rows']}, reference {counts['reference_rows']}, "
        f"duplicates {counts['duplicate_rows']}, missing IDs {counts['missing_record_ids']}, "
        f"extra IDs {counts['extra_record_ids']}"
    )
    print(
        f"Cells: {counts['mismatched_cells']} mismatches across "
        f"{counts['reference_cells']} benchmark cells"
    )
    if result["missing_columns"]:
        print("Missing columns: " + ", ".join(result["missing_columns"]))
    if result["extra_columns"]:
        print("Extra columns: " + ", ".join(result["extra_columns"]))
    if result["sample_cell_mismatches"]:
        print("Sample mismatches:")
        for item in result["sample_cell_mismatches"][:5]:
            print(
                f"  {item['record_id']} / {item['column']}: "
                f"{item['candidate']!r} -> expected {item['reference']!r}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", type=Path, help="CSV to score")
    parser.add_argument("--reference", type=Path, help="Clean reference CSV; autodetected by default")
    parser.add_argument("--dictionary", type=Path, help="Dictionary CSV; autodetected by default")
    parser.add_argument("--all", type=Path, metavar="DATASETS_DIR", help="Score every dirty and clean CSV below a datasets directory")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--fail-below", type=float, default=None, help="Exit 1 when any score is below this threshold")
    args = parser.parse_args()

    if bool(args.candidate) == bool(args.all):
        parser.error("provide exactly one candidate CSV or --all DATASETS_DIR")

    candidates = (
        sorted(args.all.glob("*/*_dirty.csv")) + sorted(args.all.glob("*/*_clean.csv"))
        if args.all
        else [args.candidate]
    )
    results = []
    for candidate in candidates:
        assert candidate is not None
        auto_reference, auto_dictionary = discover_companions(candidate)
        reference = args.reference or auto_reference
        dictionary = args.dictionary or auto_dictionary
        for required in (candidate, reference, dictionary):
            if not required.is_file():
                raise FileNotFoundError(required)
        results.append(score_file(candidate, reference, dictionary))

    if args.json:
        print(json.dumps(results[0] if len(results) == 1 else results, indent=2, ensure_ascii=False))
    else:
        for index, result in enumerate(results):
            if len(results) > 1:
                if index:
                    print()
                print(Path(result["candidate"]).name)
            print_human(result)

    if args.fail_below is not None and any(result["score"] < args.fail_below for result in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
