# Facilitator key — Sweetpotato nutrition and biofortification

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- orange_color_index has a strong positive term in the beta-carotene generating equation.
- carotenoid_pathway_score independently increases beta-carotene.

## Confounded association

storage_days appears related to beta-carotene because both differ by lab_batch; storage has no direct term in the generating equation.

## Null variable

rack_slot_number is assigned randomly.

## Leakage

beta_carotene_mg_100g is the outcome expressed in another unit.

## Dirty-file defects

- Duplicate rows: 4
- Missing cells: orange_color_index=6, iron_mg_kg=6, dry_matter_pct=6, sensory_acceptance_score=6
- Inconsistent category cells: flesh_color=8, location=8
- Mixed-unit cells: beta_carotene_ug_g=4, iron_mg_kg=4
- Impossible values: sensory_acceptance_score=[12.0], dry_matter_pct=[118.0]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:storage_days`: +0.588
- `confounded:within:storage_days`: +0.066
- `leakage:beta_carotene_mg_100g`: +1.000
- `null:rack_slot_number`: +0.075
- `real:carotenoid_pathway_score`: +0.244
- `real:orange_color_index`: +0.819

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Laboratory batch and genotype allocation are not independently randomized, and compositional measurements do not establish human nutritional impact.
