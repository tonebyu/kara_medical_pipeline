# pipeline.py
from dagster import job, op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(['python', '../src/scraper/scrape.py'], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(['python', '../src/load_raw.py'], check=True)

@op
def run_dbt_transformations():
    subprocess.run(['dbt', 'run', '--project-dir', '../kara_dbt'], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(['python', '../src/yolo/detect_objects.py'], check=True)

@job
def full_pipeline_job():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
