from pydantic_settings import BaseSettings
from typing import List


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
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./agrismart.db"
    
    # Model Settings
    MODEL_PATH: str = "./models/disease_model.pth"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
