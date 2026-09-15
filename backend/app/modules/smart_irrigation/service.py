"""
Service layer for smart irrigation predictions
"""

import os
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from .schemas import (
    IrrigationRequest,
    IrrigationResponse,
    IrrigationRecommendation,
    IrrigationLevel,
    CropType,
    SoilType,
    SeedlingStage
)


class SmartIrrigationService:
    """Service for irrigation prediction using RandomForest model"""
    
    # Water amount recommendations (L/m²) based on irrigation level
    WATER_AMOUNTS = {
        0: 0.0,      # No irrigation
        1: 15.0,     # Medium irrigation
        2: 30.0      # High irrigation
    }
    
    # Irrigation level names
    LEVEL_NAMES = {
        0: IrrigationLevel.NONE,
        1: IrrigationLevel.MEDIUM,
        2: IrrigationLevel.HIGH
    }
    
    def __init__(self):
        self.model = None
        self.metadata: Dict = None
        self.label_encoders: Dict = None
        self.feature_names: List[str] = None
        self._is_loaded = False
        
    def load_model(self) -> bool:
        """Load the trained RandomForest model and metadata"""
        try:
            # Get model path
            current_dir = Path(__file__).parent
            models_dir = current_dir / "model"
            
            model_path = models_dir / "irrigation_randomforest.joblib"
            metadata_path = models_dir / "irrigation_metadata.joblib"
            encoders_path = models_dir / "label_encoders.joblib"
            
            if not model_path.exists():
                print(f"❌ Model not found at {model_path}")
                return False
            
            if not metadata_path.exists():
                print(f"❌ Metadata not found at {metadata_path}")
                return False
            
            if not encoders_path.exists():
                print(f"❌ Label encoders not found at {encoders_path}")
                return False
            
            # Load model
            self.model = joblib.load(model_path)
            print(f"✓ RandomForest model loaded from {model_path}")
            
            # Load metadata
            self.metadata = joblib.load(metadata_path)
            self.feature_names = self.metadata['feature_names']
            
            # Load label encoders
            self.label_encoders = joblib.load(encoders_path)
            
            print(f"✓ Metadata loaded: {len(self.feature_names)} features")
            print(f"✓ Model accuracy: {self.metadata['metrics']['test_accuracy']:.4f}")
            
            self._is_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Error loading smart irrigation model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded
    
    def _encode_features(self, request: IrrigationRequest) -> pd.DataFrame:
        """
        Encode request features to match training format
        
        Features: crop ID, soil_type, Seedling Stage, MOI, temp, humidity
        """
        # Create feature dictionary
        features = {
            'crop ID': request.crop_id.value,
            'soil_type': request.soil_type.value,
            'Seedling Stage': request.seedling_stage.value,
            'MOI': request.moi,
            'temp': request.temp,
            'humidity': request.humidity
        }
        
        # Create dataframe
        df = pd.DataFrame([features])
        
        # Encode categorical features
        for col in ['crop ID', 'soil_type', 'Seedling Stage']:
            if col in self.label_encoders:
                le = self.label_encoders[col]
                try:
                    df[col] = le.transform(df[col])
                except ValueError as e:
                    # Handle unknown categories
                    print(f"⚠️  Unknown value for {col}: {df[col].iloc[0]}")
                    # Use the most common class (0)
                    df[col] = 0
        
        # Ensure column order matches training
        df = df[self.feature_names]
        
        return df
    
    def _assess_moisture(self, moi: int) -> str:
        """Assess moisture level"""
        if moi < 20:
            return "Very Low - Critical irrigation needed"
        elif moi < 40:
            return "Low - Irrigation recommended"
        elif moi < 60:
            return "Moderate - Monitor closely"
        elif moi < 80:
            return "Good - Adequate moisture"
        else:
            return "High - No irrigation needed"
    
    def _assess_temperature(self, temp: int) -> str:
        """Assess temperature conditions"""
        if temp < 10:
            return "Cold - Reduced irrigation needs"
        elif temp < 20:
            return "Cool - Moderate irrigation"
        elif temp < 30:
            return "Optimal - Normal irrigation schedule"
        elif temp < 40:
            return "Hot - Increased irrigation may be needed"
        else:
            return "Very Hot - Critical water management required"
    
    def _generate_suggestions(
        self,
        request: IrrigationRequest,
        level_code: int
    ) -> List[str]:
        """Generate contextual farming suggestions"""
        suggestions = []
        
        # Moisture-based suggestions
        if request.moi < 30:
            suggestions.append("Soil moisture is low - prioritize irrigation")
        
        # Temperature-based suggestions
        if request.temp > 35:
            suggestions.append("High temperature detected - irrigate during early morning or evening")
        elif request.temp < 15:
            suggestions.append("Cool temperature - reduce irrigation frequency")
        
        # Humidity-based suggestions
        if request.humidity < 40:
            suggestions.append("Low humidity - consider mulching to retain moisture")
        elif request.humidity > 80:
            suggestions.append("High humidity - monitor for fungal diseases")
        
        # Stage-specific suggestions
        if request.seedling_stage == SeedlingStage.FLOWERING:
            suggestions.append("Flowering stage - maintain consistent moisture")
        elif request.seedling_stage == SeedlingStage.FRUIT_FORMATION:
            suggestions.append("Fruit formation stage - adequate water is critical")
        elif request.seedling_stage == SeedlingStage.HARVEST:
            suggestions.append("Near harvest - reduce irrigation gradually")
        
        # Irrigation level specific
        if level_code == 2:
            suggestions.append("High irrigation required - check drainage to prevent waterlogging")
        elif level_code == 1:
            suggestions.append("Consider drip irrigation for water efficiency")
        
        # Soil-specific
        if request.soil_type == SoilType.SANDY:
            suggestions.append("Sandy soil drains quickly - frequent light irrigation recommended")
        elif request.soil_type == SoilType.CLAY:
            suggestions.append("Clay soil retains water - avoid overwatering")
        
        return suggestions
    
    def predict_irrigation(self, request: IrrigationRequest) -> IrrigationResponse:
        """
        Predict irrigation requirements
        
        Args:
            request: IrrigationRequest with crop and environmental data
            
        Returns:
            IrrigationResponse with recommendation and insights
            
        Raises:
            ValueError: If model is not loaded
        """
        if not self._is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Encode features
        features_df = self._encode_features(request)
        
        # Get prediction
        prediction = int(self.model.predict(features_df)[0])
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(features_df)[0]
        confidence = float(probabilities[prediction])
        
        # Create recommendation
        recommendation = IrrigationRecommendation(
            level=self.LEVEL_NAMES[prediction],
            level_code=prediction,
            confidence=confidence,
            water_amount_liters=self.WATER_AMOUNTS[prediction]
        )
        
        # Assess conditions
        moisture_status = self._assess_moisture(request.moi)
        temperature_status = self._assess_temperature(request.temp)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(request, prediction)
        
        # Create response
        response = IrrigationResponse(
            success=True,
            recommendation=recommendation,
            conditions={
                "crop": request.crop_id.value,
                "soil": request.soil_type.value,
                "stage": request.seedling_stage.value,
                "moisture": request.moi,
                "temperature": request.temp,
                "humidity": request.humidity
            },
            moisture_status=moisture_status,
            temperature_status=temperature_status,
            suggestions=suggestions
        )
        
        return response


# Global service instance
irrigation_service = SmartIrrigationService()


def get_irrigation_service() -> SmartIrrigationService:
    """Dependency to get the irrigation service"""
    return irrigation_service
