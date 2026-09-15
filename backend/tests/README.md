# Tests

Comprehensive test suite for Agrismart-AI backend modules.

---

## 🧪 Test Files

### Module Tests

#### `test_assistant_and_agent.py`
Tests for **Modules E & G** (Farmer Assistant & Agentic Advisor)
- ✅ Multilingual chat (English, Hindi, Gujarati)
- ✅ Agent decision scenarios
- ✅ Rule-based recommendations
- ✅ Status retrieval

**Run:** `python tests/test_assistant_and_agent.py`

#### `test_weather_intelligence.py`
Tests for **Module D** (Weather Intelligence)
- ✅ Weather data fetching
- ✅ Rule-based irrigation decisions
- ✅ Disease risk assessment
- ✅ Multiple locations

**Run:** `python tests/test_weather_intelligence.py`

#### `test_crop_api.py`
Tests for **Module B** (Crop Recommendation)
- ✅ Crop recommendation predictions
- ✅ Model health checks
- ✅ Feature validation

**Run:** `python tests/test_crop_api.py`

#### `test_irrigation_api.py`
Tests for **Module C** (Smart Irrigation)
- ✅ Irrigation predictions
- ✅ Model health checks
- ✅ Feature validation

**Run:** `python tests/test_irrigation_api.py`

#### `test_weather_rules.py`
Tests for weather-based rule engine
- ✅ Irrigation rule logic
- ✅ Disease risk calculations
- ✅ Edge cases

**Run:** `python tests/test_weather_rules.py`

### Comprehensive Tests

#### `test_all_modules_comprehensive.py`
Complete end-to-end tests for all modules
- ✅ All API endpoints
- ✅ Integration scenarios
- ✅ Error handling

**Run:** `python tests/test_all_modules_comprehensive.py`

#### `test_all_modules.py`
Quick sanity tests for all modules
- ✅ Health checks
- ✅ Basic functionality

**Run:** `python tests/test_all_modules.py`

### Framework Tests

#### `test_main.py`
FastAPI application tests
- ✅ Root endpoint
- ✅ Health endpoint
- ✅ Router registration

**Run:** `pytest tests/test_main.py`

#### `test_sustainability.py`
Sustainability module tests
- ✅ Score calculation
- ✅ Grade assignment
- ✅ Formula correctness

**Run:** `pytest tests/test_sustainability.py`

---

## 🚀 Running Tests

### Prerequisites
```bash
# Start the backend server first (for API tests)
cd backend
python -m uvicorn app.main:app --reload

# In another terminal...
cd backend
```

### Run All Tests
```bash
# Run pytest tests
pytest tests/ -v

# Run standalone test scripts
python tests/test_assistant_and_agent.py
python tests/test_weather_intelligence.py
python tests/test_crop_api.py
python tests/test_irrigation_api.py
```

### Run Specific Test
```bash
# Single test file
pytest tests/test_sustainability.py -v

# Single test script
python tests/test_assistant_and_agent.py
```

---

## 📋 Test Coverage

### Modules Tested
- ✅ Module A: Disease Detection
- ✅ Module B: Crop Recommendation
- ✅ Module C: Smart Irrigation
- ✅ Module D: Weather Intelligence
- ✅ Module E: Farmer Assistant
- ✅ Module G: Agentic Advisor
- ✅ Bonus: Sustainability Score

### Test Types
- ✅ Unit tests (rule logic, calculations)
- ✅ Integration tests (API endpoints)
- ✅ End-to-end tests (complete workflows)
- ✅ Multilingual tests (EN/HI/GU)

---

## 🔧 Configuration

### Required Environment Variables
```bash
# For Modules E & G tests
OPENROUTER_API_KEY=your_api_key_here
```

### Test Server
Most tests expect the backend running on:
```
http://localhost:8000
```

---

## 📊 Test Scenarios

### Farmer Assistant (Module E)
1. English irrigation question
2. Hindi disease question
3. Gujarati general question
4. Minimal context handling

### Agentic Advisor (Module G)
1. Skip irrigation (rain expected)
2. Urgent irrigation (low moisture)
3. Disease treatment (high confidence)
4. Harvest ready (mature stage)
5. Monitor only (normal conditions)

### Weather Intelligence (Module D)
1. Rain scenario (delay irrigation)
2. Dry scenario (urgent irrigation)
3. Disease risk assessment
4. Multiple locations

### Crop Recommendation (Module B)
1. Wheat recommendation
2. Rice recommendation
3. Multiple soil types
4. Different seasons

### Smart Irrigation (Module C)
1. No irrigation needed
2. Medium irrigation
3. High irrigation
4. Various crops

---

## ✅ Expected Results

### Successful Test Run
```
🚀 AGRISMART AI - TESTS
========================

✅ Health check passed
✅ Module E: 4/4 tests passed
✅ Module G: 5/5 tests passed
✅ Module D: 3/3 tests passed
✅ Module B: 4/4 tests passed
✅ Module C: 3/3 tests passed

========================
ALL TESTS PASSED
```

### Common Issues

**Problem**: Connection refused
**Solution**: Start backend server first

**Problem**: OpenRouter API error
**Solution**: Check OPENROUTER_API_KEY in .env

**Problem**: Model not loaded
**Solution**: Ensure model files are in models/ directory

---

## 🧹 Test Maintenance

### Adding New Tests
1. Create test file: `test_<module_name>.py`
2. Add to this README
3. Update test coverage section
4. Document expected results

### Test Naming Convention
- Unit tests: `test_<function>_<scenario>.py`
- Integration tests: `test_<module>_api.py`
- E2E tests: `test_all_modules*.py`

---

## 📝 Notes

### Test Data
- Uses realistic farm scenarios
- Covers edge cases
- Tests all supported languages
- Tests error conditions

### Performance
- API tests depend on network (OpenRouter, Open-Meteo)
- Free tier may have delays
- Some tests may timeout with free tier

### Dependencies
- Requires backend server running
- Requires internet connection (for LLM/weather APIs)
- Requires valid API keys

---

## 🔗 Related Documentation

- **[Quick Start Guide](../docs/QUICKSTART_E_G.md)** - Setup instructions
- **[Implementation Guide](../docs/implementation/MODULES_E_G_GUIDE.md)** - Technical details
- **[Main README](../README.md)** - Complete documentation

---

**Test Suite Version**: 1.0.0  
**Last Updated**: 2024
