#!/bin/bash
set -e

echo "Waiting for /shared/etl_done.flag..."
while [ ! -f /shared/etl_done.flag ]; do
  sleep 2
done

echo "ETL script done. Running dbt..."
dbt run --profiles-dir /root --project-dir /dbt
