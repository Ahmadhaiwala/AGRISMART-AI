"""
API routes for smart irrigation
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from .schemas import (
    IrrigationRequest,
    IrrigationResponse,
    IrrigationHealthResponse,
    CropType,
    SoilType,
    SeedlingStage
)
from .service import SmartIrrigationService, get_irrigation_service


router = APIRouter()


@router.post(
    "/irrigation/predict",
    response_model=IrrigationResponse,
    summary="Predict irrigation requirements",
    description="Get irrigation recommendations based on crop type, soil, growth stage, and environmental conditions"
)
async def predict_irrigation(
    request: IrrigationRequest,
    service: SmartIrrigationService = Depends(get_irrigation_service)
) -> IrrigationResponse:
    """
    Predict irrigation requirements based on:
    - Crop type and growth stage
    - Soil type and moisture level (MOI)
    - Temperature and humidity
    
    Returns irrigation level (None/Medium/High) with confidence and recommendations.
    """
    try:
        if not service.is_loaded():
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please wait for initialization or contact administrator."
            )
        
        # Get irrigation prediction
        response = service.predict_irrigation(request)
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during prediction: {str(e)}"
        )


@router.get(
    "/irrigation/health",
    summary="Check smart irrigation service health",
    response_model=IrrigationHealthResponse
)
async def health_check(
    service: SmartIrrigationService = Depends(get_irrigation_service)
) -> IrrigationHealthResponse:
    """
    Check if the smart irrigation model is loaded and ready
    """
    is_loaded = service.is_loaded()
    
    if is_loaded:
        return IrrigationHealthResponse(
            status="healthy",
            model_loaded=True,
            model_accuracy=service.metadata['metrics']['test_accuracy'],
            supported_crops=[crop.value for crop in CropType],
            supported_soil_types=[soil.value for soil in SoilType],
            supported_stages=[stage.value for stage in SeedlingStage]
        )
    else:
        return IrrigationHealthResponse(
            status="unhealthy",
            model_loaded=False,
            model_accuracy=None,
            supported_crops=[],
            supported_soil_types=[],
            supported_stages=[]
        )


@router.get(
    "/irrigation/info",
    summary="Get irrigation system information",
    response_model=Dict[str, Any]
)
async def get_info(
    service: SmartIrrigationService = Depends(get_irrigation_service)
) -> Dict[str, Any]:
    """
    Get detailed information about the irrigation prediction system
    """
    if not service.is_loaded():
        return {
            "status": "Model not loaded",
            "available": False
        }
    
    return {
        "status": "operational",
        "available": True,
        "model_type": "RandomForest Classifier",
        "features": service.feature_names,
        "supported_crops": [crop.value for crop in CropType],
        "supported_soil_types": [soil.value for soil in SoilType],
        "growth_stages": [stage.value for stage in SeedlingStage],
        "irrigation_levels": {
            "0": "No Irrigation Needed",
            "1": "Medium Irrigation Required (15 L/m²)",
            "2": "High Irrigation Required (30 L/m²)"
        },
        "metrics": {
            "test_accuracy": service.metadata['metrics']['test_accuracy'],
            "cv_accuracy": service.metadata['metrics']['cv_accuracy_mean'],
            "f1_weighted": service.metadata['metrics']['test_f1_weighted']
        },
        "feature_importance": {
            "primary": "Moisture (MOI)",
            "secondary": ["Temperature", "Humidity"],
            "contextual": ["Seedling Stage", "Crop Type", "Soil Type"]
        }
    }
