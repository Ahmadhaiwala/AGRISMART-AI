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
"""
import logging
from typing import List

from app.modules.sustainability.schemas import SustainabilityInput, SubScores

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
        water_efficiency = _efficiency(data.water_used_liters, data.water_required_liters)

        fertilizer_efficiency = _efficiency(data.fertilizer_used_kg, data.fertilizer_recommended_kg)
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
        suggestions = self._suggestions(data, water_efficiency, resource_use, crop_health)

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
    def _suggestions(data: SustainabilityInput, water_eff: float, resource_use: float, crop_health: float) -> List[str]:
        tips: List[str] = []

        if water_eff < 70:
            if data.water_used_liters > data.water_required_liters:
                tips.append("You're over-watering relative to crop needs -- consider reducing irrigation volume or frequency to cut water waste.")
            else:
                tips.append("Water applied is below the crop's requirement -- consider increasing irrigation to avoid crop stress.")

        if resource_use < 70:
            if data.fertilizer_used_kg > data.fertilizer_recommended_kg:
                tips.append("Fertilizer use is above the recommended amount -- reducing it can lower cost and runoff without hurting yield.")
            elif data.fertilizer_used_kg < data.fertilizer_recommended_kg:
                tips.append("Fertilizer use is below the recommended amount -- crop may be under-nourished.")

        if crop_health < 70:
            tips.append("Disease detected with meaningful confidence -- apply the recommended precaution promptly to prevent spread.")

        if not tips:
            tips.append("Resource use and crop health are both in good shape -- maintain current practices.")

        return tips


# Global service instance
sustainability_service = SustainabilityService()
