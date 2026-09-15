"""
Test script for crop recommendation API
"""

import requests
import json


def test_crop_recommendation():
    """Test the crop recommendation endpoint with realistic scenarios"""
    
    url = "http://localhost:8000/api/v1/test/crop_recommendation"
    
    # Test Case 1: Rice conditions (warm, wet, clayey soil)
    print("\n" + "="*80)
    print("TEST CASE 1: Rice Growing Conditions")
    print("="*80)
    print("🌾 Conditions: Clayey soil, Kharif season, High humidity, Rain-fed")
    
    rice_data = {
        "type_of_crop": "FOOD GRAIN",
        "soil": "CLAYEY",
        "season": "KHARIF",
        "water_source": "RAIN FED",
        "soil_ph": 6.5,
        "soil_ph_high": 7.5,
        "temp": 25.0,
        "max_temp": 35.0,
        "waterrequired": 100.0,
        "waterrequired_max": 150.0,
        "relative_humidity": 60.0,
        "relative_humidity_max": 80.0,
        "n": 40.0,
        "n_max": 60.0,
        "p": 30.0,
        "p_max": 50.0,
        "k": 20.0,
        "k_max": 40.0
    }
    
    response = requests.post(url, json=rice_data)
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Top Recommendation: {result['top_crop']} (Confidence: {result['confidence']:.2%})")
        print("\n🏆 Top 5 Predictions:")
        for i, pred in enumerate(result['top_5_predictions'], 1):
            print(f"   {i}. {pred['crop_name']:20s} - {pred['confidence']:.2%}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test Case 2: Wheat conditions (cooler, less water, Rabi season)
    print("\n" + "="*80)
    print("TEST CASE 2: Wheat Growing Conditions")
    print("="*80)
    print("🌾 Conditions: Loamy soil, Rabi season, Lower humidity, Irrigated")
    
    wheat_data = {
        "type_of_crop": "FOOD GRAIN",
        "soil": "LOAMY",
        "season": "RABI",
        "water_source": "IRRIGATED",
        "soil_ph": 6.0,
        "soil_ph_high": 7.0,
        "temp": 15.0,
        "max_temp": 25.0,
        "waterrequired": 50.0,
        "waterrequired_max": 80.0,
        "relative_humidity": 40.0,
        "relative_humidity_max": 60.0,
        "n": 50.0,
        "n_max": 70.0,
        "p": 40.0,
        "p_max": 60.0,
        "k": 30.0,
        "k_max": 50.0
    }
    
    response = requests.post(url, json=wheat_data)
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Top Recommendation: {result['top_crop']} (Confidence: {result['confidence']:.2%})")
        print("\n🏆 Top 5 Predictions:")
        for i, pred in enumerate(result['top_5_predictions'], 1):
            print(f"   {i}. {pred['crop_name']:20s} - {pred['confidence']:.2%}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test Case 3: Cotton conditions (warm, moderate water, black soil)
    print("\n" + "="*80)
    print("TEST CASE 3: Cotton Growing Conditions")
    print("="*80)
    print("🌾 Conditions: Black soil, Kharif season, Moderate conditions, Irrigated")
    
    cotton_data = {
        "type_of_crop": "CASH CROP",
        "soil": "BLACK",
        "season": "KHARIF",
        "water_source": "IRRIGATED",
        "soil_ph": 7.0,
        "soil_ph_high": 8.0,
        "temp": 25.0,
        "max_temp": 35.0,
        "waterrequired": 60.0,
        "waterrequired_max": 100.0,
        "relative_humidity": 50.0,
        "relative_humidity_max": 70.0,
        "n": 60.0,
        "n_max": 80.0,
        "p": 35.0,
        "p_max": 55.0,
        "k": 40.0,
        "k_max": 60.0
    }
    
    response = requests.post(url, json=cotton_data)
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Top Recommendation: {result['top_crop']} (Confidence: {result['confidence']:.2%})")
        print("\n🏆 Top 5 Predictions:")
        for i, pred in enumerate(result['top_5_predictions'], 1):
            print(f"   {i}. {pred['crop_name']:20s} - {pred['confidence']:.2%}")
    else:
        print(f"❌ Error: {response.text}")
    
    # Test health endpoint
    print("\n" + "="*80)
    print("HEALTH CHECK")
    print("="*80)
    
    health_response = requests.get("http://localhost:8000/api/v1/test/crop_recommendation/health")
    if health_response.status_code == 200:
        health = health_response.json()
        print(f"✅ Service Status: {health['status']}")
        print(f"   Model Loaded: {health['model_loaded']}")
        print(f"   Features: {health['num_features']}")
        print(f"   Classes: {health['num_classes']}")
        print(f"   Test Accuracy: {health['test_accuracy']:.4f}")
        print(f"   Data Leakage Fixed: {health['data_leakage_fixed']}")
    else:
        print(f"❌ Health check failed: {health_response.text}")
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_crop_recommendation()
