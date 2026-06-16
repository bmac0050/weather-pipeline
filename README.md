# Weather ETL Pipeline with Apache Airflow

A production-style weather data pipeline built with Python, Apache Airflow, PostgreSQL, Docker, and SQLAlchemy.

The pipeline retrieves current weather data from the OpenWeather API, loads the raw data into a PostgreSQL database, then transforms the data to an analytics table using an Airflow TaskFlow DAG.

---

## Project Overview

This project demonstrates a complete ELT (Extract, Load, Transform) workflow using modern data engineering tools.

The pipeline performs the following steps:

1. Extract current weather data from the OpenWeather API.
2. Save the raw response to a CSV file.
3. Load the data into PostgreSQL.
4. Perform data validation and transformation.
5. Orchestrate the workflow using Apache Airflow.

---

## Architecture

```
                    OpenWeather API
                           │
                           ▼
                  Extract Weather Task
                           │
                           ▼
                    weather_data.csv
                           │
                           ▼
                   Load Weather Task
                           │
                           ▼
                      PostgreSQL
                           │
                           ▼
                 Transform Weather Task
                           │
                           ▼
                     Airflow Scheduler
```
![Architecture](docs/weather_pipeline-graph.png)
---

## Technologies Used

- Python 3.11+
- Apache Airflow (TaskFlow API)
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- pandas
- OpenWeather API

---

## Project Structure

```
weather-pipeline/
│
├── config/
│   └── settings.py
│
├── data/
│   ├── weather_data.csv
│
├── dags/
│   └── weather_dag.py
│
├── docker/
│   ├── airflow/
│   ├───── docker-compose.airflow.yaml
│   ├── postgres/
│   └───── docker-compose.postgres.yaml
│
├── scripts/
│   ├── extract_weather.py
│   ├── transform_weather.py
│   └── load_weather.py
│
├── sql/
│   └── init.sql
│
├── requirements.txt
├── .env-example
└── README.md
```

---

## ETL Workflow

### Extract

- Retrieves weather data from the OpenWeather API.
- Extracts:
  - City
  - Temperature
  - Humidity
  - Weather timestamp
  - Retrieval timestamp
- Stores results as:

```
data/weather_data.csv
```

---

### Load

Loads extracted data into PostgreSQL using SQLAlchemy.

Performs data quality checks including:
- Empty dataset validation
- Missing column validation
- Null value checks
- Duplicate city detection

Target table:
```
raw.weather_raw
```

### Loaded Data

<img src="docs/weather_raw_data.png" width="900">

The weather observations are stored in PostgreSQL using SQLAlchemy.

---

### Transform

Loads most recent data for each city into analytics table

Adds:
- Humidity category
- Temperature fields in F and C

Target table:
```
analytics.current_weather
```

### Transformed Data

<img src="docs/current_weather_data.png" width="900">

The weather data is transformed in PostgreSQL using SQLAlchemy.

---

## Airflow DAG

The project uses Airflow's modern **TaskFlow API**.

Workflow:

```
extract_weather
        │
        ▼
load_weather
        │
        ▼
transform_weather
```

Features include:

- Task retries
- Logging
- Exception handling
- Modular Python functions
- TaskFlow decorators

---

## Logging

Python logging is used throughout the project.

Each task logs:

- Start time
- Successful completion
- Number of records processed
- Errors with full stack traces

---

## Data Quality Checks

Before loading data, the pipeline validates:

- Dataset is not empty
- Required columns exist
- Temperature values are not null
- Duplicate city detection

The DAG fails immediately if validation fails.

---

## Timezone Handling

The project stores timestamps using PostgreSQL's

```
TIMESTAMPTZ
```

to preserve timezone information.

The weather observation timestamp retains its original timezone offset while retrieval timestamps are stored in UTC.

---

## Environment Variables

Example:

```env
OPENWEATHER_API_KEY=your_api_key

DB_URL=postgresql+psycopg://weather_user:password@localhost/weather_db
```

Docker/Airflow uses a separate connection string for internal networking.

---

## Running the Project

Start PostgreSQL

```bash
docker compose up -d
```

Start Airflow

```bash
docker compose -f docker-compose.airflow.yaml up -d
```

Trigger the DAG

```bash
airflow dags trigger weather_pipeline
```

---

## Future Improvements

Potential enhancements include:

- Historical weather fact table
- Weather dimension tables
- Bronze / Silver / Gold architecture
- Weather trend dashboard
- Unit testing
- CI/CD using GitHub Actions
- Cloud deployment (AWS or GCP)
- Replace intermediate CSV files with XCom or object storage

---

## Skills Demonstrated

- ETL Development
- Apache Airflow
- TaskFlow API
- Docker
- PostgreSQL
- SQLAlchemy
- REST APIs
- Data Validation
- Logging
- Python
- pandas
- Environment Management
- Timezone Handling

---

## Lessons Learned

During development the project required solving several real-world engineering challenges including:

- Docker container networking
- Python module imports
- Airflow dependency management
- Database connectivity
- Timezone consistency
- SQLAlchemy configuration
- Absolute vs relative file paths
- Task orchestration using TaskFlow

These challenges closely mirror the issues encountered when building production ETL pipelines.

---

## Author

Brian McPhail

Built as part of a Data Engineering portfolio while learning modern ETL, Airflow, Docker, and PostgreSQL.