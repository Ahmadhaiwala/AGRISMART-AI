from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.disease_detection.router import router as disease_router
from app.modules.crop_recommendation.router import router as crop_router
from app.modules.crop_recommendation.service import crop_service
from app.modules.sustainability.router import router as sustainability_router
from app.modules.irrigation.router import router as irrigation_router
from app.modules.dashboard.router import router as dashboard_router

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
    
    # Startup event to load models
    @app.on_event("startup")
    async def startup_event():
        """Load ML models on startup"""
        print("\n" + "="*80)
        print("🚀 LOADING ML MODELS")
        print("="*80)
        
        # Load crop recommendation model
        print("\n📊 Loading Crop Recommendation Model...")
        crop_loaded = crop_service.load_model()
        if crop_loaded:
            print("✅ Crop Recommendation Model loaded successfully")
        else:
            print("⚠️  Crop Recommendation Model failed to load")
        
        print("\n" + "="*80)
        print("✅ STARTUP COMPLETE")
        print("="*80 + "\n")
    
    # Include routers
    app.include_router(disease_router, prefix="/api/v1", tags=["Disease Detection"])
    app.include_router(crop_router, prefix="/api/v1", tags=["Crop Recommendation"])
    app.include_router(sustainability_router, prefix="/api/v1", tags=["Sustainability"])
    app.include_router(irrigation_router, prefix="/api/v1", tags=["Smart Irrigation"])
    app.include_router(dashboard_router, tags=["Dashboard"])
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "dashboard": "/dashboard",
            "endpoints": {
                "disease_detection": "/api/v1/predict",
                "crop_recommendation": "/api/v1/test/crop_recommendation",
                "crop_health": "/api/v1/test/crop_recommendation/health",
                "sustainability_score": "/api/v1/sustainability/score",
                "irrigation_predict": "/api/v1/irrigation/predict"
            }
        }
    
    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "crop_model_loaded": crop_service.is_loaded()
        }
    
    return app


app = create_app()
