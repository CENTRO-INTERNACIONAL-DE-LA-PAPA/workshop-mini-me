# Native potato biodiversity and in-situ persistence

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Agrobiodiversity, in-situ conservation and indigenous seed systems

## Guiding question

Which ecological and management factors are associated with continued observation of native-potato morphotypes?

## Observation unit

One morphotype reported in one de-identified community during the baseline survey.

## Design metadata

Twelve synthetic communities stratified by region and altitude, with unequal survey effort and a simulated next-season follow-up.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Harmonize categories without merging morphotypes solely because local names resemble one another.
2. Describe richness and persistence while accounting for unequal sampling effort.
3. Model next-season observation without the copied outcome and explain why absence is not proof of disappearance.

## Causal limitation

Observed presence depends on sampling effort and reported names do not establish genetic identity; the observational survey cannot establish causes of persistence or loss.

## Ethics and interpretation

Communities, names and observations are simulated. Real traditional knowledge requires consent, attribution, governance and protection against disclosure of sensitive locations.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/native_potato_biodiversity/native_potato_biodiversity_dirty.csv
python scripts/score_cleanliness.py datasets/native_potato_biodiversity/native_potato_biodiversity_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
