import json
import pandas as pd
from pathlib import Path

def run_silver_transform(**context):
    execution_date = context["ds_nodash"]

    # 1. Get the path to the Bronze file
    bronze_file = context["ti"].xcom_pull(
        key="bronze_file",
        task_ids="ingest_bronze" 
    )

    if not bronze_file:
        print("CRITICAL: Bronze file path not found in XCom.")
        return

    # 2. Setup Silver Folder
    silver_path = Path("/opt/airflow/data/silver")
    silver_path.mkdir(parents=True, exist_ok=True)

    # 3. Load the JSON data
    with open(bronze_file, "r") as f:
        raw = json.load(f)
    
    # 4. SAFETY CHECK: Check if 'states' exists and is not None
    if not raw or 'states' not in raw or raw['states'] is None:
        print("⚠️  API returned valid JSON, but 'states' is Empty/None. No flights found.")
        # Create an empty CSV just so the task doesn't fail
        empty_df = pd.DataFrame(columns=["icao24", "origin_country", "velocity", "on_ground"])
        output_file = silver_path / f"flights_silver_{execution_date}.csv"
        empty_df.to_csv(output_file, index=False)
        context["ti"].xcom_push(key="silver_file", value=str(output_file))
        return

    # 5. Normal Processing (Only runs if data exists)
    df_raw = pd.DataFrame(raw["states"])

    # Rename columns to match OpenSky documentation
    df_raw.columns = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact", "longitude",
        "latitude", "baro_altitude", "on_ground", 
        "velocity", "true_track", "vertical_rate",
        "sensors", "geo_altitude", "squawk",
        "spi", "position_source"
    ]

    # Select only the columns we need
    df = df_raw[["icao24", "origin_country", "velocity", "on_ground"]]

    # Save
    output_file = silver_path / f"flights_silver_{execution_date}.csv"
    df.to_csv(output_file, index=False)
    
    context["ti"].xcom_push(key="silver_file", value=str(output_file))