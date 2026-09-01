# Sweetpotato nutrition and biofortification

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Sweetpotato breeding, nutrition and food quality

## Guiding question

Which synthetic materials combine provitamin-A potential, dry matter and sensory acceptance?

## Observation unit

One genotype-location-replicate sample measured in one laboratory batch.

## Design metadata

Twenty genotypes evaluated in three locations with three replicates and two laboratory batches.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Reconcile flesh-colour labels and nutritional units while preserving raw meaning.
2. Identify candidates that balance beta-carotene, dry matter and sensory acceptance.
3. Model beta-carotene without using beta_carotene_mg_100g and account for laboratory batch.

## Causal limitation

Laboratory batch and genotype allocation are not independently randomized, and compositional measurements do not establish human nutritional impact.

## Ethics and interpretation

The values are simulated and cannot support dietary, clinical or varietal-release recommendations.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/sweetpotato_nutrition/sweetpotato_nutrition_dirty.csv
python scripts/score_cleanliness.py datasets/sweetpotato_nutrition/sweetpotato_nutrition_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
