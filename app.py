from fastapi import FastAPI
import joblib
import requests
from geopy.geocoders import Nominatim

app = FastAPI()

# Load ML Model
model = joblib.load("flood_model.pkl")


@app.get("/")
def home():
    return {"message": "Flood Prediction API is running"}


@app.get("/predict")
def predict(city: str):
    try:
        # Geolocation
        geolocator = Nominatim(user_agent="geo_app")
        location = geolocator.geocode(city)

        if not location:
            return {"error": "Invalid city name"}

        # Weather API
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={location.latitude}&longitude={location.longitude}"
            "&current=relative_humidity_2m,precipitation,wind_speed_10m"
            "&daily=temperature_2m_max,temperature_2m_min"
            "&timezone=auto"
        )

        weather = requests.get(weather_url).json()

        # Extract weather features
        max_temp = weather["daily"]["temperature_2m_max"][0]
        min_temp = weather["daily"]["temperature_2m_min"][0]
        rainfall = weather["current"]["precipitation"]
        humidity = weather["current"]["relative_humidity_2m"]
        wind_speed = weather["current"]["wind_speed_10m"]

        input_data = [[max_temp, min_temp, rainfall, humidity, wind_speed]]

        # Prediction
        prediction = model.predict(input_data)
        result = "⚠️ FLOOD RISK DETECTED" if prediction[0] == 1 else "✅ No Flood Risk"

        # Webhook
        webhook = "https://hook.relay.app/api/v1/playbook/cmmelwojb06mx0qm6frnk4rvs/trigger/zANf0QEuPxuAJNQ2fx62F"
        payload = {
            "location": city,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "rainfall": rainfall,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "alert": result
        }
        requests.post(webhook, json=payload)

        return {
            "city": city,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "rainfall": rainfall,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "prediction": result,
            "webhook_sent": True
        }
    
    except Exception as e:
        return {"error": str(e)}