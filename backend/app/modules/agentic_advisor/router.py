"""
API routes for Agentic Advisor
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any

from .schemas import AgentExecutionResponse, AgentStatusResponse
from .agent import AgenticAdvisor, get_agent


router = APIRouter()


@router.post(
    "/agent/run/{farm_id}",
    response_model=AgentExecutionResponse,
    summary="Manually execute agent for a farm",
    description="Run the complete agent loop: OBSERVE → ANALYZE → DECIDE → ACT → NOTIFY"
)
async def run_agent(
    farm_id: str,
    context: Dict[str, Any] = Body(
        default={},
        example={
            "crop_name": "Tomato",
            "growth_stage": "Flowering",
            "soil_moisture": 28,
            "soil_type": "Loamy",
            "temperature": 31,
            "humidity": 78,
            "rain_probability": 85,
            "rain_amount": 12,
            "irrigation_required": False,
            "disease_detected": "Early Blight",
            "disease_confidence": 0.91,
            "is_healthy": False
        }
    ),
    agent: AgenticAdvisor = Depends(get_agent)
) -> AgentExecutionResponse:
    """
    Execute agent decision loop for a farm
    
    **Agent Flow**:
    1. **OBSERVE**: Collect farm context
    2. **ANALYZE**: Evaluate using deterministic rules
    3. **DECIDE**: Determine required action
    4. **ACT**: Generate farmer-friendly message (LLM)
    5. **NOTIFY**: Create/send notification
    
    **Decision Rules (Deterministic)**:
    - Skip irrigation if rain probability > 70%
    - Urgent irrigation if soil moisture < 25% and no rain
    - Disease treatment if confidence > 80%
    - Harvest ready if mature stage and low rain
    
    **LLM Role**: Only generates farmer-friendly explanations
    
    **Example Request**:
    ```
    POST /api/agent/run/farm_001
    {
        "soil_moisture": 28,
        "rain_probability": 85,
        "irrigation_required": false
    }
    ```
    """
    try:
        response = agent.run(farm_id=farm_id, **context)
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )


@router.get(
    "/agent/status/{farm_id}",
    response_model=AgentStatusResponse,
    summary="Get agent status for a farm",
    description="Retrieve the latest agent decision/recommendation"
)
async def get_agent_status(
    farm_id: str,
    agent: AgenticAdvisor = Depends(get_agent)
) -> AgentStatusResponse:
    """
    Get latest agent recommendation for a farm
    
    Returns the most recent decision and notification if available.
    """
    try:
        status = agent.get_status(farm_id)
        return status
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get agent status: {str(e)}"
        )
