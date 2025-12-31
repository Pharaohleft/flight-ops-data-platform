import pandas as pd
import os
from datetime import datetime

def run_gold_aggregate(**context):
    print("🚀 Starting Gold Aggregation...")

    # --- 1. SETUP PATHS ---
    base_dir = "/opt/airflow/data"
    silver_dir = os.path.join(base_dir, "silver")
    gold_dir = os.path.join(base_dir, "gold")

    # Force create the folder if it's missing
    os.makedirs(gold_dir, exist_ok=True)

    # --- 2. FIND SILVER DATA ---
    if not os.path.exists(silver_dir):
        print(f"❌ Silver folder not found at {silver_dir}")
        return

    files = [f for f in os.listdir(silver_dir) if f.endswith('.csv')]
    if not files:
        print("❌ No CSV files found in Silver folder.")
        return

    # Pick the latest file
    latest_file = max([os.path.join(silver_dir, f) for f in files], key=os.path.getmtime)
    print(f"✅ Processing latest Silver file: {latest_file}")

    # --- 3. AGGREGATE ---
    df = pd.read_csv(latest_file)
    
    # Calculate KPIs: Count flights, avg speed, etc. by Country
    # (Adjust 'origin_country' if your column name is different)
    kpi_df = df.groupby('origin_country').agg(
        total_flights=('icao24', 'count'),
        avg_velocity=('velocity', 'mean'),
        on_ground=('on_ground', 'sum') # Counts how many were on ground
    ).reset_index()

    # --- 4. SAVE TO GOLD ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    gold_file = os.path.join(gold_dir, f"flight_kpis_{timestamp}.csv")
    
    kpi_df.to_csv(gold_file, index=False)
    print(f"✅ Gold file saved: {gold_file}")

    # --- 5. PASS PATH TO NEXT TASK ---
    context["ti"].xcom_push(key="gold_file", value=gold_file)