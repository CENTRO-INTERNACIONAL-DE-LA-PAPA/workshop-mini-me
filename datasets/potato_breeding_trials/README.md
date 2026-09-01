# Potato breeding multi-environment trials

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Potato breeding and genotype-by-environment research

## Guiding question

Which synthetic genotypes combine yield, quality and stability across environments?

## Observation unit

One experimental plot for one genotype, site, season and block.

## Design metadata

Balanced 12-genotype x 4-site x 2-season x 3-block simulated trial.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Harmonize sites, seasons and units without deleting legitimate site differences.
2. Compare genotypes across environments and report uncertainty, not only global means.
3. Build a yield model that excludes harvest_value_usd_ha and respects site/season structure.

## Causal limitation

Irrigation differs systematically by site and is not independently randomized, so its marginal association with yield is not causal.

## Ethics and interpretation

All genotype identifiers and trial observations are fictitious and must not be presented as CIP performance results.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/potato_breeding_trials/potato_breeding_trials_dirty.csv
python scripts/score_cleanliness.py datasets/potato_breeding_trials/potato_breeding_trials_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
