# Agrismart AI Backend

Backend API service for Agrismart AI application, built with FastAPI and PyTorch for agricultural intelligence and image analysis.

## Features

- FastAPI-based REST API
- PyTorch deep learning inference
- Image processing and analysis
- Asynchronous request handling

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment**:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode

Start the server with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check
- `POST /api/v1/predict` - Predict plant disease from image
- `GET /api/v1/model/info` - Get model information
- `POST /api/v1/model/reload` - Reload the model (admin)

## Model Information

The API uses a CNN model for plant disease classification trained on 38 different plant disease classes. The model is automatically downloaded from HuggingFace Hub on first startup.

- **Model**: Plant Disease CNN Baseline
- **HuggingFace Repo**: [Ahmadhaiwala/agro_model](https://huggingface.co/Ahmadhaiwala/agro_model)
- **Classes**: 38 plant disease categories
- **Input Size**: 224x224 RGB images

## Project Structure

```
backend/
├── .venv/                              # Virtual environment (not in git)
├── app/                                # Main application package
│   ├── main.py                         # FastAPI application factory
│   ├── core/                           # Core configuration
│   │   ├── __init__.py
│   │   └── config.py                   # Settings and configuration
│   ├── database/                       # Database configuration
│   │   ├── __init__.py
│   │   └── base.py                     # Database setup
│   └── modules/                        # Feature modules
│       └── disease_detection/          # Disease detection module
│           ├── __init__.py
│           ├── router.py               # API endpoints
│           ├── service.py              # Business logic
│           ├── model.py                # Database models
│           └── schemas.py              # Pydantic schemas
├── models/                             # Trained ML models
│   └── .gitkeep
├── tests/                              # Test suite
│   ├── __init__.py
│   └── test_main.py
├── main.py                             # Application entry point
├── requirements.txt                    # Python dependencies
├── alembic.ini                         # Database migrations config
├── .env                                # Environment variables (not in git)
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **PyTorch**: Deep learning framework for model inference
- **TorchVision**: Computer vision utilities
- **Pillow**: Image processing
- **HuggingFace Hub**: Model downloading from HuggingFace
- **Pydantic**: Data validation and settings management

## Development

### Adding New Dependencies

1. Install the package:
   ```bash
   pip install package-name
   ```

2. Update requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```

### Environment Variables

Create a `.env` file in the backend directory for environment-specific configuration (already ignored by git).

## License

[Add your license here]

## Contact

[Add contact information]
