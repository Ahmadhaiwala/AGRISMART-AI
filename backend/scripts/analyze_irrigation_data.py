"""
Analyze the smart irrigation dataset
"""

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('app/modules/smart_irrigation/model_train/cropdata_updated.csv')

print("="*80)
print("SMART IRRIGATION DATASET ANALYSIS")
print("="*80)

print(f"\n📊 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")

print(f"\n📋 Columns:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")

print(f"\n🔍 First 5 rows:")
print(df.head())

print(f"\n📈 Data Types:")
print(df.dtypes)

print(f"\n❓ Missing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("   ✅ No missing values!")
else:
    print(missing[missing > 0])

print(f"\n📊 Statistical Summary:")
print(df.describe())

# Check if there's a target column
possible_targets = ['irrigation_needed', 'water_requirement', 'irrigation', 'label', 'target']
target_col = None

for col in df.columns:
    if col.lower() in possible_targets or 'irrigation' in col.lower() or 'water' in col.lower():
        print(f"\n🎯 Potential Target Column: '{col}'")
        print(f"   Value counts:\n{df[col].value_counts()}")
        target_col = col

print(f"\n" + "="*80)
print("READY FOR MODEL TRAINING")
print("="*80)
