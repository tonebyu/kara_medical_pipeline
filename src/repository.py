# src/repository.py
from dagster import repository
from .pipeline import full_pipeline_job  # import your job from pipeline.py

@repository
def kara_pipeline_repo():
    return [full_pipeline_job]
