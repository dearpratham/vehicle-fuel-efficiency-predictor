# 🚗 Vehicle Fuel Efficiency Predictor

An interactive **Machine Learning** web application that predicts vehicle fuel efficiency (km/l) based on vehicle specifications. Built with **scikit-learn**, **Flask**, and a modern responsive frontend.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-orange) ![Flask](https://img.shields.io/badge/Flask-3.0-green)

---

## 📋 Features

- **ML-Powered Predictions** — Random Forest Regressor with R² = 0.98
- **Interactive Web Interface** — Clean, dark-themed UI with real-time predictions
- **8 Input Factors** — Fuel type, engine CC, cylinders, gears, power, transmission, body type, driving conditions
- **Visual Gauge** — Animated fuel efficiency gauge with color-coded ratings
- **Educational** — Detailed explanations of how each factor affects fuel efficiency

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Training Data

```bash
python generate_dataset.py
```

This creates a synthetic dataset of 5,000 vehicle samples in `data/vehicle_data.csv`.

### 3. Train the Model

```bash
python train_model.py
```

This trains a Random Forest model and saves it to `model/fuel_efficiency_model.pkl`.

### 4. Run the Web App

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 📁 Project Structure

```
vehicle-fuel-efficiency-predictor/
├── app.py                  # Flask web server
├── generate_dataset.py     # Synthetic data generation
├── train_model.py          # Model training & evaluation
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── data/
│   └── vehicle_data.csv    # Generated training dataset
├── model/
│   └── fuel_efficiency_model.pkl  # Trained model
├── templates/
│   └── index.html          # Web page template
└── static/
    ├── style.css           # Stylesheet
    └── script.js           # Frontend logic
```

---

## 🔧 Input Factors

| Factor | Type | Range / Options | Impact on Efficiency |
|--------|------|----------------|---------------------|
| **Fuel Type** | Categorical | Petrol, Diesel, CNG | Diesel ~20-30% more efficient than petrol |
| **Engine CC** | Numerical | 500 – 5000 CC | Higher CC → Lower efficiency |
| **Cylinders** | Numerical | 2 – 12 | More cylinders → Lower efficiency |
| **Gears** | Numerical | 4 – 10 | More gears → Slightly better efficiency |
| **Power (HP)** | Numerical | 40 – 500 HP | Higher power → Lower efficiency |
| **Transmission** | Categorical | Manual, iVT, AMT, DCT, Torque Converter | iVT & DCT most efficient |
| **Body Type** | Categorical | Hatchback, Sedan, Sub-compact SUV, SUV, Off-Road | Lighter = more efficient |
| **Driving Condition** | Categorical | City, Highway, Mixed | Highway ~15-20% better than city |

---

## 📊 Model Performance

| Metric | Training Set | Test Set |
|--------|-------------|----------|
| **MAE** | 0.258 km/l | 0.592 km/l |
| **RMSE** | 0.365 km/l | 0.790 km/l |
| **R²** | 0.9962 | 0.9822 |

The model predicts fuel efficiency within **±0.6 km/l** on average.

---

## 🛠 Tech Stack

- **Machine Learning**: scikit-learn (Random Forest Regressor)
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Processing**: pandas, numpy

---

## 📄 License

MIT License — Feel free to use and modify.
