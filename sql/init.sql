CREATE SCHEMA IF NOT EXISTS raw;



CREATE TABLE IF NOT EXISTS analytics.current_weather (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    country TEXT,
    temperature NUMERIC(5,2),
    feels_like NUMERIC(5,2),
    humidity INTEGER,
    pressure INTEGER,
    weather_main TEXT,
    weather_description TEXT,
    wind_speed NUMERIC(6,2),
    observed_at TIMESTAMPTZ,
    retrieved_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);