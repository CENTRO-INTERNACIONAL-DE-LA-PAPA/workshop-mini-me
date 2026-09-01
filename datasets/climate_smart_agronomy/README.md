# Climate-smart agronomy and water management

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Sustainable intensification, climate resilience and crop management

## Guiding question

Which soil-water and management indicators accompany resilient yield across contrasting environments?

## Observation unit

One plot in one site, season and block.

## Design metadata

Two-season multi-site observational demonstration with nested blocks and plots.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Standardize rainfall and fertilizer units and preserve the site/block design.
2. Compare yield resilience rather than only pooled average yield.
3. Build a yield model without gross revenue and explain why irrigation is confounded by site.

## Causal limitation

Management and irrigation are not independently randomized across sites, so the dataset supports prediction and hypothesis generation, not causal treatment-effect claims.

## Ethics and interpretation

All sites and measurements are synthetic; the dataset cannot justify recommendations to farmers.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/climate_smart_agronomy/climate_smart_agronomy_dirty.csv
python scripts/score_cleanliness.py datasets/climate_smart_agronomy/climate_smart_agronomy_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
