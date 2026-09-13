from fastapi import APIRouter

router = APIRouter()


@router.get("/disease-detection")
async def get_disease_detection():
    """Get disease detection information"""
    return {
        "message": "Disease detection endpoint",
        "status": "initialized"
    }


@router.post("/disease-detection/predict")
async def predict_disease():
    """Predict disease from image"""
    return {
        "message": "Disease prediction endpoint",
        "status": "initialized"
    }
