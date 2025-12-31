# ✈️ Flight Ops Data Platform

We utilize the **Medallion Architecture** (Bronze/Silver/Gold) to ensure auditability and data quality.

```mermaid
graph LR
    A[External API] -->|Raw JSON| B(Bronze: Raw Ingestion)
    B -->|Clean & Dedup| C(Silver: Curated Flights)
    C -->|Aggregations| D(Gold: OTP Metrics)
    D -->|Loading| E[(Snowflake DW)]
🏗 Tech Stack & RationaleComponentChoiceWhy this over the alternatives?OrchestratorApache AirflowChosen over Cron for its backfilling capabilities and dependency management. If the API fails, Airflow retries automatically.ContainerizationDockerEnsures reproducibility. This project runs identically on local dev, CI/CD runners, and production clusters.StorageSnowflakeSelected for its Variant data type, allowing us to ingest semi-structured flight JSON without brittle schema enforcement.🚀 Key Engineering Challenges Solved1. Handling Late-Arriving Data (Idempotency)Scenario: A flight lands at 23:55, but the data packet arrives at 00:05.Solution: The pipeline runs based on the Logical Date ({{ ds }}), not the Execution Time. We use MERGE statements (Upserts) instead of INSERT. This allows us to re-run the pipeline for past dates without creating duplicate records.2. Dependency ManagementThe Load_to_Snowflake task is strictly dependent on the success of Transform_Silver.We use Airflow direct task dependencies to prevent "dirty data" from ever reaching the Gold layer.3. Environment IsolationBy using docker-compose, we isolated the Postgres backend and Airflow webserver, eliminating "it works on my machine" issues related to Python versioning.🛠 How to Run Locally1. Clone the RepoBashgit clone [https://github.com/Pharaohleft/flight-ops-data-platform.git](https://github.com/Pharaohleft/flight-ops-data-platform.git)
cd flight-ops-data-platform
2. Start the PlatformBashdocker-compose up --build
3. Access AirflowURL: http://localhost:8085User/Pass: airflow / airflow