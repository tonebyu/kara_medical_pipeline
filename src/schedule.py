# schedule.py
from dagster import schedule
from pipeline import full_pipeline_job

@schedule(cron_schedule="0 0 * * *", job=full_pipeline_job, execution_timezone="UTC")
def daily_pipeline_schedule(_context):
    return {}
