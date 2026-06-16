import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging
from pathlib import Path

load_dotenv()
DB_URL = os.getenv("DB_URL")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data" / "weather_data.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_weather_data():
    try:
        # Read the CSV file into a pandas DataFrame
        logger.info("Loading weather data from CSV...")
        df = pd.read_csv(CSV_PATH)

        # Convert timestamp columns to UTC datetime
        df["weather_timestamp"] = pd.to_datetime(df["weather_timestamp"], utc=True)
        df["retrieved_at"] = pd.to_datetime(df["retrieved_at"], utc=True)

        # Validate the data
        if df["temperature"].isna().any():
            raise ValueError("Temperature contains null values.")
        
        if df["city"].duplicated().any():
            logger.warning("Duplicate cities detected.")

        expected_columns = [
            "city",
            "temperature",
            "humidity",
            "weather_timestamp",
            "retrieved_at"
        ]
        missing = set(expected_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

        # Create a SQLAlchemy engine
        engine = create_engine(DB_URL)
        
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS raw.weather_raw (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100),
                    temperature FLOAT,
                    humidity INTEGER,
                    weather_timestamp TIMESTAMPTZ,
                    retrieved_at TIMESTAMPTZ
                );
            """))

            logger.info("Loading weather data into weather_raw table...")
            df.to_sql(
                "weather_raw",
                con=conn,
                schema="raw",
                if_exists="append",
                index=False,
                chunksize=1000
            )

        logger.info(f"Loaded {len(df)} rows into weather_raw...")

    except Exception as e:
        logger.error(f"Error loading weather data: {e}")
        raise

if __name__ == "__main__":
    load_weather_data()