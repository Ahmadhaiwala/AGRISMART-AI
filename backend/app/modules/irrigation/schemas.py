"""
Smart Irrigation schemas
Pydantic models for request/response validation
"""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class GrowthStage(str, Enum):
    seedling = "seedling"
    vegetative = "vegetative"
    flowering = "flowering"
    fruiting = "fruiting"


class IrrigationInput(BaseModel):
    """
    Inputs required to predict whether irrigation is needed right now.

    Designed so `soil_moisture_percent` can later come from a real/simulated
    sensor feed (Module F), and `rain_probability_percent` /
    `forecast_rain_mm_24h` can later come from a live weather API
    (Module C). Until those exist, all fields are supplied manually.
    """

    crop_type: str = Field(
        ..., description="Crop name, e.g. 'Tomato', 'Potato', 'Corn', 'Apple', 'Grape', 'Pepper'."
    )
    growth_stage: GrowthStage = Field(..., description="Current growth stage of the crop")

    soil_moisture_percent: float = Field(
        ..., ge=0, le=100, description="Current volumetric soil moisture, as a percentage"
    )

    rain_probability_percent: float = Field(
        0, ge=0, le=100, description="Forecast probability of rain in the next 24h"
    )
    forecast_rain_mm_24h: float = Field(
        0, ge=0, description="Forecast rainfall amount in the next 24h, in mm"
    )
    temperature_c: Optional[float] = Field(
        None, description="Current/forecast temperature in Celsius (optional, refines urgency)"
    )

    area_sqm: float = Field(
        1.0, gt=0, description="Field/plot area in square meters, used to scale the water recommendation"
    )


class IrrigationDecision(BaseModel):
    irrigation_required: bool
    urgency: str
    soil_moisture_status: str
    recommended_water_liters: float
    rain_delay_applied: bool


class IrrigationResponse(BaseModel):
    success: bool
    decision: IrrigationDecision
    reasons: List[str]
    logic_version: str = "1.0"
