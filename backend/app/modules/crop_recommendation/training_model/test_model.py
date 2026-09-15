"""
Test the trained CatBoost crop recommendation model with realistic scenarios
"""

import sys
from pathlib import Path
import pandas as pd
import joblib
from catboost import CatBoostClassifier

# Set up paths
SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR.parent / "models"
MODEL_PATH = MODEL_DIR / "crop_recommendation_catboost.cbm"
METADATA_PATH = MODEL_DIR / "crop_recommendation_metadata.joblib"

print("=" * 80)
print("🧪 TESTING CROP RECOMMENDATION MODEL")
print("=" * 80)

# Load model and metadata
print("\n📁 Loading model...")
if not MODEL_PATH.exists():
    print(f"❌ Model not found at {MODEL_PATH}")
    print("Please run train_crop_model.py first!")
    sys.exit(1)

model = CatBoostClassifier()
model.load_model(str(MODEL_PATH))
print(f"✓ Model loaded from {MODEL_PATH}")

metadata = joblib.load(METADATA_PATH)
print(f"✓ Metadata loaded")
print(f"  Features: {len(metadata['feature_names'])}")
print(f"  Classes: {len(metadata['classes'])}")
print(f"  Reported Test Accuracy: {metadata['metrics']['test_accuracy']:.4f}")

# ============================================================================
# CREATE REALISTIC TEST CASES
# ============================================================================
print("\n" + "=" * 80)
print("🌾 TESTING WITH REALISTIC SCENARIOS")
print("=" * 80)

