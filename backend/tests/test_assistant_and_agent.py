"""
Test script for Farmer Assistant and Agentic Advisor modules
Tests multilingual chat, agent decision-making, and rule-based logic
"""

import requests
import json
import sys
from typing import Dict, Any

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


BASE_URL = "http://localhost:8000/api/v1"


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_response(response: requests.Response):
    """Pretty print API response"""
    try:
        data = response.json()
        print(f"\n✅ Status: {response.status_code}")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Raw response: {response.text}")


def test_farmer_assistant():
    """Test Farmer Assistant with multilingual questions"""
    print_section("TESTING FARMER ASSISTANT")
    
    # Test 1: English question about irrigation
    print("\n📝 Test 1: English - Irrigation question")
    request_data = {
        "message": "Should I irrigate my tomato crop today?",
        "language": "en",
        "farm_id": "farm_001",
        "crop_name": "Tomato",
        "growth_stage": "Flowering",
        "soil_moisture": 28
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant/chat",
        json=request_data,
        timeout=30
    )
    print_response(response)
    
    # Test 2: Hindi question about disease
    print("\n📝 Test 2: Hindi - Disease question")
    request_data = {
        "message": "मेरे टमाटर के पौधे पर धब्बे हैं। क्या करूं?",
        "language": "hi",
        "farm_id": "farm_002",
        "crop_name": "Tomato",
        "growth_stage": "Fruiting"
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant/chat",
        json=request_data,
        timeout=30
    )
    print_response(response)
    
    # Test 3: Gujarati question about general farming
    print("\n📝 Test 3: Gujarati - General question")
    request_data = {
        "message": "ટામેટાની સારી પેદાશ માટે શું કરવું?",
        "language": "gu",
        "farm_id": "farm_003",
        "crop_name": "Tomato",
        "growth_stage": "Vegetative",
        "soil_moisture": 45
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant/chat",
        json=request_data,
        timeout=30
    )
    print_response(response)
    
    # Test 4: English question with minimal context
    print("\n📝 Test 4: English - Question with minimal context")
    request_data = {
        "message": "What is the best time to harvest wheat?",
        "language": "en",
        "farm_id": "farm_004"
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant/chat",
        json=request_data,
        timeout=30
    )
    print_response(response)


def test_agentic_advisor():
    """Test Agentic Advisor with different scenarios"""
    print_section("TESTING AGENTIC ADVISOR")
    
    # Scenario 1: Skip irrigation due to rain
    print("\n📝 Scenario 1: Skip Irrigation (High rain probability)")
    context = {
        "crop_name": "Tomato",
        "growth_stage": "Flowering",
        "soil_moisture": 28,
        "soil_type": "Loamy",
        "temperature": 31,
        "humidity": 78,
        "rain_probability": 85,
        "rain_amount": 12,
        "irrigation_required": False
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/run/farm_001",
        json=context,
        timeout=30
    )
    print_response(response)
    
    # Scenario 2: Urgent irrigation needed
    print("\n📝 Scenario 2: Urgent Irrigation (Low moisture, no rain)")
    context = {
        "crop_name": "Wheat",
        "growth_stage": "Grain filling",
        "soil_moisture": 20,
        "soil_type": "Sandy",
        "temperature": 35,
        "humidity": 45,
        "rain_probability": 10,
        "rain_amount": 0,
        "irrigation_required": True
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/run/farm_002",
        json=context,
        timeout=30
    )
    print_response(response)
    
    # Scenario 3: Disease treatment required
    print("\n📝 Scenario 3: Disease Treatment (High confidence disease detection)")
    context = {
        "crop_name": "Potato",
        "growth_stage": "Vegetative",
        "soil_moisture": 40,
        "temperature": 28,
        "humidity": 82,
        "disease_detected": "Late Blight",
        "disease_confidence": 0.94,
        "is_healthy": False
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/run/farm_003",
        json=context,
        timeout=30
    )
    print_response(response)
    
    # Scenario 4: Harvest ready
    print("\n📝 Scenario 4: Harvest Ready (Mature stage, favorable conditions)")
    context = {
        "crop_name": "Wheat",
        "growth_stage": "Maturity",
        "soil_moisture": 35,
        "temperature": 30,
        "humidity": 50,
        "rain_probability": 15,
        "rain_amount": 0
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/run/farm_004",
        json=context,
        timeout=30
    )
    print_response(response)
    
    # Scenario 5: Monitor only
    print("\n📝 Scenario 5: Monitor Only (All conditions normal)")
    context = {
        "crop_name": "Carrot",
        "growth_stage": "Root development",
        "soil_moisture": 45,
        "temperature": 25,
        "humidity": 60,
        "rain_probability": 30,
        "is_healthy": True
    }
    
    response = requests.post(
        f"{BASE_URL}/agent/run/farm_005",
        json=context,
        timeout=30
    )
    print_response(response)


def test_agent_status():
    """Test agent status retrieval"""
    print_section("TESTING AGENT STATUS RETRIEVAL")
    
    farm_ids = ["farm_001", "farm_002", "farm_003"]
    
    for farm_id in farm_ids:
        print(f"\n📝 Getting status for {farm_id}")
        response = requests.get(
            f"{BASE_URL}/agent/status/{farm_id}",
            timeout=10
        )
        print_response(response)


def main():
    """Main test runner"""
    print("\n" + "🚀" * 40)
    print("  AGRISMART AI - FARMER ASSISTANT & AGENTIC ADVISOR TESTS")
    print("🚀" * 40)
    
    print("\n⚠️  PREREQUISITES:")
    print("  1. Backend server running on http://localhost:8000")
    print("  2. OPENROUTER_API_KEY configured in .env file")
    print("  3. All modules properly loaded")
    
    try:
        # Test health endpoint first
        print_section("HEALTH CHECK")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print_response(response)
        
        if response.status_code != 200:
            print("\n❌ Server health check failed. Make sure the server is running.")
            return
        
        # Run tests
        test_farmer_assistant()
        test_agentic_advisor()
        test_agent_status()
        
        print("\n" + "✅" * 40)
        print("  ALL TESTS COMPLETED")
        print("✅" * 40 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server.")
        print("   Please start the server with: uvicorn app.main:app --reload")
        print("   Or: cd backend && python -m uvicorn app.main:app --reload\n")
    
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
