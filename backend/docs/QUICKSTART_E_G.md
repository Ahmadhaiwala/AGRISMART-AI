# Quick Start Guide - Modules E & G

Get up and running with Farmer Assistant and Agentic Advisor in 5 minutes.

---

## 🚀 Step 1: Get OpenRouter API Key (2 minutes)

1. Visit: **https://openrouter.ai/keys**
2. Sign up with Google/GitHub or create account
3. Click "Create Key"
4. Copy your API key (starts with `sk-or-...`)

**Cost**: Free tier available! Uses `qwen/qwen-2-7b-instruct:free`

---

## ⚙️ Step 2: Configure Environment (1 minute)

1. Create `.env` file in `backend/` directory:
   ```bash
   cd backend
   copy .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   OPENROUTER_MODEL=qwen/qwen-2-7b-instruct:free
   ```

3. Save the file

---

## ▶️ Step 3: Start Backend Server (1 minute)

```bash
# Make sure you're in the backend directory
cd backend

# Activate virtual environment (if not already active)
.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Linux/Mac

# Start server
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
🚀 LOADING ML MODELS
================================================================================
📊 Loading Crop Recommendation Model...
✅ Crop Recommendation Model loaded successfully

💧 Loading Smart Irrigation Model...
✅ Smart Irrigation Model loaded successfully
================================================================================
✅ STARTUP COMPLETE
================================================================================

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🧪 Step 4: Run Tests (1 minute)

Open **new terminal** (keep server running):

```bash
cd backend
python test_assistant_and_agent.py
```

**You should see:**
- ✅ Health check passing
- ✅ 4 Farmer Assistant tests (English, Hindi, Gujarati)
- ✅ 5 Agentic Advisor scenarios
- ✅ Status retrieval tests

---

## 🌐 Step 5: Try in Browser (30 seconds)

Visit: **http://localhost:8000/docs**

### Test Farmer Assistant:

1. Find `POST /api/v1/assistant/chat`
2. Click "Try it out"
3. Paste this example:
   ```json
   {
     "question": "Should I irrigate my tomato crop today?",
     "language": "en",
     "farm_id": "farm_001",
     "context": {
       "crop_name": "Tomato",
       "soil_moisture": 28,
       "rain_probability": 85
     }
   }
   ```
4. Click "Execute"
5. See AI response! 🎉

### Test Agentic Advisor:

1. Find `POST /api/v1/agent/run/{farm_id}`
2. Click "Try it out"
3. Enter `farm_001` in path parameter
4. Paste this example:
   ```json
   {
     "crop_name": "Tomato",
     "soil_moisture": 20,
     "rain_probability": 10,
     "temperature": 35
   }
   ```
5. Click "Execute"
6. See agent decision! 🤖

---

## 💡 Quick Examples

### Example 1: Ask in Hindi

```bash
curl -X POST "http://localhost:8000/api/v1/assistant/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "मेरे गेहूं की फसल के लिए क्या करूं?",
    "language": "hi",
    "farm_id": "farm_002"
  }'
```

### Example 2: Disease Alert

```bash
curl -X POST "http://localhost:8000/api/v1/agent/run/farm_003" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_name": "Potato",
    "disease_detected": "Late Blight",
    "disease_confidence": 0.95,
    "is_healthy": false
  }'
