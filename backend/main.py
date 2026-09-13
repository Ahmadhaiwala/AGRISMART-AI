from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from PIL import Image
import io
import numpy as np
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agrismart AI API",
    description="Agricultural intelligence and image analysis API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

class PredictionResponse(BaseModel):
    success: bool
    message: str
    predictions: Optional[List[dict]] = None

class ImageAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    threshold: float = 0.5

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Agrismart AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Service is running",
        version="1.0.0"
    )

# Image upload and analysis endpoint
@app.post("/api/v1/analyze", response_model=PredictionResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded image
    
    - **file**: Image file to analyze (JPEG, PNG)
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Convert to numpy array
        img_array = np.array(image)
        
        logger.info(f"Image processed: {image.size}, mode: {image.mode}")
        
        # TODO: Add your ML model inference here
        # Example placeholder response
        predictions = [
            {
                "class": "placeholder",
                "confidence": 0.95,
                "bbox": [0, 0, 100, 100]
            }
        ]
        
        return PredictionResponse(
            success=True,
            message="Image analyzed successfully",
            predictions=predictions
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# Batch image analysis endpoint
@app.post("/api/v1/analyze/batch")
async def analyze_batch(files: List[UploadFile] = File(...)):
    """
    Analyze multiple images in batch
    
    - **files**: List of image files to analyze
    """
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
        
        results = []
        for file in files:
            if not file.content_type.startswith("image/"):
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Invalid file type"
                })
                continue
            
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Process image
            results.append({
                "filename": file.filename,
                "success": True,
                "size": image.size,
                "format": image.format
            })
        
        return {
            "success": True,
            "total": len(files),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing batch: {str(e)}")

# Model information endpoint
@app.get("/api/v1/model/info")
async def model_info():
    """Get information about the loaded model"""
    return {
        "model_loaded": False,  # Update when model is loaded
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Agrismart AI API...")
    logger.info(f"PyTorch version: {torch.__version__}")
    logger.info(f"CUDA available: {torch.cuda.is_available()}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Agrismart AI API...")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
