"""
Service layer for crop recommendation
"""

import os
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, List, Tuple
from catboost import CatBoostClassifier

from .schemas import CropRecommendationRequest, CropRecommendationResponse, CropPrediction


class CropRecommendationService:
    """Service for crop recommendation using CatBoost model"""
    
    def __init__(self):
        self.model: CatBoostClassifier = None
        self.metadata: Dict = None
        self.feature_names: List[str] = None
        self.classes: List[str] = None
        self._is_loaded = False
        
    def load_model(self) -> bool:
        """Load the trained CatBoost model and metadata"""
        try:
            # Get model path
            current_dir = Path(__file__).parent
            models_dir = current_dir / "models"
            
            model_path = models_dir / "crop_recommendation_catboost_fixed.cbm"
            metadata_path = models_dir / "crop_recommendation_metadata_fixed.joblib"
            
            if not model_path.exists():
                print(f"❌ Model not found at {model_path}")
                return False
            
            if not metadata_path.exists():
                print(f"❌ Metadata not found at {metadata_path}")
                return False
            
            # Load model
            self.model = CatBoostClassifier()
            self.model.load_model(str(model_path))
            print(f"✓ CatBoost model loaded from {model_path}")
            
            # Load metadata
            self.metadata = joblib.load(metadata_path)
            self.feature_names = self.metadata['feature_names']
            self.classes = self.metadata['classes']
            
            print(f"✓ Metadata loaded: {len(self.feature_names)} features, {len(self.classes)} classes")
            print(f"✓ Model metrics: Test Accuracy = {self.metadata['metrics']['test_accuracy']:.4f}")
            
            self._is_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ Error loading crop recommendation model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded
    
    def _prepare_features(self, request: CropRecommendationRequest) -> pd.DataFrame:
        """
        Convert request to dataframe with correct feature order and column names
        
        Features expected by model (must match training):
        TYPE_OF_CROP, SOIL, SEASON, WATER_SOURCE, SOIL_PH, SOIL_PH_HIGH,
        TEMP, MAX_TEMP, WATERREQUIRED, WATERREQUIRED_MAX,
        RELATIVE_HUMIDITY, RELATIVE_HUMIDITY_MAX,
        N, N_MAX, P, P_MAX, K, K_MAX
        """
        # Create feature dictionary with uppercase column names (matching training data)
        features = {
            'TYPE_OF_CROP': request.type_of_crop,
            'SOIL': request.soil,
            'SEASON': request.season,
            'WATER_SOURCE': request.water_source,
            'SOIL_PH': request.soil_ph,
            'SOIL_PH_HIGH': request.soil_ph_high,
            'TEMP': request.temp,
            'MAX_TEMP': request.max_temp,
            'WATERREQUIRED': request.waterrequired,
            'WATERREQUIRED_MAX': request.waterrequired_max,
            'RELATIVE_HUMIDITY': request.relative_humidity,
            'RELATIVE_HUMIDITY_MAX': request.relative_humidity_max,
            'N': request.n,
            'N_MAX': request.n_max,
            'P': request.p,
            'P_MAX': request.p_max,
            'K': request.k,
            'K_MAX': request.k_max
        }
        
        # Create dataframe with features in the correct order
        df = pd.DataFrame([features])
        
        # Ensure column order matches training
        df = df[self.feature_names]
        
        return df
    
    def recommend_crop(self, request: CropRecommendationRequest) -> CropRecommendationResponse:
        """
        Recommend crops based on input features
        
        Args:
            request: CropRecommendationRequest with all required features
            
        Returns:
            CropRecommendationResponse with top crop and top 5 predictions
            
        Raises:
            ValueError: If model is not loaded
        """
        if not self._is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Prepare features
        features_df = self._prepare_features(request)
        
        # Get predictions (extract scalar from numpy array)
        prediction_array = self.model.predict(features_df)
        prediction = prediction_array[0] if isinstance(prediction_array, (list, tuple)) else prediction_array
        prediction = str(prediction).strip("[]' ")  # Clean up any array formatting
        
        # Get probabilities for all classes
        probabilities = self.model.predict_proba(features_df)[0]
        
        # Get top 5 predictions
        top_5_indices = probabilities.argsort()[-5:][::-1]
        top_5_predictions = [
            CropPrediction(
                crop_name=str(self.classes[idx]),
                confidence=float(probabilities[idx])
            )
            for idx in top_5_indices
        ]
        
        # Create response
        response = CropRecommendationResponse(
            success=True,
            top_crop=prediction,
            confidence=float(probabilities[probabilities.argmax()]),
            top_5_predictions=top_5_predictions
        )
        
        return response


# Global service instance
crop_service = CropRecommendationService()


def get_crop_service() -> CropRecommendationService:
    """Dependency to get the crop recommendation service"""
    return crop_service
