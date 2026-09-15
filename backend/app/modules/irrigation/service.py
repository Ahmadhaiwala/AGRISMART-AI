"""
Smart Irrigation service layer
Business logic for predicting whether irrigation is required (Bonus Module B).

LOGIC (published here for reproducibility -- rule-based, not a trained model):

  1. Look up (min_moisture, optimal_moisture) for the given crop + growth
     stage from MOISTURE_THRESHOLDS (falls back to a generic "default"
     profile for crops not in the table).

  2. Classify current soil_moisture_percent against that range:
       < min_moisture      -> "critical_deficit"
       < optimal_moisture  -> "moderate_deficit"
       >= optimal_moisture -> "adequate"

  3. Decide irrigation_required + urgency:
       critical_deficit  -> irrigate, urgency=high
                              UNLESS forecast_rain_mm_24h >= HEAVY_RAIN_MM_THRESHOLD,
                              in which case rain is expected to cover the
                              deficit -> delay, but urgency stays "high" so the
                              farmer keeps monitoring.
       moderate_deficit  -> irrigate, urgency=medium
                              UNLESS rain_probability_percent >= RAIN_PROB_DELAY_THRESHOLD
                              OR forecast_rain_mm_24h >= LIGHT_RAIN_MM_THRESHOLD,
                              in which case delay, urgency=low.
       adequate          -> no irrigation, urgency=none.

  4. recommended_water_liters = moisture_deficit_percent * WATER_FACTOR_L_PER_PERCENT_PER_SQM
                                  * area_sqm
     (0 whenever irrigation is not required, including when delayed for rain.)

Validation note: MOISTURE_THRESHOLDS is a heuristic table based on typical
published soil-moisture guidance per growth stage (higher water sensitivity
during flowering/fruiting than during the seedling stage, consistent across
common vegetable/fruit crops). It is a starting point for a rule-based demo,
not calibrated against real field sensor data -- see README limitations.
"""
import logging
from typing import Dict, List, Tuple

from app.modules.irrigation.schemas import GrowthStage, IrrigationInput

logger = logging.getLogger(__name__)

# Published thresholds -- change here only, nowhere else, to keep the logic reproducible.
# crop -> stage -> (min_moisture_percent, optimal_moisture_percent)
MOISTURE_THRESHOLDS: Dict[str, Dict[str, Tuple[float, float]]] = {
    "tomato":  {"seedling": (25, 35), "vegetative": (30, 45), "flowering": (35, 50), "fruiting": (30, 45)},
    "potato":  {"seedling": (25, 35), "vegetative": (30, 40), "flowering": (35, 45), "fruiting": (30, 40)},
    "corn":    {"seedling": (20, 30), "vegetative": (25, 40), "flowering": (35, 50), "fruiting": (30, 40)},
    "apple":   {"seedling": (25, 35), "vegetative": (25, 35), "flowering": (30, 40), "fruiting": (30, 40)},
    "grape":   {"seedling": (20, 30), "vegetative": (20, 30), "flowering": (25, 35), "fruiting": (20, 30)},
    "pepper":  {"seedling": (25, 35), "vegetative": (30, 40), "flowering": (35, 45), "fruiting": (30, 40)},
    "default": {"seedling": (25, 35), "vegetative": (28, 40), "flowering": (32, 45), "fruiting": (28, 40)},
}

HEAVY_RAIN_MM_THRESHOLD = 15.0   # expected to cover even a critical deficit
LIGHT_RAIN_MM_THRESHOLD = 5.0    # enough to cover a moderate deficit
RAIN_PROB_DELAY_THRESHOLD = 60.0  # % chance of rain, used alongside forecast mm

WATER_FACTOR_L_PER_PERCENT_PER_SQM = 0.5  # liters per 1% moisture deficit per sq. meter
HEAT_STRESS_TEMP_C = 35.0


def _thresholds_for(crop_type: str, stage: GrowthStage) -> Tuple[float, float]:
    crop_key = crop_type.strip().lower()
    stage_key = stage.value
    profile = MOISTURE_THRESHOLDS.get(crop_key, MOISTURE_THRESHOLDS["default"])
    return profile.get(stage_key, MOISTURE_THRESHOLDS["default"][stage_key])


class IrrigationService:
    """Service for predicting irrigation need (rule-based, documented above)."""

    def predict(self, data: IrrigationInput) -> dict:
        min_moisture, optimal_moisture = _thresholds_for(data.crop_type, data.growth_stage)
        reasons: List[str] = []

        if data.soil_moisture_percent < min_moisture:
            status = "critical_deficit"
        elif data.soil_moisture_percent < optimal_moisture:
            status = "moderate_deficit"
        else:
            status = "adequate"

        irrigation_required = False
        urgency = "none"
        rain_delay_applied = False

        if status == "critical_deficit":
            reasons.append(
                f"Soil moisture ({data.soil_moisture_percent}%) is below the critical threshold "
                f"({min_moisture}%) for {data.crop_type} at the {data.growth_stage.value} stage."
            )
            if data.forecast_rain_mm_24h >= HEAVY_RAIN_MM_THRESHOLD:
                irrigation_required = False
                urgency = "high"
                rain_delay_applied = True
                reasons.append(
                    f"Heavy rain expected ({data.forecast_rain_mm_24h}mm in 24h) -- likely to cover "
                    "the deficit, but keep monitoring since this is a critical shortfall."
                )
            else:
                irrigation_required = True
                urgency = "high"

        elif status == "moderate_deficit":
            reasons.append(
                f"Soil moisture ({data.soil_moisture_percent}%) is below the optimal range "
                f"({optimal_moisture}%) for {data.crop_type} at the {data.growth_stage.value} stage."
            )
            if (
                data.rain_probability_percent >= RAIN_PROB_DELAY_THRESHOLD
                or data.forecast_rain_mm_24h >= LIGHT_RAIN_MM_THRESHOLD
            ):
                irrigation_required = False
                urgency = "low"
                rain_delay_applied = True
                reasons.append(
                    f"Rain likely in the next 24h ({data.rain_probability_percent}% chance, "
                    f"{data.forecast_rain_mm_24h}mm forecast) -- delaying irrigation."
                )
            else:
                irrigation_required = True
                urgency = "medium"

        else:
            reasons.append(
                f"Soil moisture ({data.soil_moisture_percent}%) is at or above the optimal level "
                f"({optimal_moisture}%) for {data.crop_type} at the {data.growth_stage.value} stage."
            )

        if irrigation_required and data.temperature_c is not None and data.temperature_c >= HEAT_STRESS_TEMP_C:
            reasons.append(
                f"High temperature ({data.temperature_c}\u00b0C) increases evapotranspiration -- "
                "irrigate promptly to avoid heat stress."
            )

        deficit_percent = max(0.0, optimal_moisture - data.soil_moisture_percent)
        recommended_water_liters = 0.0
        if irrigation_required:
            recommended_water_liters = round(
                deficit_percent * WATER_FACTOR_L_PER_PERCENT_PER_SQM * data.area_sqm, 1
            )

        if not reasons:
            reasons.append("No irrigation needed at this time.")

        return {
            "success": True,
            "decision": {
                "irrigation_required": irrigation_required,
                "urgency": urgency,
                "soil_moisture_status": status,
                "recommended_water_liters": recommended_water_liters,
                "rain_delay_applied": rain_delay_applied,
            },
            "reasons": reasons,
        }


# Global service instance
irrigation_service = IrrigationService()
