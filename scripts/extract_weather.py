import requests
import pandas as pd
from datetime import datetime, timezone
from time import sleep
from config.settings import OPENWEATHER_API_KEY

datafile = "data/raw/weather_data.csv"
cities = ["Cincinnati, OH, US", "Dallas, TX, US", "Wilmington, NC, US"]
url = 'https://api.openweathermap.org/data/2.5/weather'
weather_rows = []

for city in cities:
    try:
        params = {
            "q": city,
            "units": "imperial",
            "appid": OPENWEATHER_API_KEY
        }
        print(f'Retrieving weather data for {city}...')
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for HTTP errors
        print(f"Status for {city}: {response.status_code}")

        data = response.json()

        weather_rows.append({
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_timestamp': datetime.fromtimestamp(data['dt']),
            'retrieved_at': datetime.now(timezone.utc)
        })

        sleep(3.0)

    except requests.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        continue


df = pd.DataFrame(weather_rows)

# Display the DataFrame
print(df)

# Write the DataFrame to a CSV file
print(f"Retrieved {len(df)} weather records")
df.to_csv(datafile, index=False)