"""
Main entry point for the application
Run with: python main.py or uvicorn main:app --reload
"""
import uvicorn
import logging

from app.main import app
from app.core.config import settings
from core.model_loader import model_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Agrismart AI API...")
    try:
        model_manager.load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.warning("API will start but predictions will not be available")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Agrismart AI API...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

