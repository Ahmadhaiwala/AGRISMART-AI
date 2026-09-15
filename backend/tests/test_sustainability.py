"""
Tests for the Sustainability Score module (Bonus Module D).

These tests only import the sustainability router/service directly, not the
full app, so they run without needing torch / the disease-detection model
to be installed or loaded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.sustainability.router import router as sustainability_router
from app.modules.sustainability.schemas import SustainabilityInput
from app.modules.sustainability.service import sustainability_service


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(sustainability_router, prefix="/api/v1")
    return TestClient(app)


VALID_PAYLOAD = {
    "water_used_liters": 100,
    "water_required_liters": 100,
    "fertilizer_used_kg": 4,
    "fertilizer_recommended_kg": 4,
    "pesticide_used_kg": 1,
    "pesticide_recommended_kg": 1,
    "is_healthy": True,
    "disease_confidence": 0.0,
}


# ---------------------------------------------------------------------------
# Service-level unit tests (pure logic, no HTTP)
# ---------------------------------------------------------------------------

def test_perfect_inputs_score_100():
    """Used == required everywhere and healthy crop -> full score, grade A."""
    data = SustainabilityInput(**VALID_PAYLOAD)
    result = sustainability_service.compute(data)
    assert result["overall_score"] == 100.0
    assert result["grade"] == "A"
    assert "maintain current practices" in result["suggestions"][0].lower()


def test_overwatering_lowers_water_efficiency_and_suggests_reduction():
    data = SustainabilityInput(**{**VALID_PAYLOAD, "water_used_liters": 150})
    result = sustainability_service.compute(data)
    assert result["sub_scores"].water_efficiency < 70
    assert any("over-watering" in s for s in result["suggestions"])


def test_underwatering_suggests_increase():
    data = SustainabilityInput(**{**VALID_PAYLOAD, "water_used_liters": 50})
    result = sustainability_service.compute(data)
    assert any("below the crop's requirement" in s for s in result["suggestions"])


def test_fertilizer_overuse_suggests_reduction():
    data = SustainabilityInput(**{**VALID_PAYLOAD, "fertilizer_used_kg": 8})
    result = sustainability_service.compute(data)
    assert any("Fertilizer use is above" in s for s in result["suggestions"])


def test_pesticide_overuse_suggests_reduction_independently_of_fertilizer():
    """Regression test: pesticide over-use must not be silently absorbed
    into the blended resource_use score without its own suggestion."""
    data = SustainabilityInput(**{**VALID_PAYLOAD, "pesticide_used_kg": 5, "pesticide_recommended_kg": 1})
    result = sustainability_service.compute(data)
    assert any("Pesticide use is above" in s for s in result["suggestions"])


def test_diseased_crop_lowers_health_score_and_adds_precaution_tip():
    data = SustainabilityInput(**{**VALID_PAYLOAD, "is_healthy": False, "disease_confidence": 0.9})
    result = sustainability_service.compute(data)
    assert result["sub_scores"].crop_health == pytest.approx(10.0, abs=0.1)
    assert any("Disease detected" in s for s in result["suggestions"])


def test_no_pesticide_data_falls_back_to_fertilizer_only():
    """pesticide_recommended_kg=0 (not provided) -> resource_use == fertilizer_efficiency."""
    payload = {**VALID_PAYLOAD, "pesticide_used_kg": 0, "pesticide_recommended_kg": 0}
    data = SustainabilityInput(**payload)
    result = sustainability_service.compute(data)
    assert result["sub_scores"].resource_use == 100.0


@pytest.mark.parametrize("score,expected_grade", [(90, "A"), (65, "B"), (45, "C"), (10, "D")])
def test_grade_bands(score, expected_grade):
    assert sustainability_service._grade(score) == expected_grade


# ---------------------------------------------------------------------------
# HTTP-level tests (via the actual router / endpoint contract)
# ---------------------------------------------------------------------------

def test_endpoint_returns_200_for_valid_payload(client):
    resp = client.post("/api/v1/sustainability/score", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert 0 <= body["overall_score"] <= 100
    assert body["grade"] in {"A", "B", "C", "D"}
    assert "formula_version" in body


def test_endpoint_rejects_missing_required_field(client):
    incomplete = {"water_used_liters": 90}
    resp = client.post("/api/v1/sustainability/score", json=incomplete)
    assert resp.status_code == 422


def test_endpoint_rejects_zero_water_required(client):
    """water_required_liters must be > 0 (Field gt=0) since it's a divisor."""
    payload = {**VALID_PAYLOAD, "water_required_liters": 0}
    resp = client.post("/api/v1/sustainability/score", json=payload)
    assert resp.status_code == 422
