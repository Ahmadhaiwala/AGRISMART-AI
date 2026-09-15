"""
API routes for Farmer Assistant
"""

from fastapi import APIRouter, HTTPException, Depends
from .schemas import ChatRequest, ChatResponse
from .service import FarmerAssistantService, get_farmer_assistant_service


router = APIRouter()


@router.post(
    "/assistant/chat",
    response_model=ChatResponse,
    summary="Chat with Farmer Assistant",
    description="Ask agricultural questions and get grounded, multilingual advice"
)
async def chat(
    request: ChatRequest,
    service: FarmerAssistantService = Depends(get_farmer_assistant_service)
) -> ChatResponse:
    """
    Chat with the Farmer Assistant
    
    **Features**:
    - Grounded in real farm data (never invents information)
    - Multilingual support (English, Hindi, Gujarati)
    - Explains existing module recommendations
    - Farmer-friendly language
    
    **Example Questions**:
    - "Should I irrigate my tomato crop today?"
    - "क्या मुझे आज सिंचाई करनी चाहिए?" (Hindi)
    - "આજે પાણી આપવું જોઈએ?" (Gujarati)
    """
    try:
        response = service.chat(request)
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )
