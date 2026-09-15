"""
Sustainability score router
Handles HTTP requests for the sustainability score (Bonus Module).
"""
import logging
from fastapi import APIRouter, HTTPException

from app.modules.sustainability.schemas import (
    SustainabilityInput, 
    SustainabilityScoreResponse,
    IntegratedSustainabilityInput,
    IntegratedSustainabilityResponse
)
from app.modules.sustainability.service import sustainability_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sustainability/score", response_model=SustainabilityScoreResponse)
async def compute_sustainability_score(data: SustainabilityInput) -> SustainabilityScoreResponse:
    """
    Compute a sustainability score (0-100) from water efficiency,
    resource use, and crop health, plus improvement suggestions.
    
    **Manual Input Mode**: Provide all values manually
    """
    try:
        result = sustainability_service.compute(data)
        return result
    except Exception as e:
        logger.error(f"Error computing sustainability score: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to compute sustainability score")


@router.post("/sustainability/score/integrated", response_model=IntegratedSustainabilityResponse)
async def compute_integrated_sustainability_score(
    data: IntegratedSustainabilityInput
) -> IntegratedSustainabilityResponse:
    """
    **INTEGRATED MODE**: Compute sustainability score with automatic data gathering
    from all modules:
    
    - **Smart Irrigation (Module C)**: Calculates water requirements based on soil, 
      weather, and crop conditions
    - **Weather Intelligence (Module D)**: Provides weather-based recommendations
      for irrigation and disease management
    - **Disease Detection (Module A)**: Uses disease detection results for crop health
    
    This endpoint automatically calls other modules to gather the required data,
    then computes a comprehensive sustainability score.
    
    **Example Request**:
    ```json
    {
      "farm_id": "farm_001",
      "crop_name": "Tomato",
      "growth_stage": "Flowering",
      "soil_moisture": 35,
      "soil_type": "Loamy",
      "latitude": 28.6139,
      "longitude": 77.2090,
      "temperature": 28,
      "humidity": 65,
      "disease_detected": "Early Blight",
      "disease_confidence": 0.91,
      "is_healthy": false,
      "water_used_liters": 1200,
      "fertilizer_used_kg": 5,
      "pesticide_used_kg": 0.5,
      "pesticide_recommended_kg": 0.3
    }
    ```
    
    **Response includes**:
    - Overall sustainability score and grade
    - Sub-scores for water, resources, and health
    - Suggestions for improvement
    - Details from each integrated module
    """
    try:
        result = await sustainability_service.compute_integrated(data)
        return result
    except Exception as e:
        logger.error(f"Error computing integrated sustainability score: {str(e)}")
        logger.exception(e)
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to compute integrated sustainability score: {str(e)}"
        )


@router.get("/sustainability/info")
async def get_sustainability_info():
    """
    Get information about the sustainability scoring system
    """
    return {
        "formula_version": "1.0",
        "weights": {
            "water_efficiency": 0.4,
            "resource_use": 0.3,
            "crop_health": 0.3
        },
        "grade_bands": {
            "A": "80-100",
            "B": "60-79",
            "C": "40-59",
            "D": "0-39"
        },
        "integrated_modules": [
            "Smart Irrigation (Module C) - Water requirements",
            "Weather Intelligence (Module D) - Weather recommendations",
            "Disease Detection (Module A) - Crop health"
        ],
        "endpoints": {
            "manual": "/api/v1/sustainability/score",
            "integrated": "/api/v1/sustainability/score/integrated"
        }
    }
