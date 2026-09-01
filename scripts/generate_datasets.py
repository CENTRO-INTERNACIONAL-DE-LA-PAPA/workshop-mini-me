#!/usr/bin/env python3
"""Generate deterministic synthetic datasets for the CIP Mini-Me workshop.

The clean files are internally consistent reference datasets.  They still contain
confounders, null variables and leakage on purpose: those are scientific/modelling
properties, not data-cleaning errors.  Dirty files are derived from the clean rows
with reproducible missingness, duplicate records, inconsistent categories, mixed
units and a few impossible values.

No row represents a real person, accession, community, trial or CIP result.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
DATASETS_ROOT = ROOT / "datasets"
BASE_SEED = 20260831


@dataclass(frozen=True)
class Column:
    name: str
    data_type: str
    unit: str
    role: str
    valid_values: str
    description: str
    cleaning_notes: str = ""


@dataclass(frozen=True)
class Validation:
    outcome: str
    real_relationships: tuple[tuple[str, int, float], ...]
    confounded_exposure: str
    confounder: str
    null_variable: str
    leakage: str
    max_null_correlation: float = 0.16
    max_within_confounder_correlation: float = 0.16


@dataclass(frozen=True)
class DirtyPlan:
    missing_columns: tuple[str, ...]
    category_variants: dict[str, dict[str, tuple[str, ...]]]
    unit_converters: dict[str, Callable[[float], str]]
    impossible_values: dict[str, tuple[Any, ...]]
    missing_rate: float = 0.035
    category_rate: float = 0.045
    unit_rate: float = 0.025
    duplicate_rate: float = 0.025


@dataclass
class DatasetSpec:
    slug: str
    title: str
    area: str
    question: str
    observation_unit: str
    design: str
    limitation: str
    columns: list[Column]
    rows: list[dict[str, Any]]
    validation: Validation
    dirty_plan: DirtyPlan
    real_relationships_text: tuple[str, str]
    confounded_text: str
    null_text: str
    leakage_text: str
    participant_tasks: tuple[str, ...]
    ethics_note: str
    corruption_summary: dict[str, Any] = field(default_factory=dict)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def logistic(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def rounded(value: float, digits: int = 2) -> float:
    return round(value, digits)


def column(
    name: str,
    data_type: str,
    unit: str,
    role: str,
    valid_values: str,
    description: str,
    cleaning_notes: str = "",
) -> Column:
    return Column(name, data_type, unit, role, valid_values, description, cleaning_notes)


def potato_breeding(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    sites = {
        "La Molina": dict(altitude=240, rain=78, temp=20.5, irrigation=410, yield_base=31),
        "Huancayo": dict(altitude=3250, rain=510, temp=11.8, irrigation=155, yield_base=23),
        "Cajamarca": dict(altitude=2750, rain=690, temp=14.7, irrigation=210, yield_base=27),
        "Canete": dict(altitude=80, rain=35, temp=22.4, irrigation=455, yield_base=35),
    }
    genotypes = [f"CIP-SYN-{i:03d}" for i in range(1, 13)]
    genotype_yield = {g: rng.uniform(-3.0, 4.0) for g in genotypes}
    resistance = {g: rng.uniform(5, 35) for g in genotypes}
    vigor = {g: rng.uniform(-8, 10) for g in genotypes}
    rows: list[dict[str, Any]] = []
    record = 1
    for season_index, season in enumerate(("2024-A", "2025-A")):
        for site, meta in sites.items():
            for genotype in genotypes:
                for block in range(1, 4):
                    rainfall = meta["rain"] + season_index * 38 + rng.gauss(0, 28)
                    temperature = meta["temp"] + season_index * 0.6 + rng.gauss(0, 0.8)
                    canopy = clamp(64 + vigor[genotype] + rng.gauss(0, 6), 32, 96)
                    blight = clamp(
                        27 + rainfall / 35 - resistance[genotype] + rng.gauss(0, 7), 0, 92
                    )
                    irrigation = meta["irrigation"] + rng.gauss(0, 24)
                    yield_t_ha = clamp(
                        meta["yield_base"]
                        + genotype_yield[genotype]
                        + 0.27 * (canopy - 62)
                        - 0.14 * blight
                        + rng.gauss(0, 2.1),
                        4,
                        52,
                    )
                    price = rng.uniform(255, 315)
                    rows.append(
                        {
                            "record_id": f"PBT-{record:04d}",
                            "site": site,
                            "season": season,
                            "block": block,
                            "replicate": block,
                            "genotype": genotype,
                            "altitude_m": rounded(meta["altitude"] + rng.gauss(0, 12), 1),
                            "rainfall_mm": rounded(rainfall, 1),
                            "mean_temperature_c": rounded(temperature, 1),
                            "irrigation_mm": rounded(irrigation, 1),
                            "canopy_cover_pct": rounded(canopy, 1),
                            "late_blight_severity_pct": rounded(blight, 1),
                            "soil_ph": rounded(clamp(rng.gauss(5.8, 0.45), 4.5, 7.2), 2),
                            "yield_t_ha": rounded(yield_t_ha, 2),
                            "dry_matter_pct": rounded(clamp(19 + genotype_yield[genotype] / 2 + rng.gauss(0, 1.4), 13, 27), 1),
                            "plot_marker_number": rng.randint(1000, 9999),
                            "harvest_value_usd_ha": rounded(yield_t_ha * price, 2),
                        }
                    )
                    record += 1

    cols = [
        column("record_id", "string", "none", "primary_key", "unique PBT-####", "Synthetic plot observation identifier."),
        column("site", "category", "none", "design", "La Molina|Huancayo|Cajamarca|Canete", "Trial location."),
        column("season", "category", "none", "design", "2024-A|2025-A", "Cropping season."),
        column("block", "integer", "none", "design", "1-3", "Randomized block number."),
        column("replicate", "integer", "none", "design", "1-3", "Replicate, equal to block in this teaching design."),
        column("genotype", "category", "none", "design", "CIP-SYN-001..012", "Fictitious breeding-line identifier."),
        column("altitude_m", "number", "m", "context", "0-4500", "Site altitude."),
        column("rainfall_mm", "number", "mm/season", "context", "0-1500", "Accumulated seasonal rainfall."),
        column("mean_temperature_c", "number", "deg C", "context", "0-35", "Mean growing-season temperature."),
        column("irrigation_mm", "number", "mm/season", "confounded_exposure", "0-800", "Applied irrigation; confounded by site."),
        column("canopy_cover_pct", "number", "%", "predictor", "0-100", "Peak canopy cover; planted positive relationship with yield."),
        column("late_blight_severity_pct", "number", "%", "predictor", "0-100", "Synthetic disease severity; planted negative relationship with yield."),
        column("soil_ph", "number", "pH", "context", "3.0-9.0", "Topsoil pH."),
        column("yield_t_ha", "number", "t/ha", "outcome", "0-80", "Harvested tuber yield."),
        column("dry_matter_pct", "number", "%", "outcome_secondary", "0-40", "Tuber dry matter."),
        column("plot_marker_number", "integer", "none", "null", "1000-9999", "Random marker deliberately unrelated to yield."),
        column("harvest_value_usd_ha", "number", "USD/ha", "leakage", ">=0", "Post-harvest value computed from yield and price; do not use to predict yield."),
    ]
    return DatasetSpec(
        slug="potato_breeding_trials",
        title="Potato breeding multi-environment trials",
        area="Potato breeding and genotype-by-environment research",
        question="Which synthetic genotypes combine yield, quality and stability across environments?",
        observation_unit="One experimental plot for one genotype, site, season and block.",
        design="Balanced 12-genotype x 4-site x 2-season x 3-block simulated trial.",
        limitation="Irrigation differs systematically by site and is not independently randomized, so its marginal association with yield is not causal.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="yield_t_ha",
            real_relationships=(("canopy_cover_pct", 1, 0.24), ("late_blight_severity_pct", -1, 0.22)),
            confounded_exposure="irrigation_mm",
            confounder="site",
            null_variable="plot_marker_number",
            leakage="harvest_value_usd_ha",
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("canopy_cover_pct", "late_blight_severity_pct", "soil_ph", "dry_matter_pct"),
            category_variants={
                "site": {"La Molina": ("la molina", "LA MOLINA "), "Canete": ("Cañete", "canete")},
                "season": {"2024-A": ("2024A", "2024-a"), "2025-A": ("2025 A",)},
            },
            unit_converters={
                "yield_t_ha": lambda value: f"{value * 1000:.0f} kg/ha",
                "altitude_m": lambda value: f"{value * 3.28084:.0f} ft",
            },
            impossible_values={"soil_ph": (14.7,), "late_blight_severity_pct": (135.0,)},
        ),
        real_relationships_text=(
            "Higher canopy cover increases simulated yield, conditional on the rest of the generating process.",
            "Higher late-blight severity decreases simulated yield.",
        ),
        confounded_text="Irrigation appears positively associated with yield because high-yield lowland sites also receive more irrigation; irrigation has no direct term in the yield equation.",
        null_text="plot_marker_number is random and unrelated to all biological outcomes.",
        leakage_text="harvest_value_usd_ha is calculated after harvest from yield and price.",
        participant_tasks=(
            "Harmonize sites, seasons and units without deleting legitimate site differences.",
            "Compare genotypes across environments and report uncertainty, not only global means.",
            "Build a yield model that excludes harvest_value_usd_ha and respects site/season structure.",
        ),
        ethics_note="All genotype identifiers and trial observations are fictitious and must not be presented as CIP performance results.",
    )


def sweetpotato_nutrition(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    locations = ("Maputo", "Kampala", "Lima")
    genotypes = [f"SP-SYN-{i:03d}" for i in range(1, 21)]
    orange_index = {g: rng.uniform(5, 95) for g in genotypes}
    pathway = {g: rng.uniform(10, 90) for g in genotypes}
    rows: list[dict[str, Any]] = []
    record = 1
    for g_index, genotype in enumerate(genotypes):
        flesh = "orange" if orange_index[genotype] >= 60 else "cream" if orange_index[genotype] >= 30 else "purple"
        batch = "LAB-A" if g_index % 2 == 0 else "LAB-B"
        batch_effect = 18 if batch == "LAB-A" else -8
        for location in locations:
            for replicate in range(1, 4):
                storage_days = (42 if batch == "LAB-A" else 12) + rng.gauss(0, 3)
                beta = clamp(
                    8
                    + 0.82 * orange_index[genotype]
                    + 0.32 * pathway[genotype]
                    + batch_effect
                    + rng.gauss(0, 6),
                    1,
                    145,
                )
                dry_matter = clamp(18 + (100 - orange_index[genotype]) * 0.06 + rng.gauss(0, 1.8), 15, 35)
                rows.append(
                    {
                        "record_id": f"SPN-{record:04d}",
                        "location": location,
                        "season": "2025-B",
                        "block": replicate,
                        "replicate": replicate,
                        "lab_batch": batch,
                        "genotype": genotype,
                        "flesh_color": flesh,
                        "orange_color_index": rounded(orange_index[genotype] + rng.gauss(0, 2), 1),
                        "carotenoid_pathway_score": rounded(pathway[genotype] + rng.gauss(0, 3), 1),
                        "storage_days": rounded(storage_days, 1),
                        "beta_carotene_ug_g": rounded(beta, 2),
                        "iron_mg_kg": rounded(clamp(rng.gauss(22, 4.5), 8, 40), 2),
                        "dry_matter_pct": rounded(dry_matter, 1),
                        "sensory_acceptance_score": rounded(clamp(4.5 + dry_matter * 0.12 + rng.gauss(0, 0.8), 1, 9), 1),
                        "rack_slot_number": rng.randint(100, 999),
                        "beta_carotene_mg_100g": rounded(beta / 10, 3),
                    }
                )
                record += 1
    cols = [
        column("record_id", "string", "none", "primary_key", "unique SPN-####", "Synthetic sample identifier."),
        column("location", "category", "none", "design", "Maputo|Kampala|Lima", "Evaluation location."),
        column("season", "category", "none", "design", "2025-B", "Evaluation season."),
        column("block", "integer", "none", "design", "1-3", "Field block."),
        column("replicate", "integer", "none", "design", "1-3", "Biological replicate."),
        column("lab_batch", "category", "none", "confounder", "LAB-A|LAB-B", "Laboratory batch that confounds storage duration and beta-carotene."),
        column("genotype", "category", "none", "design", "SP-SYN-001..020", "Fictitious sweetpotato genotype."),
        column("flesh_color", "category", "none", "context", "orange|cream|purple", "Simplified flesh-colour class."),
        column("orange_color_index", "number", "index 0-100", "predictor", "0-100", "Instrument-derived orange intensity; planted positive relationship."),
        column("carotenoid_pathway_score", "number", "index 0-100", "predictor", "0-100", "Synthetic pathway score; planted positive relationship."),
        column("storage_days", "number", "days", "confounded_exposure", "0-90", "Days before laboratory measurement; confounded by lab batch."),
        column("beta_carotene_ug_g", "number", "ug/g fresh weight", "outcome", "0-200", "Synthetic beta-carotene concentration."),
        column("iron_mg_kg", "number", "mg/kg", "outcome_secondary", "0-100", "Synthetic iron concentration."),
        column("dry_matter_pct", "number", "%", "outcome_secondary", "0-50", "Root dry matter."),
        column("sensory_acceptance_score", "number", "1-9", "outcome_secondary", "1-9", "Synthetic panel acceptance score."),
        column("rack_slot_number", "integer", "none", "null", "100-999", "Random rack position unrelated to nutrition."),
        column("beta_carotene_mg_100g", "number", "mg/100g fresh weight", "leakage", ">=0", "The target beta-carotene expressed in another unit; exclude when predicting beta_carotene_ug_g."),
    ]
    return DatasetSpec(
        slug="sweetpotato_nutrition",
        title="Sweetpotato nutrition and biofortification",
        area="Sweetpotato breeding, nutrition and food quality",
        question="Which synthetic materials combine provitamin-A potential, dry matter and sensory acceptance?",
        observation_unit="One genotype-location-replicate sample measured in one laboratory batch.",
        design="Twenty genotypes evaluated in three locations with three replicates and two laboratory batches.",
        limitation="Laboratory batch and genotype allocation are not independently randomized, and compositional measurements do not establish human nutritional impact.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="beta_carotene_ug_g",
            real_relationships=(("orange_color_index", 1, 0.55), ("carotenoid_pathway_score", 1, 0.18)),
            confounded_exposure="storage_days",
            confounder="lab_batch",
            null_variable="rack_slot_number",
            leakage="beta_carotene_mg_100g",
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("orange_color_index", "iron_mg_kg", "dry_matter_pct", "sensory_acceptance_score"),
            category_variants={
                "flesh_color": {"orange": ("Orange", "OFSP", " orange "), "cream": ("Cream", "crema")},
                "location": {"Maputo": ("maputo", "MAPUTO "), "Kampala": ("kampala",)},
            },
            unit_converters={
                "beta_carotene_ug_g": lambda value: f"{value / 10:.3f} mg/100g",
                "iron_mg_kg": lambda value: f"{value / 1000:.5f} g/kg",
            },
            impossible_values={"sensory_acceptance_score": (12.0,), "dry_matter_pct": (118.0,)},
        ),
        real_relationships_text=(
            "orange_color_index has a strong positive term in the beta-carotene generating equation.",
            "carotenoid_pathway_score independently increases beta-carotene.",
        ),
        confounded_text="storage_days appears related to beta-carotene because both differ by lab_batch; storage has no direct term in the generating equation.",
        null_text="rack_slot_number is assigned randomly.",
        leakage_text="beta_carotene_mg_100g is the outcome expressed in another unit.",
        participant_tasks=(
            "Reconcile flesh-colour labels and nutritional units while preserving raw meaning.",
            "Identify candidates that balance beta-carotene, dry matter and sensory acceptance.",
            "Model beta-carotene without using beta_carotene_mg_100g and account for laboratory batch.",
        ),
        ethics_note="The values are simulated and cannot support dietary, clinical or varietal-release recommendations.",
    )


def native_potato_biodiversity(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    communities = []
    for index in range(12):
        band = ("low", "mid", "high")[index % 3]
        altitude = {"low": 2450, "mid": 3250, "high": 3850}[band] + rng.gauss(0, 90)
        distance = {"low": 18, "mid": 43, "high": 78}[band] + rng.gauss(0, 7)
        communities.append((f"COM-{index + 1:02d}", ("Cusco", "Puno", "Ayacucho")[index % 3], band, altitude, distance))
    morphotypes = [f"MOR-SYN-{i:03d}" for i in range(1, 61)]
    names = ["Puka", "Yana", "Qeqorani", "Ccompis", "Peruanita", "Azul", "Muru", "Amarilla", "Sani", "Wenccos"]
    skin_colors = ("red", "purple", "yellow", "cream", "multicolour")
    uses = ("boiling", "chuño", "soup", "market", "ceremonial")
    rows: list[dict[str, Any]] = []
    record = 1
    for community_code, region, altitude_band, altitude, market_distance in communities:
        selected = rng.sample(morphotypes, 24)
        altitude_effect = {"low": -0.8, "mid": 0.0, "high": 0.9}[altitude_band]
        for morphotype in selected:
            exchange_events = rng.randint(0, 8)
            number_of_uses = rng.randint(1, 5)
            logit = -2.0 + 0.34 * exchange_events + 0.48 * number_of_uses + altitude_effect + rng.gauss(0, 0.35)
            probability = logistic(logit)
            observed_next = int(rng.random() < probability)
            morph_index = int(morphotype.rsplit("-", 1)[1])
            local_name = names[(morph_index + int(community_code[-2:])) % len(names)]
            rows.append(
                {
                    "record_id": f"NPB-{record:04d}",
                    "community_code": community_code,
                    "region": region,
                    "survey_round": "2025-baseline",
                    "sampling_visit": rng.randint(1, 4),
                    "households_interviewed": rng.randint(12, 38),
                    "altitude_band": altitude_band,
                    "altitude_m": rounded(altitude + rng.gauss(0, 35), 1),
                    "market_distance_km": rounded(market_distance + rng.gauss(0, 4), 1),
                    "morphotype_id": morphotype,
                    "local_variety_name": local_name,
                    "skin_primary_color": skin_colors[morph_index % len(skin_colors)],
                    "main_use": uses[morph_index % len(uses)],
                    "seed_exchange_events_year": exchange_events,
                    "number_of_reported_uses": number_of_uses,
                    "years_reported_in_community": rng.randint(3, 70),
                    "observed_next_season": observed_next,
                    "interviewer_badge_number": rng.randint(1000, 9999),
                    "next_season_observed_copy": observed_next,
                }
            )
            record += 1
    cols = [
        column("record_id", "string", "none", "primary_key", "unique NPB-####", "Synthetic community-morphotype observation."),
        column("community_code", "category", "none", "design", "COM-01..COM-12", "De-identified fictitious community code."),
        column("region", "category", "none", "design", "Cusco|Puno|Ayacucho", "Broad synthetic region."),
        column("survey_round", "category", "none", "design", "2025-baseline", "Survey campaign."),
        column("sampling_visit", "integer", "none", "design", "1-4", "Visit number within the campaign."),
        column("households_interviewed", "integer", "households", "sampling", "1-100", "Sampling effort, not community population."),
        column("altitude_band", "category", "none", "confounder", "low|mid|high", "Altitude stratum confounding market distance and persistence."),
        column("altitude_m", "number", "m", "context", "1500-5000", "Generalized altitude; no precise coordinates are supplied."),
        column("market_distance_km", "number", "km", "confounded_exposure", "0-250", "Road distance to a reference market."),
        column("morphotype_id", "category", "none", "design", "MOR-SYN-001..060", "Fictitious morphotype identifier; not a genetic identity claim."),
        column("local_variety_name", "string", "none", "context", "local names", "Synthetic local name; synonyms and homonyms may be legitimate."),
        column("skin_primary_color", "category", "none", "context", "red|purple|yellow|cream|multicolour", "Simplified skin-colour descriptor."),
        column("main_use", "category", "none", "context", "boiling|chuño|soup|market|ceremonial", "Primary reported use."),
        column("seed_exchange_events_year", "integer", "events/year", "predictor", "0-20", "Reported seed-exchange frequency; planted positive relationship with persistence."),
        column("number_of_reported_uses", "integer", "count", "predictor", "1-10", "Number of distinct reported uses; planted positive relationship with persistence."),
        column("years_reported_in_community", "integer", "years", "context", "0-150", "Reported duration, not independently verified."),
        column("observed_next_season", "integer", "0/1", "outcome", "0|1", "Whether the morphotype was observed in the simulated follow-up."),
        column("interviewer_badge_number", "integer", "none", "null", "1000-9999", "Random interviewer badge, unrelated to persistence."),
        column("next_season_observed_copy", "integer", "0/1", "leakage", "0|1", "Direct copy of the future outcome; intentionally unsafe for prediction."),
    ]
    return DatasetSpec(
        slug="native_potato_biodiversity",
        title="Native potato biodiversity and in-situ persistence",
        area="Agrobiodiversity, in-situ conservation and indigenous seed systems",
        question="Which ecological and management factors are associated with continued observation of native-potato morphotypes?",
        observation_unit="One morphotype reported in one de-identified community during the baseline survey.",
        design="Twelve synthetic communities stratified by region and altitude, with unequal survey effort and a simulated next-season follow-up.",
        limitation="Observed presence depends on sampling effort and reported names do not establish genetic identity; the observational survey cannot establish causes of persistence or loss.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="observed_next_season",
            real_relationships=(("seed_exchange_events_year", 1, 0.22), ("number_of_reported_uses", 1, 0.20)),
            confounded_exposure="market_distance_km",
            confounder="altitude_band",
            null_variable="interviewer_badge_number",
            leakage="next_season_observed_copy",
            max_within_confounder_correlation=0.18,
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("local_variety_name", "skin_primary_color", "years_reported_in_community", "households_interviewed"),
            category_variants={
                "region": {"Cusco": ("CUSCO", "Cuzco"), "Ayacucho": ("ayacucho", "Ayacucho ")},
                "skin_primary_color": {"purple": ("Purple", "morado", "púrpura"), "multicolour": ("multi-color", "Multicolor")},
                "altitude_band": {"high": ("High", "alta"), "mid": ("medium", "media")},
            },
            unit_converters={
                "altitude_m": lambda value: f"{value * 3.28084:.0f} ft",
                "market_distance_km": lambda value: f"{value * 0.621371:.1f} miles",
            },
            impossible_values={"households_interviewed": (-4,), "seed_exchange_events_year": (99,)},
        ),
        real_relationships_text=(
            "More seed-exchange events increase the simulated probability of next-season observation.",
            "A larger number of reported uses independently increases persistence probability.",
        ),
        confounded_text="Market distance appears positively related to persistence because high-altitude communities are both farther away and assigned a higher baseline persistence; distance has no direct generating term.",
        null_text="interviewer_badge_number is random.",
        leakage_text="next_season_observed_copy duplicates the outcome exactly.",
        participant_tasks=(
            "Harmonize categories without merging morphotypes solely because local names resemble one another.",
            "Describe richness and persistence while accounting for unequal sampling effort.",
            "Model next-season observation without the copied outcome and explain why absence is not proof of disappearance.",
        ),
        ethics_note="Communities, names and observations are simulated. Real traditional knowledge requires consent, attribution, governance and protection against disclosure of sensitive locations.",
    )


def genebank_regeneration(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    crops = {
        "potato": dict(temp=-20.0, viability=6.0, storage="cryogenic"),
        "sweetpotato": dict(temp=4.0, viability=-2.0, storage="in-vitro"),
        "andean-root": dict(temp=8.0, viability=-5.0, storage="in-vitro"),
    }
    rows: list[dict[str, Any]] = []
    for index in range(1, 241):
        crop = tuple(crops)[index % 3]
        meta = crops[crop]
        duration = rng.uniform(12, 132)
        contamination = clamp(rng.gauss(4.5 if crop == "potato" else 7.5, 3), 0, 22)
        temperature = meta["temp"] + rng.gauss(0, 0.7)
        viability = clamp(98 - 0.13 * duration - 0.95 * contamination + meta["viability"] + rng.gauss(0, 3), 20, 100)
        rows.append(
            {
                "record_id": f"GBR-{index:04d}",
                "accession_id": f"ACC-SYN-{index:05d}",
                "crop_group": crop,
                "storage_method": meta["storage"],
                "storage_room": f"ROOM-{(index % 6) + 1}",
                "lab_batch": f"BATCH-{2024 + index % 2}-{(index % 8) + 1:02d}",
                "regeneration_cycle": (index % 4) + 1,
                "evaluation_year": 2025 + index % 2,
                "storage_duration_months": rounded(duration, 1),
                "contamination_load_pct": rounded(contamination, 2),
                "cold_room_temperature_c": rounded(temperature, 2),
                "subculture_count": rng.randint(1, 12),
                "viability_pct": rounded(viability, 2),
                "tray_position_number": rng.randint(100, 999),
                "viability_loss_pct": rounded(100 - viability, 2),
            }
        )
    cols = [
        column("record_id", "string", "none", "primary_key", "unique GBR-####", "Synthetic conservation assessment."),
        column("accession_id", "string", "none", "design", "ACC-SYN-#####", "Fictitious accession identifier."),
        column("crop_group", "category", "none", "confounder", "potato|sweetpotato|andean-root", "Broad crop group confounding room temperature and viability."),
        column("storage_method", "category", "none", "design", "cryogenic|in-vitro", "Synthetic storage method."),
        column("storage_room", "category", "none", "design", "ROOM-1..ROOM-6", "Storage room identifier."),
        column("lab_batch", "category", "none", "design", "BATCH-year-number", "Laboratory processing batch."),
        column("regeneration_cycle", "integer", "cycle", "design", "1-4", "Regeneration cycle number."),
        column("evaluation_year", "integer", "year", "design", "2025-2026", "Assessment year."),
        column("storage_duration_months", "number", "months", "predictor", "0-240", "Storage duration; planted negative relationship with viability."),
        column("contamination_load_pct", "number", "%", "predictor", "0-100", "Observed contamination; planted negative relationship with viability."),
        column("cold_room_temperature_c", "number", "deg C", "confounded_exposure", "-196 to 30", "Room temperature, confounded by crop group and storage method."),
        column("subculture_count", "integer", "count", "context", "0-30", "Number of subculture events."),
        column("viability_pct", "number", "%", "outcome", "0-100", "Synthetic viability estimate."),
        column("tray_position_number", "integer", "none", "null", "100-999", "Random tray position unrelated to viability."),
        column("viability_loss_pct", "number", "%", "leakage", "0-100", "100 minus viability; exclude when predicting viability."),
    ]
    return DatasetSpec(
        slug="genebank_regeneration",
        title="Genebank conservation and regeneration",
        area="Ex-situ conservation, quality control and regeneration operations",
        question="Which accessions need priority regeneration and what operational factors accompany lower viability?",
        observation_unit="One simulated accession assessment in a regeneration cycle and laboratory batch.",
        design="Cross-sectional operational snapshot across crop groups, storage rooms, batches and regeneration cycles.",
        limitation="Storage method and temperature are assigned by crop group rather than randomized; operational records cannot estimate their causal effects.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="viability_pct",
            real_relationships=(("storage_duration_months", -1, 0.48), ("contamination_load_pct", -1, 0.20)),
            confounded_exposure="cold_room_temperature_c",
            confounder="crop_group",
            null_variable="tray_position_number",
            leakage="viability_loss_pct",
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("contamination_load_pct", "subculture_count", "storage_method", "lab_batch"),
            category_variants={
                "crop_group": {"sweetpotato": ("sweet potato", "Sweetpotato"), "andean-root": ("Andean Root", "ARTC")},
                "storage_method": {"in-vitro": ("in vitro", "IN-VITRO"), "cryogenic": ("cryo", "Cryogenic")},
            },
            unit_converters={
                "storage_duration_months": lambda value: f"{value / 12:.2f} years",
                "cold_room_temperature_c": lambda value: f"{value * 9 / 5 + 32:.1f} F",
            },
            impossible_values={"viability_pct": (132.0,), "contamination_load_pct": (-8.0,)},
        ),
        real_relationships_text=(
            "Longer storage duration decreases simulated viability.",
            "Higher contamination load independently decreases viability.",
        ),
        confounded_text="Cold-room temperature is associated with viability because crop groups use different storage systems and have different baseline viability; temperature has no direct generating term.",
        null_text="tray_position_number is random.",
        leakage_text="viability_loss_pct is an exact transformation of viability_pct.",
        participant_tasks=(
            "Standardize crop groups, storage methods and duration/temperature units.",
            "Prioritize records for review without interpreting the ranking as biological value.",
            "Model viability while excluding viability_loss_pct and controlling for crop group and batch.",
        ),
        ethics_note="All accession IDs and operational records are fictitious; no conclusion applies to material held by the CIP Genebank.",
    )


def seed_system_quality(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    sites = {
        "Peru-Cusco": dict(fee=18, quality=-6),
        "Kenya-Nakuru": dict(fee=34, quality=3),
        "Uganda-Kabale": dict(fee=27, quality=-1),
        "India-Karnataka": dict(fee=42, quality=9),
    }
    rows: list[dict[str, Any]] = []
    for index in range(1, 321):
        site = tuple(sites)[index % len(sites)]
        meta = sites[site]
        crop = "potato" if index % 3 else "sweetpotato"
        virus = clamp(rng.gauss(8.5, 5), 0, 35)
        training = rng.randint(0, 7)
        fee = meta["fee"] + rng.gauss(0, 3)
        marketable = clamp(88 - 1.35 * virus + 1.45 * training + meta["quality"] + rng.gauss(0, 4), 20, 100)
        lot_weight = clamp(rng.gauss(620 if crop == "potato" else 410, 140), 60, 1200)
        rows.append(
            {
                "record_id": f"SSQ-{index:04d}",
                "lot_id": f"LOT-SYN-{index:05d}",
                "country_site": site,
                "crop": crop,
                "season": ("2025-A", "2025-B")[index % 2],
                "producer_scale": ("small", "medium", "commercial")[index % 3],
                "inspection_round": (index % 3) + 1,
                "multiplication_cycle": (index % 5) + 1,
                "virus_incidence_pct": rounded(virus, 2),
                "training_visits": training,
                "inspection_fee_usd": rounded(fee, 2),
                "lot_weight_kg": rounded(lot_weight, 1),
                "marketable_seed_pct": rounded(marketable, 2),
                "rejection_pct": rounded(100 - marketable, 2),
                "bag_label_number": rng.randint(1000, 9999),
                "marketable_seed_fraction": rounded(marketable / 100, 4),
            }
        )
    cols = [
        column("record_id", "string", "none", "primary_key", "unique SSQ-####", "Synthetic inspected-lot record."),
        column("lot_id", "string", "none", "design", "LOT-SYN-#####", "Fictitious seed-lot identifier."),
        column("country_site", "category", "none", "confounder", "Peru-Cusco|Kenya-Nakuru|Uganda-Kabale|India-Karnataka", "Synthetic production/inspection site."),
        column("crop", "category", "none", "design", "potato|sweetpotato", "Crop represented by the planting material."),
        column("season", "category", "none", "design", "2025-A|2025-B", "Production season."),
        column("producer_scale", "category", "none", "design", "small|medium|commercial", "Simplified producer scale."),
        column("inspection_round", "integer", "round", "design", "1-3", "Quality-inspection round."),
        column("multiplication_cycle", "integer", "cycle", "design", "1-5", "Vegetative multiplication cycle."),
        column("virus_incidence_pct", "number", "%", "predictor", "0-100", "Synthetic virus incidence; planted negative relationship with marketable seed."),
        column("training_visits", "integer", "visits", "predictor", "0-20", "Technical-support visits; planted positive relationship."),
        column("inspection_fee_usd", "number", "USD", "confounded_exposure", ">=0", "Inspection fee, confounded by country_site."),
        column("lot_weight_kg", "number", "kg", "context", ">=0", "Lot weight."),
        column("marketable_seed_pct", "number", "%", "outcome", "0-100", "Share meeting the synthetic quality criteria."),
        column("rejection_pct", "number", "%", "outcome_secondary", "0-100", "Complement of marketable seed."),
        column("bag_label_number", "integer", "none", "null", "1000-9999", "Random label number unrelated to quality."),
        column("marketable_seed_fraction", "number", "fraction", "leakage", "0-1", "The target expressed as a fraction; exclude when predicting marketable_seed_pct."),
    ]
    return DatasetSpec(
        slug="seed_system_quality",
        title="Seed-system lot quality",
        area="Potato and sweetpotato seed systems, multiplication and quality control",
        question="Which management and health indicators identify lots at risk of failing quality requirements?",
        observation_unit="One synthetic seed lot at an inspection round.",
        design="Operational records across four country-sites, two seasons and five multiplication cycles.",
        limitation="Only inspected lots are represented and training is not randomly assigned, so observed differences cannot establish the impact of training.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="marketable_seed_pct",
            real_relationships=(("virus_incidence_pct", -1, 0.60), ("training_visits", 1, 0.18)),
            confounded_exposure="inspection_fee_usd",
            confounder="country_site",
            null_variable="bag_label_number",
            leakage="marketable_seed_fraction",
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("virus_incidence_pct", "training_visits", "producer_scale", "lot_weight_kg"),
            category_variants={
                "crop": {"sweetpotato": ("sweet potato", "SweetPotato"), "potato": ("Potato", "POTATO ")},
                "producer_scale": {"small": ("Smallholder", "small "), "commercial": ("Commercial", "large")},
            },
            unit_converters={
                "lot_weight_kg": lambda value: f"{value / 1000:.3f} tonnes",
                "inspection_fee_usd": lambda value: f"USD {value:.2f}",
            },
            impossible_values={"virus_incidence_pct": (145.0,), "lot_weight_kg": (-25.0,)},
        ),
        real_relationships_text=(
            "Higher virus incidence decreases simulated marketable-seed percentage.",
            "More training visits increase simulated marketable-seed percentage.",
        ),
        confounded_text="Inspection fee appears associated with quality because both vary by country_site; fee has no direct generating term.",
        null_text="bag_label_number is random.",
        leakage_text="marketable_seed_fraction is marketable_seed_pct divided by 100.",
        participant_tasks=(
            "Standardize crop/producer categories and lot-weight units.",
            "Identify lots requiring review without hiding missing health observations.",
            "Predict lot quality without marketable_seed_fraction and discuss selection bias from inspected lots only.",
        ),
        ethics_note="Producer identities, countries and lot outcomes are simulated and must not be used to evaluate real seed-system partners.",
    )


def climate_smart_agronomy(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    sites = {
        "Andes-high": dict(yield_base=2, irrigation=4, rain=610),
        "Coast-dry": dict(yield_base=9, irrigation=11, rain=55),
        "Lake-region": dict(yield_base=5, irrigation=7, rain=430),
        "Rift-highland": dict(yield_base=7, irrigation=9, rain=310),
    }
    rows: list[dict[str, Any]] = []
    record = 1
    for season_index, season in enumerate(("2024-25", "2025-26")):
        for site, meta in sites.items():
            for block in range(1, 5):
                for plot in range(1, 11):
                    moisture = clamp(rng.gauss(22, 5), 8, 40)
                    mulch = clamp(rng.gauss(48, 25), 0, 100)
                    irrigation_events = meta["irrigation"] + rng.gauss(0, 1.4)
                    yield_t_ha = clamp(
                        8 + meta["yield_base"] + 0.66 * moisture + 0.10 * mulch + season_index * 1.2 + rng.gauss(0, 2.2),
                        5,
                        52,
                    )
                    price = rng.uniform(250, 330)
                    rows.append(
                        {
                            "record_id": f"CSA-{record:04d}",
                            "site": site,
                            "season": season,
                            "block": block,
                            "plot": plot,
                            "crop": ("potato", "sweetpotato")[plot % 2],
                            "management_system": ("farmer-practice", "improved")[block % 2],
                            "rainfall_mm": rounded(meta["rain"] + season_index * 25 + rng.gauss(0, 35), 1),
                            "soil_moisture_pct": rounded(moisture, 1),
                            "mulch_coverage_pct": rounded(mulch, 1),
                            "irrigation_events": rounded(irrigation_events, 1),
                            "nitrogen_kg_ha": rounded(clamp(rng.gauss(95, 25), 20, 180), 1),
                            "yield_t_ha": rounded(yield_t_ha, 2),
                            "water_use_efficiency_kg_m3": rounded(clamp(yield_t_ha * 1000 / (meta["rain"] + irrigation_events * 25), 2, 80), 2),
                            "weather_station_serial_digit": rng.randint(1000, 9999),
                            "gross_revenue_usd_ha": rounded(yield_t_ha * price, 2),
                        }
                    )
                    record += 1
    cols = [
        column("record_id", "string", "none", "primary_key", "unique CSA-####", "Synthetic plot-season record."),
        column("site", "category", "none", "confounder", "Andes-high|Coast-dry|Lake-region|Rift-highland", "Broad synthetic agroecological site."),
        column("season", "category", "none", "design", "2024-25|2025-26", "Cropping season."),
        column("block", "integer", "none", "design", "1-4", "Block within site."),
        column("plot", "integer", "none", "design", "1-10", "Plot number within block."),
        column("crop", "category", "none", "design", "potato|sweetpotato", "Crop."),
        column("management_system", "category", "none", "design", "farmer-practice|improved", "Synthetic management label; not randomized independently of block."),
        column("rainfall_mm", "number", "mm/season", "context", "0-2000", "Seasonal rainfall."),
        column("soil_moisture_pct", "number", "%", "predictor", "0-100", "Root-zone soil moisture; planted positive relationship with yield."),
        column("mulch_coverage_pct", "number", "%", "predictor", "0-100", "Surface mulch cover; planted positive relationship with yield."),
        column("irrigation_events", "number", "events/season", "confounded_exposure", "0-40", "Irrigation events, confounded by site."),
        column("nitrogen_kg_ha", "number", "kg/ha", "context", "0-400", "Applied nitrogen."),
        column("yield_t_ha", "number", "t/ha", "outcome", "0-80", "Synthetic harvested yield."),
        column("water_use_efficiency_kg_m3", "number", "kg/m3", "outcome_secondary", ">=0", "Derived water-use-efficiency indicator."),
        column("weather_station_serial_digit", "integer", "none", "null", "1000-9999", "Random station serial digit unrelated to yield."),
        column("gross_revenue_usd_ha", "number", "USD/ha", "leakage", ">=0", "Post-harvest revenue derived from yield and price."),
    ]
    return DatasetSpec(
        slug="climate_smart_agronomy",
        title="Climate-smart agronomy and water management",
        area="Sustainable intensification, climate resilience and crop management",
        question="Which soil-water and management indicators accompany resilient yield across contrasting environments?",
        observation_unit="One plot in one site, season and block.",
        design="Two-season multi-site observational demonstration with nested blocks and plots.",
        limitation="Management and irrigation are not independently randomized across sites, so the dataset supports prediction and hypothesis generation, not causal treatment-effect claims.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="yield_t_ha",
            real_relationships=(("soil_moisture_pct", 1, 0.55), ("mulch_coverage_pct", 1, 0.24)),
            confounded_exposure="irrigation_events",
            confounder="site",
            null_variable="weather_station_serial_digit",
            leakage="gross_revenue_usd_ha",
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("soil_moisture_pct", "mulch_coverage_pct", "nitrogen_kg_ha", "rainfall_mm"),
            category_variants={
                "management_system": {"farmer-practice": ("farmer practice", "FP"), "improved": ("Improved", "IMP")},
                "crop": {"sweetpotato": ("sweet potato", "SweetPotato"), "potato": ("Potato",)},
            },
            unit_converters={
                "rainfall_mm": lambda value: f"{value / 25.4:.2f} inches",
                "nitrogen_kg_ha": lambda value: f"{value * 0.892179:.1f} lb/acre",
            },
            impossible_values={"soil_moisture_pct": (128.0,), "rainfall_mm": (-12.0,)},
        ),
        real_relationships_text=(
            "Higher soil moisture increases simulated yield.",
            "Higher mulch coverage independently increases simulated yield.",
        ),
        confounded_text="Irrigation events appear related to yield because both differ by site; irrigation count has no direct term in the yield equation.",
        null_text="weather_station_serial_digit is random.",
        leakage_text="gross_revenue_usd_ha is calculated after harvest from yield and price.",
        participant_tasks=(
            "Standardize rainfall and fertilizer units and preserve the site/block design.",
            "Compare yield resilience rather than only pooled average yield.",
            "Build a yield model without gross revenue and explain why irrigation is confounded by site.",
        ),
        ethics_note="All sites and measurements are synthetic; the dataset cannot justify recommendations to farmers.",
    )


def value_chain_adoption(seed: int) -> DatasetSpec:
    rng = random.Random(seed)
    countries = ("Peru", "Kenya", "Uganda")
    education_effect = {"primary": -1.3, "secondary": 0.0, "post-secondary": 1.3}
    rows: list[dict[str, Any]] = []
    for index in range(1, 451):
        country = countries[index % 3]
        education = ("primary", "secondary", "post-secondary")[index % 3]
        extension = rng.randint(0, 8)
        market_access = clamp(rng.gauss(52, 20), 5, 100)
        smartphone_probability = logistic(-2.2 + 4.4 * (education == "post-secondary") + 2.1 * (education == "secondary"))
        smartphone = int(rng.random() < smartphone_probability)
        adoption_probability = logistic(-2.6 + 0.38 * extension + 0.035 * market_access + education_effect[education] + rng.gauss(0, 0.25))
        adopted = int(rng.random() < adoption_probability)
        income = clamp(rng.lognormvariate(8.2, 0.45), 800, 18000)
        sales = 0.0 if not adopted else clamp(income * rng.uniform(0.28, 0.62), 300, 11000)
        rows.append(
            {
                "record_id": f"VCA-{index:04d}",
                "country": country,
                "district_code": f"D-{country[:2].upper()}-{(index % 8) + 1:02d}",
                "survey_round": "2026-baseline",
                "cluster": f"CL-{(index % 30) + 1:02d}",
                "enumerator_team": f"TEAM-{(index % 6) + 1}",
                "respondent_gender": ("woman", "man", "another/prefer-not-to-say")[index % 3],
                "respondent_age_years": rng.randint(19, 72),
                "education_band": education,
                "extension_contacts_year": extension,
                "market_access_score": rounded(market_access, 1),
                "smartphone_owned": smartphone,
                "annual_farm_income_usd": rounded(income, 2),
                "technology_adopted": adopted,
                "questionnaire_version_digit": rng.randint(1000, 9999),
                "post_adoption_sales_usd": rounded(sales, 2),
            }
        )
    cols = [
        column("record_id", "string", "none", "primary_key", "unique VCA-####", "Synthetic de-identified respondent record."),
        column("country", "category", "none", "design", "Peru|Kenya|Uganda", "Synthetic country context."),
        column("district_code", "category", "none", "design", "synthetic district code", "De-identified district code."),
        column("survey_round", "category", "none", "design", "2026-baseline", "Survey campaign."),
        column("cluster", "category", "none", "design", "CL-01..CL-30", "Sampling cluster."),
        column("enumerator_team", "category", "none", "design", "TEAM-1..TEAM-6", "Enumerator team."),
        column("respondent_gender", "category", "none", "protected_context", "woman|man|another/prefer-not-to-say", "Self-described gender category."),
        column("respondent_age_years", "integer", "years", "context", "18-100", "Synthetic respondent age."),
        column("education_band", "category", "none", "confounder", "primary|secondary|post-secondary", "Education band confounding smartphone ownership and adoption."),
        column("extension_contacts_year", "integer", "contacts/year", "predictor", "0-30", "Extension contacts; planted positive relationship with adoption."),
        column("market_access_score", "number", "index 0-100", "predictor", "0-100", "Composite market-access score; planted positive relationship."),
        column("smartphone_owned", "integer", "0/1", "confounded_exposure", "0|1", "Smartphone ownership, confounded by education."),
        column("annual_farm_income_usd", "number", "USD/year", "context", ">=0", "Synthetic annual farm income."),
        column("technology_adopted", "integer", "0/1", "outcome", "0|1", "Whether the synthetic technology was adopted."),
        column("questionnaire_version_digit", "integer", "none", "null", "1000-9999", "Random questionnaire digit unrelated to adoption."),
        column("post_adoption_sales_usd", "number", "USD/year", "leakage", ">=0", "Measured after adoption and structurally zero for non-adopters; unsafe for adoption prediction."),
    ]
    return DatasetSpec(
        slug="value_chain_adoption",
        title="Value-chain technology adoption and inclusion",
        area="Markets, adoption, livelihoods, gender and social inclusion",
        question="Which service and market-access indicators predict adoption, and for whom does the model perform poorly?",
        observation_unit="One synthetic, de-identified survey respondent.",
        design="Cross-sectional clustered baseline survey across three synthetic country contexts.",
        limitation="Cross-sectional self-reports, nonrandom extension contact and unmeasured wealth prevent causal attribution of adoption or income effects.",
        columns=cols,
        rows=rows,
        validation=Validation(
            outcome="technology_adopted",
            real_relationships=(("extension_contacts_year", 1, 0.25), ("market_access_score", 1, 0.18)),
            confounded_exposure="smartphone_owned",
            confounder="education_band",
            null_variable="questionnaire_version_digit",
            leakage="post_adoption_sales_usd",
            max_within_confounder_correlation=0.20,
        ),
        dirty_plan=DirtyPlan(
            missing_columns=("respondent_gender", "education_band", "annual_farm_income_usd", "market_access_score"),
            category_variants={
                "respondent_gender": {"woman": ("Female", "WOMAN ", "mujer"), "man": ("Male", "MAN", "hombre")},
                "country": {"Peru": ("Perú", "PERU"), "Kenya": ("kenya",)},
                "education_band": {"post-secondary": ("tertiary", "Post secondary"), "primary": ("Primary",)},
            },
            unit_converters={
                "annual_farm_income_usd": lambda value: f"PEN {value * 3.75:.2f}",
                "respondent_age_years": lambda value: f"{value * 12:.0f} months",
            },
            impossible_values={"respondent_age_years": (7,), "market_access_score": (145.0,)},
        ),
        real_relationships_text=(
            "More extension contacts increase the simulated probability of adoption.",
            "Higher market-access score independently increases adoption probability.",
        ),
        confounded_text="Smartphone ownership appears associated with adoption because education increases both; smartphone ownership has no direct term in the adoption equation.",
        null_text="questionnaire_version_digit is random.",
        leakage_text="post_adoption_sales_usd is observed after adoption and is zero for non-adopters.",
        participant_tasks=(
            "Standardize survey categories and currencies without inventing missing respondent attributes.",
            "Evaluate prediction errors across gender, country and education groups.",
            "Exclude post_adoption_sales_usd and avoid describing observational associations as program impacts.",
        ),
        ethics_note="All respondent records are synthetic. Real household data require consent, minimization, de-identification and an approved external-AI data policy.",
    )


def _numeric(values: Iterable[Any]) -> list[float]:
    return [float(value) for value in values]


def pearson(left: Iterable[Any], right: Iterable[Any]) -> float:
    x = _numeric(left)
    y = _numeric(right)
    if len(x) != len(y) or not x:
        raise ValueError("Correlation requires equally sized non-empty vectors")
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    numerator = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
    denominator = math.sqrt(
        sum((a - mean_x) ** 2 for a in x) * sum((b - mean_y) ** 2 for b in y)
    )
    return 0.0 if denominator == 0 else numerator / denominator


def within_group_correlation(rows: list[dict[str, Any]], exposure: str, outcome: str, group: str) -> float:
    grouped: dict[Any, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row[group], []).append(row)
    exposure_residuals: list[float] = []
    outcome_residuals: list[float] = []
    for group_rows in grouped.values():
        exposure_mean = sum(float(row[exposure]) for row in group_rows) / len(group_rows)
        outcome_mean = sum(float(row[outcome]) for row in group_rows) / len(group_rows)
        exposure_residuals.extend(float(row[exposure]) - exposure_mean for row in group_rows)
        outcome_residuals.extend(float(row[outcome]) - outcome_mean for row in group_rows)
    return pearson(exposure_residuals, outcome_residuals)


def validate_scientific_structure(spec: DatasetSpec) -> dict[str, float]:
    outcome = [row[spec.validation.outcome] for row in spec.rows]
    metrics: dict[str, float] = {}
    for predictor, direction, minimum in spec.validation.real_relationships:
        correlation = pearson([row[predictor] for row in spec.rows], outcome)
        metrics[f"real:{predictor}"] = correlation
        if direction * correlation < minimum:
            raise ValueError(
                f"{spec.slug}: planted relationship {predictor} has r={correlation:.3f}, expected {direction:+d} >= {minimum}"
            )
    null_correlation = pearson([row[spec.validation.null_variable] for row in spec.rows], outcome)
    metrics[f"null:{spec.validation.null_variable}"] = null_correlation
    if abs(null_correlation) > spec.validation.max_null_correlation:
        raise ValueError(f"{spec.slug}: null variable is too correlated (r={null_correlation:.3f})")
    leakage_correlation = pearson([row[spec.validation.leakage] for row in spec.rows], outcome)
    metrics[f"leakage:{spec.validation.leakage}"] = leakage_correlation
    if abs(leakage_correlation) < 0.70:
        raise ValueError(f"{spec.slug}: leakage is not strong enough (r={leakage_correlation:.3f})")
    marginal = pearson([row[spec.validation.confounded_exposure] for row in spec.rows], outcome)
    within = within_group_correlation(
        spec.rows,
        spec.validation.confounded_exposure,
        spec.validation.outcome,
        spec.validation.confounder,
    )
    metrics[f"confounded:marginal:{spec.validation.confounded_exposure}"] = marginal
    metrics[f"confounded:within:{spec.validation.confounded_exposure}"] = within
    if abs(marginal) < 0.16 or abs(within) > spec.validation.max_within_confounder_correlation:
        raise ValueError(
            f"{spec.slug}: confounding check failed (marginal r={marginal:.3f}, within r={within:.3f})"
        )
    return metrics


def corrupt_rows(spec: DatasetSpec, seed: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rng = random.Random(seed)
    dirty = [dict(row) for row in spec.rows]
    summary: dict[str, Any] = {"missing": {}, "category_variants": {}, "mixed_units": {}, "impossible_values": {}}
    row_count = len(dirty)

    for name in spec.dirty_plan.missing_columns:
        count = max(2, round(row_count * spec.dirty_plan.missing_rate))
        indices = rng.sample(range(row_count), count)
        for index in indices:
            dirty[index][name] = ""
        summary["missing"][name] = count

    for name, canonical_map in spec.dirty_plan.category_variants.items():
        candidates = [i for i, row in enumerate(dirty) if row.get(name) in canonical_map]
        count = min(len(candidates), max(2, round(row_count * spec.dirty_plan.category_rate)))
        for index in rng.sample(candidates, count):
            canonical = str(dirty[index][name])
            dirty[index][name] = rng.choice(canonical_map[canonical])
        summary["category_variants"][name] = count

    for name, converter in spec.dirty_plan.unit_converters.items():
        candidates = [i for i, row in enumerate(dirty) if isinstance(row.get(name), (int, float))]
        count = min(len(candidates), max(2, round(row_count * spec.dirty_plan.unit_rate)))
        for index in rng.sample(candidates, count):
            dirty[index][name] = converter(float(dirty[index][name]))
        summary["mixed_units"][name] = count

    reserved: set[int] = set()
    for name, values in spec.dirty_plan.impossible_values.items():
        indices = [index for index in range(row_count) if index not in reserved]
        selected = rng.sample(indices, len(values))
        for index, value in zip(selected, values):
            dirty[index][name] = value
            reserved.add(index)
        summary["impossible_values"][name] = list(values)

    duplicate_count = max(2, round(row_count * spec.dirty_plan.duplicate_rate))
    duplicate_indices = rng.sample(range(row_count), duplicate_count)
    dirty.extend(dict(dirty[index]) for index in duplicate_indices)
    summary["duplicate_rows"] = duplicate_count
    rng.shuffle(dirty)
    return dirty, summary


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_dictionary(path: Path, columns: list[Column]) -> None:
    rows = [
        {
            "column": item.name,
            "data_type": item.data_type,
            "unit": item.unit,
            "role": item.role,
            "valid_values_or_range": item.valid_values,
            "description": item.description,
            "cleaning_notes": item.cleaning_notes,
        }
        for item in columns
    ]
    write_csv(path, list(rows[0]), rows)


def participant_readme(spec: DatasetSpec) -> str:
    tasks = "\n".join(f"{index}. {task}" for index, task in enumerate(spec.participant_tasks, 1))
    return f"""# {spec.title}

