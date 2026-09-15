"""
Pydantic schemas for weather-based intelligence
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ActionPriority(str, Enum):
    """Priority levels for recommended actions"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ActionCategory(str, Enum):
    """Categories of farming actions"""
    IRRIGATION = "irrigation"
    DISEASE_PREVENTION = "disease_prevention"
    PEST_MANAGEMENT = "pest_management"
    HARVESTING = "harvesting"
    PLANTING = "planting"
    FERTILIZATION = "fertilization"
    GENERAL = "general"


class FarmConditions(BaseModel):
    """Current farm conditions"""
    crop_type: str = Field(..., description="Type of crop being grown")
    growth_stage: str = Field(..., description="Current growth stage")
    soil_moisture: int = Field(..., ge=0, le=100, description="Current soil moisture (0-100%)")
    has_irrigation: bool = Field(True, description="Whether farm has irrigation system")
    disease_detected: bool = Field(False, description="Whether disease was recently detected")
    recent_fertilization: bool = Field(False, description="Whether fertilization was done in last 7 days")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_type": "Wheat",
                "growth_stage": "Flowering",
                "soil_moisture": 45,
                "has_irrigation": True,
                "disease_detected": False,
                "recent_fertilization": False
            }
        }


class WeatherIntelligenceRequest(BaseModel):
    """Request for weather-based farming intelligence"""
    latitude: float = Field(..., ge=-90, le=90, description="Farm latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Farm longitude")
    farm_conditions: FarmConditions = Field(..., description="Current farm conditions")
    forecast_days: int = Field(7, ge=1, le=14, description="Number of days to forecast (1-14)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 28.6139,
                "longitude": 77.2090,
                "farm_conditions": {
                    "crop_type": "Wheat",
                    "growth_stage": "Flowering",
                    "soil_moisture": 45,
                    "has_irrigation": True,
                    "disease_detected": False,
                    "recent_fertilization": False
                },
                "forecast_days": 7
            }
        }


class WeatherSummary(BaseModel):
    """Summary of weather conditions"""
    current_temp: float = Field(..., description="Current temperature (°C)")
    current_humidity: float = Field(..., description="Current relative humidity (%)")
    current_precipitation: float = Field(..., description="Current precipitation (mm)")
    current_wind_speed: float = Field(..., description="Current wind speed (km/h)")
    
    forecast_rain_probability: float = Field(..., description="Probability of rain in next 24h (%)")
    forecast_rain_amount: float = Field(..., description="Expected rain amount in next 24h (mm)")
    forecast_max_temp: float = Field(..., description="Max temperature in next 24h (°C)")
    forecast_min_temp: float = Field(..., description="Min temperature in next 24h (°C)")


class Action(BaseModel):
    """Recommended farming action"""
    category: ActionCategory = Field(..., description="Action category")
    priority: ActionPriority = Field(..., description="Action priority")
    title: str = Field(..., description="Short action title")
    description: str = Field(..., description="Detailed action description")
    reasoning: str = Field(..., description="Why this action is recommended")
    timing: str = Field(..., description="When to perform this action")


class RiskAlert(BaseModel):
    """Risk alert based on weather and farm conditions"""
    risk_type: str = Field(..., description="Type of risk")
    severity: ActionPriority = Field(..., description="Risk severity")
    description: str = Field(..., description="Risk description")
    prevention_tips: List[str] = Field(default_factory=list, description="Prevention measures")


class WeatherIntelligenceResponse(BaseModel):
    """Response with weather-based farming intelligence"""
    success: bool = Field(..., description="Request success status")
    location: dict = Field(..., description="Location information")
    weather_summary: WeatherSummary = Field(..., description="Current and forecast weather")
    
    # Actionable recommendations
    recommended_actions: List[Action] = Field(default_factory=list, description="Recommended actions")
    risk_alerts: List[RiskAlert] = Field(default_factory=list, description="Risk alerts")
    
    # Additional insights
    irrigation_recommendation: str = Field(..., description="Specific irrigation guidance")
    disease_risk_level: str = Field(..., description="Disease risk assessment")
    optimal_work_hours: List[str] = Field(default_factory=list, description="Best hours for farm work")
    
    # Data source attribution
    data_source: str = Field(default="Open-Meteo API", description="Weather data source")
    generated_at: datetime = Field(default_factory=datetime.now, description="Response generation time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "location": {
                    "latitude": 28.6139,
                    "longitude": 77.2090,
                    "elevation": 216
                },
                "weather_summary": {
                    "current_temp": 28.5,
                    "current_humidity": 65.0,
                    "current_precipitation": 0.0,
                    "current_wind_speed": 12.5,
                    "forecast_rain_probability": 75.0,
                    "forecast_rain_amount": 15.5,
                    "forecast_max_temp": 32.0,
                    "forecast_min_temp": 22.0
                },
                "recommended_actions": [
                    {
                        "category": "irrigation",
                        "priority": "high",
                        "title": "Delay Irrigation - Rain Expected",
                        "description": "Postpone irrigation for 24-48 hours",
                        "reasoning": "75% chance of 15.5mm rain in next 24 hours",
                        "timing": "Wait until after expected rainfall"
                    }
                ],
                "risk_alerts": [
                    {
                        "risk_type": "disease",
                        "severity": "medium",
                        "description": "Elevated disease risk due to high humidity and upcoming rain",
                        "prevention_tips": ["Monitor crop closely", "Ensure good drainage"]
                    }
                ],
                "irrigation_recommendation": "DELAY - Rain likely within 24 hours",
                "disease_risk_level": "Medium - Monitor closely",
                "optimal_work_hours": ["06:00-10:00", "16:00-18:00"],
                "data_source": "Open-Meteo API"
            }
        }
