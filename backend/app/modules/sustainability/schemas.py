"""
Sustainability score schemas
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class SustainabilityInput(BaseModel):
    """
    Inputs required to compute the sustainability score.

    Designed to be filled in manually by a farmer/user right now, and
    later auto-populated from the irrigation (Module B) and weather
    (Module C) modules once they exist -- the response shape and
    formula stay the same either way.
    """

    # --- Water usage ---
    water_used_liters: float = Field(..., gt=0, description="Water actually applied, in liters")
    water_required_liters: float = Field(..., gt=0, description="Crop's estimated water requirement, in liters")

    # --- Resource use (fertilizer / pesticide) ---
    fertilizer_used_kg: float = Field(..., ge=0, description="Fertilizer actually applied, in kg")
    fertilizer_recommended_kg: float = Field(..., gt=0, description="Recommended fertilizer amount, in kg")
    pesticide_used_kg: float = Field(0, ge=0, description="Pesticide actually applied, in kg (optional)")
    pesticide_recommended_kg: float = Field(0, ge=0, description="Recommended pesticide amount, in kg (optional)")

    # --- Crop health ---
    # If the disease-detection module has already run on this crop's image,
    # pass its result straight through here. If the crop is healthy,
    # leave disease_confidence at 0.
    is_healthy: bool = Field(True, description="Whether the crop was classified as healthy")
    disease_confidence: float = Field(
        0.0, ge=0, le=1,
        description="Model confidence in the detected disease (0 if healthy), used as a severity proxy"
    )


class SubScores(BaseModel):
    water_efficiency: float
    resource_use: float
    crop_health: float


class SustainabilityScoreResponse(BaseModel):
    success: bool
    overall_score: float
    grade: str
    sub_scores: SubScores
    suggestions: List[str]
    formula_version: str = "1.0"
