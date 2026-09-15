"""
API routes for crop recommendation
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from .schemas import CropRecommendationRequest, CropRecommendationResponse
from .service import CropRecommendationService, get_crop_service


router = APIRouter()


@router.post(
    "/test/crop_recommendation",
    response_model=CropRecommendationResponse,
    summary="Get crop recommendation",
    description="Recommend the best crop based on environmental and soil conditions"
)
async def recommend_crop(
    request: CropRecommendationRequest,
    service: CropRecommendationService = Depends(get_crop_service)
) -> CropRecommendationResponse:
    """
    Recommend crops based on:
    - Soil type and pH
    - Temperature and humidity
    - Water availability
    - NPK (Nitrogen, Phosphorus, Potassium) levels
    - Season and crop type category
    
    Returns top recommended crop with confidence scores for top 5 options.
    """
    try:
        if not service.is_loaded():
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please wait for initialization or contact administrator."
            )
        
        # Get crop recommendation
        response = service.recommend_crop(request)
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
    "/test/crop_recommendation/health",
    summary="Check crop recommendation service health",
    response_model=Dict[str, Any]
)
async def health_check(
    service: CropRecommendationService = Depends(get_crop_service)
) -> Dict[str, Any]:
    """
    Check if the crop recommendation model is loaded and ready
    """
    is_loaded = service.is_loaded()
    
    if is_loaded:
        return {
            "status": "healthy",
            "model_loaded": True,
            "num_features": len(service.feature_names),
            "num_classes": len(service.classes),
            "test_accuracy": service.metadata['metrics']['test_accuracy'],
            "data_leakage_fixed": service.metadata.get('data_leakage_fixed', False)
        }
    else:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "message": "Model not loaded yet"
        }
