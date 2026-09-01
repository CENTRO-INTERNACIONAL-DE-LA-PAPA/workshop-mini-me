# Facilitator key — Seed-system lot quality

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- Higher virus incidence decreases simulated marketable-seed percentage.
- More training visits increase simulated marketable-seed percentage.

## Confounded association

Inspection fee appears associated with quality because both vary by country_site; fee has no direct generating term.

## Null variable

bag_label_number is random.

## Leakage

marketable_seed_fraction is marketable_seed_pct divided by 100.

## Dirty-file defects

- Duplicate rows: 8
- Missing cells: virus_incidence_pct=11, training_visits=11, producer_scale=11, lot_weight_kg=11
- Inconsistent category cells: crop=14, producer_scale=14
- Mixed-unit cells: lot_weight_kg=8, inspection_fee_usd=8
- Impossible values: virus_incidence_pct=[145.0], lot_weight_kg=[-25.0]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:inspection_fee_usd`: +0.514
- `confounded:within:inspection_fee_usd`: -0.105
- `leakage:marketable_seed_fraction`: +1.000
- `null:bag_label_number`: +0.001
- `real:training_visits`: +0.322
- `real:virus_incidence_pct`: -0.708

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Only inspected lots are represented and training is not randomly assigned, so observed differences cannot establish the impact of training.