> **Synthetic workshop data.** Nothing in these files describes a real person, community,
> accession, genotype, site, partner or CIP research result.

## Research area

{spec.area}

## Guiding question

{spec.question}

## Observation unit

{spec.observation_unit}

## Design metadata

{spec.design}

The `dirty.csv` file is the participant starting point. The `clean.csv` file is the
facilitator benchmark and should not be distributed during the cleaning exercise. The
`dictionary.csv` file defines the expected columns, units, roles and valid ranges.

## Suggested tasks

{tasks}

## Causal limitation

{spec.limitation}

## Ethics and interpretation

{spec.ethics_note}

## Cleanliness score

From the workshop root:

```powershell
python scripts/score_cleanliness.py datasets/{spec.slug}/{spec.slug}_dirty.csv
python scripts/score_cleanliness.py datasets/{spec.slug}/{spec.slug}_clean.csv
```

The clean reference scores 100. The score measures agreement with the workshop benchmark;
it does not decide whether an analysis is scientifically valid. In particular, confounders,
null variables and leakage remain in the clean file so participants must reason about them.
"""


def facilitator_readme(spec: DatasetSpec, metrics: dict[str, float]) -> str:
    relationships = "\n".join(f"- {item}" for item in spec.real_relationships_text)
    metric_lines = "\n".join(f"- `{name}`: {value:+.3f}" for name, value in sorted(metrics.items()))
    missing = ", ".join(f"{name}={count}" for name, count in spec.corruption_summary["missing"].items())
    categories = ", ".join(f"{name}={count}" for name, count in spec.corruption_summary["category_variants"].items())
    units = ", ".join(f"{name}={count}" for name, count in spec.corruption_summary["mixed_units"].items())
    impossible = ", ".join(
        f"{name}={values}" for name, values in spec.corruption_summary["impossible_values"].items()
    )
    return f"""# Facilitator key — {spec.title}

