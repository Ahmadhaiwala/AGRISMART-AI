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

## Project Structure

```
backend/
├── .venv/              # Virtual environment (not in git)
├── main.py             # Main application entry point
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **PyTorch**: Deep learning framework
- **TorchVision**: Computer vision models and utilities
- **Pillow**: Image processing library
- **NumPy**: Numerical computing library

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
