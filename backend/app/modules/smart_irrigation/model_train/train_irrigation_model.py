"""
Smart Irrigation Model Training Script
Trains a RandomForest classifier to predict irrigation requirements
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support
)

# Set up paths
SCRIPT_DIR = Path(__file__).parent
DATA_PATH = SCRIPT_DIR / "cropdata_updated.csv"
MODEL_OUTPUT_DIR = SCRIPT_DIR.parent / "model"
MODEL_OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("🌾 SMART IRRIGATION MODEL TRAINING - RandomForest")
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
print(f"  Columns: {df.columns.tolist()}")

# Display target distribution
print(f"\n📊 Target Distribution:")
print(df['result'].value_counts().sort_index())
print(f"\nTarget interpretation:")
print(f"  0 = No irrigation needed ({df['result'].value_counts()[0]} samples)")
print(f"  1 = Medium irrigation ({df['result'].value_counts()[1]} samples)")
print(f"  2 = High irrigation needed ({df['result'].value_counts()[2]} samples)")

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================
print("\n" + "=" * 80)
print("2. FEATURE ENGINEERING")
print("=" * 80)

# Separate features and target
target_col = 'result'
feature_cols = [col for col in df.columns if col != target_col]

X = df[feature_cols].copy()
y = df[target_col].copy()

print(f"\n✓ Features: {feature_cols}")
print(f"✓ Target: {target_col}")

# Identify categorical and numerical features
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\n📊 Categorical features: {categorical_features}")
print(f"📊 Numerical features: {numerical_features}")

# Encode categorical features
label_encoders = {}
for col in categorical_features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le
    print(f"   ✓ Encoded '{col}': {len(le.classes_)} unique values")

# Store feature names after encoding
feature_names = X.columns.tolist()

print(f"\n✓ Final feature count: {len(feature_names)}")

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
print(f"✓ Train target distribution:\n{y_train.value_counts().sort_index()}")
print(f"✓ Test target distribution:\n{y_test.value_counts().sort_index()}")

# ============================================================================
# 4. TRAIN RANDOMFOREST MODEL
# ============================================================================
print("\n" + "=" * 80)
print("4. TRAINING RANDOMFOREST MODEL")
print("=" * 80)

# Initialize RandomForest with balanced parameters
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1,
    class_weight='balanced',  # Handle class imbalance
    verbose=1
)

print("\n🔄 Training model...")
print(f"  Estimators: 200")
print(f"  Max depth: 15")
print(f"  Min samples split: 10")
print(f"  Min samples leaf: 4")
print(f"  Class weight: balanced")

# Train model
model.fit(X_train, y_train)

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

# Calculate metrics
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

train_f1 = f1_score(y_train, y_train_pred, average='weighted')
test_f1 = f1_score(y_test, y_test_pred, average='weighted')

# Per-class metrics
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_test_pred)

print("\n📊 OVERALL METRICS:")
print(f"  Train Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"  Test Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  Gap:            {(train_accuracy - test_accuracy):.4f}")
print(f"\n  Train F1 (weighted): {train_f1:.4f}")
print(f"  Test F1 (weighted):  {test_f1:.4f}")

print("\n📊 PER-CLASS METRICS (Test Set):")
class_labels = ['No Irrigation', 'Medium Irrigation', 'High Irrigation']
for i, label in enumerate(class_labels):
    print(f"\n  Class {i} ({label}):")
    print(f"    Precision: {precision[i]:.4f}")
    print(f"    Recall:    {recall[i]:.4f}")
    print(f"    F1-Score:  {f1[i]:.4f}")
    print(f"    Support:   {support[i]}")

# Cross-validation
print("\n📊 CROSS-VALIDATION (5-fold):")
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy', n_jobs=-1)
print(f"  CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
print(f"  CV Scores: {cv_scores}")

# Classification report
print("\n📊 DETAILED CLASSIFICATION REPORT:")
print(classification_report(y_test, y_test_pred, target_names=class_labels))

# Feature importance
print("\n📊 FEATURE IMPORTANCE (Top 10):")
feature_importance = model.feature_importances_
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
model_path = MODEL_OUTPUT_DIR / "irrigation_randomforest.joblib"
joblib.dump(model, model_path)
print(f"✓ Model saved: {model_path}")

# Save label encoders
encoders_path = MODEL_OUTPUT_DIR / "label_encoders.joblib"
joblib.dump(label_encoders, encoders_path)
print(f"✓ Label encoders saved: {encoders_path}")

# Save metadata
metadata = {
    'feature_names': feature_names,
    'categorical_features': categorical_features,
    'numerical_features': numerical_features,
    'target_classes': [0, 1, 2],
    'class_labels': class_labels,
    'metrics': {
        'test_accuracy': float(test_accuracy),
        'train_accuracy': float(train_accuracy),
        'test_f1_weighted': float(test_f1),
        'cv_accuracy_mean': float(cv_scores.mean()),
        'cv_accuracy_std': float(cv_scores.std()),
        'per_class_precision': precision.tolist(),
        'per_class_recall': recall.tolist(),
        'per_class_f1': f1.tolist()
    },
    'model_type': 'RandomForestClassifier',
    'model_params': model.get_params()
}

metadata_path = MODEL_OUTPUT_DIR / "irrigation_metadata.joblib"
joblib.dump(metadata, metadata_path)
print(f"✓ Metadata saved: {metadata_path}")

# Save feature importance
importance_df.to_csv(MODEL_OUTPUT_DIR / "feature_importance.csv", index=False)
print(f"✓ Feature importance saved: {MODEL_OUTPUT_DIR / 'feature_importance.csv'}")

# ============================================================================
# 7. GENERATE VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("7. GENERATING VISUALIZATIONS")
print("=" * 80)

# Confusion matrix
plt.figure(figsize=(10, 8))
cm = confusion_matrix(y_test, y_test_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_labels,
            yticklabels=class_labels,
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix - Smart Irrigation RandomForest', fontsize=14, pad=15)
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
confusion_matrix_path = MODEL_OUTPUT_DIR / "confusion_matrix.png"
plt.savefig(confusion_matrix_path, dpi=150, bbox_inches='tight')
print(f"✓ Confusion matrix saved: {confusion_matrix_path}")
plt.close()

# Feature importance plot
plt.figure(figsize=(12, 8))
top_features = importance_df.head(10)
plt.barh(range(len(top_features)), top_features['importance'])
plt.yticks(range(len(top_features)), top_features['feature'])
plt.xlabel('Importance', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.title('Top 10 Feature Importance - RandomForest Model', fontsize=14, pad=15)
plt.gca().invert_yaxis()
plt.tight_layout()
importance_plot_path = MODEL_OUTPUT_DIR / "feature_importance.png"
plt.savefig(importance_plot_path, dpi=150, bbox_inches='tight')
print(f"✓ Feature importance plot saved: {importance_plot_path}")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED")
print("=" * 80)
print(f"\n📁 Output files:")
print(f"  - Model: {model_path}")
print(f"  - Metadata: {metadata_path}")
print(f"  - Label Encoders: {encoders_path}")

print(f"\n📊 Final Metrics:")
print(f"  Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  Test F1 (weighted): {test_f1:.4f}")
print(f"  CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

print(f"\n✅ Model ready for deployment!")
print(f"✅ Use this model to predict irrigation requirements based on:")
print(f"   - Crop type, Soil type, Seedling stage")
print(f"   - Moisture (MOI), Temperature, Humidity")

print("\n" + "=" * 80)
print("Next: Integrate the model into the API service")
print("=" * 80 + "\n")
