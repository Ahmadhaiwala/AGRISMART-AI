"""
API routes for weather-based intelligence
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from .schemas import (
    WeatherIntelligenceRequest,
    WeatherIntelligenceResponse
)
from .service import WeatherIntelligenceService, get_weather_intelligence_service


router = APIRouter()


@router.post(
    "/weather-intelligence",
    response_model=WeatherIntelligenceResponse,
    summary="Get weather-based farming intelligence",
    description="Combines live/forecast weather with farm conditions to produce actionable recommendations"
)
async def get_weather_intelligence(
    request: WeatherIntelligenceRequest,
    service: WeatherIntelligenceService = Depends(get_weather_intelligence_service)
) -> WeatherIntelligenceResponse:
    """
    Get comprehensive weather-based farming intelligence:
    
    **Combines**:
    - Live and forecast weather data (Open-Meteo API)
    - Current farm conditions (crop, soil moisture, growth stage)
    
    **Produces**:
    - Irrigation recommendations (e.g., "delay irrigation - rain likely")
    - Disease risk alerts (e.g., "raised disease risk - monitor closely")
    - Optimal work hours
    - Prioritized action items
    
    **Data Source**: Open-Meteo API (https://open-meteo.com/)
    - Free, open-source weather API
    - High accuracy global coverage
    - No API key required
    """
    try:
        response = service.generate_intelligence(request)
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating weather intelligence: {str(e)}"
        )


@router.get(
    "/weather-intelligence/info",
    summary="Get weather intelligence system information",
    response_model=Dict[str, Any]
)
async def get_system_info() -> Dict[str, Any]:
    """
    Get information about the weather intelligence system
    """
    return {
        "service": "Smart Weather-Based Intelligence",
        "description": "Combines weather forecasts with farm conditions for actionable farming insights",
        "data_source": {
            "name": "Open-Meteo API",
            "url": "https://open-meteo.com/",
            "type": "Free, open-source weather API",
            "coverage": "Global",
            "update_frequency": "Hourly",
            "features": [
                "Current weather conditions",
                "Hourly forecasts (up to 16 days)",
                "Daily forecasts (up to 16 days)",
                "Historical weather data",
                "High accuracy predictions"
            ]
        },
        "rule_based_intelligence": {
            "irrigation_rules": [
                "Delay if rain probability > 60% and amount > 5mm",
                "Urgent if soil moisture < 30% and no rain expected",
                "Monitor if moisture 30-50% with low rain chance",
                "No irrigation if moisture > 70%"
            ],
            "disease_risk_factors": [
                "High humidity (>70%)",
                "Moderate temperature (20-30°C)",
                "Recent/forecast rainfall",
                "Vulnerable growth stages",
                "Existing disease presence"
            ],
            "action_categories": [
                "Irrigation management",
                "Disease prevention",
                "Pest management",
                "Harvesting timing",
                "Fertilization timing",
                "General farm operations"
            ]
        },
        "supported_parameters": {
            "weather": [
                "Temperature",
                "Humidity",
                "Precipitation",
                "Wind speed",
                "Weather codes"
            ],
            "farm_conditions": [
                "Crop type",
                "Growth stage",
                "Soil moisture",
                "Irrigation availability",
                "Disease status",
                "Recent fertilization"
            ]
        },
        "output_features": [
            "Prioritized action recommendations",
            "Risk alerts with severity levels",
            "Specific irrigation guidance",
            "Disease risk assessment",
            "Optimal work hours",
            "Weather summaries"
        ]
    }


@router.get(
    "/weather-intelligence/sample-locations",
    summary="Get sample farm locations for testing",
    response_model=Dict[str, Any]
)
async def get_sample_locations() -> Dict[str, Any]:
    """
    Get sample locations for testing the weather intelligence system
    """
    return {
        "locations": {
            "delhi_india": {
                "name": "Delhi, India",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "typical_crops": ["Wheat", "Rice", "Sugarcane"]
            },
            "punjab_india": {
                "name": "Punjab, India (Breadbasket)",
                "latitude": 30.7333,
                "longitude": 76.7794,
                "typical_crops": ["Wheat", "Rice", "Cotton"]
            },
            "maharashtra_india": {
                "name": "Maharashtra, India",
                "latitude": 19.7515,
                "longitude": 75.7139,
                "typical_crops": ["Cotton", "Sugarcane", "Soybean"]
            },
            "iowa_usa": {
                "name": "Iowa, USA (Corn Belt)",
                "latitude": 41.8780,
                "longitude": -93.0977,
                "typical_crops": ["Corn", "Soybeans"]
            },
            "california_usa": {
                "name": "California, USA",
                "latitude": 36.7783,
                "longitude": -119.4179,
                "typical_crops": ["Almonds", "Grapes", "Tomatoes"]
            }
        },
        "usage": "Use these coordinates in your weather intelligence requests"
    }
