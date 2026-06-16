import sys
from datetime import datetime, timedelta
from airflow.decorators import dag, task

sys.path.append("/opt/airflow/project")

from scripts.extract_weather import extract_weather_data
from scripts.load_weather import load_weather_data
from scripts.transform_weather import transform_weather_data


default_args = {
    "owner": "Brian",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

@dag(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args=default_args,
    tags=["weather", "etl", "postgres"]
    
)

def weather_pipeline():
    @task
    def extract_weather():
        extract_weather_data()

    @task
    def load_weather():
        load_weather_data()

    @task
    def transform_weather():
        transform_weather_data()

    extract = extract_weather()
    load = load_weather()
    transform = transform_weather()

    extract >> load >> transform

weather_pipeline()