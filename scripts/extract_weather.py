import requests
import pandas as pd
from datetime import datetime


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

weather_data = [{
    "city": data["name"],
    "temperature": data["main"]["temp"],
    "humidity": data["main"]["humidity"],
    "weather_timestamp": datetime.fromtimestamp(data["dt"]),
    "retrieved_at": datetime.now()
}]

df = pd.DataFrame(weather_data)

# Display the DataFrame
# print(df)

# Write the DataFrame to a CSV file
df.to_csv("data/raw/weather_data.csv", index=False)