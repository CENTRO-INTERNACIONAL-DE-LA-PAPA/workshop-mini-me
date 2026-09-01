# Facilitator key — Genebank conservation and regeneration

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- Longer storage duration decreases simulated viability.
- Higher contamination load independently decreases viability.

## Confounded association

Cold-room temperature is associated with viability because crop groups use different storage systems and have different baseline viability; temperature has no direct generating term.

## Null variable

tray_position_number is random.

## Leakage

viability_loss_pct is an exact transformation of viability_pct.

## Dirty-file defects

- Duplicate rows: 6
- Missing cells: contamination_load_pct=8, subculture_count=8, storage_method=8, lab_batch=8
- Inconsistent category cells: crop_group=11, storage_method=11
- Mixed-unit cells: storage_duration_months=6, cold_room_temperature_c=6
- Impossible values: viability_pct=[132.0], contamination_load_pct=[-8.0]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:cold_room_temperature_c`: -0.714
- `confounded:within:cold_room_temperature_c`: +0.062
- `leakage:viability_loss_pct`: -1.000
- `null:tray_position_number`: +0.055
- `real:contamination_load_pct`: -0.596
- `real:storage_duration_months`: -0.547

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Storage method and temperature are assigned by crop group rather than randomized; operational records cannot estimate their causal effects.
