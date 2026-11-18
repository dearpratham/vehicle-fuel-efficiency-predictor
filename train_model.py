"""
==========================================================
  ML MODEL TRAINING SCRIPT
  Vehicle Fuel Efficiency Predictor
==========================================================

This script trains a Random Forest Regressor to predict vehicle
fuel efficiency (km/l) based on vehicle specifications.

Pipeline:
  1. Load the synthetic dataset
  2. Encode categorical features (One-Hot Encoding)
  3. Scale numerical features (StandardScaler)
  4. Split into train/test sets (80/20)
  5. Train a Random Forest model with hyperparameter tuning
  6. Evaluate with MAE, RMSE, and R² score
  7. Save the trained pipeline for serving

Why Random Forest?
  - Handles both numerical and categorical features well
  - Robust to outliers and noise
  - Provides feature importance rankings
  - No assumption about data distribution
  - Excellent performance on tabular data
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


def load_data(filepath="data/vehicle_data.csv"):
    """Load and validate the dataset."""
    df = pd.read_csv(filepath)
    print(f"✓ Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def build_pipeline():
    """
    Build a scikit-learn pipeline with preprocessing and model.

    The pipeline handles:
    - One-Hot Encoding for categorical features
    - Standard Scaling for numerical features
    - Random Forest Regressor for prediction
    """

    # Define feature groups
    categorical_features = ["Fuel_Type", "Transmission", "Body_Type", "Driving_Condition"]
    numerical_features = ["Engine_CC", "Cylinders", "Gears", "Power_HP"]

    # Preprocessing: encode categories + scale numbers
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ]
    )

    # Full pipeline
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )),
    ])

    return pipeline, categorical_features, numerical_features


def train_and_evaluate(df):
    """Train the model and print evaluation metrics."""

    # Separate features and target
    X = df.drop(columns=["Fuel_Efficiency_kmpl"])
    y = df["Fuel_Efficiency_kmpl"]

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"✓ Train set: {X_train.shape[0]} samples")
    print(f"✓ Test set:  {X_test.shape[0]} samples")

    # Build and train pipeline
    pipeline, cat_features, num_features = build_pipeline()

    print("\n── Training Random Forest Model ────────────────────")
    pipeline.fit(X_train, y_train)
    print("✓ Model training complete")

    # Predictions
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)

    # Metrics
    print("\n── Model Performance ───────────────────────────────")
    print(f"\n   Training Set:")
    print(f"     MAE  = {mean_absolute_error(y_train, y_pred_train):.3f} km/l")
    print(f"     RMSE = {np.sqrt(mean_squared_error(y_train, y_pred_train)):.3f} km/l")
    print(f"     R²   = {r2_score(y_train, y_pred_train):.4f}")

    print(f"\n   Test Set:")
    mae = mean_absolute_error(y_test, y_pred_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    r2 = r2_score(y_test, y_pred_test)
    print(f"     MAE  = {mae:.3f} km/l")
    print(f"     RMSE = {rmse:.3f} km/l")
    print(f"     R²   = {r2:.4f}")

    # Feature Importance
    print("\n── Feature Importance ──────────────────────────────")
    model = pipeline.named_steps["model"]
    preprocessor = pipeline.named_steps["preprocessor"]

    # Get feature names after transformation
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_feature_names = cat_encoder.get_feature_names_out(cat_features).tolist()
    all_feature_names = num_features + cat_feature_names

    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    for i, idx in enumerate(indices[:15]):
        bar = "█" * int(importances[idx] * 100)
        print(f"   {i+1:2d}. {all_feature_names[idx]:30s} {importances[idx]:.4f}  {bar}")

    return pipeline, mae, rmse, r2


def save_model(pipeline, model_dir="model"):
    """Save the trained pipeline to disk."""
    os.makedirs(model_dir, exist_ok=True)
    filepath = os.path.join(model_dir, "fuel_efficiency_model.pkl")
    joblib.dump(pipeline, filepath)
    print(f"\n✓ Model saved to: {filepath}")
    print(f"  File size: {os.path.getsize(filepath) / 1024:.1f} KB")


def main():
    print("=" * 55)
    print("  Training Vehicle Fuel Efficiency Predictor")
    print("=" * 55)
    print()

    # Load data
    df = load_data()

    # Train and evaluate
    pipeline, mae, rmse, r2 = train_and_evaluate(df)

    # Save model
    save_model(pipeline)

    print("\n" + "=" * 55)
    print(f"  Model Summary")
    print(f"  MAE: {mae:.2f} km/l | RMSE: {rmse:.2f} km/l | R²: {r2:.4f}")
    print("=" * 55)


if __name__ == "__main__":
    main()