# Test Case 1: Rice-like conditions (should predict rice or similar cereal)
test_cases = [
    {
        "name": "Test 1: Typical Rice Growing Conditions",
        "data": {
            "TYPE_OF_CROP": "cereals",
            "SOIL": "Alluvial soil",
            "SEASON": "kharif",
            "WATER_SOURCE": "irrigated",
            "SOIL_PH": 6.5,
            "SOIL_PH_HIGH": 7.0,
            "CROPDURATION": 120,
            "CROPDURATION_MAX": 150,
            "TEMP": 25,
            "MAX_TEMP": 35,
            "WATERREQUIRED": 1500,
            "WATERREQUIRED_MAX": 2000,
            "RELATIVE_HUMIDITY": 70,
            "RELATIVE_HUMIDITY_MAX": 85,
            "N": 80,
            "N_MAX": 120,
            "P": 40,
            "P_MAX": 60,
            "K": 40,
            "K_MAX": 60
        },
        "expected": ["rice", "wheat", "maize"]
    },
    {
        "name": "Test 2: Wheat Growing Conditions",
        "data": {
            "TYPE_OF_CROP": "cereals",
            "SOIL": "Loamy soil",
            "SEASON": "rabi",
            "WATER_SOURCE": "irrigated",
            "SOIL_PH": 6.0,
            "SOIL_PH_HIGH": 7.5,
            "CROPDURATION": 100,
            "CROPDURATION_MAX": 130,
            "TEMP": 20,
            "MAX_TEMP": 25,
            "WATERREQUIRED": 450,
            "WATERREQUIRED_MAX": 650,
            "RELATIVE_HUMIDITY": 50,
            "RELATIVE_HUMIDITY_MAX": 70,
            "N": 100,
            "N_MAX": 150,
            "P": 50,
            "P_MAX": 75,
            "K": 30,
            "K_MAX": 50
        },
        "expected": ["wheat", "maize"]
    },
    {
        "name": "Test 3: Cotton Growing Conditions",
        "data": {
            "TYPE_OF_CROP": "commercial",
            "SOIL": "Black soil",
            "SEASON": "kharif",
            "WATER_SOURCE": "irrigated",
            "SOIL_PH": 6.5,
            "SOIL_PH_HIGH": 8.0,
            "CROPDURATION": 150,
            "CROPDURATION_MAX": 180,
            "TEMP": 25,
            "MAX_TEMP": 35,
            "WATERREQUIRED": 650,
            "WATERREQUIRED_MAX": 800,
            "RELATIVE_HUMIDITY": 50,
            "RELATIVE_HUMIDITY_MAX": 70,
            "N": 100,
            "N_MAX": 120,
            "P": 40,
            "P_MAX": 60,
            "K": 40,
            "K_MAX": 60
        },
        "expected": ["cotton", "sugarcane"]
    },
    {
        "name": "Test 4: Tomato Growing Conditions",
        "data": {
            "TYPE_OF_CROP": "vegetables",
            "SOIL": "Sandy loam soil",
            "SEASON": "rabi",
            "WATER_SOURCE": "irrigated",
            "SOIL_PH": 6.0,
            "SOIL_PH_HIGH": 7.0,
            "CROPDURATION": 90,
            "CROPDURATION_MAX": 120,
            "TEMP": 20,
            "MAX_TEMP": 30,
            "WATERREQUIRED": 400,
            "WATERREQUIRED_MAX": 600,
            "RELATIVE_HUMIDITY": 50,
            "RELATIVE_HUMIDITY_MAX": 70,
            "N": 100,
            "N_MAX": 150,
            "P": 50,
            "P_MAX": 80,
            "K": 50,
            "K_MAX": 80
        },
        "expected": ["tomato", "onion", "chillies"]
    },
    {
        "name": "Test 5: Generic Pulse Conditions",
        "data": {
            "TYPE_OF_CROP": "pulses",
            "SOIL": "Loamy soil",
            "SEASON": "kharif",
            "WATER_SOURCE": "rainfed",
            "SOIL_PH": 6.0,
            "SOIL_PH_HIGH": 7.0,
            "CROPDURATION": 80,
            "CROPDURATION_MAX": 100,
            "TEMP": 25,
            "MAX_TEMP": 30,
            "WATERREQUIRED": 300,
            "WATERREQUIRED_MAX": 450,
            "RELATIVE_HUMIDITY": 60,
            "RELATIVE_HUMIDITY_MAX": 75,
            "N": 20,
            "N_MAX": 40,
            "P": 40,
            "P_MAX": 60,
            "K": 30,
            "K_MAX": 50
        },
        "expected": ["blackgram", "greengram", "bengalgram", "redgram"]
    },
    {
        "name": "Test 6: Mixed Moderate Conditions (ambiguous)",
        "data": {
            "TYPE_OF_CROP": "vegetables",
            "SOIL": "Loamy soil",
            "SEASON": "rabi",
            "WATER_SOURCE": "irrigated",
            "SOIL_PH": 6.5,
            "SOIL_PH_HIGH": 7.0,
            "CROPDURATION": 60,
            "CROPDURATION_MAX": 90,
            "TEMP": 22,
            "MAX_TEMP": 28,
            "WATERREQUIRED": 350,
            "WATERREQUIRED_MAX": 500,
            "RELATIVE_HUMIDITY": 55,
            "RELATIVE_HUMIDITY_MAX": 70,
            "N": 60,
            "N_MAX": 90,
            "P": 45,
            "P_MAX": 70,
            "K": 40,
            "K_MAX": 65
        },
        "expected": None  # No specific expectation - should see diverse predictions
    }
]

# ============================================================================
# RUN TESTS
# ============================================================================
results = []

for i, test_case in enumerate(test_cases, 1):
    print(f"\n{'-' * 80}")
    print(f"Test Case {i}: {test_case['name']}")
    print(f"{'-' * 80}")
    
    # Create DataFrame with single row
    test_df = pd.DataFrame([test_case['data']])
    
    # Get prediction and probabilities
    prediction = model.predict(test_df)[0]
    probabilities = model.predict_proba(test_df)[0]
    
    # Get top 5 predictions
    top5_indices = probabilities.argsort()[-5:][::-1]
    top5_crops = [metadata['classes'][idx] for idx in top5_indices]
    top5_probs = [probabilities[idx] for idx in top5_indices]
    
    print(f"\n🎯 Top Prediction: {prediction}")
    print(f"   Confidence: {probabilities[metadata['classes'].index(prediction)]:.4f}")
    
    print(f"\n📊 Top 5 Predictions:")
    for rank, (crop, prob) in enumerate(zip(top5_crops, top5_probs), 1):
        print(f"   {rank}. {crop:25s} - {prob:.4f} ({prob*100:.2f}%)")
    
    # Check if prediction is reasonable
    if test_case['expected']:
        is_reasonable = prediction in test_case['expected'] or any(
            crop in test_case['expected'] for crop in top5_crops[:3]
        )
        print(f"\n✓ Expected: {', '.join(test_case['expected'])}")
        if is_reasonable:
            print(f"✅ Result: REASONABLE (found in top-3)")
        else:
            print(f"⚠️  Result: UNEXPECTED (none of expected crops in top-3)")
    else:
        print(f"\n📝 Note: Ambiguous test case - checking confidence distribution")
        max_prob = top5_probs[0]
        if max_prob > 0.9:
            print(f"⚠️  Warning: Very high confidence ({max_prob:.4f}) for ambiguous input")
        elif max_prob < 0.5:
            print(f"✓ Good: Low confidence ({max_prob:.4f}) reflects uncertainty")
        else:
            print(f"✓ Reasonable: Moderate confidence ({max_prob:.4f})")
    
    results.append({
        'test': test_case['name'],
        'prediction': prediction,
        'top5': top5_crops,
        'confidence': probabilities[metadata['classes'].index(prediction)],
        'expected': test_case['expected']
    })

