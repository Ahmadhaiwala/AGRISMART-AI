# Agrismart AI Backend

Backend API service for Agrismart AI application, built with FastAPI and PyTorch for agricultural intelligence and plant disease detection.

## Features

- FastAPI-based REST API
- PyTorch deep learning inference
- **Plant Disease Detection** - EfficientNet-B0 (38 classes)
- **Crop Recommendation** - CatBoost model (57 crops)
- **Smart Irrigation** - RandomForest predictor (96.47% accuracy)
- **Weather Intelligence** - Rule-based farming decisions with Open-Meteo API
- **Sustainability Score** - Farm sustainability assessment
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
- `GET /` - Root endpoint with all available endpoints
- `GET /health` - Health check with model status

### Disease Detection (Module A)
- `GET /api/v1/predict` - Web UI for testing predictions
- `POST /api/v1/predict` - Predict plant disease from image (38 classes)

### Crop Recommendation (Module B)
- `POST /api/v1/test/crop_recommendation` - Get crop recommendations based on soil, weather, NPK
- `GET /api/v1/test/crop_recommendation/health` - Check crop recommendation model status

### Smart Irrigation (Module C)
- `POST /api/v1/irrigation/predict` - Predict irrigation requirements (No/Medium/High)
- `GET /api/v1/irrigation/health` - Check irrigation model status
- `GET /api/v1/irrigation/info` - Get irrigation system information

### Weather Intelligence (Module D)
- `POST /api/v1/weather-intelligence` - Get actionable farming insights from weather + farm conditions
- `GET /api/v1/weather-intelligence/info` - Get system information and rules
- `GET /api/v1/weather-intelligence/sample-locations` - Get sample test locations

### Sustainability Score (Bonus Module)
- `POST /api/v1/sustainability/score` - Compute sustainability score (0-100)

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

## Weather-Based Intelligence

The Weather Intelligence module combines **real-time weather data** from Open-Meteo API with **farm conditions** to produce actionable farming recommendations.

### Data Source: Open-Meteo API
- **Free, open-source** weather API (no API key required)
- **Global coverage** with high accuracy
- Provides current weather, hourly forecasts (16 days), and daily forecasts
- Website: https://open-meteo.com/

### Rule-Based Decision Making

The system applies intelligent rules to generate recommendations:

#### Irrigation Rules:
- **Delay if rain likely**: Rain probability > 60% and amount > 5mm → "Delay irrigation - rain expected"
- **Urgent if critical**: Soil moisture < 30% and no rain → "URGENT irrigation required"
- **Monitor if moderate**: Moisture 30-50% with low rain → "Monitor and prepare"
- **No irrigation**: Moisture > 70% → "No irrigation needed"

#### Disease Risk Assessment:
- **High humidity (>70%)**: Increases fungal disease risk
- **Temperature 20-30°C + moisture**: Ideal for disease spread
- **Recent/forecast rainfall**: Increases disease spread risk
- **Existing disease + vulnerable stage**: Raises priority to CRITICAL
- **Risk score (0-100)** calculated from multiple factors

#### Example Request:
```bash
curl -X POST "http://localhost:8000/api/v1/weather-intelligence" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 28.6139,
    "longitude": 77.2090,
    "farm_conditions": {
      "crop_type": "Wheat",
      "growth_stage": "Flowering",
      "soil_moisture": 35,
      "has_irrigation": true,
      "disease_detected": false,
      "recent_fertilization": false
    },
    "forecast_days": 7
  }'
```

