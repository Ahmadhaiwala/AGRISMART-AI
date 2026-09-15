"""
Tests for the Smart Irrigation module (Bonus Module B).

These tests only import the irrigation router/service directly, not the
full app, so they run without needing torch / the disease-detection model
to be installed or loaded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.irrigation.router import router as irrigation_router
from app.modules.irrigation.schemas import IrrigationInput
from app.modules.irrigation.service import irrigation_service


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(irrigation_router, prefix="/api/v1")
    return TestClient(app)


VALID_PAYLOAD = {
    "crop_type": "Tomato",
    "growth_stage": "vegetative",
    "soil_moisture_percent": 50,
    "rain_probability_percent": 0,
    "forecast_rain_mm_24h": 0,
    "temperature_c": 28,
    "area_sqm": 10,
}


# ---------------------------------------------------------------------------
# Service-level unit tests (pure logic, no HTTP)
# ---------------------------------------------------------------------------

def test_adequate_moisture_no_irrigation_needed():
    """Tomato/vegetative optimal threshold is 45% -- 50% is above it."""
    data = IrrigationInput(**VALID_PAYLOAD)
    result = irrigation_service.predict(data)
    assert result["decision"]["irrigation_required"] is False
    assert result["decision"]["urgency"] == "none"
    assert result["decision"]["soil_moisture_status"] == "adequate"
    assert result["decision"]["recommended_water_liters"] == 0.0


def test_critical_deficit_triggers_high_urgency_irrigation():
    """Tomato/vegetative critical threshold is 30% -- 15% is well below it."""
    data = IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 15})
    result = irrigation_service.predict(data)
    assert result["decision"]["irrigation_required"] is True
    assert result["decision"]["urgency"] == "high"
    assert result["decision"]["soil_moisture_status"] == "critical_deficit"
    assert result["decision"]["recommended_water_liters"] > 0


def test_moderate_deficit_triggers_medium_urgency_irrigation():
    """35% is between the 30% critical and 45% optimal thresholds."""
    data = IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 35})
    result = irrigation_service.predict(data)
    assert result["decision"]["irrigation_required"] is True
    assert result["decision"]["urgency"] == "medium"
    assert result["decision"]["soil_moisture_status"] == "moderate_deficit"


def test_moderate_deficit_delayed_by_high_rain_probability():
    data = IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 35, "rain_probability_percent": 80})
    result = irrigation_service.predict(data)
    assert result["decision"]["irrigation_required"] is False
    assert result["decision"]["urgency"] == "low"
    assert result["decision"]["rain_delay_applied"] is True
    assert result["decision"]["recommended_water_liters"] == 0.0


def test_critical_deficit_not_delayed_by_light_rain():
    """Critical deficit + light rain forecast (below heavy-rain threshold) should still irrigate."""
    data = IrrigationInput(**{
        **VALID_PAYLOAD, "soil_moisture_percent": 15,
        "rain_probability_percent": 80, "forecast_rain_mm_24h": 3,
    })
    result = irrigation_service.predict(data)
    assert result["decision"]["irrigation_required"] is True
    assert result["decision"]["urgency"] == "high"


def test_critical_deficit_delayed_by_heavy_rain():
    data = IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 15, "forecast_rain_mm_24h": 20})
    result = irrigation_service.predict(data)
    assert result["decision"]["irrigation_required"] is False
    assert result["decision"]["rain_delay_applied"] is True
    assert result["decision"]["urgency"] == "high"  # still flagged for monitoring


def test_heat_stress_reason_added_when_hot_and_irrigating():
    data = IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 15, "temperature_c": 38})
    result = irrigation_service.predict(data)
    assert any("evapotranspiration" in r for r in result["reasons"])


def test_unknown_crop_falls_back_to_default_thresholds():
    data = IrrigationInput(**{**VALID_PAYLOAD, "crop_type": "Dragonfruit", "soil_moisture_percent": 15})
    result = irrigation_service.predict(data)
    # default/vegetative critical threshold is 28% -- 15% should still trigger irrigation
    assert result["decision"]["irrigation_required"] is True


def test_recommended_water_scales_with_area():
    small = irrigation_service.predict(IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 15, "area_sqm": 1}))
    large = irrigation_service.predict(IrrigationInput(**{**VALID_PAYLOAD, "soil_moisture_percent": 15, "area_sqm": 10}))
    assert large["decision"]["recommended_water_liters"] == pytest.approx(
        small["decision"]["recommended_water_liters"] * 10, rel=0.01
    )


# ---------------------------------------------------------------------------
# HTTP-level tests (via the actual router / endpoint contract)
# ---------------------------------------------------------------------------

def test_endpoint_returns_200_for_valid_payload(client):
    resp = client.post("/api/v1/irrigation/predict", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert "decision" in body
    assert body["decision"]["urgency"] in {"none", "low", "medium", "high"}
    assert "logic_version" in body


def test_endpoint_rejects_missing_required_field(client):
    incomplete = {"crop_type": "Tomato"}
    resp = client.post("/api/v1/irrigation/predict", json=incomplete)
    assert resp.status_code == 422


def test_endpoint_rejects_invalid_growth_stage(client):
    payload = {**VALID_PAYLOAD, "growth_stage": "dormant"}
    resp = client.post("/api/v1/irrigation/predict", json=payload)
    assert resp.status_code == 422


def test_endpoint_rejects_moisture_above_100(client):
    payload = {**VALID_PAYLOAD, "soil_moisture_percent": 150}
    resp = client.post("/api/v1/irrigation/predict", json=payload)
    assert resp.status_code == 422
