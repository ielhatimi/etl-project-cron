import subprocess
import time


def wait_for_postgres(host, max_retries=5, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host, "-p", "5432"],
                check=True,
                capture_output=True,
                text=True,
            )
            if "accepting connections" in result.stdout:
                print(f"Postgres at {host} is ready.")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to Postgres : {e}")
            retries += 1
            print(
                (
                    f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})"
                )
            )
            time.sleep(delay)
    print("Max retries reached. Exiting...")
    return False


if not wait_for_postgres(host="source_postgres"):
    exit(1)

if not wait_for_postgres(host="destination_postgres"):
    exit(1)

print("Starting ETL process...")

source_config = {
    "dbname": "source_db",
    "user": "postgres",
    "password": "secret",
    "host": "source_postgres",
}

destination_config = {
    "dbname": "destination_db",
    "user": "postgres",
    "password": "secret",
    "host": "destination_postgres",
}

dump_command = [
    "pg_dump",
    "-h",
    source_config["host"],
    "-U",
    source_config["user"],
    "-d",
    source_config["dbname"],
    "-f",
    "data_dump.sql",
    "-w",
]

subprocess_env = dict(PGPASSWORD=source_config["password"])

subprocess.run(dump_command, env=subprocess_env, check=True)

load_command = [
    "psql",
    "-h",
    destination_config["host"],
    "-U",
    destination_config["user"],
    "-d",
    destination_config["dbname"],
    "-a",
    "-f",
    "data_dump.sql",
]

subprocess_env = dict(PGPASSWORD=destination_config["password"])

subprocess.run(load_command, env=subprocess_env, check=True)

with open("/shared/etl_done.flag", "w") as f:
    f.write("done")

print("Flag file created...")

print("Ending ELT script...")
