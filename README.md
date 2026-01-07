#  Flight Ops Data Platform
# Flight Operations Data Engineering Project

A near real-time, fully Airflow-native end-to-end data engineering project. This pipeline sources real flight data from the OpenSky Network API rather than using mock data. The system handles extraction, cleaning, transformation, and loading (ETL) entirely within Apache Airflow, culminating in a Snowflake dashboard for aviation analytics.

## Executive Summary
This project simulates a solution for an Aviation Analytics and Operations Department. The goal is to monitor flight patterns to aid in decision-making. The project is designed to be "Airflow Native," meaning Apache Airflow is the primary driver for orchestration, while Python is used for data transformation. The final output is a dashboard in Snowflake that visualizes key performance indicators (KPIs) regarding flight activities.

## Architecture and Workflow
<img width="1341" height="5224" alt="Untitled diagram-2026-01-07-054356" src="https://github.com/user-attachments/assets/b479dfb0-3d4c-4945-a3e3-834f3d91c294" />

The pipeline follows a Medallion Architecture pattern, processing data through specific stages as defined below:

1.  **Source (API):** Data is extracted from the OpenSky Network API, providing real-time flight telemetry.
2.  **Bronze Layer (Raw Ingestion):** The raw data pulled from the API is stored locally as a JSON file. This serves as the raw history.
3.  **Silver Layer (Cleaned Data):** The system reads the JSON file from the Bronze layer. Using Python, the data is cleaned and transformed. The output is stored as a CSV file.
4.  **Gold Layer (Business Ready):** Data is pulled from the Silver CSV file. Specific columns are excluded, and data is aggregated to meet business requirements. This final dataset is stored in the Gold layer.
5.  **Data Warehouse (Snowflake):** The Gold layer data is ingested into a Snowflake table.
6.  **Visualization:** A dashboard is created directly within Snowflake using the loaded table. This includes KPI matrices and bar charts to visualize the flight operations data.

## Technologies Used
* **Apache Airflow:** The core orchestration tool used for scheduling and managing the entire pipeline from beginning to end.
* **Python:** Used for extraction logic and data transformation (cleaning, aggregating, and format conversion).
* **OpenSky Network API:** The source of real-time flight data.
* **Snowflake:** Used as the final destination for the data and for generating the analytic dashboard.
* **Docker:** Used to containerize the environment, ensuring the project is portable and portfolio-ready.

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
