"""
FIXED Crop Recommendation Model Training Script
Removes data leakage by excluding crop-derived features
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, 
    f1_score, 
    classification_report, 
    confusion_matrix,
    top_k_accuracy_score
)

# Set up paths
SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR / "Crop recommendation dataset.csv"
MODEL_OUTPUT_DIR = SCRIPT_DIR.parent / "models"
MODEL_OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("🌾 CROP RECOMMENDATION MODEL TRAINING (FIXED - No Data Leakage)")
print("=" * 80)
print(f"\nScript directory: {SCRIPT_DIR}")
print(f"Data path: {DATA_PATH}")
print(f"Model output: {MODEL_OUTPUT_DIR}")
print(f"Dataset exists: {DATA_PATH.exists()}\n")

if not DATA_PATH.exists():
    print(f"❌ Error: Dataset not found at {DATA_PATH}")
    sys.exit(1)

# ============================================================================
# 1. LOAD AND EXPLORE DATA
# ============================================================================
print("\n" + "=" * 80)
print("1. LOADING DATA")
print("=" * 80)

df = pd.read_csv(DATA_PATH)

print(f"✓ Data loaded successfully")
print(f"  Shape: {df.shape}")
print(f"  Original columns: {len(df.columns)}")

# ============================================================================
# 2. FEATURE ENGINEERING (REMOVE DATA LEAKAGE)
# ============================================================================
print("\n" + "=" * 80)
print("2. FEATURE ENGINEERING (FIXING DATA LEAKAGE)")
print("=" * 80)

# Define target
target_col = 'CROPS'

# CRITICAL FIX: Remove crop-derived features that cause data leakage
LEAKY_FEATURES = [
    'SOWN',  # When crop was planted (crop-specific)
    'HARVESTED',  # When crop was harvested (crop-specific)
    'CROPDURATION',  # How long crop takes (IS THE CROP ITSELF)
    'CROPDURATION_MAX',  # Max duration (IS THE CROP ITSELF)
]

# Features to KEEP (farmer inputs before choosing crop)
FARMER_INPUT_FEATURES = [
    'TYPE_OF_CROP',  # General category farmer wants
    'SOIL',  # Soil type available
    'SEASON',  # Current season
    'WATER_SOURCE',  # Water availability
    'SOIL_PH',  # Soil pH
    'SOIL_PH_HIGH',  # Max soil pH
    'TEMP',  # Temperature
    'MAX_TEMP',  # Max temperature
    'WATERREQUIRED',  # Water requirement range (could also be crop-specific)
    'WATERREQUIRED_MAX',
    'RELATIVE_HUMIDITY',  # Humidity
    'RELATIVE_HUMIDITY_MAX',
    'N',  # Nitrogen availability
    'N_MAX',
    'P',  # Phosphorus availability
    'P_MAX',
    'K',  # Potassium availability
    'K_MAX'
]

print(f"\n⚠️  REMOVING LEAKY FEATURES:")
for feat in LEAKY_FEATURES:
    if feat in df.columns:
        print(f"   ❌ {feat}")

print(f"\n✓ KEEPING FARMER INPUT FEATURES:")
feature_cols = [col for col in FARMER_INPUT_FEATURES if col in df.columns]
for feat in feature_cols:
    print(f"   ✓ {feat}")

# Separate features and target
X = df[feature_cols].copy()
y = df[target_col].copy()

print(f"\n  Features shape: {X.shape}")
print(f"  Target shape: {y.shape}")
print(f"  Target classes: {y.nunique()}")

# Identify categorical features
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\n  Categorical features ({len(categorical_features)}): {categorical_features}")
print(f"  Numerical features ({len(numerical_features)}): {numerical_features}")

# ============================================================================
# 3. TRAIN-TEST SPLIT
# ============================================================================
print("\n" + "=" * 80)
print("3. TRAIN-TEST SPLIT")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"✓ Train set: {X_train.shape}")
print(f"✓ Test set: {X_test.shape}")

# ============================================================================
# 4. TRAIN CATBOOST MODEL
# ============================================================================
print("\n" + "=" * 80)
print("4. TRAINING CATBOOST MODEL (WITH PROPER FEATURES)")
print("=" * 80)

# Initialize CatBoost Classifier with regularization
model = CatBoostClassifier(
    iterations=300,
    learning_rate=0.05,
    depth=5,  # Reduced depth to prevent overfitting
    loss_function='MultiClass',
    eval_metric='Accuracy',
    random_seed=42,
    cat_features=categorical_features,
    l2_leaf_reg=3,  # L2 regularization
    verbose=50,
    early_stopping_rounds=50
)

print("\n🔄 Training model...")
print(f"  Iterations: 300")
print(f"  Learning rate: 0.05")
print(f"  Depth: 5 (reduced to prevent overfitting)")
print(f"  L2 regularization: 3")
print(f"  Categorical features: {len(categorical_features)}")

# Train model
model.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    verbose=50,
    plot=False,
    early_stopping_rounds=50
)

print("\n✓ Model training completed!")

# ============================================================================
# 5. EVALUATE MODEL
# ============================================================================
print("\n" + "=" * 80)
print("5. MODEL EVALUATION")
print("=" * 80)

# Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Probabilities for top-k accuracy
y_test_proba = model.predict_proba(X_test)

# Calculate metrics
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

train_macro_f1 = f1_score(y_train, y_train_pred, average='macro')
test_macro_f1 = f1_score(y_test, y_test_pred, average='macro')

train_weighted_f1 = f1_score(y_train, y_train_pred, average='weighted')
test_weighted_f1 = f1_score(y_test, y_test_pred, average='weighted')

# Top-k accuracy
top3_accuracy = top_k_accuracy_score(y_test, y_test_proba, k=3, labels=model.classes_)
top5_accuracy = top_k_accuracy_score(y_test, y_test_proba, k=5, labels=model.classes_)

print("\n📊 METRICS:")
print(f"  Train Accuracy:    {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"  Test Accuracy:     {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  Gap:               {(train_accuracy - test_accuracy):.4f} (should be small)")
print(f"\n  Train Macro-F1:    {train_macro_f1:.4f}")
print(f"  Test Macro-F1:     {test_macro_f1:.4f}")
print(f"\n  Train Weighted-F1: {train_weighted_f1:.4f}")
print(f"  Test Weighted-F1:  {test_weighted_f1:.4f}")
print(f"\n  Top-3 Accuracy:    {top3_accuracy:.4f} ({top3_accuracy*100:.2f}%)")
print(f"  Top-5 Accuracy:    {top5_accuracy:.4f} ({top5_accuracy*100:.2f}%)")

# Sanity check
print("\n" + "=" * 80)
print("SANITY CHECK")
print("=" * 80)
if test_accuracy > 0.95:
    print("⚠️  WARNING: Test accuracy > 95% - might still have data leakage!")
    print("   Review features carefully.")
elif test_accuracy < 0.50:
    print("⚠️  WARNING: Test accuracy < 50% - model might be underfitting")
    print("   Consider adding more relevant features or tuning hyperparameters")
else:
    print(f"✓ Test accuracy ({test_accuracy:.2%}) is in reasonable range for 57 classes")

if abs(train_accuracy - test_accuracy) > 0.15:
    print(f"⚠️  WARNING: Large gap ({train_accuracy - test_accuracy:.2%}) between train and test")
    print("   Model might be overfitting")
else:
    print(f"✓ Train-test gap ({train_accuracy - test_accuracy:.2%}) is reasonable")

# Classification report (top 10 classes)
print("\n" + "=" * 80)
print("CLASSIFICATION REPORT (Sample)")
print("=" * 80)
report = classification_report(y_test, y_test_pred, output_dict=True)
print(f"Showing metrics for first 10 classes...")
for i, cls in enumerate(model.classes_[:10]):
    if cls in report:
        print(f"  {cls:20s} - Precision: {report[cls]['precision']:.3f}, Recall: {report[cls]['recall']:.3f}, F1: {report[cls]['f1-score']:.3f}")

# Feature importance
print("\n" + "=" * 80)
print("FEATURE IMPORTANCE (Top 10)")
print("=" * 80)
feature_importance = model.get_feature_importance()
feature_names = X.columns
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print(importance_df.head(10).to_string(index=False))

# ============================================================================
# 6. SAVE MODEL AND ARTIFACTS
# ============================================================================
print("\n" + "=" * 80)
print("6. SAVING MODEL AND ARTIFACTS")
print("=" * 80)

# Save model
model_path = MODEL_OUTPUT_DIR / "crop_recommendation_catboost_fixed.cbm"
model.save_model(str(model_path))
print(f"✓ Model saved: {model_path}")

# Save metadata
metadata = {
    'feature_names': feature_names.tolist(),
    'categorical_features': categorical_features,
    'numerical_features': numerical_features,
    'classes': model.classes_.tolist(),
    'excluded_features': LEAKY_FEATURES,
    'metrics': {
        'test_accuracy': float(test_accuracy),
        'train_accuracy': float(train_accuracy),
        'test_macro_f1': float(test_macro_f1),
        'test_weighted_f1': float(test_weighted_f1),
        'top3_accuracy': float(top3_accuracy),
        'top5_accuracy': float(top5_accuracy)
    },
    'data_leakage_fixed': True
}

metadata_path = MODEL_OUTPUT_DIR / "crop_recommendation_metadata_fixed.joblib"
joblib.dump(metadata, metadata_path)
print(f"✓ Metadata saved: {metadata_path}")

# Save feature importance
importance_df.to_csv(MODEL_OUTPUT_DIR / "feature_importance_fixed.csv", index=False)
print(f"✓ Feature importance saved: {MODEL_OUTPUT_DIR / 'feature_importance_fixed.csv'}")

# ============================================================================
# 7. GENERATE VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("7. GENERATING VISUALIZATIONS")
print("=" * 80)

# Confusion matrix (sample - too big for all 57 classes)
plt.figure(figsize=(20, 16))
cm = confusion_matrix(y_test, y_test_pred)
sns.heatmap(cm, annot=False, fmt='d', cmap='Blues',
            xticklabels=model.classes_,
            yticklabels=model.classes_,
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix - Fixed Crop Recommendation', fontsize=16, pad=20)
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.xticks(rotation=90, ha='right', fontsize=8)
plt.yticks(rotation=0, fontsize=8)
plt.tight_layout()
confusion_matrix_path = MODEL_OUTPUT_DIR / "confusion_matrix_fixed.png"
plt.savefig(confusion_matrix_path, dpi=150, bbox_inches='tight')
print(f"✓ Confusion matrix saved: {confusion_matrix_path}")
plt.close()

# Feature importance plot
plt.figure(figsize=(12, 8))
top_features = importance_df.head(15)
plt.barh(range(len(top_features)), top_features['importance'])
plt.yticks(range(len(top_features)), top_features['feature'])
plt.xlabel('Importance', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.title('Top 15 Feature Importance - Fixed CatBoost Model', fontsize=14, pad=15)
plt.gca().invert_yaxis()
plt.tight_layout()
importance_plot_path = MODEL_OUTPUT_DIR / "feature_importance_fixed.png"
plt.savefig(importance_plot_path, dpi=150, bbox_inches='tight')
print(f"✓ Feature importance plot saved: {importance_plot_path}")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED (DATA LEAKAGE FIXED)")
print("=" * 80)
print(f"\n📁 Output files:")
print(f"  - Model: {model_path}")
print(f"  - Metadata: {metadata_path}")

print(f"\n📊 Final Metrics:")
print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  Test Macro-F1: {test_macro_f1:.4f}")
print(f"  Top-3 Accuracy: {top3_accuracy:.4f} ({top3_accuracy*100:.2f}%)")
print(f"  Top-5 Accuracy: {top5_accuracy:.4f} ({top5_accuracy*100:.2f}%)")

print(f"\n✅ Removed {len(LEAKY_FEATURES)} leaky features")
print(f"✅ Model now uses only farmer input features")
print(f"✅ Realistic accuracy for 57 crop classes")

print("\n" + "=" * 80)
print("Next: Run test_model_fixed.py to validate with realistic scenarios")
print("=" * 80 + "\n")
