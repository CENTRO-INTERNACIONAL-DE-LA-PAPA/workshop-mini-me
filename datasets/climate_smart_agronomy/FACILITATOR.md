# Facilitator key — Climate-smart agronomy and water management

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- Higher soil moisture increases simulated yield.
- Higher mulch coverage independently increases simulated yield.

## Confounded association

Irrigation events appear related to yield because both differ by site; irrigation count has no direct term in the yield equation.

## Null variable

weather_station_serial_digit is random.

## Leakage

gross_revenue_usd_ha is calculated after harvest from yield and price.

## Dirty-file defects

- Duplicate rows: 8
- Missing cells: soil_moisture_pct=11, mulch_coverage_pct=11, nitrogen_kg_ha=11, rainfall_mm=11
- Inconsistent category cells: management_system=14, crop=14
- Mixed-unit cells: rainfall_mm=8, nitrogen_kg_ha=8
- Impossible values: soil_moisture_pct=[128.0], rainfall_mm=[-12.0]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:irrigation_events`: +0.328
- `confounded:within:irrigation_events`: -0.028
- `leakage:gross_revenue_usd_ha`: +0.895
- `null:weather_station_serial_digit`: -0.014
- `real:mulch_coverage_pct`: +0.483
- `real:soil_moisture_pct`: +0.599

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Management and irrigation are not independently randomized across sites, so the dataset supports prediction and hypothesis generation, not causal treatment-effect claims.
