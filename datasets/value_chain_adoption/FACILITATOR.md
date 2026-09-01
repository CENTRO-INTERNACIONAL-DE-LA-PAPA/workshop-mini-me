# Facilitator key — Value-chain technology adoption and inclusion

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

- More extension contacts increase the simulated probability of adoption.
- Higher market-access score independently increases adoption probability.

## Confounded association

Smartphone ownership appears associated with adoption because education increases both; smartphone ownership has no direct term in the adoption equation.

## Null variable

questionnaire_version_digit is random.

## Leakage

post_adoption_sales_usd is observed after adoption and is zero for non-adopters.

## Dirty-file defects

- Duplicate rows: 11
- Missing cells: respondent_gender=16, education_band=16, annual_farm_income_usd=16, market_access_score=16
- Inconsistent category cells: respondent_gender=20, country=20, education_band=20
- Mixed-unit cells: annual_farm_income_usd=11, respondent_age_years=11
- Impossible values: respondent_age_years=[7], market_access_score=[145.0]

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

- `confounded:marginal:smartphone_owned`: +0.188
- `confounded:within:smartphone_owned`: -0.054
- `leakage:post_adoption_sales_usd`: +0.762
- `null:questionnaire_version_digit`: +0.033
- `real:extension_contacts_year`: +0.316
- `real:market_access_score`: +0.280

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

Cross-sectional self-reports, nonrandom extension contact and unmeasured wealth prevent causal attribution of adoption or income effects.
