"""
Pydantic schemas for Farmer Assistant
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    HINDI = "hi"
    GUJARATI = "gu"


class ChatRequest(BaseModel):
    """Request for farmer assistant chat"""
    farm_id: str = Field(..., description="Farm identifier")
    message: str = Field(..., min_length=1, max_length=500, description="Farmer's question")
    language: Language = Field(default=Language.ENGLISH, description="Response language")
    
    # Optional context overrides (if not fetched from modules)
    crop_name: Optional[str] = Field(None, description="Current crop")
    growth_stage: Optional[str] = Field(None, description="Growth stage")
    soil_moisture: Optional[int] = Field(None, ge=0, le=100, description="Soil moisture %")
    
    class Config:
        json_schema_extra = {
            "example": {
                "farm_id": "farm_001",
                "message": "Should I irrigate my tomato crop today?",
                "language": "en",
                "crop_name": "Tomato",
                "soil_moisture": 28
            }
        }


class ChatResponse(BaseModel):
    """Response from farmer assistant"""
    answer: str = Field(..., description="Grounded answer to farmer's question")
    language: str = Field(..., description="Language of the response")
    grounded: bool = Field(..., description="Whether answer is grounded in farm data")
    context_used: Optional[dict] = Field(None, description="Farm context used for grounding")
    warning: Optional[str] = Field(None, description="Warning if data is incomplete")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "You should not irrigate today because the soil moisture is sufficient and there is a high chance of rain.",
                "language": "en",
                "grounded": True,
                "context_used": {
                    "soil_moisture": 28,
                    "rain_probability": 85
                }
            }
        }
