# ETL Pipeline with Docker, Cron & dbt

This project is a simple ELT pipeline using Docker Compose. It extracts data from a PostgreSQL source, loads it into a destination database via a Python script, and applies transformations using dbt.

## Stack

- PostgreSQL (source + destination)
- Python ETL script (scheduled with cron)
- dbt (for transformations)
- Docker Compose (for orchestration)

## How It Works

1. `elt_script.py` runs daily at 3 AM via a cron job inside the container.
2. It pulls data from `source_postgres` and inserts into `destination_postgres`.
3. The `dbt` service waits for the ETL script to finish, then runs models defined in `custom_postgres/`.

## Setup

```bash
docker compose up --build
```

## ✨ Author  
Ismail El Hatimi (📍 Data Scientist & Engineer)  

🔗 [LinkedIn](https://www.linkedin.com/in/isma%C3%AFl-e-59b45737/)
