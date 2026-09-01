# Facilitator key — Potato breeding multi-environment trials

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- Higher canopy cover increases simulated yield, conditional on the rest of the generating process.
- Higher late-blight severity decreases simulated yield.

## Confounded association

Irrigation appears positively associated with yield because high-yield lowland sites also receive more irrigation; irrigation has no direct term in the yield equation.

## Null variable

plot_marker_number is random and unrelated to all biological outcomes.

## Leakage

harvest_value_usd_ha is calculated after harvest from yield and price.

## Dirty-file defects

- Duplicate rows: 7
- Missing cells: canopy_cover_pct=10, late_blight_severity_pct=10, soil_ph=10, dry_matter_pct=10
- Inconsistent category cells: site=13, season=13
- Mixed-unit cells: yield_t_ha=7, altitude_m=7
- Impossible values: soil_ph=[14.7], late_blight_severity_pct=[135.0]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:irrigation_mm`: +0.809
- `confounded:within:irrigation_mm`: +0.037
- `leakage:harvest_value_usd_ha`: +0.959
- `null:plot_marker_number`: -0.035
- `real:canopy_cover_pct`: +0.307
- `real:late_blight_severity_pct`: -0.574

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Irrigation differs systematically by site and is not independently randomized, so its marginal association with yield is not causal.