#### Example Response:
```json
{
  "success": true,
  "location": {"latitude": 28.6139, "longitude": 77.209, "elevation": 216},
  "weather_summary": {
    "current_temp": 28.5,
    "current_humidity": 65.0,
    "forecast_rain_probability": 75.0,
    "forecast_rain_amount": 15.5
  },
  "irrigation_recommendation": "DELAY - Rain likely within 24 hours (75% chance, 15.5mm expected)",
  "disease_risk_level": "MEDIUM - Regular monitoring",
  "recommended_actions": [
    {
      "category": "irrigation",
      "priority": "high",
      "title": "Delay Irrigation - Rain Expected",
      "description": "Postpone irrigation for 24-48 hours",
      "reasoning": "Expected rainfall will provide natural irrigation",
      "timing": "Wait until after rainfall"
    }
  ],
  "risk_alerts": [
    {
      "risk_type": "Fungal Disease Risk",
      "severity": "medium",
      "description": "High humidity + rain creates ideal conditions",
      "prevention_tips": ["Monitor crop closely", "Ensure good drainage"]
    }
  ],
  "optimal_work_hours": ["06:00-07:00", "07:00-08:00", "16:00-17:00"]
}

## Model Information

The API integrates multiple AI/ML models for comprehensive agricultural intelligence:

### 1. Disease Detection - EfficientNet-B0
- **Architecture**: EfficientNet-B0 with custom classifier
- **Classes**: 38 plant disease categories
- **Input**: 224x224 RGB images
- **HuggingFace**: [Ahmadhaiwala/agro_model](https://huggingface.co/Ahmadhaiwala/agro_model)
- **Model File**: `plant_disease_efficientnet_b0_38class_best.pth`
- **Auto-download**: Model downloads from HuggingFace on first startup

### 2. Crop Recommendation - CatBoost
- **Algorithm**: CatBoost Classifier
- **Classes**: 57 different crops
- **Features**: 18 input features (soil, season, NPK, temperature, humidity, etc.)
- **Accuracy**: Training optimized (data leakage fixed)
- **Removed Features**: Crop-specific leaky features (CROPDURATION, SOWN, HARVESTED)
- **Model Files**: 
  - `crop_recommendation_catboost_fixed.cbm`
  - `crop_recommendation_metadata_fixed.joblib`

### 3. Smart Irrigation - RandomForest
- **Algorithm**: RandomForest Classifier
- **Classes**: 3 irrigation levels (No irrigation, Medium 15L/m², High 30L/m²)
- **Features**: 6 features (crop type, soil type, seedling stage, moisture, temp, humidity)
- **Accuracy**: 96.47% test accuracy, 95.17% cross-validation
- **Training Data**: 16,411 samples across 5 crops
- **Feature Importance**: Moisture (43.74%), Temperature (23.99%), Humidity (17.19%)
- **Model Files**:
  - `irrigation_randomforest.joblib`
  - `irrigation_metadata.joblib`
  - `label_encoders.joblib`

### 4. Weather Intelligence - Rule-Based System
- **Data Source**: Open-Meteo API (https://open-meteo.com/)
- **Type**: Rule-based decision engine
- **Coverage**: Global weather data
- **Rules**: 
  - Irrigation timing (4 main rules based on moisture & rain forecast)
  - Disease risk assessment (multi-factor scoring 0-100)
  - Work hour optimization
- **No API Key Required**: Free, open-source weather data

### 5. Sustainability Score - Formula-Based
- **Type**: Algorithmic calculation
- **Inputs**: Water efficiency, resource use, crop health
- **Output**: Score (0-100) with letter grade (A-F)
- **Formula**: Documented in `/report/SUSTAINABILITY_FORMULA.md`

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
│   │   └── sustainability/     # Sustainability score module (Bonus D)
│   │       ├── __init__.py
│   │       ├── router.py      # POST /sustainability/score
│   │       ├── service.py     # Scoring formula + suggestions
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

### Core Framework
- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation and settings management

### Machine Learning
- **PyTorch**: Deep learning framework for disease detection
- **TorchVision**: Computer vision utilities
- **CatBoost**: Gradient boosting for crop recommendation
- **scikit-learn**: Machine learning utilities and RandomForest

### Image Processing
- **Pillow**: Image loading and preprocessing
- **NumPy**: Numerical computations

### Weather Data
- **openmeteo-requests**: Client for Open-Meteo API
- **requests-cache**: Caching for API responses
- **retry-requests**: Automatic retry logic

### Utilities
- **HuggingFace Hub**: Model downloading
- **pandas**: Data manipulation
- **joblib**: Model serialization

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
