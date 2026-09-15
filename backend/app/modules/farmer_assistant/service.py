"""
Service layer for Farmer Assistant
Handles context building and LLM interaction
"""

import logging
from typing import Dict, Optional

from core.llm_client import llm_client
from core.farm_context import create_farm_context, FarmContext
from .schemas import ChatRequest, ChatResponse
from .prompts import get_system_prompt, get_user_message

logger = logging.getLogger(__name__)


class FarmerAssistantService:
    """
    Farmer Assistant Service
    
    Responsibilities:
    1. Build farm context from existing modules
    2. Ground farmer questions in real farm data
    3. Generate multilingual responses via LLM
    """
    
    def __init__(self):
        self.llm = llm_client
    
    def _build_context(self, request: ChatRequest) -> FarmContext:
        """
        Build farm context
        
        In a real implementation, this would call existing module services:
        - smart_irrigation.service.irrigation_service
        - smart_weather_based_Intelligence.service.weather_intelligence_service
        - disease_detection.service
        - crop_recommendation.service
        
        For now, it uses provided context or defaults
        """
        context = create_farm_context(
            farm_id=request.farm_id,
            crop_name=request.crop_name,
            growth_stage=request.growth_stage,
            soil_moisture=request.soil_moisture
        )
        
        # In production, you would fetch data from other modules here:
        # Example:
        # if request.crop_name and request.soil_moisture is not None:
        #     irrigation_result = irrigation_service.predict_irrigation(...)
        #     context.add_irrigation_recommendation(
        #         required=irrigation_result.recommendation.level_code > 0,
        #         level=irrigation_result.recommendation.level,
        #         reason=irrigation_result.moisture_status
        #     )
        
        return context
    
    def _check_context_completeness(self, context: FarmContext) -> Optional[str]:
        """Check if context has sufficient information"""
        ctx = context.get_context()
        
        warnings = []
        
        if "crop" not in ctx:
            warnings.append("crop information")
        if "soil" not in ctx:
            warnings.append("soil data")
        if "weather" not in ctx:
            warnings.append("weather forecast")
        
        if warnings:
            return f"Limited data available: missing {', '.join(warnings)}"
        
        return None
    
    def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process farmer's question and return grounded answer
        
        Args:
            request: ChatRequest with farmer's question
            
        Returns:
            ChatResponse with grounded answer
        """
        # Build context from existing modules
        context = self._build_context(request)
        warning = self._check_context_completeness(context)
        
        # Convert context to text
        context_text = context.to_text()
        
        # Get system prompt in requested language
        system_prompt = get_system_prompt(request.language.value, context_text)
        
        # Format user message
        user_message = get_user_message(request.message, request.language.value)
        
        # Call LLM
        try:
            answer = self.llm.chat(
                system_prompt=system_prompt,
                user_message=user_message,
                temperature=0.7,
                max_tokens=500
            )
            
            if answer is None:
                # Fallback if LLM fails
                if request.language.value == "hi":
                    answer = "क्षमा करें, मैं अभी आपकी मदद नहीं कर सकता। कृपया बाद में पुनः प्रयास करें।"
                elif request.language.value == "gu":
                    answer = "માફ કરશો, હું અત્યારે મદદ કરી શકતો નથી। કૃપા કરીને પછીથી ફરી પ્રયાસ કરો।"
                else:
                    answer = "I'm sorry, I cannot assist you right now. Please try again later."
                
                grounded = False
            else:
                grounded = True
        
        except Exception as e:
            logger.error(f"Error in farmer assistant chat: {e}")
            answer = "An error occurred. Please try again."
            grounded = False
        
        return ChatResponse(
            answer=answer,
            language=request.language.value,
            grounded=grounded,
            context_used=context.get_context() if grounded else None,
            warning=warning
        )


# Global service instance
farmer_assistant_service = FarmerAssistantService()


def get_farmer_assistant_service() -> FarmerAssistantService:
    """Dependency to get the farmer assistant service"""
    return farmer_assistant_service
