# Weather Pipeline

A small ETL pipeline that retrieves weather observations from the OpenWeather API and loads them into PostgreSQL.

## Architecture

OpenWeather API
- Extract (Python)
- CSV
- PostgreSQL Raw Layer
- Analytics Layer

## Technologies

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Git/GitHub

## Usage
Start project venv:
source .venv/bin/activate

- python -m scripts.extract_weather
- python -m scripts.load_weather
- python -m scripts.transform_weather