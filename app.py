from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import requests
from geopy.geocoders import Nominatim

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load ML Model
model = joblib.load("flood_model.pkl")

# Webhook URL
WEBHOOK_URL = "https://hook.relay.app/api/v1/playbook/cmmelwojb06mx0qm6frnk4rvs/trigger/zANf0QEuPxuAJNQ2fx62Fg"


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(request: Request, city: str = Form(...)):
    try:
        # Get city coordinates
        geolocator = Nominatim(user_agent="geo_app")
        location = geolocator.geocode(city)
        if not location:
            return templates.TemplateResponse(
                "result.html", {"request": request, "city": city, "prediction": "❌ Invalid city name"}
            )

        # Fetch weather
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={location.latitude}&longitude={location.longitude}"
            f"&hourly=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m"
            f"&timezone=auto"
        )
        weather = requests.get(url).json()
        hourly = weather.get("hourly", {})

        # Extract values safely
        max_temp = max(hourly.get("temperature_2m", [0]))
        min_temp = min(hourly.get("temperature_2m", [0]))
        rainfall = hourly.get("precipitation", [0])[0]
        humidity = hourly.get("relative_humidity_2m", [0])[0]
        wind_speed = hourly.get("windspeed_10m", [0])[0]

        input_data = [[max_temp, min_temp, rainfall, humidity, wind_speed]]
        prediction = model.predict(input_data)
        result = "⚠️ Flood Risk Detected" if prediction[0] == 1 else "✅ No Flood Found"

        # Send webhook after prediction
        payload = {
            "location": city,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "rainfall": rainfall,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "alert": result
        }
        try:
            WEBHOOK_URL = "https://hook.relay.app/api/v1/playbook/cmmelwojb06mx0qm6frnk4rvs/trigger/zANf0QEuPxuAJNQ2fx62Fg"

            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            print("Webhook failed:", e)
            return templates.TemplateResponse(
                "result.html", {"request": request, "city": city, "prediction": e}
            )

        return templates.TemplateResponse(
            "result.html", {"request": request, "city": city, "prediction": result}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "result.html", {"request": request, "city": city, "prediction": f"Error: {str(e)}"}
        )
