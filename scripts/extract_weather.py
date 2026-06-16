import requests
import pandas as pd
from datetime import datetime, timezone
from time import sleep
from config.settings import OPENWEATHER_API_KEY
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
CSV_PATH = DATA_DIR / "weather_data.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def extract_weather_data():

    cities = ["Cincinnati, OH, US", "Dallas, TX, US", "Wilmington, NC, US"]
    datafile = "data/raw/weather_raw.csv"
    url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_rows = []

    for city in cities:
        try:
            params = {
                "q": city,
                "units": "imperial",
                "appid": OPENWEATHER_API_KEY
            }
            logger.info(f'Retrieving weather data for {city}...')
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for HTTP errors
            logger.info(f"Status for {city}: {response.status_code}")

            data = response.json()

            weather_rows.append({
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'weather_timestamp': datetime.fromtimestamp(data['dt'], tz=timezone.utc),
                'retrieved_at': datetime.now(timezone.utc)
            })

            sleep(3.0)

        except requests.RequestException as e:
            logger.info(f"Error fetching weather data for {city}: {e}")
            continue


    df = pd.DataFrame(weather_rows)

    if df.empty:
        raise ValueError("No weather data was extracted.")

    # Display the DataFrame
    logger.info(df)

    # Write the DataFrame to a CSV file
    logger.info(f"Retrieved {len(df)} weather records")
    df.to_csv(CSV_PATH, index=False)

if __name__ == "__main__":
    extract_weather_data()