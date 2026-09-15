"""
Disease detection router
Handles HTTP requests for plant disease prediction
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict
import logging

from app.modules.disease_detection.service import disease_detection_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/predict", response_class=HTMLResponse)
async def predict_interface():
    """
    HTML interface for testing image predictions
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agrismart AI - Plant Disease Detection</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5rem;
            }
            
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                background: #f8f9ff;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 20px;
            }
            
            .upload-area:hover {
                border-color: #764ba2;
                background: #f0f2ff;
            }
            
            .upload-area.dragover {
                border-color: #764ba2;
                background: #e8ebff;
            }
            
            .upload-icon {
                font-size: 4rem;
                margin-bottom: 15px;
            }
            
            #fileInput {
                display: none;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 10px;
                font-size: 1.1rem;
                cursor: pointer;
                transition: transform 0.2s;
                display: inline-block;
                margin-top: 10px;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }
            
            .preview-container {
                margin: 20px 0;
                text-align: center;
                display: none;
            }
            
            .preview-image {
                max-width: 100%;
                max-height: 400px;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            
            .results {
                margin-top: 30px;
                display: none;
            }
            
            .result-card {
                background: #f8f9ff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
            }
            
            .result-header {
                font-size: 1.3rem;
                color: #667eea;
                margin-bottom: 10px;
                font-weight: bold;
            }
            
            .prediction-item {
                background: white;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .class-name {
                font-weight: 600;
                color: #333;
            }
            
            .confidence {
                background: #667eea;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
            }
            
            .loading {
                display: none;
                text-align: center;
                margin: 20px 0;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .error {
                background: #fee;
                border: 2px solid #fcc;
                color: #c33;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Agrismart AI</h1>
            <p class="subtitle">Plant Disease Detection System</p>
            
            <div class="upload-area" id="uploadArea" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📸</div>
                <h3>Click or drag image here</h3>
                <p>Supports JPG, JPEG, PNG (max 10MB)</p>
                <input type="file" id="fileInput" accept="image/jpeg,image/jpg,image/png">
            </div>
            
            <div class="preview-container" id="previewContainer">
                <img id="previewImage" class="preview-image" alt="Preview">
                <br>
                <button class="btn" id="predictBtn" onclick="predictDisease()">Analyze Plant 🔍</button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing image...</p>
            </div>
            
            <div class="error" id="error"></div>
            
            <div class="results" id="results">
                <div class="result-card">
                    <div class="result-header">🎯 Top Prediction</div>
                    <div class="prediction-item" style="background: #e8f5e9;">
                        <span class="class-name" id="topClass"></span>
                        <span class="confidence" id="topConfidence" style="background: #4caf50;"></span>
                    </div>
                </div>
                
                <div class="result-card">
                    <div class="result-header">📊 Top 5 Predictions</div>
                    <div id="top5Predictions"></div>
                </div>
            </div>
        </div>
        
        <script>
            let selectedFile = null;
            
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const previewContainer = document.getElementById('previewContainer');
            const previewImage = document.getElementById('previewImage');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const errorDiv = document.getElementById('error');
            
            // File input change
            fileInput.addEventListener('change', handleFileSelect);
            
            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    fileInput.files = e.dataTransfer.files;
                    handleFileSelect({ target: fileInput });
                }
            });
            
            function handleFileSelect(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                selectedFile = file;
                
                // Show preview
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImage.src = e.target.result;
                    previewContainer.style.display = 'block';
                    results.style.display = 'none';
                    errorDiv.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
            
            async function predictDisease() {
                if (!selectedFile) return;
                
                // Hide previous results and errors
                results.style.display = 'none';
                errorDiv.style.display = 'none';
                loading.style.display = 'block';
                
                // Create form data
                const formData = new FormData();
                formData.append('file', selectedFile);
                
                try {
                    const response = await fetch('/api/v1/predict', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        displayResults(data);
                    } else {
                        throw new Error(data.detail || 'Prediction failed');
                    }
                } catch (error) {
                    showError(error.message);
                } finally {
                    loading.style.display = 'none';
                }
            }
            
            function displayResults(data) {
                const prediction = data.prediction;
                
                // Top prediction
                document.getElementById('topClass').textContent = formatClassName(prediction.predicted_class);
                document.getElementById('topConfidence').textContent = (prediction.confidence * 100).toFixed(2) + '%';
                
                // Top 5 predictions
                const top5Container = document.getElementById('top5Predictions');
                top5Container.innerHTML = '';
                
                prediction.top5_predictions.forEach((pred, index) => {
                    const item = document.createElement('div');
                    item.className = 'prediction-item';
                    item.innerHTML = `
                        <span class="class-name">${index + 1}. ${formatClassName(pred.class)}</span>
                        <span class="confidence">${(pred.confidence * 100).toFixed(2)}%</span>
                    `;
                    top5Container.appendChild(item);
                });
                
                results.style.display = 'block';
            }
            
            function formatClassName(className) {
                return className.replace(/_/g, ' ').replace(/___/g, ' - ');
            }
            
            function showError(message) {
                errorDiv.textContent = '❌ Error: ' + message;
                errorDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post("/predict")
async def predict_disease(file: UploadFile = File(...)) -> Dict:
    """
    Predict plant disease from uploaded image
    
    Args:
        file: Uploaded image file (JPEG, PNG)
        
    Returns:
        Prediction results with confidence scores
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Call service
        result = await disease_detection_service.predict_from_file(file_content, file.filename)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in prediction endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/model/info")
async def get_model_info() -> Dict:
    """Get information about the loaded model"""
    return disease_detection_service.get_model_info()


@router.post("/model/reload")
async def reload_model() -> Dict:
    """Reload the model (admin endpoint)"""
    try:
        return disease_detection_service.reload_model()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diseases")
async def get_all_diseases() -> Dict:
    """Get list of all detectable diseases"""
    return await disease_detection_service.get_all_diseases()
