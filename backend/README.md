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

### Sustainability Score (Bonus Module D)
- `POST /api/v1/sustainability/score` - Compute a sustainability score (0-100) from water
  efficiency, resource use (fertilizer/pesticide), and crop health, with improvement
  suggestions.

  **Request body:**
  ```json
  {
    "water_used_liters": 120,
    "water_required_liters": 100,
    "fertilizer_used_kg": 5,
    "fertilizer_recommended_kg": 4,
    "pesticide_used_kg": 0,
    "pesticide_recommended_kg": 0,
    "is_healthy": false,
    "disease_confidence": 0.91
  }
  ```
  `is_healthy` / `disease_confidence` are meant to be passed straight through from the
  `/api/v1/predict` (disease detection) response for the same crop.

  **Response:**
  ```json
  {
    "success": true,
    "overall_score": 57.2,
    "grade": "C",
    "sub_scores": { "water_efficiency": 80.0, "resource_use": 75.0, "crop_health": 9.0 },
    "suggestions": ["Disease detected with meaningful confidence -- apply the recommended precaution promptly to prevent spread."],
    "formula_version": "1.0"
  }
  ```

  The exact formula (weights, grade bands, and rationale) is published in
  [`/report/SUSTAINABILITY_FORMULA.md`](../report/SUSTAINABILITY_FORMULA.md) so the score is
  fully reproducible. Try it via Swagger UI at `/docs` or:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/sustainability/score" \
    -H "Content-Type: application/json" \
    -d '{"water_used_liters":120,"water_required_liters":100,"fertilizer_used_kg":5,"fertilizer_recommended_kg":4,"pesticide_used_kg":0,"pesticide_recommended_kg":0,"is_healthy":false,"disease_confidence":0.91}'
  ```

### Smart Irrigation (Bonus Module B)
- `POST /api/v1/irrigation/predict` - Predict whether irrigation is required right now
  from soil moisture, weather forecast, crop type, and growth stage, with a recommended
  water volume and the reasons behind the decision. Rule-based (not a trained model) so
  the decision is fully transparent and auditable.

  **Request body:**
  ```json
  {
    "crop_type": "Tomato",
    "growth_stage": "flowering",
    "soil_moisture_percent": 28,
    "rain_probability_percent": 10,
    "forecast_rain_mm_24h": 0,
    "temperature_c": 33,
    "area_sqm": 10
  }
  ```

  **Response:**
  ```json
  {
    "success": true,
    "decision": {
      "irrigation_required": true,
      "urgency": "high",
      "soil_moisture_status": "critical_deficit",
      "recommended_water_liters": 110.0,
      "rain_delay_applied": false
    },
    "reasons": ["Soil moisture (28%) is below the critical threshold (35%) for Tomato at the flowering stage."],
    "logic_version": "1.0"
  }
  ```

  The exact thresholds, decision rules, and rationale are published in
  [`/report/IRRIGATION_LOGIC.md`](../report/IRRIGATION_LOGIC.md) so the decision is fully
  reproducible. `recommended_water_liters` is designed to feed straight into the
  Sustainability Score's `water_used_liters` input for the same crop. Try it via Swagger
  UI at `/docs` or:
  ```bash
  curl -X POST "http://localhost:8000/api/v1/irrigation/predict" \
    -H "Content-Type: application/json" \
    -d '{"crop_type":"Tomato","growth_stage":"flowering","soil_moisture_percent":28,"rain_probability_percent":10,"forecast_rain_mm_24h":0,"temperature_c":33,"area_sqm":10}'
  ```

## Model Information

The API uses an EfficientNet-B0 model for plant disease classification trained on 38 different plant disease classes. The model is automatically downloaded from HuggingFace Hub on first startup.

- **Model**: EfficientNet-B0 (38 classes)
- **HuggingFace Repo**: [Ahmadhaiwala/agro_model](https://huggingface.co/Ahmadhaiwala/agro_model)
- **Model File**: plant_disease_efficientnet_b0_38class_best.pth
- **Classes**: 38 plant disease categories
- **Input Size**: 224x224 RGB images
- **Architecture**: EfficientNet-B0 with custom classifier

## Project Structure

```
backend/
├── .venv/                  # Virtual environment (not in git)
├── app/                    # Main application package
│   ├── core/              # App-level config
│   │   ├── __init__.py
│   │   └── config.py      # Settings
│   ├── modules/           # Feature modules
│   │   ├── disease_detection/  # Disease detection module
│   │   │   ├── __init__.py
│   │   │   ├── router.py      # HTTP endpoints + UI
│   │   │   ├── service.py     # Business logic
│   │   │   ├── schemas.py     # Pydantic models
│   │   │   └── model.py       # Database models
│   │   ├── sustainability/     # Sustainability score module (Bonus D)
│   │   │   ├── __init__.py
│   │   │   ├── router.py      # POST /sustainability/score
│   │   │   ├── service.py     # Scoring formula + suggestions
│   │   │   └── schemas.py     # Pydantic models
│   │   └── irrigation/         # Smart irrigation module (Bonus B)
│   │       ├── __init__.py
│   │       ├── router.py      # POST /irrigation/predict
│   │       ├── service.py     # Rule-based decision logic
│   │       └── schemas.py     # Pydantic models
│   └── main.py            # FastAPI app factory
├── core/                   # Core utilities (shared)
│   ├── __init__.py
│   ├── config.py          # Application settings
│   ├── model_loader.py    # Model loading and inference
│   └── image_utils.py     # Image preprocessing
├── models/                 # Model files (not in git)
│   ├── .cache/             # HuggingFace cache
│   └── plant_disease_efficientnet_b0_38class_best.pth
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

### Running Automated Tests

```bash
pytest tests/ -v
```

`tests/test_sustainability.py` covers the sustainability score module (formula
correctness, grade bands, suggestion logic, and the HTTP endpoint contract) and does not
require the disease-detection model or `torch` to be installed to run.

## License

[Add your license here]

## Contact

[Add contact information]
