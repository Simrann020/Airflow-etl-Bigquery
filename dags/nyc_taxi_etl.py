from __future__ import annotations
import os
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import bigquery

DATA_DIR = "/opt/airflow/data"
RAW = f"{DATA_DIR}/raw/nyc_taxi_sample.csv"
STAGING = f"{DATA_DIR}/staging/nyc_taxi_clean.csv"
PROCESSED = f"{DATA_DIR}/processed/nyc_taxi_ready.csv"

GCP_PROJECT = os.environ.get("GCP_PROJECT_ID")
BQ_DATASET = os.environ.get("BQ_DATASET", "demo_ds")
BQ_TABLE = os.environ.get("BQ_TABLE", "nyc_taxi")

def extract():
    df = pd.read_csv(RAW)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df.to_csv(STAGING, index=False)

def transform():
    df = pd.read_csv(STAGING)
    for col in ("pickup_datetime", "dropoff_datetime"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    if all(c in df.columns for c in ("pickup_datetime", "dropoff_datetime")):
        df["trip_duration_minutes"] = (
            (df["dropoff_datetime"] - df["pickup_datetime"]).dt.total_seconds() / 60.0
        )
    if "trip_duration_minutes" in df.columns:
        df = df[(df["trip_duration_minutes"].notnull()) & (df["trip_duration_minutes"] >= 0)]
    df.to_csv(PROCESSED, index=False)

def load_to_bq():
    client = bigquery.Client(project=GCP_PROJECT)
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    with open(PROCESSED, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()  # wait for completion

default_args = {
    "owner": "simran",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="nyc_taxi_etl",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Extract -> Transform -> Load to BigQuery",
) as dag:
    t_extract = PythonOperator(task_id="extract", python_callable=extract)
    t_transform = PythonOperator(task_id="transform", python_callable=transform)
    t_load_bq = PythonOperator(task_id="load_to_bq", python_callable=load_to_bq)
    t_extract >> t_transform >> t_load_bq

