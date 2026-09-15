# Integrated Sustainability Score

Complete guide to the enhanced Sustainability module that integrates with all other modules.

---

## 🎯 Overview

The **Integrated Sustainability Score** automatically gathers data from multiple modules to compute a comprehensive sustainability assessment:

- **Smart Irrigation (Module C)** → Water requirements
- **Weather Intelligence (Module D)** → Weather recommendations
- **Disease Detection (Module A)** → Crop health status

This eliminates manual data entry and provides real-time sustainability scoring based on actual farm conditions.

---

## 🔄 Two Modes

### Mode 1: Manual (Original)
**Endpoint**: `POST /api/v1/sustainability/score`

Requires all values to be provided manually:
- Water used vs required
- Fertilizer used vs recommended
- Pesticide used vs recommended
- Crop health status

**Use when**: You have all values already calculated.

### Mode 2: Integrated (New)
**Endpoint**: `POST /api/v1/sustainability/score/integrated`

Automatically calls other modules to gather data:
- Calls Smart Irrigation to calculate water requirements
- Calls Weather Intelligence for recommendations
- Uses Disease Detection results for crop health

**Use when**: You want automatic data gathering and comprehensive analysis.

---

## 📊 How Integration Works

```
┌─────────────────────────────────────────────────────────┐
│         INTEGRATED SUSTAINABILITY REQUEST               │
│  (farm data + resource usage + location)                │
└────────────────┬────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌──────────────┐      ┌──────────────┐
│   Module C   │      │   Module D   │
│    Smart     │      │   Weather    │
│  Irrigation  │      │ Intelligence │
└──────┬───────┘      └──────┬───────┘
       │                     │
       │  Water Requirements │
       │  (based on soil,    │
       │   weather, crop)    │
       └──────────┬──────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Sustainability │
         │    Scoring     │
         │    Engine      │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │  Score + Grade │
         │  + Suggestions │
         │  + Module Data │
         └────────────────┘
```

---

## 🔧 API Reference

### Integrated Endpoint

**POST** `/api/v1/sustainability/score/integrated`

#### Request Body

```json
{
  // Farm identification
  "farm_id": "farm_001",
  
  // Crop information (for Module C)
  "crop_name": "Tomato",
  "growth_stage": "Flowering",
  
  // Soil information (for Module C)
  "soil_moisture": 45,
  "soil_type": "Loamy",
  "seedling_stage": 2,
  
  // Location (for Module D)
  "latitude": 28.6139,
  "longitude": 77.2090,
  
  // Weather (for Modules C & D)
  "temperature": 28,
  "humidity": 65,
  
  // Disease detection (from Module A)
  "disease_detected": "Early Blight",
  "disease_confidence": 0.91,
  "is_healthy": false,
  
  // Actual resource usage (farmer input)
  "water_used_liters": 1500,
  "fertilizer_used_kg": 4,
  "pesticide_used_kg": 0.5,
  "pesticide_recommended_kg": 0.3,
  
  // Configuration
  "has_irrigation": true
}
```

#### Response

```json
{
  "success": true,
  "overall_score": 72.5,
  "grade": "B",
  
  "sub_scores": {
    "water_efficiency": 85.7,
    "resource_use": 75.0,
    "crop_health": 9.0
  },
  
  "suggestions": [
    "Disease detected with meaningful confidence -- apply the recommended precaution promptly to prevent spread.",
    "Consider reducing pesticide use slightly to match recommendations."
  ],
  
  // Integration details
  "modules_used": [
    "Smart Irrigation",
    "Weather Intelligence",
    "Disease Detection"
  ],
  
  "irrigation_recommendation": {
    "irrigation_required": 1,
    "irrigation_level": "Medium (15 L/m²)",
    "confidence": 0.85,
    "explanation": "Moderate soil moisture requires medium irrigation"
  },
  
  "weather_recommendation": {
    "irrigation": "PROCEED - No rain expected in next 24 hours",
    "disease_risk": "HIGH - Monitor closely",
    "recommended_actions": [
      "Apply irrigation within next 12 hours",
      "Monitor for disease spread",
      "Ensure good drainage"
    ]
  },
  
  "crop_health_details": {
    "disease": "Early Blight",
    "confidence": 0.91,
    "is_healthy": false
  },
  
  "formula_version": "1.0"
}
```

