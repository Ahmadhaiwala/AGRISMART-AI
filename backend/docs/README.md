# Documentation

Complete documentation for the Agrismart-AI backend system.

---

## 📚 Quick Navigation

### Getting Started
- **[Quick Start Guide](QUICKSTART_E_G.md)** - Get Modules E & G running in 5 minutes
- **[Main README](../README.md)** - Complete project documentation
- **[Sustainability Integration](SUSTAINABILITY_INTEGRATION.md)** - Integrated sustainability scoring with all modules

### Implementation Guides
- **[Implementation Summary](implementation/IMPLEMENTATION_SUMMARY.md)** - Complete overview of Modules E & G
- **[Modules E & G Guide](implementation/MODULES_E_G_GUIDE.md)** - Technical deep dive
- **[Modules Summary](implementation/MODULES_SUMMARY.md)** - All modules overview

---

## 📖 Documentation Structure

```
docs/
├── README.md                           # This file - documentation index
├── QUICKSTART_E_G.md                   # 5-minute quick start guide
└── implementation/                     # Implementation details
    ├── IMPLEMENTATION_SUMMARY.md       # What was built, files created
    ├── MODULES_E_G_GUIDE.md           # Complete technical guide
    └── MODULES_SUMMARY.md             # All modules overview
```

---

## 🎯 What Should I Read?

### I want to use Modules E & G
👉 Start with **[QUICKSTART_E_G.md](QUICKSTART_E_G.md)**

### I want to understand the architecture
👉 Read **[MODULES_E_G_GUIDE.md](implementation/MODULES_E_G_GUIDE.md)**

### I want to see what was built
👉 Check **[IMPLEMENTATION_SUMMARY.md](implementation/IMPLEMENTATION_SUMMARY.md)**

### I want complete project info
👉 See **[Main README](../README.md)**

---

## 🗂️ Related Folders

### `/tests`
All test files for the backend modules:
- `test_assistant_and_agent.py` - Tests for Modules E & G
- `test_weather_intelligence.py` - Weather intelligence tests
- `test_crop_api.py` - Crop recommendation tests
- `test_irrigation_api.py` - Irrigation system tests
- And more...

### `/app/modules`
Source code for all backend modules:
- `disease_detection/` - Module A
- `crop_recommendation/` - Module B
- `smart_irrigation/` - Module C
- `smart_weather_based_Intelligence/` - Module D
- `farmer_assistant/` - Module E
- `agentic_advisor/` - Module G
- `sustainability/` - Bonus module

### `/core`
Shared utilities:
- `llm_client.py` - OpenRouter/Qwen integration
- `farm_context.py` - Context builder
- `model_loader.py` - ML model loading
- `image_utils.py` - Image preprocessing

---

## 📝 Documentation Coverage

### Modules Documented
- ✅ Module A: Disease Detection
- ✅ Module B: Crop Recommendation
- ✅ Module C: Smart Irrigation
- ✅ Module D: Weather Intelligence
- ✅ Module E: Farmer Assistant
- ✅ Module G: Agentic Advisor
- ✅ Bonus: Sustainability Score

### API Documentation
- ✅ All endpoints documented
- ✅ Request/response examples
- ✅ Error handling
- ✅ Interactive docs at `/docs`

### Architecture Documentation
- ✅ Module boundaries explained
- ✅ Data flow diagrams
- ✅ Decision rules documented
- ✅ LLM role clarified

---

## 🔗 External Resources

### API Reference
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Dependencies
- **OpenRouter**: https://openrouter.ai/docs
- **Open-Meteo**: https://open-meteo.com/en/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **PyTorch**: https://pytorch.org/docs/

---

## 🤝 Contributing

When adding new features:
1. Update relevant module documentation
2. Add API examples
3. Create/update test files
4. Update this documentation index

---

## 📧 Questions?

- Check the **[Main README](../README.md)** first
- Review **[QUICKSTART_E_G.md](QUICKSTART_E_G.md)** for setup issues
- See **[MODULES_E_G_GUIDE.md](implementation/MODULES_E_G_GUIDE.md)** for technical details
- Check `/tests` folder for working examples

---

**Last Updated**: 2024  
**Version**: 1.0.0
