from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.disease_detection.router import router as disease_router
from app.modules.crop_recommendation.router import router as crop_router
from app.modules.crop_recommendation.service import crop_service
from app.modules.sustainability.router import router as sustainability_router
from app.modules.smart_irrigation.router import router as irrigation_router
from app.modules.smart_irrigation.service import irrigation_service
from app.modules.smart_weather_based_Intelligence.router import router as weather_intelligence_router
from app.modules.farmer_assistant.router import router as farmer_assistant_router
from app.modules.agentic_advisor.router import router as agentic_advisor_router

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
        
        # Load smart irrigation model
        print("\n💧 Loading Smart Irrigation Model...")
        irrigation_loaded = irrigation_service.load_model()
        if irrigation_loaded:
            print("✅ Smart Irrigation Model loaded successfully")
        else:
            print("⚠️  Smart Irrigation Model failed to load")
        
        print("\n" + "="*80)
        print("✅ STARTUP COMPLETE")
        print("="*80 + "\n")
    
    # Include routers
    app.include_router(disease_router, prefix="/api/v1", tags=["Disease Detection"])
    app.include_router(crop_router, prefix="/api/v1", tags=["Crop Recommendation"])
    app.include_router(sustainability_router, prefix="/api/v1", tags=["Sustainability"])
    app.include_router(irrigation_router, prefix="/api/v1", tags=["Smart Irrigation"])
    app.include_router(weather_intelligence_router, prefix="/api/v1", tags=["Weather Intelligence"])
    app.include_router(farmer_assistant_router, prefix="/api/v1", tags=["Farmer Assistant"])
    app.include_router(agentic_advisor_router, prefix="/api/v1", tags=["Agentic Advisor"])
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "endpoints": {
                "disease_detection": "/api/v1/predict",
                "crop_recommendation": "/api/v1/test/crop_recommendation",
                "crop_health": "/api/v1/test/crop_recommendation/health",
                "sustainability_score": "/api/v1/sustainability/score",
                "irrigation_predict": "/api/v1/irrigation/predict",
                "irrigation_health": "/api/v1/irrigation/health",
                "irrigation_info": "/api/v1/irrigation/info",
                "weather_intelligence": "/api/v1/weather-intelligence",
                "weather_intelligence_info": "/api/v1/weather-intelligence/info",
                "sample_locations": "/api/v1/weather-intelligence/sample-locations",
                "farmer_assistant_chat": "/api/v1/assistant/chat",
                "agent_run": "/api/v1/agent/run/{farm_id}",
                "agent_status": "/api/v1/agent/status/{farm_id}"
            }
        }
    
    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "app_name": settings.APP_NAME,
            "crop_model_loaded": crop_service.is_loaded(),
            "irrigation_model_loaded": irrigation_service.is_loaded()
        }
    
    return app


app = create_app()
