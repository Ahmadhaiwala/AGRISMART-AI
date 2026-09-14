# Agrismart AI Backend

Backend API service for Agrismart AI application, built with FastAPI and PyTorch for agricultural intelligence and plant disease detection.

## Features

- FastAPI-based REST API
- PyTorch deep learning inference
- Plant disease classification (38 classes)
- Image processing and analysis
- Web UI for testing
- Asynchronous request handling
- Modular architecture with service layer

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
python main.py
```

Or with uvicorn directly:

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
- **Web Testing UI**: http://localhost:8000/api/v1/predict

## API Endpoints

### Root & Health
- `GET /` - Root endpoint with API information
- `GET /health` - Health check

### Disease Detection
- `GET /api/v1/predict` - Web UI for testing predictions
- `POST /api/v1/predict` - Predict plant disease from image
- `GET /api/v1/model/info` - Get model information
- `POST /api/v1/model/reload` - Reload the model (admin)
- `GET /api/v1/diseases` - Get list of all detectable diseases

## Model Information

The API uses a CNN model for plant disease classification trained on 38 different plant disease classes. The model is automatically downloaded from HuggingFace Hub on first startup.

- **Model**: Plant Disease CNN Baseline
- **HuggingFace Repo**: [Ahmadhaiwala/agro_model](https://huggingface.co/Ahmadhaiwala/agro_model)
- **Classes**: 38 plant disease categories
- **Input Size**: 224x224 RGB images

## Project Structure

```
backend/
├── .venv/                  # Virtual environment (not in git)
├── app/                    # Main application package
│   ├── core/              # App-level config
│   │   ├── __init__.py
│   │   └── config.py      # Settings
│   ├── modules/           # Feature modules
│   │   └── disease_detection/  # Disease detection module
│   │       ├── __init__.py
│   │       ├── router.py      # HTTP endpoints + UI
│   │       ├── service.py     # Business logic
│   │       ├── schemas.py     # Pydantic models
│   │       └── model.py       # Database models
│   └── main.py            # FastAPI app factory
├── core/                   # Core utilities (shared)
│   ├── __init__.py
│   ├── config.py          # Application settings
│   ├── model_loader.py    # Model loading and inference
│   └── image_utils.py     # Image preprocessing
├── models/                 # Model files (not in git)
│   ├── cache/             # HuggingFace cache
│   └── plant_disease_cnn_baseline.pth
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (not in git)
└── README.md             # This file
```

## Architecture

The application follows a clean, modular architecture:

- **app/**: Main application package with FastAPI setup
  - **core/**: App-level configuration
  - **modules/**: Feature modules (disease_detection, etc.)
    - Each module has: router, service, schemas, model
- **core/**: Shared utilities (model loader, image processing, config)
- **models/**: ML model files
- **main.py**: Entry point that loads the model and starts the server

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

Create a `.env` file in the backend directory for environment-specific configuration (already ignored by git). See `.env.example` for reference.

### Testing the API

Use the web interface at http://localhost:8000/api/v1/predict or use curl:

```bash
curl -X POST "http://localhost:8000/api/v1/predict" -F "file=@plant_image.jpg"
```

## License

[Add your license here]

## Contact

[Add contact information]
