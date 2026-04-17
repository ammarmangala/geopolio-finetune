from __future__ import annotations

import json

from geopolio.dataset import (
    CATEGORIES,
    REGION_DETAILS,
    canonical_category,
    impact_from_score,
    normalize_sample,
    validate_sample,
)


def test_region_catalog_is_aligned() -> None:
    assert len(REGION_DETAILS) == 18
    assert len({*REGION_DETAILS}) == len(REGION_DETAILS)


def test_impact_from_score_maps_ranges() -> None:
    assert impact_from_score(2) == "Low"
    assert impact_from_score(4) == "Moderate"
    assert impact_from_score(7) == "High"
    assert impact_from_score(10) == "Critical"


def test_validate_sample_accepts_expected_schema() -> None:
    sample = {
        "instruction": "Analyze the geopolitical risk of the following situation for European retail investors.",
        "input": "A border closure disrupts trade flows.",
        "output": json.dumps(
            {
                "risk_score": 5,
                "region": "Europe",
                "category": "Energy Security",
                "impact": "Moderate",
                "analysis": "Short but valid analysis that is long enough to pass validation.",
            }
        ),
    }

    assert validate_sample(sample)


def test_normalize_sample_maps_category_alias() -> None:
    sample = {
        "instruction": "Analyze the geopolitical risk of the following situation for European retail investors.",
        "input": "A trade dispute escalates.",
        "output": json.dumps(
            {
                "risk_score": 6,
                "region": "Europe",
                "category": "Trade War",
                "impact": "Moderate",
                "analysis": "Short but valid analysis that is long enough to pass validation.",
            }
        ),
    }

    normalized = normalize_sample(sample)

    assert normalized is not None
    output = json.loads(normalized["output"])
    assert canonical_category(output["category"]) == "Trade Disruption"
    assert output["impact"] == "High"
