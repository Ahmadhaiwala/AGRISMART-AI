from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
import logging

from core.model_loader import model_manager
from core.image_utils import image_processor

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/predict")
async def predict_disease(file: UploadFile = File(...)) -> Dict:
    """
    Predict plant disease from uploaded image
    
    Args:
        file: Uploaded image file (JPEG, PNG)
        
    Returns:
        Prediction results with confidence scores
    """
    try:
        # Check if model is loaded
        if not model_manager.is_loaded:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded. Please wait for initialization."
            )
        
        # Read file content
        file_content = await file.read()
        
        # Validate image
        is_valid, error_msg = image_processor.validate_image(file_content, file.filename)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Preprocess image
        import io
        image_tensor = image_processor.preprocess(io.BytesIO(file_content))
        
        # Make prediction
        prediction = model_manager.predict(image_tensor)
        
        return {
            "success": True,
            "filename": file.filename,
            "prediction": prediction
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/model/info")
async def get_model_info() -> Dict:
    """Get information about the loaded model"""
    return model_manager.get_info()


@router.post("/model/reload")
async def reload_model() -> Dict:
    """Reload the model (admin endpoint)"""
    try:
        model_manager.load_model()
        return {
            "success": True,
            "message": "Model reloaded successfully"
        }
    except Exception as e:
        logger.error(f"Error reloading model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reload model: {str(e)}")
