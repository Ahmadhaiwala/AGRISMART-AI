"""
Pydantic schemas for crop recommendation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional


class CropRecommendationRequest(BaseModel):
    """Request model for crop recommendation"""
    
    # Categorical features
    type_of_crop: str = Field(..., description="Type of crop category")
    soil: str = Field(..., description="Soil type")
    season: str = Field(..., description="Current season")
    water_source: str = Field(..., description="Water source availability")
    
    # Numerical features - basic ranges
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    soil_ph_high: float = Field(..., ge=0, le=14, description="Maximum soil pH value")
    
    temp: float = Field(..., ge=-10, le=60, description="Temperature (°C)")
    max_temp: float = Field(..., ge=-10, le=60, description="Maximum temperature (°C)")
    
    waterrequired: float = Field(..., ge=0, description="Minimum water required (mm)")
    waterrequired_max: float = Field(..., ge=0, description="Maximum water required (mm)")
    
    relative_humidity: float = Field(..., ge=0, le=100, description="Relative humidity (%)")
    relative_humidity_max: float = Field(..., ge=0, le=100, description="Maximum relative humidity (%)")
    
    # NPK values
    n: float = Field(..., ge=0, description="Nitrogen (N) content")
    n_max: float = Field(..., ge=0, description="Maximum Nitrogen (N) content")
    
    p: float = Field(..., ge=0, description="Phosphorus (P) content")
    p_max: float = Field(..., ge=0, description="Maximum Phosphorus (P) content")
    
    k: float = Field(..., ge=0, description="Potassium (K) content")
    k_max: float = Field(..., ge=0, description="Maximum Potassium (K) content")
    
    @validator('soil_ph_high')
    def validate_ph_high(cls, v, values):
        if 'soil_ph' in values and v < values['soil_ph']:
            raise ValueError('soil_ph_high must be >= soil_ph')
        return v
    
    @validator('max_temp')
    def validate_temp_max(cls, v, values):
        if 'temp' in values and v < values['temp']:
            raise ValueError('max_temp must be >= temp')
        return v
    
    @validator('waterrequired_max')
    def validate_water_max(cls, v, values):
        if 'waterrequired' in values and v < values['waterrequired']:
            raise ValueError('waterrequired_max must be >= waterrequired')
        return v
    
    @validator('relative_humidity_max')
    def validate_humidity_max(cls, v, values):
        if 'relative_humidity' in values and v < values['relative_humidity']:
            raise ValueError('relative_humidity_max must be >= relative_humidity')
        return v
    
    @validator('n_max')
    def validate_n_max(cls, v, values):
        if 'n' in values and v < values['n']:
            raise ValueError('n_max must be >= n')
        return v
    
    @validator('p_max')
    def validate_p_max(cls, v, values):
        if 'p' in values and v < values['p']:
            raise ValueError('p_max must be >= p')
        return v
    
    @validator('k_max')
    def validate_k_max(cls, v, values):
        if 'k' in values and v < values['k']:
            raise ValueError('k_max must be >= k')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "type_of_crop": "FOOD GRAIN",
                "soil": "CLAYEY",
                "season": "KHARIF",
                "water_source": "RAIN FED",
                "soil_ph": 6.5,
                "soil_ph_high": 7.5,
                "temp": 25.0,
                "max_temp": 35.0,
                "waterrequired": 100.0,
                "waterrequired_max": 150.0,
                "relative_humidity": 60.0,
                "relative_humidity_max": 80.0,
                "n": 40.0,
                "n_max": 60.0,
                "p": 30.0,
                "p_max": 50.0,
                "k": 20.0,
                "k_max": 40.0
            }
        }


class CropPrediction(BaseModel):
    """Single crop prediction with confidence"""
    crop_name: str = Field(..., description="Predicted crop name")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")


class CropRecommendationResponse(BaseModel):
    """Response model for crop recommendation"""
    success: bool = Field(..., description="Whether the prediction was successful")
    top_crop: str = Field(..., description="Top recommended crop")
    confidence: float = Field(..., ge=0, le=1, description="Confidence of top prediction")
    top_5_predictions: List[CropPrediction] = Field(..., description="Top 5 crop recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "top_crop": "rice",
                "confidence": 0.85,
                "top_5_predictions": [
                    {"crop_name": "rice", "confidence": 0.85},
                    {"crop_name": "wheat", "confidence": 0.08},
                    {"crop_name": "maize", "confidence": 0.04},
                    {"crop_name": "sugarcane", "confidence": 0.02},
                    {"crop_name": "cotton", "confidence": 0.01}
                ]
            }
        }
