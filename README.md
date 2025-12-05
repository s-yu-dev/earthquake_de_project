# Earthquake Data Engineering Project

Pet-project for building an ETL pipeline for earthquake data (USGS API -> S3 -> Postgres -> Metabase).

## Tech Stack
- **Infrastructure:** Docker, Docker Compose
- **Orchestration:** Apache Airflow 2.10 (LocalExecutor)
- **Storage:** MinIO (S3), Postgres 16
- **Processing:** DuckDB
- **BI:** Metabase
- **Package Manager:** Poetry

## How to run locally

1. **Requirements:**
   - Docker & Docker Compose
   - Python 3.11+
   - Poetry

2. **Install dependencies:**
   ```bash
   poetry install