---

## 📋 Scoring Formula

### Components (unchanged from original)

1. **Water Efficiency (40% weight)**
   ```
   efficiency = 100 * (1 - |used - required| / required)
   ```
   - Penalizes both over-watering and under-watering
   - Optimal when `used == required`

2. **Resource Use (30% weight)**
   ```
   efficiency = average(fertilizer_efficiency, pesticide_efficiency)
   ```
   - Each calculated same as water efficiency
   - Encourages optimal resource application

3. **Crop Health (30% weight)**
   ```
   health = 100 if healthy
   health = 100 * (1 - disease_confidence) if diseased
   ```
   - Full score for healthy crops
   - Reduced based on disease confidence

### Overall Score
```
score = 0.4 * water_efficiency + 0.3 * resource_use + 0.3 * crop_health
```

### Grades
- **A**: 80-100 (Excellent sustainability)
- **B**: 60-79 (Good sustainability)
- **C**: 40-59 (Fair sustainability)
- **D**: 0-39 (Poor sustainability)

---

## 🧪 Testing

### Run Integrated Tests

```bash
python tests/test_sustainability_integrated.py
```

### Test Scenarios Covered

1. **Good Sustainability** (A/B grade)
   - Efficient water use
   - Healthy crop
   - Optimal fertilizer

2. **Poor Sustainability** (C/D grade)
   - Over-watering
   - Disease detected
   - Excessive fertilizer/pesticide

3. **Medium Sustainability** (B/C grade)
   - Under-watering
   - Healthy crop
   - Room for improvement

4. **Optimal Sustainability** (A grade)
   - Perfect water balance
   - Minimal pesticide
   - Healthy crop

---

## 🔍 Module Integration Details

### Smart Irrigation (Module C)

**What it provides**:
- Water requirements based on:
  - Crop type and growth stage
  - Soil moisture and type
  - Temperature and humidity
  - Seedling stage

**How it's used**:
- Calls irrigation prediction API
- Converts irrigation level to liters:
  - Level 0 (None): 0 L
  - Level 1 (Medium): 15 L/m²
  - Level 2 (High): 30 L/m²
- Assumes 100 m² plot (configurable)

**Fallback**:
- If module unavailable: uses water_used_liters as baseline

### Weather Intelligence (Module D)

**What it provides**:
- Weather-based recommendations:
  - Irrigation timing advice
  - Disease risk assessment
  - Optimal work hours

**How it's used**:
- Calls weather intelligence API with:
  - Location (lat/long)
  - Farm conditions
  - Forecast period (7 days)
- Extracts key recommendations

**Fallback**:
- If module unavailable: continues without weather data

### Disease Detection (Module A)

**What it provides**:
- Disease classification
- Confidence score
- Health status

**How it's used**:
- Uses detection results from request
- Calculates crop health score
- Affects overall sustainability

**Note**: Detection happens before this API call

---

## 💡 Example Use Cases

### Use Case 1: Post-Irrigation Assessment

After irrigating, farmer wants to know sustainability:

```bash
curl -X POST "http://localhost:8000/api/v1/sustainability/score/integrated" \
  -H "Content-Type: application/json" \
  -d '{
    "farm_id": "farm_001",
    "crop_name": "Tomato",
    "growth_stage": "Flowering",
    "soil_moisture": 55,
    "soil_type": "Loamy",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "temperature": 28,
    "humidity": 65,
    "is_healthy": true,
    "water_used_liters": 1500,
    "fertilizer_used_kg": 4,
    "has_irrigation": true,
    "seedling_stage": 2
  }'
```

