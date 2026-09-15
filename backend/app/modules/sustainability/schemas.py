"""
Sustainability score schemas
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class SustainabilityInput(BaseModel):
    """
    Inputs required to compute the sustainability score.

    Can be provided manually OR auto-populated from other modules
    using the integrated endpoint.
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
    # From disease detection module
    is_healthy: bool = Field(True, description="Whether the crop was classified as healthy")
    disease_confidence: float = Field(
        0.0, ge=0, le=1,
        description="Model confidence in the detected disease (0 if healthy), used as a severity proxy"
    )


class IntegratedSustainabilityInput(BaseModel):
    """
    Input for integrated sustainability score that automatically gathers
    data from all modules (Disease Detection, Crop Recommendation, 
    Smart Irrigation, Weather Intelligence)
    """
    
    # Farm information
    farm_id: str = Field(..., description="Unique farm identifier")
    
    # Crop information (for irrigation and crop recommendation)
    crop_name: str = Field(..., description="Name of the crop (e.g., 'Tomato', 'Wheat')")
    growth_stage: str = Field(..., description="Current growth stage")
    
    # Soil information (for irrigation)
    soil_moisture: int = Field(..., ge=0, le=100, description="Current soil moisture percentage")
    soil_type: str = Field(..., description="Soil type (e.g., 'Loamy', 'Sandy', 'Clayey')")
    
    # Weather information (for weather intelligence)
    latitude: float = Field(..., ge=-90, le=90, description="Farm latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Farm longitude")
    temperature: float = Field(..., description="Current temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Current humidity percentage")
    
    # Disease detection (optional - from image upload)
    disease_detected: Optional[str] = Field(None, description="Disease name if detected")
    disease_confidence: Optional[float] = Field(None, ge=0, le=1, description="Disease detection confidence")
    is_healthy: bool = Field(True, description="Whether crop is healthy")
    
    # Resource usage (actual farmer inputs)
    water_used_liters: float = Field(..., gt=0, description="Water actually applied")
    fertilizer_used_kg: float = Field(..., ge=0, description="Fertilizer actually applied")
    pesticide_used_kg: float = Field(0, ge=0, description="Pesticide actually applied")
    pesticide_recommended_kg: float = Field(0, ge=0, description="Recommended pesticide amount")
    
    # Irrigation configuration
    has_irrigation: bool = Field(True, description="Whether farm has irrigation system")
    seedling_stage: int = Field(1, ge=0, description="Seedling stage (0-4)")


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


class IntegratedSustainabilityResponse(BaseModel):
    """Enhanced response with module integration details"""
    success: bool
    overall_score: float
    grade: str
    sub_scores: SubScores
    suggestions: List[str]
    
    # Module integration details
    modules_used: List[str] = Field(description="List of modules that contributed data")
    irrigation_recommendation: Optional[dict] = Field(None, description="From Smart Irrigation module")
    weather_recommendation: Optional[dict] = Field(None, description="From Weather Intelligence module")
    crop_health_details: Optional[dict] = Field(None, description="From Disease Detection module")
    
    formula_version: str = "1.0"