# ============================================================================
# ANALYSIS AND RED FLAGS
# ============================================================================
print("\n" + "=" * 80)
print("🔍 RED FLAG ANALYSIS")
print("=" * 80)

red_flags = []

# Check if all predictions have very high confidence
high_confidence_count = sum(1 for r in results if r['confidence'] > 0.95)
if high_confidence_count == len(results):
    red_flags.append("⚠️  ALL predictions have >95% confidence (possible overfitting)")
elif high_confidence_count > len(results) * 0.8:
    red_flags.append(f"⚠️  {high_confidence_count}/{len(results)} predictions have >95% confidence")

# Check if model predictions are reasonable
unreasonable_count = 0
for r in results:
    if r['expected'] and r['prediction'] not in r['expected'] and not any(c in r['expected'] for c in r['top5'][:3]):
        unreasonable_count += 1

if unreasonable_count > 0:
    red_flags.append(f"⚠️  {unreasonable_count}/{len([r for r in results if r['expected']])} test cases had unreasonable predictions")

# Check for identical features issue (data leakage indicator)
print("\n📋 Reported Metrics from Training:")
print(f"  Test Accuracy: {metadata['metrics']['test_accuracy']:.4f} ({metadata['metrics']['test_accuracy']*100:.1f}%)")
print(f"  Test Macro-F1: {metadata['metrics']['test_macro_f1']:.4f}")
print(f"  Top-3 Accuracy: {metadata['metrics']['top3_accuracy']:.4f}")

if metadata['metrics']['test_accuracy'] >= 0.99:
    red_flags.append("🚨 CRITICAL: 99%+ test accuracy with 57 classes suggests DATA LEAKAGE")
    red_flags.append("   Possible causes:")
    red_flags.append("   - Features include target-derived information (e.g., CROPDURATION)")
    red_flags.append("   - Synthetic/perfectly separated data")
    red_flags.append("   - Test set not truly independent")

if red_flags:
    print(f"\n🚩 {len(red_flags)} Red Flag(s) Detected:")
    for flag in red_flags:
        print(f"  {flag}")
else:
    print("\n✅ No obvious red flags detected in basic testing")

# ============================================================================
# RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 80)
print("💡 RECOMMENDATIONS")
print("=" * 80)

print("""
1. ⚠️  DATA LEAKAGE CHECK:
   - Review features like CROPDURATION, CROPDURATION_MAX
   - These might be crop-specific and not farmer inputs
   - Remove features that are outcomes rather than inputs

2. 🔄 FEATURE REVIEW:
   - Keep: SOIL, SEASON, WATER_SOURCE, SOIL_PH, TEMP, HUMIDITY, N, P, K
   - Remove: Features derived FROM the crop choice itself

3. 🧪 VALIDATION:
   - Test with completely new, unseen conditions
   - Use cross-validation with multiple splits
   - Check if model works with slightly noisy inputs

4. 📊 EXPECTED PERFORMANCE:
   - For 57 classes with realistic farming data: 70-85% accuracy is good
   - 99-100% accuracy is suspicious and likely not generalizable

5. 🎯 RETRAIN:
   - Remove crop-derived features
   - Add regularization if needed
   - Validate with real farmer input scenarios
""")

print("=" * 80)
print("Test completed. Review the results above carefully.")
print("=" * 80 + "\n")
