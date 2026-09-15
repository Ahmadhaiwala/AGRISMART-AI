"""
Farm context builder - gathers information from existing modules
Shared by Farmer Assistant and Agentic Advisor
"""

from typing import Dict, Optional, Any
from datetime import datetime


class FarmContext:
    """
    Builds farm context by collecting data from existing modules
    This does NOT duplicate module logic - it calls their services
    """
    
    def __init__(self, farm_id: str):
        self.farm_id = farm_id
        self.context: Dict[str, Any] = {
            "farm_id": farm_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def add_crop_info(self, crop_name: Optional[str] = None, growth_stage: Optional[str] = None):
        """Add crop information"""
        if crop_name or growth_stage:
            self.context["crop"] = {}
            if crop_name:
                self.context["crop"]["name"] = crop_name
            if growth_stage:
                self.context["crop"]["growth_stage"] = growth_stage
    
    def add_soil_info(self, moisture: Optional[int] = None, soil_type: Optional[str] = None):
        """Add soil information"""
        if moisture is not None or soil_type:
            self.context["soil"] = {}
            if moisture is not None:
                self.context["soil"]["moisture"] = moisture
            if soil_type:
                self.context["soil"]["type"] = soil_type
    
    def add_weather_info(
        self,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None,
        rain_probability: Optional[float] = None,
        rain_amount: Optional[float] = None
    ):
        """Add weather information"""
        weather = {}
        if temperature is not None:
            weather["temperature"] = temperature
        if humidity is not None:
            weather["humidity"] = humidity
        if rain_probability is not None:
            weather["rain_probability"] = rain_probability
        if rain_amount is not None:
            weather["rain_amount"] = rain_amount
        
        if weather:
            self.context["weather"] = weather
    
    def add_irrigation_recommendation(
        self,
        required: Optional[bool] = None,
        level: Optional[str] = None,
        reason: Optional[str] = None,
        water_amount: Optional[float] = None
    ):
        """Add irrigation recommendation from smart_irrigation module"""
        irrigation = {}
        if required is not None:
            irrigation["required"] = required
        if level:
            irrigation["level"] = level
        if reason:
            irrigation["reason"] = reason
        if water_amount is not None:
            irrigation["water_amount_liters"] = water_amount
        
        if irrigation:
            self.context["irrigation"] = irrigation
    
    def add_disease_detection(
        self,
        detected: Optional[str] = None,
        confidence: Optional[float] = None,
        is_healthy: Optional[bool] = None
    ):
        """Add disease detection results from disease_detection module"""
        disease = {}
        if detected:
            disease["detected"] = detected
        if confidence is not None:
            disease["confidence"] = confidence
        if is_healthy is not None:
            disease["is_healthy"] = is_healthy
        
        if disease:
            self.context["disease"] = disease
    
    def add_sustainability_score(
        self,
        score: Optional[float] = None,
        grade: Optional[str] = None
    ):
        """Add sustainability assessment from sustainability module"""
        if score is not None or grade:
            self.context["sustainability"] = {}
            if score is not None:
                self.context["sustainability"]["score"] = score
            if grade:
                self.context["sustainability"]["grade"] = grade
    
    def add_crop_recommendation(
        self,
        recommended_crop: Optional[str] = None,
        confidence: Optional[float] = None
    ):
        """Add crop recommendation from crop_recommendation module"""
        if recommended_crop or confidence is not None:
            self.context["crop_recommendation"] = {}
            if recommended_crop:
                self.context["crop_recommendation"]["crop"] = recommended_crop
            if confidence is not None:
                self.context["crop_recommendation"]["confidence"] = confidence
    
    def get_context(self) -> Dict[str, Any]:
        """Get the built context"""
        return self.context
    
    def to_text(self) -> str:
        """Convert context to human-readable text"""
        lines = [f"Farm ID: {self.farm_id}"]
        
        if "crop" in self.context:
            crop = self.context["crop"]
            lines.append(f"Crop: {crop.get('name', 'N/A')} ({crop.get('growth_stage', 'N/A')})")
        
        if "soil" in self.context:
            soil = self.context["soil"]
            lines.append(f"Soil: {soil.get('type', 'N/A')}, Moisture: {soil.get('moisture', 'N/A')}%")
        
        if "weather" in self.context:
            weather = self.context["weather"]
            temp = weather.get('temperature', 'N/A')
            humidity = weather.get('humidity', 'N/A')
            rain_prob = weather.get('rain_probability', 'N/A')
            lines.append(f"Weather: {temp}°C, {humidity}% humidity, {rain_prob}% rain probability")
        
        if "irrigation" in self.context:
            irrigation = self.context["irrigation"]
            required = irrigation.get('required', 'unknown')
            reason = irrigation.get('reason', 'No reason provided')
            lines.append(f"Irrigation: {'Required' if required else 'Not required'} - {reason}")
        
        if "disease" in self.context:
            disease = self.context["disease"]
            if disease.get('is_healthy'):
                lines.append("Disease: Crop is healthy")
            else:
                detected = disease.get('detected', 'Unknown')
                conf = disease.get('confidence', 0)
                lines.append(f"Disease: {detected} detected (confidence: {conf:.0%})")
        
        if "sustainability" in self.context:
            sust = self.context["sustainability"]
            lines.append(f"Sustainability: {sust.get('score', 'N/A')}/100 (Grade: {sust.get('grade', 'N/A')})")
        
        return "\n".join(lines)


def create_farm_context(farm_id: str, **kwargs) -> FarmContext:
    """
    Factory function to create a farm context
    
    Usage:
        context = create_farm_context(
            farm_id="farm_001",
            crop_name="Tomato",
            soil_moisture=28,
            temperature=31
        )
    """
    ctx = FarmContext(farm_id)
    
    # Add information based on provided kwargs
    if "crop_name" in kwargs or "growth_stage" in kwargs:
        ctx.add_crop_info(
            crop_name=kwargs.get("crop_name"),
            growth_stage=kwargs.get("growth_stage")
        )
    
    if "soil_moisture" in kwargs or "soil_type" in kwargs:
        ctx.add_soil_info(
            moisture=kwargs.get("soil_moisture"),
            soil_type=kwargs.get("soil_type")
        )
    
    if any(k in kwargs for k in ["temperature", "humidity", "rain_probability", "rain_amount"]):
        ctx.add_weather_info(
            temperature=kwargs.get("temperature"),
            humidity=kwargs.get("humidity"),
            rain_probability=kwargs.get("rain_probability"),
            rain_amount=kwargs.get("rain_amount")
        )
    
    if any(k in kwargs for k in ["irrigation_required", "irrigation_level", "irrigation_reason"]):
        ctx.add_irrigation_recommendation(
            required=kwargs.get("irrigation_required"),
            level=kwargs.get("irrigation_level"),
            reason=kwargs.get("irrigation_reason"),
            water_amount=kwargs.get("irrigation_water_amount")
        )
    
    if any(k in kwargs for k in ["disease_detected", "disease_confidence", "is_healthy"]):
        ctx.add_disease_detection(
            detected=kwargs.get("disease_detected"),
            confidence=kwargs.get("disease_confidence"),
            is_healthy=kwargs.get("is_healthy")
        )
    
    if "sustainability_score" in kwargs or "sustainability_grade" in kwargs:
        ctx.add_sustainability_score(
            score=kwargs.get("sustainability_score"),
            grade=kwargs.get("sustainability_grade")
        )
    
    if "recommended_crop" in kwargs or "recommendation_confidence" in kwargs:
        ctx.add_crop_recommendation(
            recommended_crop=kwargs.get("recommended_crop"),
            confidence=kwargs.get("recommendation_confidence")
        )
    
    return ctx