```

### Example 3: Check Status

```bash
curl http://localhost:8000/api/v1/agent/status/farm_001
```

---

## 🎯 What to Expect

### Farmer Assistant Response:
```json
{
  "answer": "Based on the high rain probability (85%), I recommend delaying irrigation for your tomato crop. The expected rainfall will provide natural watering, saving you water and energy. Monitor the situation after the rain.",
  "language": "en",
  "context_used": true,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### Agentic Advisor Response:
```json
{
  "success": true,
  "farm_id": "farm_001",
  "decision": {
    "action": "URGENT_IRRIGATION",
    "reason": "Critical soil moisture level (20%) and no rain expected",
    "priority": "critical",
    "confidence": 0.95
  },
  "notification": {
    "title": "⚠️ Urgent: Irrigation Needed",
    "message": "Your wheat crop needs immediate irrigation. Soil moisture is critically low (20%) and no rain is forecast. Irrigate within the next 24 hours to prevent crop stress.",
    "priority": "critical"
  }
}
```

---

## ❓ Troubleshooting

### Problem: "Cannot connect to backend server"
**Solution**: Make sure server is running on http://localhost:8000
```bash
python -m uvicorn app.main:app --reload
```

### Problem: "OPENROUTER_API_KEY not configured"
**Solution**: 
1. Check `.env` file exists in `backend/` directory
2. Check key is correctly formatted: `OPENROUTER_API_KEY=sk-or-v1-...`
3. Restart server after adding key

### Problem: "OpenRouter API error"
**Solutions**:
- Check API key is valid at https://openrouter.ai/keys
- Check you have credits (free tier should work)
- Wait a few seconds (free tier has rate limits)
- Try again - free tier may have queuing

### Problem: Test script fails
**Solution**:
1. Ensure server is running first
2. Check `OPENROUTER_API_KEY` in `.env`
3. Wait a few seconds between requests (rate limits)

### Problem: Module import errors
**Solution**:
```bash
# Make sure you're in backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version (need 3.8+)
python --version
```

---

## 📚 Next Steps

1. ✅ Read full guide: `MODULES_E_G_GUIDE.md`
2. ✅ Read implementation details: `IMPLEMENTATION_SUMMARY.md`
3. ✅ Read updated README: `README.md`
4. ✅ Test all scenarios in `test_assistant_and_agent.py`
5. ✅ Try different languages (en, hi, gu)
6. ✅ Test different weather scenarios
7. ✅ Integrate with frontend

---

## 🎓 Learning Resources

### Understanding the Code:
- **Core utilities**: `core/llm_client.py`, `core/farm_context.py`
- **Module E**: `app/modules/farmer_assistant/`
- **Module G**: `app/modules/agentic_advisor/`

### Key Files to Review:
1. `farmer_assistant/service.py` - Chat logic
2. `farmer_assistant/prompts.py` - Language prompts
3. `agentic_advisor/agent.py` - Agent loop
4. `agentic_advisor/rules.py` - Decision rules

---

## 💬 Example Conversations

### English (Irrigation):
```
Q: "Should I water my wheat crop today?"
A: "Based on current conditions (soil moisture 45%, rain probability 30%), your wheat crop has adequate moisture. You can skip irrigation today and monitor conditions. Consider irrigating in 2-3 days if no rain occurs."
```

### Hindi (Disease):
```
Q: "मेरे टमाटर के पत्तों पर धब्बे हैं। क्या करूं?"
A: "आपके टमाटर में Early Blight रोग का पता चला है (91% निश्चितता)। तुरंत फफूंदनाशक का छिड़काव करें। प्रभावित पत्तियों को हटा दें और खेत में जल निकासी सुनिश्चित करें।"
```

### Gujarati (General):
```
Q: "ટામેટાની સારી પેદાશ માટે શું કરવું?"
A: "ટામેટા માટે: જમીનની ભેજ 40-60% જાળવો, તાપમાન 20-30°C રાખો, નિયમિત NPK ખાતર આપો. હાલની સ્થિતિ (ભેજ 45%, તાપમાન 25°C) સારી છે. પાકની વૃદ્ધિ માટે આગળ વધતા રહો."
```

---

## 🔥 Advanced Usage

### Run Agent for Multiple Farms:
```python
# create_script.py
import requests

farms = ["farm_001", "farm_002", "farm_003"]

for farm_id in farms:
    response = requests.post(
        f"http://localhost:8000/api/v1/agent/run/{farm_id}",
        json={"crop_name": "Wheat", "soil_moisture": 35}
    )
    print(f"{farm_id}: {response.json()['decision']['action']}")
```

### Schedule Hourly Checks:
```python
# scheduler.py (optional enhancement)
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

def check_all_farms():
    # Your farm checking logic
    pass

scheduler = BlockingScheduler()
scheduler.add_job(check_all_farms, 'interval', hours=1)
scheduler.start()
```

---

## ✅ Success Checklist

After following this guide, you should be able to:

- [x] Start the backend server
- [x] See API documentation at /docs
- [x] Run the test script successfully
- [x] Ask questions in English via Farmer Assistant
- [x] Ask questions in Hindi via Farmer Assistant
- [x] Ask questions in Gujarati via Farmer Assistant
- [x] Execute agent decisions for irrigation
- [x] Execute agent decisions for disease treatment
- [x] Execute agent decisions for harvest timing
- [x] Retrieve agent status for farms
- [x] See farmer-friendly notifications

---

## 🎉 You're Ready!

Modules E & G are now fully operational. You can:
- Chat with farmers in their language
- Get autonomous farming recommendations
- Receive proactive alerts and notifications
- Integrate with your frontend application

**Questions?** Check the detailed guides:
- `MODULES_E_G_GUIDE.md` - Complete technical guide
- `IMPLEMENTATION_SUMMARY.md` - What was built
- `README.md` - Full project documentation

**Happy Farming! 🌾🚜**
