# Value-chain technology adoption and inclusion

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

Markets, adoption, livelihoods, gender and social inclusion

## Guiding question

Which service and market-access indicators predict adoption, and for whom does the model perform poorly?

## Observation unit

One synthetic, de-identified survey respondent.

## Design metadata

Cross-sectional clustered baseline survey across three synthetic country contexts.

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

1. Standardize survey categories and currencies without inventing missing respondent attributes.
2. Evaluate prediction errors across gender, country and education groups.
3. Exclude post_adoption_sales_usd and avoid describing observational associations as program impacts.

## Causal limitation

Cross-sectional self-reports, nonrandom extension contact and unmeasured wealth prevent causal attribution of adoption or income effects.

## Ethics and interpretation

All respondent records are synthetic. Real household data require consent, minimization, de-identification and an approved external-AI data policy.

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/value_chain_adoption/value_chain_adoption_dirty.csv
python scripts/score_cleanliness.py datasets/value_chain_adoption/value_chain_adoption_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
