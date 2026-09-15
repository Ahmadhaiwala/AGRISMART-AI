"""
Service layer for weather-based intelligence
Combines Open-Meteo weather data with farm conditions for actionable insights
"""

import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np

from .schemas import (
    WeatherIntelligenceRequest,
    WeatherIntelligenceResponse,
    WeatherSummary,
    Action,
    RiskAlert,
    ActionPriority,
    ActionCategory
)


class WeatherIntelligenceService:
    """
    Weather Data Source: Open-Meteo API (https://open-meteo.com/)
    
    A free, open-source weather API providing:
    - Historical, current, and forecast weather data
    - High accuracy global coverage
    - No API key required
    - Reliable and fast
    """
    
    def __init__(self):
        # Setup Open-Meteo API client with cache and retry
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.client = openmeteo_requests.Client(session=retry_session)
        self.forecast_url = "https://api.open-meteo.com/v1/forecast"
    
    def fetch_weather_data(
        self,
        latitude: float,
        longitude: float,
        forecast_days: int = 7
    ) -> Dict:
        """Fetch weather data from Open-Meteo API"""
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "weather_code"
            ],
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation_probability",
                "precipitation",
                "weather_code",
                "wind_speed_10m"
            ],
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max"
            ],
            "timezone": "auto",
            "forecast_days": forecast_days
        }
        
        responses = self.client.weather_api(self.forecast_url, params=params)
        response = responses[0]
        
        # Extract current weather
        current = response.Current()
        current_data = {
            "temperature": current.Variables(0).Value(),
            "humidity": current.Variables(1).Value(),
            "precipitation": current.Variables(2).Value(),
            "wind_speed": current.Variables(3).Value(),
            "weather_code": current.Variables(4).Value()
        }
        
        # Extract hourly forecast (next 24 hours)
        hourly = response.Hourly()
        hourly_data = {
            "temperature": hourly.Variables(0).ValuesAsNumpy()[:24],
            "humidity": hourly.Variables(1).ValuesAsNumpy()[:24],
            "precipitation_probability": hourly.Variables(2).ValuesAsNumpy()[:24],
            "precipitation": hourly.Variables(3).ValuesAsNumpy()[:24],
            "weather_code": hourly.Variables(4).ValuesAsNumpy()[:24],
            "wind_speed": hourly.Variables(5).ValuesAsNumpy()[:24]
        }
        
        # Extract daily forecast
        daily = response.Daily()
        daily_data = {
            "temp_max": daily.Variables(0).ValuesAsNumpy(),
            "temp_min": daily.Variables(1).ValuesAsNumpy(),
            "precipitation_sum": daily.Variables(2).ValuesAsNumpy(),
            "precipitation_probability": daily.Variables(3).ValuesAsNumpy(),
            "wind_speed_max": daily.Variables(4).ValuesAsNumpy()
        }
        
        return {
            "location": {
                "latitude": response.Latitude(),
                "longitude": response.Longitude(),
                "elevation": response.Elevation()
            },
            "current": current_data,
            "hourly": hourly_data,
            "daily": daily_data
        }
    
    def create_weather_summary(self, weather_data: Dict) -> WeatherSummary:
        """Create weather summary from raw data"""
        current = weather_data["current"]
        hourly = weather_data["hourly"]
        
        return WeatherSummary(
            current_temp=float(current["temperature"]),
            current_humidity=float(current["humidity"]),
            current_precipitation=float(current["precipitation"]),
            current_wind_speed=float(current["wind_speed"]),
            forecast_rain_probability=float(np.max(hourly["precipitation_probability"])),
            forecast_rain_amount=float(np.sum(hourly["precipitation"])),
            forecast_max_temp=float(np.max(hourly["temperature"])),
            forecast_min_temp=float(np.min(hourly["temperature"]))
        )
    
    def assess_irrigation_need(
        self,
        request: WeatherIntelligenceRequest,
        weather_summary: WeatherSummary
    ) -> Tuple[str, List[Action]]:
        """Rule-based irrigation assessment"""
        actions = []
        soil_moisture = request.farm_conditions.soil_moisture
        rain_prob = weather_summary.forecast_rain_probability
        rain_amount = weather_summary.forecast_rain_amount
        
        # Rule 1: Rain expected - delay irrigation
        if rain_prob > 60 and rain_amount > 5:
            recommendation = f"DELAY - Rain likely within 24 hours ({rain_prob:.0f}% chance, {rain_amount:.1f}mm expected)"
            actions.append(Action(
                category=ActionCategory.IRRIGATION,
                priority=ActionPriority.HIGH,
                title="Delay Irrigation - Rain Expected",
                description=f"Postpone irrigation for 24-48 hours. Forecast shows {rain_prob:.0f}% chance of {rain_amount:.1f}mm rain.",
                reasoning=f"Expected rainfall will provide natural irrigation and prevent waterlogging",
                timing="Wait until after rainfall, then reassess soil moisture"
            ))
        
        # Rule 2: Low moisture + no rain - irrigate urgently
        elif soil_moisture < 30 and rain_prob < 30:
            recommendation = f"IRRIGATE URGENTLY - Low moisture ({soil_moisture}%) and no rain expected"
            actions.append(Action(
                category=ActionCategory.IRRIGATION,
                priority=ActionPriority.CRITICAL,
                title="Urgent Irrigation Required",
                description=f"Soil moisture critically low at {soil_moisture}%. No significant rain expected.",
                reasoning="Prevent crop stress and yield loss",
                timing="Within next 12 hours, preferably early morning or evening"
            ))
        
        # Rule 3: Moderate moisture + low rain chance - monitor
        elif 30 <= soil_moisture <= 50 and rain_prob < 50:
            recommendation = f"MONITOR - Current moisture adequate ({soil_moisture}%), but plan irrigation if no rain"
            actions.append(Action(
                category=ActionCategory.IRRIGATION,
                priority=ActionPriority.MEDIUM,
                title="Monitor and Prepare for Irrigation",
                description=f"Soil moisture at {soil_moisture}%. Low rain probability ({rain_prob:.0f}%).",
                reasoning="Maintain optimal moisture levels for crop health",
                timing="Prepare to irrigate in 24-48 hours if conditions don't improve"
            ))
        
        # Rule 4: High moisture - no irrigation needed
        elif soil_moisture > 70:
            recommendation = f"NO IRRIGATION - Soil moisture adequate ({soil_moisture}%)"
            actions.append(Action(
                category=ActionCategory.IRRIGATION,
                priority=ActionPriority.INFO,
                title="No Irrigation Needed",
                description=f"Soil moisture is adequate at {soil_moisture}%.",
                reasoning="Excess irrigation can cause waterlogging and root diseases",
                timing="Next irrigation assessment in 48-72 hours"
            ))
        
        else:
            recommendation = f"NORMAL SCHEDULE - Continue regular irrigation (moisture: {soil_moisture}%)"
        
        return recommendation, actions
    
    def assess_disease_risk(
        self,
        request: WeatherIntelligenceRequest,
        weather_summary: WeatherSummary,
        weather_data: Dict
    ) -> Tuple[str, List[RiskAlert], List[Action]]:
        """Rule-based disease risk assessment"""
        alerts = []
        actions = []
        
        humidity = weather_summary.current_humidity
        temp = weather_summary.current_temp
        rain_amount = weather_summary.forecast_rain_amount
        
        # Calculate risk score (0-100)
        risk_score = 0
        
        # High humidity increases fungal disease risk
        if humidity > 80:
            risk_score += 30
        elif humidity > 70:
            risk_score += 20
        elif humidity > 60:
            risk_score += 10
        
        # Warm temperatures + moisture = disease risk
        if 20 <= temp <= 30 and humidity > 70:
            risk_score += 25
        
        # Rain increases disease spread risk
        if rain_amount > 10:
            risk_score += 20
        elif rain_amount > 5:
            risk_score += 10
        
        # Existing disease detected
        if request.farm_conditions.disease_detected:
            risk_score += 35
        
        # Vulnerable growth stages
        if request.farm_conditions.growth_stage.lower() in ["flowering", "fruit formation", "seedling"]:
            risk_score += 15
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "CRITICAL - Immediate action required"
            severity = ActionPriority.CRITICAL
        elif risk_score >= 50:
            risk_level = "HIGH - Monitor very closely"
            severity = ActionPriority.HIGH
        elif risk_score >= 30:
            risk_level = "MEDIUM - Regular monitoring"
            severity = ActionPriority.MEDIUM
        else:
            risk_level = "LOW - Continue normal care"
            severity = ActionPriority.LOW
        
        # Create alerts and actions based on risk
        if risk_score >= 50:
            alerts.append(RiskAlert(
                risk_type="Disease Outbreak Risk",
                severity=severity,
                description=f"Weather conditions favorable for disease development (Risk Score: {risk_score}/100)",
                prevention_tips=[
                    "Inspect crops daily for disease symptoms",
                    "Ensure proper air circulation between plants",
                    "Avoid overhead irrigation if possible",
                    "Remove and destroy any infected plant material",
                    "Consider preventive fungicide application"
                ]
            ))
            
            actions.append(Action(
                category=ActionCategory.DISEASE_PREVENTION,
                priority=severity,
                title="Increase Disease Monitoring",
                description=f"Weather conditions (temp: {temp:.1f}°C, humidity: {humidity:.0f}%) increase disease risk.",
                reasoning=f"Risk score of {risk_score}/100 requires preventive measures",
                timing="Start immediately and continue daily monitoring"
            ))
        
        if humidity > 75 and rain_amount > 5:
            alerts.append(RiskAlert(
                risk_type="Fungal Disease Risk",
                severity=ActionPriority.HIGH,
                description="High humidity + rain creates ideal conditions for fungal diseases",
                prevention_tips=[
                    "Improve field drainage",
                    "Avoid working in fields when wet",
                    "Consider fungicide treatment if disease symptoms appear",
                    "Increase plant spacing if possible"
                ]
            ))
        
        return risk_level, alerts, actions
    
    def generate_work_schedule(
        self,
        weather_data: Dict
    ) -> List[str]:
        """Generate optimal work hours based on weather"""
        hourly = weather_data["hourly"]
        optimal_hours = []
        
        for hour in range(24):
            temp = hourly["temperature"][hour]
            rain_prob = hourly["precipitation_probability"][hour]
            wind = hourly["wind_speed"][hour]
            
            # Optimal conditions: moderate temp, low rain, moderate wind
            if 15 <= temp <= 30 and rain_prob < 20 and wind < 25:
                time_str = f"{hour:02d}:00-{(hour+1):02d}:00"
                optimal_hours.append(time_str)
        
        return optimal_hours[:6]  # Return top 6 hours
    
    def generate_additional_actions(
        self,
        request: WeatherIntelligenceRequest,
        weather_summary: WeatherSummary
    ) -> List[Action]:
        """Generate additional contextual actions"""
        actions = []
        
        # High temperature alerts
        if weather_summary.forecast_max_temp > 35:
            actions.append(Action(
                category=ActionCategory.GENERAL,
                priority=ActionPriority.HIGH,
                title="Heat Stress Protection",
                description=f"Extreme heat expected ({weather_summary.forecast_max_temp:.1f}°C)",
                reasoning="Protect crops from heat stress and excessive transpiration",
                timing="Before temperature peaks (morning preparation)"
            ))
        
        # Strong wind alerts
        if weather_summary.current_wind_speed > 30:
            actions.append(Action(
                category=ActionCategory.GENERAL,
                priority=ActionPriority.MEDIUM,
                title="Wind Protection Measures",
                description=f"Strong winds detected ({weather_summary.current_wind_speed:.1f} km/h)",
                reasoning="Prevent physical damage to crops and soil erosion",
                timing="Immediate - secure loose materials and support structures"
            ))
        
        # Fertilization timing
        if not request.farm_conditions.recent_fertilization:
            if weather_summary.forecast_rain_probability < 30:
                actions.append(Action(
                    category=ActionCategory.FERTILIZATION,
                    priority=ActionPriority.LOW,
                    title="Consider Fertilization",
                    description="Good weather window for fertilizer application",
                    reasoning="Low rain risk minimizes nutrient runoff",
                    timing="Within next 24 hours, before any forecasted rain"
                ))
        
        # Harvesting recommendations
        if request.farm_conditions.growth_stage.lower() in ["maturation", "harvest"]:
            if weather_summary.forecast_rain_probability < 20 and weather_summary.current_humidity < 60:
                actions.append(Action(
                    category=ActionCategory.HARVESTING,
                    priority=ActionPriority.HIGH,
                    title="Optimal Harvest Window",
                    description="Ideal weather conditions for harvesting",
                    reasoning="Dry conditions with low rain risk ensure quality harvest",
                    timing="Next 24-48 hours before weather changes"
                ))
        
        return actions
    
    def generate_intelligence(
        self,
        request: WeatherIntelligenceRequest
    ) -> WeatherIntelligenceResponse:
        """
        Main intelligence generation combining weather and farm conditions
        """
        # Fetch weather data
        weather_data = self.fetch_weather_data(
            request.latitude,
            request.longitude,
            request.forecast_days
        )
        
        # Create weather summary
        weather_summary = self.create_weather_summary(weather_data)
        
        # Initialize collections
        all_actions = []
        all_alerts = []
        
        # Assess irrigation needs
        irrigation_rec, irrigation_actions = self.assess_irrigation_need(
            request, weather_summary
        )
        all_actions.extend(irrigation_actions)
        
        # Assess disease risk
        disease_risk, disease_alerts, disease_actions = self.assess_disease_risk(
            request, weather_summary, weather_data
        )
        all_alerts.extend(disease_alerts)
        all_actions.extend(disease_actions)
        
        # Generate work schedule
        optimal_hours = self.generate_work_schedule(weather_data)
        
        # Generate additional actions
        additional_actions = self.generate_additional_actions(
            request, weather_summary
        )
        all_actions.extend(additional_actions)
        
        # Sort actions by priority
        priority_order = {
            ActionPriority.CRITICAL: 0,
            ActionPriority.HIGH: 1,
            ActionPriority.MEDIUM: 2,
            ActionPriority.LOW: 3,
            ActionPriority.INFO: 4
        }
        all_actions.sort(key=lambda x: priority_order[x.priority])
        
        # Create response
        return WeatherIntelligenceResponse(
            success=True,
            location=weather_data["location"],
            weather_summary=weather_summary,
            recommended_actions=all_actions,
            risk_alerts=all_alerts,
            irrigation_recommendation=irrigation_rec,
            disease_risk_level=disease_risk,
            optimal_work_hours=optimal_hours,
            data_source="Open-Meteo API (https://open-meteo.com/)",
            generated_at=datetime.now()
        )


# Global service instance
weather_intelligence_service = WeatherIntelligenceService()


def get_weather_intelligence_service() -> WeatherIntelligenceService:
    """Dependency to get the weather intelligence service"""
    return weather_intelligence_service