Do not distribute this file before the exercise: it describes the planted data-generating
relationships and the exact corruption families.

## Two real relationships

{relationships}

## Confounded association

{spec.confounded_text}

## Null variable

{spec.null_text}

## Leakage

{spec.leakage_text}

## Dirty-file defects

- Duplicate rows: {spec.corruption_summary['duplicate_rows']}
- Missing cells: {missing}
- Inconsistent category cells: {categories}
- Mixed-unit cells: {units}
- Impossible values: {impossible}

The corruption is deterministic. Re-running `scripts/generate_datasets.py` reproduces the
same files byte for byte with the default seed.

## Validation correlations on the clean reference

{metric_lines}

The `confounded:marginal` value is intentionally noticeable. The corresponding `within`
correlation is calculated after demeaning exposure and outcome within the named confounder
groups and should be close to zero.

## Causal limitation

{spec.limitation}
"""


def build_specs(seed: int) -> list[DatasetSpec]:
    builders = (
        potato_breeding,
        sweetpotato_nutrition,
        native_potato_biodiversity,
        genebank_regeneration,
        seed_system_quality,
        climate_smart_agronomy,
        value_chain_adoption,
    )
    return [builder(seed + index * 101) for index, builder in enumerate(builders)]


def generate(seed: int = BASE_SEED, datasets_root: Path = DATASETS_ROOT) -> list[DatasetSpec]:
    specs = build_specs(seed)
    for index, spec in enumerate(specs):
        metrics = validate_scientific_structure(spec)
        dirty, summary = corrupt_rows(spec, seed + 10_000 + index * 211)
        spec.corruption_summary = summary
        dataset_dir = datasets_root / spec.slug
        fields = [item.name for item in spec.columns]
        write_csv(dataset_dir / f"{spec.slug}_clean.csv", fields, spec.rows)
        write_csv(dataset_dir / f"{spec.slug}_dirty.csv", fields, dirty)
        write_dictionary(dataset_dir / f"{spec.slug}_dictionary.csv", spec.columns)
        (dataset_dir / "README.md").write_text(participant_readme(spec), encoding="utf-8")
        (dataset_dir / "FACILITATOR.md").write_text(
            facilitator_readme(spec, metrics), encoding="utf-8"
        )
    return specs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=BASE_SEED, help="Deterministic base seed")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT,
        help="Workshop root; generated packages are written below its datasets/ folder",
    )
    args = parser.parse_args()
    datasets_root = args.output_dir.resolve() / "datasets"
    specs = generate(args.seed, datasets_root)
    print(f"Generated {len(specs)} synthetic workshop packages in {datasets_root}")
    for spec in specs:
        print(f"- {spec.slug}: {len(spec.rows)} clean rows")


if __name__ == "__main__":
    main()
