# Facilitator key — Native potato biodiversity and in-situ persistence

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- More seed-exchange events increase the simulated probability of next-season observation.
- A larger number of reported uses independently increases persistence probability.

## Confounded association

Market distance appears positively related to persistence because high-altitude communities are both farther away and assigned a higher baseline persistence; distance has no direct generating term.

## Null variable

interviewer_badge_number is random.

## Leakage

next_season_observed_copy duplicates the outcome exactly.

## Dirty-file defects

- Duplicate rows: 7
- Missing cells: local_variety_name=10, skin_primary_color=10, years_reported_in_community=10, households_interviewed=10
- Inconsistent category cells: region=13, skin_primary_color=13, altitude_band=13
- Mixed-unit cells: altitude_m=7, market_distance_km=7
- Impossible values: households_interviewed=[-4], seed_exchange_events_year=[99]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:market_distance_km`: +0.226
- `confounded:within:market_distance_km`: +0.037
- `leakage:next_season_observed_copy`: +1.000
- `null:interviewer_badge_number`: +0.008
- `real:number_of_reported_uses`: +0.302
- `real:seed_exchange_events_year`: +0.247

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Observed presence depends on sampling effort and reported names do not establish genetic identity; the observational survey cannot establish causes of persistence or loss.
