"""
Smart Irrigation router
Handles HTTP requests for irrigation prediction (Bonus Module B).
"""
import logging
from fastapi import APIRouter, HTTPException

from app.modules.irrigation.schemas import IrrigationInput, IrrigationResponse
from app.modules.irrigation.service import irrigation_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/irrigation/predict", response_model=IrrigationResponse)
async def predict_irrigation(data: IrrigationInput) -> IrrigationResponse:
    """
    Predict whether irrigation is required right now from soil moisture,
    weather forecast, crop type, and growth stage, plus a recommended
    water volume and the reasons behind the decision.
    """
    try:
        result = irrigation_service.predict(data)
        return result
    except Exception as e:
        logger.error(f"Error predicting irrigation need: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to predict irrigation need")
