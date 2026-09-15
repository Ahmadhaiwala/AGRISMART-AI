"""
Deterministic decision rules for Agentic Advisor
The LLM does NOT make these decisions - it only explains them
"""

from typing import Dict, Optional, Tuple
from .schemas import AgentAction


class AgentRules:
    """
    Deterministic rule engine for agricultural decisions
    
    IMPORTANT: These rules are authoritative
    The LLM only generates farmer-friendly explanations
    """
    
    @staticmethod
    def evaluate_irrigation(context: Dict) -> Tuple[Optional[AgentAction], Optional[str], str]:
        """
        Evaluate if irrigation action is needed
        
        Returns:
            (action, reason, priority)
        """
        irrigation = context.get("irrigation", {})
        weather = context.get("weather", {})
        soil = context.get("soil", {})
        
        irrigation_required = irrigation.get("required")
        rain_probability = weather.get("rain_probability", 0)
        rain_amount = weather.get("rain_amount", 0)
        soil_moisture = soil.get("moisture")
        
        # Rule 1: Skip irrigation if rain is coming and irrigation not required
        if irrigation_required == False and rain_probability >= 70:
            return (
                AgentAction.SKIP_IRRIGATION,
                f"Rain probability is {rain_probability}% and irrigation model says irrigation is not required",
                "HIGH"
            )
        
        # Rule 2: Skip irrigation if heavy rain expected
        if rain_amount >= 10:
            return (
                AgentAction.SKIP_IRRIGATION,
                f"Heavy rain expected ({rain_amount}mm), irrigation not needed",
                "HIGH"
            )
        
        # Rule 3: Urgent irrigation if critical moisture and no rain
        if soil_moisture is not None and soil_moisture < 25 and rain_probability < 30:
            return (
                AgentAction.IRRIGATE_NOW,
                f"Critical soil moisture ({soil_moisture}%) and no rain forecast",
                "CRITICAL"
            )
        
        # Rule 4: Irrigate soon if required and low rain chance
        if irrigation_required == True and rain_probability < 40:
            return (
                AgentAction.IRRIGATE_SOON,
                f"Irrigation required and low rain probability ({rain_probability}%)",
                "MEDIUM"
            )
        
        # Rule 5: Irrigate now if very low moisture
        if soil_moisture is not None and soil_moisture < 30:
            return (
                AgentAction.IRRIGATE_SOON,
                f"Low soil moisture ({soil_moisture}%)",
                "MEDIUM"
            )
        
        return (None, None, "LOW")
    
    @staticmethod
    def evaluate_disease(context: Dict) -> Tuple[Optional[AgentAction], Optional[str], str]:
        """
        Evaluate if disease action is needed
        
        Returns:
            (action, reason, priority)
        """
        disease = context.get("disease", {})
        
        if not disease:
            return (None, None, "LOW")
        
        confidence = disease.get("confidence", 0)
        detected = disease.get("detected")
        is_healthy = disease.get("is_healthy", True)
        
        # Rule 1: High confidence disease detection
        if not is_healthy and confidence >= 0.80:
            return (
                AgentAction.DISEASE_TREATMENT,
                f"Disease '{detected}' detected with {confidence:.0%} confidence",
                "CRITICAL"
            )
        
        # Rule 2: Medium confidence disease detection
        if not is_healthy and confidence >= 0.60:
            return (
                AgentAction.DISEASE_MONITORING,
                f"Possible disease '{detected}' detected with {confidence:.0%} confidence",
                "HIGH"
            )
        
        return (None, None, "LOW")
    
    @staticmethod
    def evaluate_harvest(context: Dict) -> Tuple[Optional[AgentAction], Optional[str], str]:
        """
        Evaluate if harvest action is needed
        
        Returns:
            (action, reason, priority)
        """
        crop = context.get("crop", {})
        weather = context.get("weather", {})
        
        growth_stage = crop.get("growth_stage", "").lower()
        rain_probability = weather.get("rain_probability", 0)
        
        # Rule: Ready for harvest with good weather
        if growth_stage in ["maturation", "harvest", "mature"] and rain_probability < 30:
            return (
                AgentAction.HARVEST_READY,
                f"Crop is in {growth_stage} stage and weather is suitable (low rain probability)",
                "HIGH"
            )
        
        return (None, None, "LOW")
    
    @staticmethod
    def evaluate_fertilization(context: Dict) -> Tuple[Optional[AgentAction], Optional[str], str]:
        """
        Evaluate if fertilization action is needed
        
        Returns:
            (action, reason, priority)
        """
        weather = context.get("weather", {})
        crop = context.get("crop", {})
        
        rain_probability = weather.get("rain_probability", 0)
        growth_stage = crop.get("growth_stage", "").lower()
        
        # Rule: Good time for fertilization (low rain, vegetative stage)
        if rain_probability < 30 and growth_stage in ["vegetative", "seedling"]:
            return (
                AgentAction.FERTILIZE,
                f"Low rain probability ({rain_probability}%) and crop in {growth_stage} stage - good time for fertilization",
                "MEDIUM"
            )
        
        return (None, None, "LOW")
    
    @staticmethod
    def decide(context: Dict) -> Tuple[AgentAction, str, str]:
        """
        Main decision function - evaluates all rules
        
        Returns:
            (action, reason, priority)
        """
        # Evaluate all rule categories
        decisions = [
            AgentRules.evaluate_disease(context),
            AgentRules.evaluate_irrigation(context),
            AgentRules.evaluate_harvest(context),
            AgentRules.evaluate_fertilization(context)
        ]
        
        # Filter out None decisions
        valid_decisions = [(a, r, p) for a, r, p in decisions if a is not None]
        
        if not valid_decisions:
            return (
                AgentAction.NO_ACTION,
                "All parameters are within normal range",
                "LOW"
            )
        
        # Priority order
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        
        # Sort by priority and return highest priority action
        valid_decisions.sort(key=lambda x: priority_order.get(x[2], 99))
        
        return valid_decisions[0]
