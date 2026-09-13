"""
Main entry point for the application
Run with: python main.py or uvicorn main:app --reload
"""
import uvicorn
from app.main import app
from app.core.config import settings


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
