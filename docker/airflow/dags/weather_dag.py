from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import sys
sys.path.append("/opt/airflow/project")
from scripts.extract_weather import extract_weather_data
from scripts.load_weather import load_weather_data
from scripts.transform_weather import transform_weather_data
from datetime import datetime, timedelta

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args = {
        "owner": "Brian",
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
    },
) as dag:

    extract = PythonOperator(
        task_id="extract_weather",
        python_callable=extract_weather_data,
    )

    load = PythonOperator(
        task_id="load_weather",
        python_callable=load_weather_data,
    )

    transform = PythonOperator(
        task_id="transform_weather",
        python_callable=transform_weather_data,
    )

    extract >> load >> transform