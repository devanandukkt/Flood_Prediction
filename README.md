# 🌧️ FloodPredictionAI

## 📌 Project Description

FloodPredictionAI is a machine-learning powered web application designed to predict the likelihood of flooding in any city using **real-time weather data**.

The platform allows users to:
- Enter a city name  
- Fetch live weather parameters  
- Predict whether flood risk is **High / Moderate / Low**  
- View probability-based results  

This project follows a separated architecture using FastAPI backend with an ML model and a simple HTML frontend.

---

![Flood Prediction Dashboard](./your-image.jpg)

---

## 🛠 Tech Stack

### 🔹 Backend
- FastAPI  
- Python  
- Scikit-learn  
- Geopy (Geocoding)  
- Open-Meteo API (Weather)

### 🔹 Frontend
- HTML  
- CSS  
- Jinja Templates

### 🔹 Tools
- Render (Deployment)
- Git & GitHub  
- VS Code  

---

## ✨ Features

- City-based flood prediction  
- Automatic weather fetching  
- ML-powered classification  
- REST API backend  
- Swagger documentation at `/docs`  
- Clean and responsive UI  

---

## 📂 Project Structure

```
Flood_Prediction_ML/
│
├── app.py                      # Main FastAPI application
├── flood_prediction.py         # ML prediction logic
├── flood_prediction_model.py   # ML model training script
├── flood_model.pkl             # Trained ML model
├── FloodDataset.csv            # Training dataset
├── templates/
│   └── index.html              # Application UI
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```
git clone https://github.com/devanandukkt/Flood_Prediction_ML.git
cd Flood_Prediction_ML
```

---

### 2️⃣ Backend Setup

```
pip install -r requirements.txt
```

Start backend:

```
uvicorn app:app --reload
```

---

## 🔗 API Base URL (Live Deployment)

```
https://flood-prediction-ml.onrender.com/
```

---

## 🧪 API Endpoints

### 🌆 Predict Flood by City  
Fetches live weather + predicts flood risk.

```
GET /predict_city/{city}
```

### 🌦️ Manual Weather Prediction  

```
POST /predict
```

Body example:
```
{
  "rainfall": 120,
  "humidity": 80,
  "temperature": 29,
  "river_level": 6.5
}
```

---

## 👥 Team Members

- Devanand U K  
- Aswathi K  

---
