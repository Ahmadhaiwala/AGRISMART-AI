# Modules E & G Implementation Guide

Complete guide for Farmer Assistant (Module E) and Agentic Advisor (Module G)

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module E: Farmer Assistant](#module-e-farmer-assistant)
3. [Module G: Agentic Advisor](#module-g-agentic-advisor)
4. [Shared Components](#shared-components)
5. [API Reference](#api-reference)
6. [Testing](#testing)
7. [Configuration](#configuration)

---

## 🏗️ Architecture Overview

### Design Principles

✅ **CRITICAL RULES:**
- **Respect module boundaries** - Never duplicate functionality
- **LLM explains, rules decide** - Deterministic rules make decisions, LLM generates messages
- **Grounded context only** - Never fabricate missing information
- **Multilingual support** - English, Hindi, Gujarati

### Module Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                             │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌─────────────┐         ┌──────────────┐
│  Module E   │         │  Module G    │
│  Farmer     │         │  Agentic     │
│  Assistant  │         │  Advisor     │
└──────┬──────┘         └──────┬───────┘
       │                       │
       │  ┌────────────────────┤
       │  │                    │
       ▼  ▼                    ▼
   ┌────────────┐      ┌──────────────┐
   │ LLM Client │      │  Rule Engine │
   │ (OpenRouter│      │ (Deterministic)│
   │   /Qwen)   │      └──────┬───────┘
   └─────┬──────┘             │
         │                    │
         └────────┬───────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Farm Context   │
         │ Builder        │
         └────────┬───────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌──────────────┐   ┌──────────────┐
│ Existing     │   │ Existing     │
│ Modules      │   │ Modules      │
│ (A,B,C,D)    │   │ Services     │
└──────────────┘   └──────────────┘
```

---

## 🤖 Module E: Farmer Assistant

### Purpose
Conversational AI assistant that answers farmer questions in their native language using grounded farm data.

### Key Features
- **Multilingual**: English, Hindi (हिन्दी), Gujarati (ગુજરાતી)
- **Grounded**: Uses real farm data, never invents information
- **Contextual**: Integrates data from all other modules
- **Explanatory**: Explains existing module recommendations

### File Structure

```
farmer_assistant/
├── __init__.py          # Package initialization
├── router.py            # POST /api/v1/assistant/chat
├── service.py           # Business logic, LLM interaction
├── schemas.py           # Request/Response models
└── prompts.py           # System prompts (EN/HI/GU)
```

### Service Flow

```python
# 1. Receive chat request
ChatRequest {
    question: str
    language: "en" | "hi" | "gu"
    farm_id: str
    context: Dict (optional)
}

# 2. Build farm context
context = create_farm_context(
    farm_id=farm_id,
    **context_data  # Calls existing modules if needed
)

# 3. Select language-specific prompt
system_prompt = get_prompt_by_language(language)

# 4. Build user message
user_message = f"{context.to_text()}\n\nQuestion: {question}"

# 5. Call LLM
answer = llm_client.chat(
    system_prompt=system_prompt,
    user_message=user_message
)

# 6. Return response
ChatResponse {
    answer: str
    language: str
    context_used: bool
    timestamp: str
}
```

### Example Usage

**English:**
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Should I irrigate my tomato crop today?",
    "language": "en",
    "farm_id": "farm_001",
    "context": {
      "crop_name": "Tomato",
      "soil_moisture": 28,
      "rain_probability": 85
    }
  }'
```

**Hindi:**
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "क्या मुझे आज सिंचाई करनी चाहिए?",
    "language": "hi",
    "farm_id": "farm_001",
    "context": {
      "crop_name": "टमाटर",
      "soil_moisture": 28,
      "rain_probability": 85
    }
  }'
```

**Gujarati:**
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "આજે પાણી આપવું જોઈએ?",
    "language": "gu",
    "farm_id": "farm_001",
    "context": {
      "crop_name": "ટામેટા",
      "soil_moisture": 28,
      "rain_probability": 85
    }
  }'
```

---

## 🤖 Module G: Agentic Advisor

### Purpose
Autonomous agent that monitors farm conditions and generates proactive recommendations using deterministic rules.

### Key Features
- **Autonomous**: Runs periodically or on-demand
- **Rule-Based**: 100% deterministic decision-making
- **Proactive**: Generates notifications before problems occur
- **LLM-Enhanced**: Uses LLM only for farmer-friendly explanations

### File Structure

```
agentic_advisor/
├── __init__.py          # Package initialization
├── router.py            # POST /agent/run/{farm_id}, GET /agent/status/{farm_id}
├── agent.py             # Main agent loop (OBSERVE→ANALYZE→DECIDE→ACT→NOTIFY)
├── rules.py             # Deterministic decision rules
├── notifier.py          # Notification system (in-memory)
└── schemas.py           # Agent data models
```

### Agent Loop

```
┌──────────────┐
│  1. OBSERVE  │  Gather farm context
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  2. ANALYZE  │  Apply deterministic rules
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  3. DECIDE   │  Determine action + priority
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  4. ACT      │  Generate farmer-friendly message (LLM)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  5. NOTIFY   │  Create/send notification
└──────────────┘
```

### Decision Rules

#### 1. Irrigation Rules
```python
# Rule: Skip irrigation if rain likely
if rain_probability > 70% and rain_amount > 5:
    return SKIP_IRRIGATION

# Rule: Urgent irrigation if critical moisture
if soil_moisture < 25% and rain_probability < 30%:
    return URGENT_IRRIGATION

# Rule: Prepare irrigation if moderate
if 25% <= soil_moisture < 50% and rain_probability < 50%:
    return PREPARE_IRRIGATION

# Default: Monitor
return MONITOR
```

#### 2. Disease Rules
```python
# Rule: Urgent treatment if high confidence
if disease_detected and confidence > 0.80 and not is_healthy:
    return DISEASE_TREATMENT

# Rule: Monitor if low confidence
if disease_detected and 0.50 < confidence <= 0.80:
    return MONITOR_DISEASE

# Default: No action
return NO_ACTION
```

#### 3. Harvest Rules
```python
# Rule: Harvest ready
if growth_stage == "Maturity" and rain_probability < 40%:
    return HARVEST_READY

# Rule: Delay harvest if rain
if growth_stage == "Maturity" and rain_probability >= 40%:
    return DELAY_HARVEST

# Default: Not ready
return NOT_READY
```

### Example Usage

**Execute Agent:**
```bash
curl -X POST "http://localhost:8000/api/v1/agent/run/farm_001" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_name": "Tomato",
    "growth_stage": "Flowering",
    "soil_moisture": 28,
    "rain_probability": 85,
    "disease_detected": "Early Blight",
    "disease_confidence": 0.91
  }'
```

**Response:**
```json
{
  "success": true,
  "farm_id": "farm_001",
  "timestamp": "2024-01-15T10:30:00",
  "observation": {
    "context_summary": "Tomato crop at Flowering stage..."
  },
  "analysis": {
    "rules_evaluated": 3,
    "rules_triggered": ["skip_irrigation", "disease_treatment"]
  },
  "decision": {
    "action": "SKIP_IRRIGATION",
    "reason": "High rain probability (85%) makes irrigation unnecessary",
    "priority": "high",
    "confidence": 0.95
  },
  "action_taken": {
    "message_generated": true,
    "llm_used": true,
    "message": "🌧️ Good news! No need to irrigate today. Heavy rain expected (85% chance, 12mm). Your tomato crop will get natural watering. Save water and energy!"
  },
  "notification": {
    "notification_id": "notif_20240115_103000_farm_001",
    "title": "Irrigation Recommendation",
    "message": "Delay irrigation - rain expected soon...",
    "priority": "high",
    "created_at": "2024-01-15T10:30:00",
    "status": "pending"
  }
}
```

**Get Status:**
```bash
curl -X GET "http://localhost:8000/api/v1/agent/status/farm_001"
```

---

## 🔧 Shared Components

### 1. LLM Client (`core/llm_client.py`)

```python
from core.llm_client import llm_client

# Basic chat
answer = llm_client.chat(
    system_prompt="You are an agricultural advisor",
    user_message="Should I irrigate today?",
    temperature=0.7,
    max_tokens=500
)

# Generate explanation
explanation = llm_client.generate_explanation(
    decision="Skip irrigation",
    reason="High rain probability",
    context={"rain_prob": 85}
)
```

### 2. Farm Context Builder (`core/farm_context.py`)

```python
from core.farm_context import create_farm_context

# Build context
context = create_farm_context(
    farm_id="farm_001",
    crop_name="Tomato",
    soil_moisture=28,
    temperature=31,
    rain_probability=85
)

# Get as dict
data = context.get_context()

# Get as human-readable text
text = context.to_text()
```

---

## 📚 API Reference

### Farmer Assistant

#### POST `/api/v1/assistant/chat`

**Request:**
```json
{
  "question": "string (required)",
  "language": "en|hi|gu (required)",
  "farm_id": "string (required)",
  "context": {
    "crop_name": "string (optional)",
    "soil_moisture": "number (optional)",
    "temperature": "number (optional)",
    "...": "... (any farm data)"
  }
}
```

**Response:**
```json
{
  "answer": "string",
  "language": "string",
  "context_used": "boolean",
  "timestamp": "string (ISO 8601)"
}
```

**Status Codes:**
- `200` - Success
- `422` - Validation error (invalid request)
- `500` - Server error (LLM failure, etc.)

### Agentic Advisor

#### POST `/api/v1/agent/run/{farm_id}`

**Path Parameters:**
- `farm_id` - Unique farm identifier

**Request Body:**
```json
{
  "crop_name": "string (optional)",
  "growth_stage": "string (optional)",
  "soil_moisture": "number (optional)",
  "rain_probability": "number (optional)",
  "disease_detected": "string (optional)",
  "disease_confidence": "number (optional)",
  "...": "... (any farm data)"
}
```

**Response:** See example in Module G section above

#### GET `/api/v1/agent/status/{farm_id}`

**Path Parameters:**
- `farm_id` - Unique farm identifier

**Response:**
```json
{
  "farm_id": "string",
  "has_status": "boolean",
  "last_decision": {
    "action": "string",
    "priority": "string",
    "timestamp": "string"
  },
  "last_notification": {
    "title": "string",
    "message": "string",
    "status": "string"
  }
}
```

---

## 🧪 Testing

### Running Tests

```bash
# Make sure server is running
python -m uvicorn app.main:app --reload

# In another terminal, run tests
python test_assistant_and_agent.py
```

### Test Scenarios Covered

#### Farmer Assistant:
1. ✅ English irrigation question
2. ✅ Hindi disease question
3. ✅ Gujarati general question
4. ✅ Minimal context handling

#### Agentic Advisor:
1. ✅ Skip irrigation (rain expected)
2. ✅ Urgent irrigation (low moisture)
3. ✅ Disease treatment (high confidence)
4. ✅ Harvest ready (mature stage)
5. ✅ Monitor only (normal conditions)

#### Status Retrieval:
1. ✅ Get status for multiple farms
2. ✅ Handle missing status gracefully

### Manual Testing with cURL

See API Reference section for curl examples.

---

## ⚙️ Configuration

### Environment Variables

Add to `.env` file:

```bash
# LLM Settings (Required for Modules E & G)
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=qwen/qwen-2-7b-instruct:free
```

### Getting OpenRouter API Key

1. Visit: https://openrouter.ai/keys
2. Sign up / Log in
3. Create new API key
4. Copy to `.env` file

### Supported Models

Default: `qwen/qwen-2-7b-instruct:free` (Free tier)

Alternative models (paid):
- `qwen/qwen-2-7b-instruct` - Standard Qwen
- `anthropic/claude-3-haiku` - Fast, affordable
- `meta-llama/llama-3-8b-instruct` - Open source

### Cost Considerations

**Free Tier** (`qwen/qwen-2-7b-instruct:free`):
- ✅ No cost
- ✅ Good quality
- ⚠️ Rate limited
- ⚠️ May have queuing delays

**Paid Tier**:
- Typical cost: $0.001 - $0.01 per request
- No queuing
- Higher rate limits

---

## 🔄 Optional Enhancements

### 1. Scheduled Agent Execution

Add periodic agent runs using APScheduler:

```python
# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from app.modules.agentic_advisor.agent import get_agent

scheduler = BackgroundScheduler()

def run_agent_for_all_farms():
    agent = get_agent()
    farm_ids = ["farm_001", "farm_002", "farm_003"]
    for farm_id in farm_ids:
        agent.run(farm_id)

# Run every hour
scheduler.add_job(run_agent_for_all_farms, 'interval', hours=1)
scheduler.start()
```

### 2. SMS/Email Notifications

Replace in-memory store with real notification service:

```python
# notifier.py
import twilio  # or sendgrid, etc.

def send_notification(notification):
    # Send SMS
    client = twilio.rest.Client(account_sid, auth_token)
    client.messages.create(
        to=farmer_phone,
        from_=twilio_phone,
        body=notification.message
    )
```

### 3. Database Storage

Store agent decisions and notifications in database:

```python
# models.py
from sqlalchemy import Column, String, DateTime, JSON

class AgentDecision(Base):
    __tablename__ = "agent_decisions"
    
    id = Column(String, primary_key=True)
    farm_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    context = Column(JSON)
    timestamp = Column(DateTime, nullable=False)
```

---

## 📝 Summary

### Module E (Farmer Assistant)
- ✅ Multilingual AI chat
- ✅ Grounded in real data
- ✅ Calls existing module services
- ✅ Never fabricates information

### Module G (Agentic Advisor)
- ✅ Autonomous decision-making
- ✅ Rule-based (deterministic)
- ✅ LLM-enhanced explanations
- ✅ Proactive notifications

### Shared Components
- ✅ LLM Client (OpenRouter/Qwen)
- ✅ Farm Context Builder
- ✅ Respects module boundaries
- ✅ Clean, maintainable architecture

---

## 🚀 Next Steps

1. ✅ Start backend server
2. ✅ Configure OPENROUTER_API_KEY
3. ✅ Run test script
4. ✅ Test via Swagger UI (/docs)
5. ⏭️ Integrate with frontend
6. ⏭️ Add scheduling (optional)
7. ⏭️ Add real notifications (optional)
8. ⏭️ Add database storage (optional)

---

**Questions or Issues?**  
Check `/docs` endpoint for interactive API testing or review the test script for working examples.
