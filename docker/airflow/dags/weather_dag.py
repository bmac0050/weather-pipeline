from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract_weather",
        bash_command="cd /opt/airflow/project && python -m scripts.extract_weather",
    )

    load = BashOperator(
    task_id="load_weather",
    bash_command="cd /opt/airflow/project && python -m scripts.load_weather",
)

    transform = BashOperator(
    task_id="transform_weather",
    bash_command="cd /opt/airflow/project && python -m scripts.transform_weather",
    )

    extract >> load >> transform