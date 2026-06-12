from sqlalchemy import create_engine, text
from config.settings import DB_URL


def transform_weather_data():
    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics;"))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.current_weather (
                city VARCHAR(100) PRIMARY KEY,
                temperature_f FLOAT,
                temperature_c FLOAT,
                humidity INTEGER,
                humidity_category VARCHAR(20),
                observation_date DATE,
                observation_hour INTEGER,
                weather_timestamp TIMESTAMP,
                retrieved_at TIMESTAMP
            );
        """))

        print("Truncating analytics.current_weather table...")
        conn.execute(text("""
            TRUNCATE TABLE analytics.current_weather;
        """))

        print("Inserting transformed data into analytics.current_weather...")
        conn.execute(text("""
            INSERT INTO analytics.current_weather (
            city,
            temperature_f,
            temperature_c,
            humidity,
            humidity_category,
            observation_date,
            observation_hour,
            weather_timestamp,
            retrieved_at
        )
        SELECT DISTINCT ON (city)
            city,
            temperature AS temperature_f,
            ROUND(((temperature - 32) * 5.0 / 9.0)::numeric, 2) AS temperature_c,
            humidity,
            CASE
                WHEN humidity >= 70 THEN 'High'
                WHEN humidity >= 40 THEN 'Moderate'
                ELSE 'Low'
            END AS humidity_category,
            weather_timestamp::timestamp::date AS observation_date,
            EXTRACT(HOUR FROM weather_timestamp::timestamp) AS observation_hour,
            weather_timestamp::timestamp,
            retrieved_at::timestamp
        FROM raw.weather_raw
        ORDER BY city, retrieved_at::timestamp DESC;
        """))

    print("Transformed latest weather observations into analytics.current_weather")


if __name__ == "__main__":
    transform_weather_data()