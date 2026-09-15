"""
Test script for Integrated Sustainability Score
Tests the new integrated endpoint that gathers data from all modules
"""

import requests
import json


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
        print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Raw response: {response.text}")


def test_integrated_sustainability():
    """Test integrated sustainability score with all modules"""
    print_section("TESTING INTEGRATED SUSTAINABILITY SCORE")
    
    # Scenario 1: Good sustainability - efficient water use, healthy crop
    print("\n📝 Scenario 1: Good Sustainability (Should get A or B grade)")
    request_data = {
        "farm_id": "farm_001",
        "crop_name": "Tomato",
        "growth_stage": "Flowering",
        "soil_moisture": 45,
        "soil_type": "Loamy",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "temperature": 28,
        "humidity": 65,
        "is_healthy": True,
        "water_used_liters": 1500,
        "fertilizer_used_kg": 4,
        "pesticide_used_kg": 0,
        "pesticide_recommended_kg": 0,
        "has_irrigation": True,
        "seedling_stage": 2
    }
    
    response = requests.post(
        f"{BASE_URL}/sustainability/score/integrated",
        json=request_data,
        timeout=30
    )
    print_response(response)
    
    # Scenario 2: Poor sustainability - over-watering, disease detected
    print("\n📝 Scenario 2: Poor Sustainability (Should get C or D grade)")
    request_data = {
        "farm_id": "farm_002",
        "crop_name": "Potato",
        "growth_stage": "Vegetative",
        "soil_moisture": 75,  # High moisture but still watering
        "soil_type": "Clayey",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "temperature": 30,
        "humidity": 85,
        "disease_detected": "Late Blight",
        "disease_confidence": 0.94,
        "is_healthy": False,
        "water_used_liters": 3000,  # Over-watering
        "fertilizer_used_kg": 10,  # Excessive
        "pesticide_used_kg": 2,
        "pesticide_recommended_kg": 0.5,
        "has_irrigation": True,
        "seedling_stage": 1
    }
    
    response = requests.post(
        f"{BASE_URL}/sustainability/score/integrated",
        json=request_data,
        timeout=30
    )
    print_response(response)
    
    # Scenario 3: Medium sustainability - room for improvement
    print("\n📝 Scenario 3: Medium Sustainability (Should get B or C grade)")
    request_data = {
        "farm_id": "farm_003",
        "crop_name": "Wheat",
        "growth_stage": "Grain filling",
        "soil_moisture": 30,  # Low moisture
        "soil_type": "Sandy",
        "latitude": 26.8467,
        "longitude": 80.9462,
        "temperature": 32,
        "humidity": 55,
        "is_healthy": True,
        "water_used_liters": 800,  # Under-watering
        "fertilizer_used_kg": 3,
        "pesticide_used_kg": 0.2,
        "pesticide_recommended_kg": 0.3,
        "has_irrigation": True,
        "seedling_stage": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/sustainability/score/integrated",
        json=request_data,
        timeout=30
    )
    print_response(response)
    
    # Scenario 4: Optimal conditions with minimal pesticide
    print("\n📝 Scenario 4: Optimal Sustainability (Should get A grade)")
    request_data = {
        "farm_id": "farm_004",
        "crop_name": "Carrot",
        "growth_stage": "Root development",
        "soil_moisture": 50,
        "soil_type": "Loamy",
        "latitude": 23.0225,
        "longitude": 72.5714,
        "temperature": 25,
        "humidity": 60,
        "is_healthy": True,
        "water_used_liters": 1200,
        "fertilizer_used_kg": 3.5,
        "pesticide_used_kg": 0.1,
        "pesticide_recommended_kg": 0.1,
        "has_irrigation": True,
        "seedling_stage": 2
    }
    
    response = requests.post(
        f"{BASE_URL}/sustainability/score/integrated",
        json=request_data,
        timeout=30
    )
    print_response(response)


def test_sustainability_info():
    """Test the info endpoint"""
    print_section("TESTING SUSTAINABILITY INFO ENDPOINT")
    
    response = requests.get(
        f"{BASE_URL}/sustainability/info",
        timeout=10
    )
    print_response(response)


def test_manual_vs_integrated():
    """Compare manual and integrated endpoints"""
    print_section("COMPARING MANUAL VS INTEGRATED ENDPOINTS")
    
    # Test manual endpoint first
    print("\n📝 Manual Endpoint")
    manual_data = {
        "water_used_liters": 1500,
        "water_required_liters": 1400,
        "fertilizer_used_kg": 4,
        "fertilizer_recommended_kg": 3.5,
        "pesticide_used_kg": 0,
        "pesticide_recommended_kg": 0,
        "is_healthy": True,
        "disease_confidence": 0
    }
    
    response = requests.post(
        f"{BASE_URL}/sustainability/score",
        json=manual_data,
        timeout=10
    )
    print_response(response)
    
    # Test integrated endpoint
    print("\n📝 Integrated Endpoint (with same data)")
    integrated_data = {
        "farm_id": "farm_compare",
        "crop_name": "Tomato",
        "growth_stage": "Flowering",
        "soil_moisture": 45,
        "soil_type": "Loamy",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "temperature": 28,
        "humidity": 65,
        "is_healthy": True,
        "water_used_liters": 1500,
        "fertilizer_used_kg": 4,
        "pesticide_used_kg": 0,
        "pesticide_recommended_kg": 0,
        "has_irrigation": True,
        "seedling_stage": 2
    }
    
    response = requests.post(
        f"{BASE_URL}/sustainability/score/integrated",
        json=integrated_data,
        timeout=30
    )
    print_response(response)


def main():
    """Main test runner"""
    print("\n" + "🌱" * 40)
    print("  AGRISMART AI - INTEGRATED SUSTAINABILITY SCORE TESTS")
    print("🌱" * 40)
    
    print("\n⚠️  PREREQUISITES:")
    print("  1. Backend server running on http://localhost:8000")
    print("  2. All ML models loaded (Smart Irrigation)")
    print("  3. Internet connection (for Weather Intelligence API)")
    
    try:
        # Test health endpoint first
        print_section("HEALTH CHECK")
        response = requests.get("http://localhost:8000/health", timeout=5)
        print_response(response)
        
        if response.status_code != 200:
            print("\n❌ Server health check failed. Make sure the server is running.")
            return
        
        # Run tests
        test_sustainability_info()
        test_integrated_sustainability()
        test_manual_vs_integrated()
        
        print("\n" + "✅" * 40)
        print("  ALL TESTS COMPLETED")
        print("✅" * 40 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server.")
        print("   Please start the server with: python -m uvicorn app.main:app --reload\n")
    
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
