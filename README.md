
#  Real-Time Flight Operations Analytics Pipeline

This project simulates a solution for an Aviation Analytics and Operations Department. The goal is to monitor near real-time flight patterns to aid in decision-making. The project is designed to be "Airflow Native," meaning Apache Airflow is the primary driver for orchestration, utilizing a modular **Dockerized** architecture for reproducibility while Python is used for data transformation. The final output is a dashboard in Snowflake that visualizes key performance indicators (KPIs) regarding flight activities.
This pipeline sources real flight data from the OpenSky Network API rather than using mock data. The system handles extraction, cleaning, transformation, and loading (ETL) entirely within Apache Airflow, culminating in a Snowflake dashboard for aviation analytics.

###  Project Overview
Optimizing airline operations requires analyzing telemetry data (Altitude, Velocity, Geo-Location) in near real-time. This project is an **Airflow-Native ELT Pipeline** that extracts live flight data from the **OpenSky Network API**, processes it for operational insights, and visualizes airspace density.


---

###  System Architecture
*(From API Telemetry to Operational Dashboard)*
<img width="1341" height="5224" alt="Untitled diagram-2026-01-07-054356" src="https://github.com/user-attachments/assets/b479dfb0-3d4c-4945-a3e3-834f3d91c294" />


The pipeline follows a Medallion Architecture pattern:

1.  **Source (API):** Data is extracted from the OpenSky Network API, providing real-time flight telemetry. **OpenSky Network API** (Live REST API).
2.  **Bronze Layer (Raw Ingestion):** The raw data pulled from the API is stored locally as a JSON file. This serves as the raw history.
3.  **Silver Layer (Cleaned Data):** The system reads the JSON file from the Bronze layer. Using Python, the data is cleaned and transformed. The output is stored as a CSV file.
4.  **Gold Layer (Business Ready):** Data is pulled from the Silver CSV file. Specific columns are excluded, and data is aggregated to meet business requirements. This final dataset is stored in the Gold layer.
5.  **Data Warehouse (Snowflake):** The Gold layer data is ingested into a Snowflake table.
6.  **Visualization:** A dashboard is created directly within Snowflake using the loaded table. This includes KPI matrices and bar charts to visualize the flight operations data.

---

###  Tech Stack

* **Apache Airflow:** The core orchestration tool used for scheduling and managing the entire pipeline from beginning to end.
* **Python:** Used for extraction logic and data transformation (cleaning, aggregating, and format conversion).
* **OpenSky Network API:** The source of real-time flight data.
* **Snowflake:** Used as the final destination for the data and for generating the analytic dashboard.
* **Docker:** Used to containerize the environment, ensuring the project is portable and portfolio-ready.

---

###  Key Technical Features

#### 1. Airflow-Native Design
Instead of external scripts, the logic is encapsulated within **Airflow DAGs**.
* **Modularity:** The pipeline is split into distinct tasks (`extract_data`, `transform_data`, `load_to_snowflake`).
* **XComs:** Used to pass metadata (filenames, execution timestamps) between tasks.

#### 2. Robust API Interaction
Real-world APIs are flaky. The extraction logic includes:
* **Rate Limiting:** Respects OpenSky's request limits to avoid IP bans.
* **Retries & Backoff:** If the API returns a 500 or 429 error, Airflow automatically retries the task with exponential backoff.

#### 3. Data Cleaning with Pandas
Flight data is often messy (null sensors, duplicate signals). The Silver layer handles:
* **Flattening:** Converting complex nested JSON arrays into flat CSVs.
* **Imputation:** Handling missing altitude data ensuring downstream aggregations remain accurate.

---
###  Engineering Challenges & Solutions

#### 1. The "Thundering Herd" Problem (API Rate Limits)
The OpenSky API has strict rate limits. Early iterations of the pipeline crashed frequently with `429: Too Many Requests`.
* **Solution:** I implemented **Exponential Backoff** strategies within the Airflow Tasks.
* **Logic:** If the API fails, the task waits 30s, then 60s, then 120s before retrying. This "politeness" ensures high availability without getting our IP banned.

#### 2. Handling Telemetry "Ghosting" (Signal Loss)
Real-world flight data is imperfect. Planes flying over oceans or mountains often stop transmitting ADS-B signals for minutes, resulting in `NULL` lat/lon values or "teleporting" planes.
* **Solution:** Implemented a **Data Cleaning Layer (Silver)** using Pandas to drop records with incomplete geospatial coordinates (`lat/lon IS NULL`) before they reach the warehouse, ensuring the analytics dashboard only reflects verified flight paths.

#### 3. Airflow Docker Networking
Running Airflow in Docker is complex because the *Worker* needs to talk to the *Scheduler*, *Webserver*, and *Postgres Metadata DB*.
* **Solution:** Utilized a custom `docker-compose` network bridge to isolate the Airflow internal components from the external API extraction logic, ensuring container security and stability.


###  Operational Impact
* **Visibility:** Provides real-time visibility into active flights for operational planning.
* **Stability:** Dockerized environment eliminates "it works on my machine" deployment issues.
* **Efficiency:** Automates a process that previously required manual CSV downloads and Excel manipulation.

---

 
## How to Run
1.  Clone the repository.
2.  Ensure Docker is installed and running.
3.  Execute the docker-compose command to spin up the Airflow environment.
4.  Access the Airflow UI (typically localhost:8080).
5.  Configure the Snowflake connection details in the Airflow Admin panel.
6.  Trigger the DAG to start the extraction and transformation process.
7.  Access Snowflake to view the populated tables and the final dashboard.

## Author
Austin Abraham
