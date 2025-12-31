from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
from pathlib import Path

# This helps Airflow find your 'scripts' folder
# It adds the parent directory to the Python path
AIRFLOW_HOME = Path("/opt/airflow")
sys.path.insert(0, str(AIRFLOW_HOME))

# Import the functions we defined in the scripts folder
from scripts.bronze_ingest import run_bronze_ingestion
from scripts.silver_transform import run_silver_transform
from scripts.gold_aggregate import run_gold_aggregate
from scripts.load_gold_to_snowflake import load_gold_to_snowflake

# Default settings for the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1), # Set to a past date so it can run immediately
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="flight_ops_pipeline",
    default_args=default_args,
    schedule_interval="@daily",  # Run once a day
    catchup=False,               # Don't run for past dates
    tags=["portfolio", "flight_data"],
) as dag:

    # 1. Ingest Data
    bronze_task = PythonOperator(
        task_id="ingest_bronze",
        python_callable=run_bronze_ingestion,
    )

    # 2. Transform to Silver
    silver_task = PythonOperator(
        task_id="transform_silver",
        python_callable=run_silver_transform,
    )

    # 3. Aggregate to Gold
    gold_task = PythonOperator(
        task_id="aggregate_gold",
        python_callable=run_gold_aggregate,
    )

    # 4. Load to Snowflake
    load_task = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_gold_to_snowflake,
    )

    # Define the order of tasks (Dependencies)
    bronze_task >> silver_task >> gold_task >> load_task