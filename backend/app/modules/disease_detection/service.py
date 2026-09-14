"""
Disease detection service layer
Business logic for disease detection
"""
import logging
from typing import Dict
import io

from core.model_loader import model_manager
from core.image_utils import image_processor

logger = logging.getLogger(__name__)


class DiseaseDetectionService:
    """Service for handling disease detection logic"""
    
    def __init__(self):
        pass
    
    async def predict_from_file(self, file_content: bytes, filename: str) -> Dict:
        """
        Predict plant disease from image file
        
        Args:
            file_content: Image file bytes
            filename: Original filename
            
        Returns:
            Prediction results with confidence scores
            
        Raises:
            ValueError: If model is not loaded or image is invalid
            RuntimeError: If prediction fails
        """
        try:
            # Check if model is loaded
            if not model_manager.is_loaded:
                raise ValueError("Model not loaded. Please wait for initialization.")
            
            # Validate image
            is_valid, error_msg = image_processor.validate_image(file_content, filename)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Preprocess image
            image_tensor = image_processor.preprocess(io.BytesIO(file_content))
            
            # Make prediction
            prediction = model_manager.predict(image_tensor)
            
            return {
                "success": True,
                "filename": filename,
                "prediction": prediction
            }
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error in prediction service: {str(e)}")
            raise RuntimeError(f"Prediction failed: {str(e)}")
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return model_manager.get_info()
    
    def reload_model(self) -> Dict:
        """Reload the model"""
        try:
            model_manager.load_model()
            return {
                "success": True,
                "message": "Model reloaded successfully"
            }
        except Exception as e:
            logger.error(f"Error reloading model: {str(e)}")
            raise RuntimeError(f"Failed to reload model: {str(e)}")
    
    async def get_all_diseases(self):
        """Get list of all detectable diseases"""
        if model_manager.is_loaded:
            return {
                "diseases": model_manager.class_names,
                "count": len(model_manager.class_names)
            }
        return {
            "diseases": [],
            "count": 0
        }


# Global service instance
disease_detection_service = DiseaseDetectionService()
