# ✈️ Flight Ops Data Platform

We utilize the **Medallion Architecture** (Bronze/Silver/Gold) to ensure auditability and data quality.

```mermaid
graph LR
    A[External API] -->|Raw JSON| B(Bronze: Raw Ingestion)
    B -->|Clean & Dedup| C(Silver: Curated Flights)
    C -->|Aggregations| D(Gold: OTP Metrics)
    D -->|Loading| E[(Snowflake DW)]

    Component,Choice,Why this over the alternatives?
Orchestrator,Apache Airflow,"Chosen over Cron for its backfilling capabilities and dependency management. If the API fails, Airflow retries automatically."
Containerization,Docker,"Ensures reproducibility. This project runs identically on local dev, CI/CD runners, and production clusters."
Storage,Snowflake,"Selected for its Variant data type, allowing us to ingest semi-structured flight JSON without brittle schema enforcement."
git clone [https://github.com/Pharaohleft/flight-ops-data-platform.git](https://github.com/Pharaohleft/flight-ops-data-platform.git)
cd flight-ops-data-platform

docker-compose up --build