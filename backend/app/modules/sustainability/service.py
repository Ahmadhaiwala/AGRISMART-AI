"""
Sustainability score service layer
Business logic for computing the AgriSmart AI sustainability score.

FORMULA (published here for reproducibility -- see also SUSTAINABILITY_FORMULA.md):

    water_efficiency = 100 * (1 - |used - required| / required)      [clipped to 0-100]
    resource_use     = average(fertilizer_efficiency, pesticide_efficiency)
                        where each *_efficiency = 100 * (1 - |used - recommended| / recommended)
    crop_health       = 100                        if healthy
                       = 100 * (1 - disease_confidence)  if diseased

    overall_score = 0.4 * water_efficiency + 0.3 * resource_use + 0.3 * crop_health

    grade: A >= 80, B >= 60, C >= 40, D < 40

Both over-use and under-use are penalized for water/resources, since neither
extreme is sustainable (under-watering stresses the crop; over-watering wastes
a scarce resource).

INTEGRATION: Enhanced version integrates with all modules:
- Smart Irrigation (Module C): Gets water requirements
- Weather Intelligence (Module D): Gets weather-based recommendations
- Disease Detection (Module A): Gets crop health status
"""
import logging
from typing import List, Dict, Optional

from app.modules.sustainability.schemas import (
    SustainabilityInput, 
    IntegratedSustainabilityInput,
    SubScores
)

logger = logging.getLogger(__name__)

# Published weights -- change here only, nowhere else, to keep the formula reproducible.
WATER_WEIGHT = 0.4
RESOURCE_WEIGHT = 0.3
HEALTH_WEIGHT = 0.3


def _efficiency(used: float, required: float) -> float:
    """Shared efficiency formula: 100 when used == required, decaying as they diverge."""
    if required <= 0:
        return 100.0
    ratio = 1 - abs(used - required) / required
    return max(0.0, min(100.0, ratio * 100))


