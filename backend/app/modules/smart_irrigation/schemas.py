"""
Pydantic schemas for smart irrigation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class CropType(str, Enum):
    """Available crop types"""
    WHEAT = "Wheat"
    CHILLI = "Chilli"
    POTATO = "Potato"
    CARROT = "Carrot"
    TOMATO = "Tomato"


class SoilType(str, Enum):
    """Available soil types"""
    CLAY = "Clay Soil"
    SANDY = "Sandy Soil"
    RED = "Red Soil"
    LOAM = "Loam Soil"
    BLACK = "Black Soil"
    ALLUVIAL = "Alluvial Soil"
    CHALKY = "Chalky Soil"


class SeedlingStage(str, Enum):
    """Crop growth stages"""
    GERMINATION = "Germination"
    SEEDLING = "Seedling Stage"
    VEGETATIVE = "Vegetative Growth / Root or Tuber Development"
    FLOWERING = "Flowering"
    POLLINATION = "Pollination"
    FRUIT_FORMATION = "Fruit/Grain/Bulb Formation"
    MATURATION = "Maturation"
    HARVEST = "Harvest"


class IrrigationRequest(BaseModel):
    """Request model for irrigation prediction"""
    
    crop_id: CropType = Field(..., description="Type of crop")
    soil_type: SoilType = Field(..., description="Soil type")
    seedling_stage: SeedlingStage = Field(..., description="Current growth stage")
    
    moi: int = Field(..., ge=0, le=100, description="Moisture level (0-100%)")
    temp: int = Field(..., ge=-10, le=60, description="Temperature (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Humidity (%)")
    
    @validator('moi')
    def validate_moisture(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Moisture (MOI) must be between 0 and 100')
        return v
    
    @validator('humidity')
    def validate_humidity(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Humidity must be between 0 and 100')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_id": "Wheat",
                "soil_type": "Clay Soil",
                "seedling_stage": "Flowering",
                "moi": 45,
                "temp": 28,
                "humidity": 65.5
            }
        }


class IrrigationLevel(str, Enum):
    """Irrigation requirement levels"""
    NONE = "No Irrigation Needed"
    MEDIUM = "Medium Irrigation Required"
    HIGH = "High Irrigation Required"


class IrrigationRecommendation(BaseModel):
    """Detailed irrigation recommendation"""
    level: IrrigationLevel = Field(..., description="Irrigation level")
    level_code: int = Field(..., ge=0, le=2, description="Level code (0=None, 1=Medium, 2=High)")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    water_amount_liters: Optional[float] = Field(None, description="Recommended water amount (L/m²)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "level": "Medium Irrigation Required",
                "level_code": 1,
                "confidence": 0.92,
                "water_amount_liters": 15.0
            }
        }


class IrrigationResponse(BaseModel):
    """Response model for irrigation prediction"""
    success: bool = Field(..., description="Prediction success status")
    recommendation: IrrigationRecommendation = Field(..., description="Irrigation recommendation")
    
    # Input summary
    conditions: dict = Field(..., description="Input conditions summary")
    
    # Additional insights
    moisture_status: str = Field(..., description="Current moisture level assessment")
    temperature_status: str = Field(..., description="Temperature assessment")
    suggestions: List[str] = Field(default_factory=list, description="Additional farming suggestions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "recommendation": {
                    "level": "Medium Irrigation Required",
                    "level_code": 1,
                    "confidence": 0.92,
                    "water_amount_liters": 15.0
                },
                "conditions": {
                    "crop": "Wheat",
                    "soil": "Clay Soil",
                    "stage": "Flowering",
                    "moisture": 45,
                    "temperature": 28,
                    "humidity": 65.5
                },
                "moisture_status": "Moderate - irrigation recommended",
                "temperature_status": "Optimal for growth",
                "suggestions": [
                    "Monitor soil moisture regularly",
                    "Apply irrigation during cooler hours",
                    "Consider drip irrigation for efficiency"
                ]
            }
        }


class IrrigationHealthResponse(BaseModel):
    """Health check response for irrigation service"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_accuracy: Optional[float] = Field(None, description="Model test accuracy")
    supported_crops: List[str] = Field(default_factory=list, description="Supported crop types")
    supported_soil_types: List[str] = Field(default_factory=list, description="Supported soil types")
    supported_stages: List[str] = Field(default_factory=list, description="Supported growth stages")
