import requests
import joblib

# Load Model
model = joblib.load("flood_model.pkl")

loc = requests.get("https://geo.kamero.ai/api/geo").json()
latitude = float(loc.get("latitude", 0))
longitude = float(loc.get("longitude", 0))
city = loc.get("city", "Unknown")

weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=relative_humidity_2m,precipitation,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=auto"

weather = requests.get(weather_url).json()

# Extract values
max_temp = weather["daily"]["temperature_2m_max"][0]
min_temp = weather["daily"]["temperature_2m_min"][0]
rainfall = weather["current"]["precipitation"]
humidity = weather["current"]["relative_humidity_2m"]
wind_speed = weather["current"]["wind_speed_10m"]

# Prepare Input
input_data = [[
    max_temp,
    min_temp,
    rainfall,
    humidity,
    wind_speed
]]

print("Weather Input:", input_data)

# Predict Flood
prediction = model.predict(input_data)

# Result
if prediction[0] == 1:
    result = "⚠️ FLOOD RISK DETECTED"
else:
    result = "✅ No Flood Risk"
print(result)

# Send Webhook
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
print(payload)

requests.post(webhook, json=payload)