"""
Disease detection schemas
Pydantic models for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DiseaseBase(BaseModel):
    """Base disease schema"""
    disease_name: str
    confidence: float


class DiseasePredictionRequest(BaseModel):
    """Request schema for disease prediction"""
    image_url: Optional[str] = None
    threshold: float = 0.5


class DiseasePredictionResponse(BaseModel):
    """Response schema for disease prediction"""
    success: bool
    message: str
    predictions: Optional[List[DiseaseBase]] = None
    timestamp: datetime


class DiseaseInfo(BaseModel):
    """Disease information schema"""
    id: int
    name: str
    description: Optional[str] = None
    treatment: Optional[str] = None
    
    class Config:
        from_attributes = True
