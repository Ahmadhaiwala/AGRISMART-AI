"""
Sustainability score router
Handles HTTP requests for the sustainability score (Bonus Module D).
"""
import logging
from fastapi import APIRouter, HTTPException

from app.modules.sustainability.schemas import SustainabilityInput, SustainabilityScoreResponse
from app.modules.sustainability.service import sustainability_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sustainability/score", response_model=SustainabilityScoreResponse)
async def compute_sustainability_score(data: SustainabilityInput) -> SustainabilityScoreResponse:
    """
    Compute a sustainability score (0-100) from water efficiency,
    resource use, and crop health, plus improvement suggestions.
    """
    try:
        result = sustainability_service.compute(data)
        return result
    except Exception as e:
        logger.error(f"Error computing sustainability score: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to compute sustainability score")
