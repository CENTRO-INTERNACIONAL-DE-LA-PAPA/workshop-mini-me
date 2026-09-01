# Mini-Me CIP Research Workshop — synthetic data library

This package contains seven deterministic, entirely synthetic research datasets for a
three-day Mini-Me workshop. It spans potato and sweetpotato breeding, nutrition,
in-situ biodiversity, ex-situ genebank operations, seed systems, climate-smart
agronomy, and social/value-chain research.

Nothing in these files represents a real participant, community, accession, genotype,
site, partner or CIP result. The domains reflect CIP's public research portfolio:

- https://cipotato.org/research/
- https://cipotato.org/research/potato-agri-food-systems-program/
- https://cipotato.org/research/sweetpotato-agri-food-systems-program/
- https://cipotato.org/genebankcip/

## Dataset packages

| Folder | Research area | Clean rows |
|---|---|---:|
| `potato_breeding_trials` | Multi-environment potato breeding | 288 |
| `sweetpotato_nutrition` | Nutrition and biofortification | 180 |
| `native_potato_biodiversity` | Native-potato diversity and in-situ persistence | 288 |
| `genebank_regeneration` | Ex-situ conservation and regeneration | 240 |
| `seed_system_quality` | Planting-material quality and multiplication | 320 |
| `climate_smart_agronomy` | Water, management and climate resilience | 320 |
| `value_chain_adoption` | Adoption, markets, gender and inclusion | 450 |

Every folder contains:

- `*_dirty.csv` — participant starting point.
- `*_clean.csv` — facilitator benchmark; 100/100 in the scoring script.
- `*_dictionary.csv` — type, unit, analytical role, valid range and description.
- `README.md` — participant brief, tasks, limitations and ethics note.
- `FACILITATOR.md` — planted relationships and exact corruption families; withhold it
  until the exercise ends.

## Common scientific structure

Every dataset contains:

- Two real relationships created by the simulation.
- One association caused by a named confounder.
- One deliberately null variable.
- One leakage variable that must be excluded from the relevant prediction.
- Duplicates, missing values, inconsistent categories and mixed units in `dirty.csv`.
- Design metadata such as site, block, replicate, season, batch, cluster or time.
- A documented limitation that prevents causal interpretation.

`clean.csv` retains the confounder, null and leakage columns. They are valid recorded
data, even though some are invalid predictors. Data cleanliness and analytical validity
are intentionally taught as separate questions.

## Score a cleaned file

The scorer uses only the Python standard library and ignores row order:

```powershell
python scripts/score_cleanliness.py datasets/potato_breeding_trials/potato_breeding_trials_dirty.csv
python scripts/score_cleanliness.py datasets/potato_breeding_trials/potato_breeding_trials_clean.csv
```

Score every supplied file:

```powershell
python scripts/score_cleanliness.py --all datasets
```

The score is weighted as follows:

- Schema agreement: 15%.
- Record integrity, including missing/extra IDs and duplicates: 20%.
- Cell agreement with the clean benchmark: 65%.

A score of 100 means exact benchmark cleanliness after numeric parsing. It does not
mean an analysis is unbiased, causal or scientifically correct.

## Reproduce the library

```powershell
python scripts/generate_datasets.py --output-dir .
```

The default seed is fixed. Re-running the command reproduces the same scientific
relationships and dirty-file defects.

## Bring Your Own Data alternative

Participants may replace the supplied data on Day 3 only after completing a Data
Passport covering ownership, confidentiality, observation unit, design, outcome,
missing-value codes, allowed tools and causal limitations. Synthetic data remain the
fallback so no team is blocked or pressured to upload sensitive research data.
