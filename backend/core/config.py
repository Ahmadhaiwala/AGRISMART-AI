from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Settings
    APP_NAME: str = "Agrismart AI"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Model Settings
    MODEL_PATH: str = "models/plant_disease_efficientnet_b0_38class_best.pth"
    HF_MODEL_REPO: str = "Ahmadhaiwala/agro_model"
    HF_MODEL_FILE: str = "plant_disease_efficientnet_b0_38class_best.pth"
    DEVICE: str = "cuda" if os.getenv("CUDA_AVAILABLE", "false").lower() == "true" else "cpu"
    
    # Image Processing
    IMAGE_SIZE: int = 224
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
