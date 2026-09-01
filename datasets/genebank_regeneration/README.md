# Genebank conservation and regeneration

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Ex-situ conservation, quality control and regeneration operations

## Guiding question

Which accessions need priority regeneration and what operational factors accompany lower viability?

## Observation unit

One simulated accession assessment in a regeneration cycle and laboratory batch.

## Design metadata

Cross-sectional operational snapshot across crop groups, storage rooms, batches and regeneration cycles.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Standardize crop groups, storage methods and duration/temperature units.
2. Prioritize records for review without interpreting the ranking as biological value.
3. Model viability while excluding viability_loss_pct and controlling for crop group and batch.

## Causal limitation

Storage method and temperature are assigned by crop group rather than randomized; operational records cannot estimate their causal effects.

## Ethics and interpretation

All accession IDs and operational records are fictitious; no conclusion applies to material held by the CIP Genebank.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/genebank_regeneration/genebank_regeneration_dirty.csv
python scripts/score_cleanliness.py datasets/genebank_regeneration/genebank_regeneration_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
