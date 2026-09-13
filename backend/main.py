"""
Main entry point for the application
Run with: python main.py or uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from core.config import settings
from core.model_loader import model_manager
from api.routes import health, root, predict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Application factory"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.DEBUG
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Include routers
    app.include_router(root.router, tags=["Root"])
    app.include_router(health.router, tags=["Health"])
    app.include_router(predict.router, prefix=settings.API_PREFIX, tags=["Prediction"])
    
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
    
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

