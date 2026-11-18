"""
==========================================================
  FLASK WEB APPLICATION
  Vehicle Fuel Efficiency Predictor
==========================================================

This is the main web server that:
  1. Serves the interactive frontend (HTML/CSS/JS)
  2. Loads the trained ML model on startup
  3. Accepts prediction requests via a REST API
  4. Returns predicted fuel efficiency in km/l

API Endpoint:
  POST /predict
  Body (JSON):
    {
      "Fuel_Type": "Petrol",
      "Engine_CC": 1200,
      "Cylinders": 4,
      "Gears": 5,
      "Power_HP": 90,
      "Transmission": "Manual",
      "Body_Type": "Hatchback",
      "Driving_Condition": "Mixed"
    }
  Response (JSON):
    {
      "success": true,
      "prediction": 18.5,
      "unit": "km/l"
    }
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# ── Load Model on Startup ────────────────────────────────────────────
MODEL_PATH = os.path.join("model", "fuel_efficiency_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print(f"✓ Model loaded from {MODEL_PATH}")
except FileNotFoundError:
    print(f"✗ Model not found at {MODEL_PATH}")
    print("  Run 'python generate_dataset.py' and 'python train_model.py' first.")
    model = None


# ── Valid Input Values ────────────────────────────────────────────────
VALID_VALUES = {
    "Fuel_Type": ["Petrol", "Diesel", "CNG"],
    "Transmission": ["Manual", "iVT", "AMT", "DCT", "Torque Converter"],
    "Body_Type": ["Hatchback", "Sedan", "SUV", "Sub-compact SUV", "Off-Road"],
    "Driving_Condition": ["City", "Highway", "Mixed"],
}

NUMERIC_RANGES = {
    "Engine_CC": (0, 4500),
    "Cylinders": (2, 12),
    "Gears": (4, 10),
    "Power_HP": (40, 500),
}


@app.route("/")
def index():
    """Serve the main prediction page."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Handle prediction requests."""
    if model is None:
        return jsonify({"success": False, "error": "Model not loaded. Train the model first."}), 500

    try:
        data = request.get_json()

        # Validate categorical inputs
        for field, valid in VALID_VALUES.items():
            if data.get(field) not in valid:
                return jsonify({
                    "success": False,
                    "error": f"Invalid {field}: '{data.get(field)}'. Must be one of: {valid}"
                }), 400

        # Validate numerical inputs
        for field, (min_val, max_val) in NUMERIC_RANGES.items():
            try:
                val = float(data.get(field, 0))
                if val < min_val or val > max_val:
                    return jsonify({
                        "success": False,
                        "error": f"{field} must be between {min_val} and {max_val}. Got: {val}"
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": f"Invalid {field}: must be a number."
                }), 400

        # Create DataFrame for prediction (must match training format)
        input_df = pd.DataFrame([{
            "Fuel_Type": data["Fuel_Type"],
            "Engine_CC": int(data["Engine_CC"]),
            "Cylinders": int(data["Cylinders"]),
            "Gears": int(data["Gears"]),
            "Power_HP": int(data["Power_HP"]),
            "Transmission": data["Transmission"],
            "Body_Type": data["Body_Type"],
            "Driving_Condition": data["Driving_Condition"],
        }])

        # Predict
        prediction = model.predict(input_df)[0]
        prediction = round(float(prediction), 1)

        return jsonify({
            "success": True,
            "prediction": prediction,
            "unit": "km/l",
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 55)
    print("  Vehicle Fuel Efficiency Predictor")
    print(f"  Open http://127.0.0.1:{port} in your browser")
    print("=" * 55 + "\n")
    app.run(debug=False, host="0.0.0.0", port=port)
