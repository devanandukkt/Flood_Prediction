import requests
import joblib
from geopy.geocoders import Nominatim

# Load Model
model = joblib.load("flood_model.pkl")


city = input("Enter city name: ")
geolocator = Nominatim(user_agent="geo_app")
location = geolocator.geocode(city)

weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current=relative_humidity_2m,precipitation,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
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
webhook = "https://hook.relay.app/api/v1/playbook/cmmelwojb06mx0qm6frnk4rvs/trigger/zANf0QEuPxuAJNQ2fx62Fg"
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