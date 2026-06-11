import requests

from config.settings import OPENWEATHER_API_KEY

city = "Cincinnati, OH, US"

url = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}"
    f"&appid={OPENWEATHER_API_KEY}"
    "&units=imperial"
)

response = requests.get(url)

print("Status:", response.status_code)

data = response.json()

print("City:", data["name"])
print("Temperature:", data["main"]["temp"])
print("Humidity:", data["main"]["humidity"])