"""
==========================================================
  SYNTHETIC DATASET GENERATOR
  Vehicle Fuel Efficiency Predictor
==========================================================

This script generates a realistic synthetic dataset of vehicle
specifications and their corresponding fuel efficiency (km/l).

The relationships between features and fuel efficiency are modeled
based on real-world automotive engineering principles:
  - Larger engines consume more fuel
  - Diesel engines are generally more efficient than petrol
  - CNG vehicles have the highest km/kg efficiency
  - SUVs and off-road vehicles are less efficient due to weight/drag
  - Highway driving is more efficient than city driving
  - Automatic transmissions vary by type in efficiency

The generated data includes realistic noise to simulate real-world
variability in fuel efficiency measurements.
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)

NUM_SAMPLES = 5000

# ── Feature Definitions ──────────────────────────────────────────────

FUEL_TYPES = ["Petrol", "Diesel", "CNG"]
TRANSMISSION_TYPES = ["Manual", "iVT", "AMT", "DCT", "Torque Converter"]
BODY_TYPES = ["Hatchback", "Sedan", "SUV", "Sub-compact SUV", "Off-Road"]
DRIVING_CONDITIONS = ["City", "Highway", "Mixed"]

# ── Base Efficiency Matrix (km/l) ────────────────────────────────────
# Rows: Body Types, Columns: Fuel Types (Petrol, Diesel, CNG)
BASE_EFFICIENCY = {
    "Hatchback":       {"Petrol": 19.0, "Diesel": 23.5, "CNG": 26.0},
    "Sedan":           {"Petrol": 16.0, "Diesel": 20.0, "CNG": 23.0},
    "Sub-compact SUV": {"Petrol": 14.5, "Diesel": 18.5, "CNG": 21.0},
    "SUV":             {"Petrol": 11.0, "Diesel": 15.0, "CNG": 17.0},
    "Off-Road":        {"Petrol":  8.5, "Diesel": 12.5, "CNG": 14.0},
}

# ── Realistic Engine Specs by Body Type ──────────────────────────────
# Real-world engine CC values sourced from actual production vehicles
REAL_ENGINE_CC = {
    "Hatchback": [
        799, 814, 998, 999, 1047, 1086, 1120, 1197, 1199,
        1248, 1298, 1368, 1396, 1497, 1498,
    ],
    "Sedan": [
        1197, 1199, 1248, 1298, 1368, 1396, 1462, 1493,
        1497, 1498, 1582, 1591, 1598, 1796, 1798, 1956, 1999,
    ],
    "Sub-compact SUV": [
        998, 999, 1047, 1086, 1197, 1199, 1248, 1298,
        1368, 1396, 1462, 1493, 1497, 1498, 1582,
    ],
    "SUV": [
        1493, 1497, 1498, 1582, 1591, 1598, 1796, 1798,
        1956, 1999, 2143, 2179, 2199, 2359, 2393, 2497,
        2694, 2696, 2755, 2956, 2996,
    ],
    "Off-Road": [
        1956, 1999, 2143, 2179, 2199, 2359, 2393, 2497,
        2694, 2696, 2755, 2894, 2956, 2996, 3198, 3604,
        3799, 3956, 3996,
    ],
}

ENGINE_SPECS = {
    "Hatchback":       {"cyl": [3, 4],    "power_range": (60, 120),  "gears": [5, 6]},
    "Sedan":           {"cyl": [4],        "power_range": (85, 170),  "gears": [5, 6, 7]},
    "Sub-compact SUV": {"cyl": [3, 4],    "power_range": (80, 140),  "gears": [5, 6]},
    "SUV":             {"cyl": [4, 6],    "power_range": (120, 250), "gears": [5, 6, 7, 8]},
    "Off-Road":        {"cyl": [4, 6, 8], "power_range": (150, 350), "gears": [5, 6, 7, 8]},
}

# ── Modifier Coefficients ────────────────────────────────────────────
TRANSMISSION_MODIFIER = {
    "Manual":           0.00,
    "AMT":              0.02,   # Slightly better than manual
    "DCT":              0.05,   # Dual clutch is efficient
    "iVT":              0.07,   # Intelligent variable is most efficient
    "Torque Converter": -0.03,  # Traditional auto, slightly less efficient
}

DRIVING_MODIFIER = {
    "City":    -0.18,   # 18% less efficient in city
    "Highway":  0.15,   # 15% more efficient on highway
    "Mixed":    0.00,   # Baseline
}


def generate_sample():
    """Generate a single realistic vehicle sample with fuel efficiency."""

    # Pick body type
    body_type = np.random.choice(BODY_TYPES)
    specs = ENGINE_SPECS[body_type]

    # Pick fuel type
    fuel_type = np.random.choice(FUEL_TYPES)

    # Generate engine specs within realistic ranges for this body type
    engine_cc = int(np.random.choice(REAL_ENGINE_CC[body_type]))

    cylinders = int(np.random.choice(specs["cyl"]))
    power = int(np.random.uniform(*specs["power_range"]))
    gears = int(np.random.choice(specs["gears"]))

    # Pick transmission and driving condition
    transmission = np.random.choice(TRANSMISSION_TYPES)
    driving = np.random.choice(DRIVING_CONDITIONS)

    # ── Calculate Fuel Efficiency ─────────────────────────────────────
    base = BASE_EFFICIENCY[body_type][fuel_type]

    # Engine displacement penalty: larger engines = less efficient
    cc_mid = np.mean(REAL_ENGINE_CC[body_type])
    cc_effect = -0.003 * (engine_cc - cc_mid)

    # Power penalty: more power = less efficient
    power_mid = np.mean(specs["power_range"])
    power_effect = -0.015 * (power - power_mid)

    # Gear bonus: more gears = slightly better efficiency
    gear_effect = 0.3 * (gears - 5)

    # Transmission modifier
    trans_effect = base * TRANSMISSION_MODIFIER[transmission]

    # Driving condition modifier
    drive_effect = base * DRIVING_MODIFIER[driving]

    # Cylinder penalty (more cylinders = less efficient for same displacement)
    cyl_effect = -0.5 * (cylinders - 4)

    # Combine all effects
    efficiency = base + cc_effect + power_effect + gear_effect + trans_effect + drive_effect + cyl_effect

    # Add realistic noise (±5%)
    noise = np.random.normal(0, efficiency * 0.05)
    efficiency = max(4.0, efficiency + noise)  # Floor at 4 km/l
    efficiency = round(efficiency, 1)

    return {
        "Fuel_Type": fuel_type,
        "Engine_CC": engine_cc,
        "Cylinders": cylinders,
        "Gears": gears,
        "Power_HP": power,
        "Transmission": transmission,
        "Body_Type": body_type,
        "Driving_Condition": driving,
        "Fuel_Efficiency_kmpl": efficiency,
    }


def main():
    print("=" * 55)
    print("  Generating Synthetic Vehicle Dataset")
    print("=" * 55)

    samples = [generate_sample() for _ in range(NUM_SAMPLES)]
    df = pd.DataFrame(samples)

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", "vehicle_data.csv")
    df.to_csv(filepath, index=False)

    print(f"\n✓ Generated {NUM_SAMPLES} samples")
    print(f"✓ Saved to: {filepath}")
    print(f"\n── Dataset Summary ─────────────────────────────────")
    print(f"   Shape: {df.shape}")
    print(f"   Fuel Efficiency Range: {df['Fuel_Efficiency_kmpl'].min():.1f} - {df['Fuel_Efficiency_kmpl'].max():.1f} km/l")
    print(f"   Mean Efficiency: {df['Fuel_Efficiency_kmpl'].mean():.1f} km/l")
    print(f"\n── Feature Distribution ────────────────────────────")
    for col in ["Fuel_Type", "Transmission", "Body_Type", "Driving_Condition"]:
        print(f"\n   {col}:")
        for val, count in df[col].value_counts().items():
            print(f"     {val:20s} : {count}")

    print(f"\n── Numerical Features ──────────────────────────────")
    print(df[["Engine_CC", "Cylinders", "Gears", "Power_HP", "Fuel_Efficiency_kmpl"]].describe().round(1).to_string())
    print()


if __name__ == "__main__":
    main()
