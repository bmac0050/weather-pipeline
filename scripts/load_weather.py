import pandas as pd
from sqlalchemy import create_engine, text
from config.settings import DB_URL

CSV_PATH = "data/raw/weather_data.csv"

def load_weather_data():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(CSV_PATH)
    
    # Create a SQLAlchemy engine
    engine = create_engine(DB_URL)
    
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weather_raw (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                temperature FLOAT,
                humidity INTEGER,
                weather_timestamp TIMESTAMP,
                retrieved_at TIMESTAMP
            );
        """))

        df.to_sql(
            "weather_observations",
            con=conn,
            schema="raw",
            if_exists="append",
            index=False,
            chunksize=1000
        )

    print(f"Loaded {len(df)} rows into raw.weather_observations")

if __name__ == "__main__":
    load_weather_data()