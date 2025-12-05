import json

from airflow import DAG
from airflow.decorators import task
from airflow.hooks.base import BaseHook
import pendulum
import requests
import s3fs

default_args = {
    "owner": "s-yu-dev",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="earthquake_extract",
    default_args=default_args,
    description="Extract data from USGS API to S3 (MinIO)",
    schedule="@daily",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    tags=["earthquake", "etl"],
) as dag:

    @task
    def extract_usgs_data(**context):
        """
        Extracts earthquake data from USGS API for a specific date
        and saves it to S3 (MinIO).
        """
        execution_date = context["logical_date"]
        start_time = execution_date.to_date_string()
        end_time = execution_date.add(days=1).to_date_string()

        print(f"Fetching data for period: {start_time} to {end_time}")

        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        params = {"format": "geojson", "starttime": start_time, "endtime": end_time}

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            raise

        connection = BaseHook.get_connection("aws_default")
        fs = s3fs.S3FileSystem(
            key=connection.login,
            secret=connection.password,
            client_kwargs={"endpoint_url": connection.extra_dejson.get("endpoint_url")},
        )

        bucket_name = "earthquakes"
        if not fs.exists(bucket_name):
            print(f"Bucket '{bucket_name}' does not exist. Creating...")
            fs.mkdir(bucket_name)
        file_path = f"{bucket_name}/raw/{start_time}.json"

        print(f"Saving data to s3://{file_path}")

        with fs.open(file_path, "w") as f:
            json.dump(data, f)

    extract_task = extract_usgs_data()
