"""
Agentic Advisor - Autonomous farming advisor
OBSERVE → ANALYZE → DECIDE → ACT → NOTIFY
"""

import logging
from typing import Dict, Optional

from core.llm_client import llm_client
from core.farm_context import FarmContext, create_farm_context
from .schemas import AgentDecision, AgentAction, AgentExecutionResponse, AgentStatusResponse
from .rules import AgentRules
from .notifier import notifier

logger = logging.getLogger(__name__)


class AgenticAdvisor:
    """
    Autonomous agricultural advisor
    
    Flow:
    1. OBSERVE: Collect farm context from existing modules
    2. ANALYZE: Evaluate context using deterministic rules
    3. DECIDE: Determine if action is required (rules-based)
    4. ACT: Generate farmer-friendly message (LLM)
    5. NOTIFY: Send/store notification
    """
    
    def __init__(self):
        self.llm = llm_client
        self.rules = AgentRules()
    
    def _observe(self, farm_id: str, **context_data) -> FarmContext:
        """
        STEP 1: OBSERVE
        Collect current farm context from existing modules
        
        In production, this would call:
        - smart_irrigation service
        - smart_weather_based_Intelligence service
        - disease_detection service
        - crop_recommendation service
        """
        context = create_farm_context(farm_id=farm_id, **context_data)
        return context
    
    def _analyze_and_decide(self, context: FarmContext) -> AgentDecision:
        """
        STEP 2-3: ANALYZE & DECIDE
        Use deterministic rules to make decision
        
        IMPORTANT: LLM does NOT make decisions here
        Rules are authoritative
        """
        ctx = context.get_context()
        
        # Apply deterministic rules
        action, reason, priority = self.rules.decide(ctx)
        
        decision = AgentDecision(
            farm_id=context.farm_id,
            action=action,
            reason=reason,
            priority=priority,
            context=ctx
        )
        
        logger.info(f"Decision for {context.farm_id}: {action.value} ({priority})")
        return decision
    
    def _generate_message(self, decision: AgentDecision) -> Optional[str]:
        """
        STEP 4: ACT (Generate message)
        Use LLM to create farmer-friendly explanation
        
        The LLM explains the decision - it does NOT change it
        """
        if decision.action == AgentAction.NO_ACTION:
            return None
        
        # Create system prompt for message generation
        system_prompt = """You are an agricultural advisor explaining a farming decision.
Create a brief, friendly message (1-2 sentences) for farmers.
Use simple language and one relevant emoji.
DO NOT change the decision - only explain it."""
        
        user_message = f"""Decision: {decision.action.value}
Reason: {decision.reason}
Priority: {decision.priority}

Create a farmer-friendly message explaining this decision."""
        
        try:
            message = self.llm.chat(
                system_prompt=system_prompt,
                user_message=user_message,
                temperature=0.7,
                max_tokens=150
            )
            
            if message:
                return message
        except Exception as e:
            logger.error(f"LLM failed to generate message: {e}")
        
        # Fallback messages if LLM fails
        fallback_messages = {
            AgentAction.SKIP_IRRIGATION: "💧 Skip irrigation today - rain is expected and soil moisture is adequate.",
            AgentAction.IRRIGATE_NOW: "💧 Irrigate your crop now - soil moisture is low and no rain is forecast.",
            AgentAction.IRRIGATE_SOON: "💧 Plan to irrigate soon - soil moisture is getting low.",
            AgentAction.DISEASE_MONITORING: "🦠 Monitor your crop closely - disease symptoms detected.",
            AgentAction.DISEASE_TREATMENT: "🦠 Disease treatment needed urgently - high confidence detection.",
            AgentAction.FERTILIZE: "🌱 Good time to apply fertilizer - weather conditions are suitable.",
            AgentAction.HARVEST_READY: "🌾 Consider harvesting soon - crop is mature and weather is good.",
        }
        
        return fallback_messages.get(
            decision.action,
            f"Action recommended: {decision.action.value}"
        )
    
    def _notify(self, decision: AgentDecision, message: Optional[str]) -> bool:
        """
        STEP 5: NOTIFY
        Create and send notification
        """
        if decision.action == AgentAction.NO_ACTION or not message:
            return False
        
        try:
            notifier.create_notification(
                farm_id=decision.farm_id,
                action=decision.action,
                message=message,
                priority=decision.priority
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create notification: {e}")
            return False
    
    def run(self, farm_id: str, **context_data) -> AgentExecutionResponse:
        """
        Execute complete agent loop for a farm
        
        Args:
            farm_id: Farm identifier
            **context_data: Farm context data (crop, soil, weather, etc.)
            
        Returns:
            AgentExecutionResponse with decision and notification status
        """
        try:
            # Step 1: OBSERVE
            context = self._observe(farm_id, **context_data)
            
            # Step 2-3: ANALYZE & DECIDE
            decision = self._analyze_and_decide(context)
            
            # Step 4: ACT (Generate message)
            message = self._generate_message(decision)
            
            # Step 5: NOTIFY
            notification_created = self._notify(decision, message)
            
            return AgentExecutionResponse(
                farm_id=farm_id,
                action=decision.action,
                reason=decision.reason,
                message=message,
                notification_created=notification_created,
                priority=decision.priority
            )
            
        except Exception as e:
            logger.error(f"Agent execution failed for {farm_id}: {e}")
            raise
    
    def get_status(self, farm_id: str) -> AgentStatusResponse:
        """
        Get latest agent status for a farm
        
        Args:
            farm_id: Farm identifier
            
        Returns:
            AgentStatusResponse with latest recommendation
        """
        latest_notification = notifier.get_latest_notification(farm_id)
        
        if latest_notification:
            return AgentStatusResponse(
                farm_id=farm_id,
                has_recommendation=True,
                latest_action=latest_notification.action,
                latest_message=latest_notification.message,
                latest_timestamp=latest_notification.created_at,
                priority=latest_notification.priority
            )
        else:
            return AgentStatusResponse(
                farm_id=farm_id,
                has_recommendation=False
            )


# Global agent instance
agent = AgenticAdvisor()


def get_agent() -> AgenticAdvisor:
    """Dependency to get the agent"""
    return agent