**Result**: Gets comprehensive score with recommendations from all modules.

### Use Case 2: Disease Outbreak Assessment

After detecting disease, check sustainability impact:

```bash
curl -X POST "http://localhost:8000/api/v1/sustainability/score/integrated" \
  -H "Content-Type: application/json" \
  -d '{
    "farm_id": "farm_002",
    "crop_name": "Potato",
    "disease_detected": "Late Blight",
    "disease_confidence": 0.94,
    "is_healthy": false,
    "water_used_liters": 2000,
    "pesticide_used_kg": 2,
    "pesticide_recommended_kg": 0.5,
    ...
  }'
```

**Result**: Shows how disease affects sustainability + treatment recommendations.

### Use Case 3: Weekly Sustainability Report

Generate weekly report for multiple farms:

```python
import requests

farms = ["farm_001", "farm_002", "farm_003"]

for farm_id in farms:
    response = requests.post(
        "http://localhost:8000/api/v1/sustainability/score/integrated",
        json={
            "farm_id": farm_id,
            # ... farm data ...
        }
    )
    
    score = response.json()["overall_score"]
    grade = response.json()["grade"]
    print(f"{farm_id}: {score} ({grade})")
```

---

## ⚙️ Configuration

### Irrigation Area Calculation

Default assumes 100 m² plot. To change:

```python
# In service.py, line ~140
area_m2 = 100  # Change this value
```

### Crop ID Mapping

Supported crops for irrigation:
- Wheat (0)
- Chilli (1)
- Potato (2)
- Carrot (3)
- Tomato (4)

To add more crops:
```python
# In service.py, _get_crop_id method
crop_map = {
    "wheat": 0,
    "chilli": 1,
    "your_crop": 5,  # Add here
    ...
}
```

---

## 🚀 Best Practices

### 1. Use Disease Detection First
Always run disease detection before sustainability scoring:
```
1. Upload image → Disease Detection API
2. Get disease results
3. Pass to Sustainability API with other data
```

### 2. Provide Accurate Location
Weather recommendations depend on accurate coordinates:
- Use GPS coordinates from farm
- Ensure lat/long are correct format

### 3. Regular Monitoring
Check sustainability score:
- After each irrigation
- Weekly for trend analysis
- After disease treatment
- Before fertilizer application

### 4. Act on Suggestions
The API provides actionable suggestions:
- Review each suggestion
- Prioritize based on impact
- Track improvements over time

---

## 📈 Future Enhancements

Potential improvements:
1. **Database Storage**: Store scores over time for trends
2. **Crop Recommendation Integration**: Add crop-specific fertilizer recommendations
3. **Historical Analysis**: Compare current vs past performance
4. **Alerts**: Automatic alerts when score drops below threshold
5. **Multi-Farm Comparison**: Benchmark across multiple farms

---

## 🔗 Related Documentation

- **[Main README](../README.md)** - Complete project documentation
- **[Smart Irrigation](../app/modules/smart_irrigation/)** - Module C details
- **[Weather Intelligence](../app/modules/smart_weather_based_Intelligence/)** - Module D details
- **[Disease Detection](../app/modules/disease_detection/)** - Module A details

---

## ❓ FAQ

**Q: Can I use manual mode if one module is unavailable?**  
A: Yes, use `/sustainability/score` endpoint with manual values.

**Q: What happens if irrigation model isn't loaded?**  
A: Falls back to using provided water_used_liters as baseline.

**Q: Do I need weather API for this to work?**  
A: No, weather integration is optional. Scoring works without it.

**Q: Can I customize the scoring weights?**  
A: Yes, modify WATER_WEIGHT, RESOURCE_WEIGHT, HEALTH_WEIGHT in service.py.

**Q: How often should I check sustainability?**  
A: After major operations (irrigation, fertilization) or weekly for monitoring.

---

**Version**: 1.0  
**Last Updated**: 2024
