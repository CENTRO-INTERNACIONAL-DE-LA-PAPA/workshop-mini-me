# Seed-system lot quality

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Potato and sweetpotato seed systems, multiplication and quality control

## Guiding question

Which management and health indicators identify lots at risk of failing quality requirements?

## Observation unit

One synthetic seed lot at an inspection round.

## Design metadata

Operational records across four country-sites, two seasons and five multiplication cycles.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Standardize crop/producer categories and lot-weight units.
2. Identify lots requiring review without hiding missing health observations.
3. Predict lot quality without marketable_seed_fraction and discuss selection bias from inspected lots only.

## Causal limitation

Only inspected lots are represented and training is not randomly assigned, so observed differences cannot establish the impact of training.

## Ethics and interpretation

Producer identities, countries and lot outcomes are simulated and must not be used to evaluate real seed-system partners.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/seed_system_quality/seed_system_quality_dirty.csv
python scripts/score_cleanliness.py datasets/seed_system_quality/seed_system_quality_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