class SustainabilityService:
    """Service for computing the sustainability score."""

    def compute(self, data: SustainabilityInput) -> dict:
        """Original method: compute from manual inputs"""
        water_efficiency = _efficiency(data.water_used_liters, data.water_required_liters)

        fertilizer_efficiency = _efficiency(data.fertilizer_used_kg, data.fertilizer_recommended_kg)
        pesticide_efficiency = None
        if data.pesticide_recommended_kg > 0:
            pesticide_efficiency = _efficiency(data.pesticide_used_kg, data.pesticide_recommended_kg)
            resource_use = (fertilizer_efficiency + pesticide_efficiency) / 2
        else:
            resource_use = fertilizer_efficiency

        crop_health = 100.0 if data.is_healthy else max(0.0, 100 * (1 - data.disease_confidence))

        overall = (
            WATER_WEIGHT * water_efficiency
            + RESOURCE_WEIGHT * resource_use
            + HEALTH_WEIGHT * crop_health
        )
        overall = round(overall, 1)

        grade = self._grade(overall)
        suggestions = self._suggestions(
            data, water_efficiency, fertilizer_efficiency, pesticide_efficiency, crop_health
        )

        return {
            "success": True,
            "overall_score": overall,
            "grade": grade,
            "sub_scores": SubScores(
                water_efficiency=round(water_efficiency, 1),
                resource_use=round(resource_use, 1),
                crop_health=round(crop_health, 1),
            ),
            "suggestions": suggestions,
        }
    
    async def compute_integrated(self, data: IntegratedSustainabilityInput) -> dict:
        """
        Enhanced method: integrates with all modules to gather data automatically
        
        Calls:
        - Smart Irrigation: Get water requirements
        - Weather Intelligence: Get recommendations
        - Uses provided disease detection results
        """
        modules_used = []
        irrigation_recommendation = None
        weather_recommendation = None
        crop_health_details = None
        
        # 1. Get irrigation recommendation (water requirements)
        water_required_liters = 0
        fertilizer_recommended_kg = data.fertilizer_used_kg  # Default to what was used
        
        try:
            from app.modules.smart_irrigation.service import irrigation_service
            
            # Prepare irrigation prediction request
            irrigation_input = {
                "crop_id": self._get_crop_id(data.crop_name),
                "soil_type": data.soil_type,
                "seedling_stage": data.seedling_stage,
                "moi": data.soil_moisture,
                "temp": data.temperature,
                "humidity": data.humidity
            }
            
            # Get irrigation prediction
            irrigation_result = irrigation_service.predict(irrigation_input)
            
            if irrigation_result:
                modules_used.append("Smart Irrigation")
                irrigation_recommendation = irrigation_result
                
                # Calculate water requirements based on irrigation level
                # 0 = None (0 L), 1 = Medium (15 L/m²), 2 = High (30 L/m²)
                irrigation_level = irrigation_result.get("irrigation_required", 0)
                area_m2 = 100  # Assume 100 m² plot (can be parameterized)
                
                if irrigation_level == 0:
                    water_required_liters = 0
                elif irrigation_level == 1:
                    water_required_liters = 15 * area_m2
                else:  # level == 2
                    water_required_liters = 30 * area_m2
                
                # If no irrigation predicted but some was used, use the used amount as baseline
                if water_required_liters == 0 and data.water_used_liters > 0:
                    water_required_liters = data.water_used_liters
                elif water_required_liters == 0:
                    # Minimum baseline for calculation
                    water_required_liters = 500  # 500L minimum
                    
        except Exception as e:
            logger.warning(f"Could not get irrigation recommendation: {e}")
            # Fallback: use what was provided or default
            water_required_liters = data.water_used_liters if data.water_used_liters > 0 else 1000
        
        # 2. Get weather intelligence recommendation
        try:
            from app.modules.smart_weather_based_Intelligence.service import weather_intelligence_service
            
            weather_input = {
                "latitude": data.latitude,
                "longitude": data.longitude,
                "farm_conditions": {
                    "crop_type": data.crop_name,
                    "growth_stage": data.growth_stage,
                    "soil_moisture": data.soil_moisture,
                    "has_irrigation": data.has_irrigation,
                    "disease_detected": data.disease_detected is not None,
                    "recent_fertilization": False
                },
                "forecast_days": 7
            }
            
            weather_result = await weather_intelligence_service.get_weather_intelligence(weather_input)
            
            if weather_result.get("success"):
                modules_used.append("Weather Intelligence")
                weather_recommendation = {
                    "irrigation": weather_result.get("irrigation_recommendation"),
                    "disease_risk": weather_result.get("disease_risk_level"),
                    "recommended_actions": [
                        action.get("title") 
                        for action in weather_result.get("recommended_actions", [])
                    ]
                }
                
        except Exception as e:
            logger.warning(f"Could not get weather recommendation: {e}")
        
        # 3. Process disease detection results (from input)
        if data.disease_detected and data.disease_confidence:
            modules_used.append("Disease Detection")
            crop_health_details = {
                "disease": data.disease_detected,
                "confidence": data.disease_confidence,
                "is_healthy": data.is_healthy
            }
        
        # 4. Compute sustainability score
        # Estimate fertilizer recommendation (simplified - could be from crop recommendation module)
        if fertilizer_recommended_kg == 0:
            fertilizer_recommended_kg = data.fertilizer_used_kg * 0.9  # Assume 10% reduction is optimal
        
        # Create manual input for scoring
        score_input = SustainabilityInput(
            water_used_liters=data.water_used_liters,
            water_required_liters=water_required_liters,
            fertilizer_used_kg=data.fertilizer_used_kg,
            fertilizer_recommended_kg=fertilizer_recommended_kg,
            pesticide_used_kg=data.pesticide_used_kg,
            pesticide_recommended_kg=data.pesticide_recommended_kg,
            is_healthy=data.is_healthy,
            disease_confidence=data.disease_confidence if data.disease_confidence else 0.0
        )
        
        # Get base score
        result = self.compute(score_input)
        
        # Add integration details
        result["modules_used"] = modules_used
        result["irrigation_recommendation"] = irrigation_recommendation
        result["weather_recommendation"] = weather_recommendation
        result["crop_health_details"] = crop_health_details
        
        return result
    
    @staticmethod
    def _get_crop_id(crop_name: str) -> int:
        """Map crop name to crop ID for irrigation model"""
        crop_map = {
            "wheat": 0,
            "chilli": 1,
            "potato": 2,
            "carrot": 3,
            "tomato": 4
        }
        return crop_map.get(crop_name.lower(), 0)

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 80:
            return "A"
        if score >= 60:
            return "B"
        if score >= 40:
            return "C"
        return "D"

    @staticmethod
    def _suggestions(
        data: SustainabilityInput,
        water_eff: float,
        fertilizer_eff: float,
        pesticide_eff: float,
        crop_health: float,
    ) -> List[str]:
        tips: List[str] = []

        if water_eff < 70:
            if data.water_used_liters > data.water_required_liters:
                tips.append("You're over-watering relative to crop needs -- consider reducing irrigation volume or frequency to cut water waste.")
            else:
                tips.append("Water applied is below the crop's requirement -- consider increasing irrigation to avoid crop stress.")

        if fertilizer_eff < 70:
            if data.fertilizer_used_kg > data.fertilizer_recommended_kg:
                tips.append("Fertilizer use is above the recommended amount -- reducing it can lower cost and runoff without hurting yield.")
            elif data.fertilizer_used_kg < data.fertilizer_recommended_kg:
                tips.append("Fertilizer use is below the recommended amount -- crop may be under-nourished.")

        if pesticide_eff is not None and pesticide_eff < 70:
            if data.pesticide_used_kg > data.pesticide_recommended_kg:
                tips.append("Pesticide use is above the recommended amount -- reducing it can lower cost, protect beneficial insects, and cut chemical runoff.")
            elif data.pesticide_used_kg < data.pesticide_recommended_kg:
                tips.append("Pesticide use is below the recommended amount -- pest pressure may go unchecked.")

        if crop_health < 70:
            tips.append("Disease detected with meaningful confidence -- apply the recommended precaution promptly to prevent spread.")

        if not tips:
            tips.append("Resource use and crop health are both in good shape -- maintain current practices.")

        return tips


# Global service instance
sustainability_service = SustainabilityService()
