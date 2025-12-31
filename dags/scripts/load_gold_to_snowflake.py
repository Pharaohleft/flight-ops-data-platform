import pandas as pd
import snowflake.connector
from airflow.hooks.base import BaseHook
import os
import traceback
from datetime import datetime

def load_gold_to_snowflake(**context):
    # --- SETUP DEBUG LOGGING ---
    log_path = "/opt/airflow/data/debug_log.txt"
    
    def log_msg(msg):
        print(msg)
        with open(log_path, "a") as f:
            f.write(f"{msg}\n")

    # Clear previous log
    with open(log_path, "w") as f:
        f.write(f"--- ATTEMPT AT {datetime.now()} ---\n")

    log_msg("🚀 Script started. Fixing Account URL...")

    try:
        # --- STEP 1: FIND FILE ---
        base_dir = "/opt/airflow/data/gold"
        if not os.path.exists(base_dir):
            raise ValueError(f"Gold folder missing at {base_dir}")

        files = [x for x in os.listdir(base_dir) if x.endswith('.csv')]
        if not files:
            raise ValueError("No CSV files in Gold folder")
            
        gold_file = max([os.path.join(base_dir, x) for x in files], key=os.path.getmtime)
        log_msg(f"✅ Found File: {gold_file}")
        
        df = pd.read_csv(gold_file)

        # --- STEP 2: CONNECT (FIXED) ---
        conn = BaseHook.get_connection("snowflake_default")
        
        # RAW VALUE from Airflow
        raw_account = conn.extra_dejson.get("account") or conn.host
        log_msg(f"   Raw Account from Airflow: {raw_account}")

        # CLEAN IT UP
        # 1. Remove https://
        clean_account = raw_account.replace("https://", "")
        # 2. Remove .snowflakecomputing.com (The connector adds this automatically!)
        clean_account = clean_account.replace(".snowflakecomputing.com", "")
        
        log_msg(f"   Fixed Account ID: {clean_account}")
        
        sf_conn = snowflake.connector.connect(
            user=conn.login,
            password=conn.password,
            account=clean_account,  # <--- USES THE CLEAN ID
            warehouse="COMPUTE_WH",
            database="SKYFLY_DB",
            schema="PUBLIC"
        )
        log_msg("✅ Connection Successful!")

        # --- STEP 3: UPLOAD ---
        with sf_conn.cursor() as cursor:
            log_msg("🔨 Creating Table...")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS FLIGHT_KPIS (
                WINDOW_START TIMESTAMP,
                ORIGIN_COUNTRY STRING,
                TOTAL_FLIGHTS INTEGER,
                AVG_VELOCITY FLOAT,
                ON_GROUND BOOLEAN,
                LOAD_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
            """)
            
            log_msg("📥 Inserting Data...")
            ts = context["data_interval_start"].strftime("%Y-%m-%d %H:%M:%S")
            
            insert_sql = """
            INSERT INTO FLIGHT_KPIS 
            (WINDOW_START, ORIGIN_COUNTRY, TOTAL_FLIGHTS, AVG_VELOCITY, ON_GROUND)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            for _, row in df.iterrows():
                cursor.execute(insert_sql, (
                    ts,
                    row['origin_country'],
                    row['total_flights'],
                    row['avg_velocity'],
                    bool(row['on_ground'])
                ))
            
            log_msg(f"✅ Inserted {len(df)} rows.")

    except Exception as e:
        log_msg("\n❌ ERROR:")
        log_msg(str(e))
        log_msg(traceback.format_exc())
        raise e