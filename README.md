# Kara Medical Data Pipeline

An end-to-end ELT pipeline built for extracting insights from Ethiopian medical Telegram channels. This data product transforms raw Telegram messages into structured analytics through scraping, modeling, enrichment, and API exposure.

## Overview

Kara Solutions is building a robust data platform to analyze Ethiopian medical businesses using public Telegram data. This pipeline enables the business to answer key questions like:

- What are the top 10 most frequently mentioned medical products?
- How do prices or availability vary across channels?
- Which channels share the most visual content?
- What are the posting trends in health-related topics?

## Technologies Used

| Tool/Library       | Purpose                                      |
|--------------------|----------------------------------------------|
| Python 3.11        | Core language for scripting and orchestration|
| Telethon           | Telegram data scraping                       |
| PostgreSQL         | Data warehouse                               |
| dbt                | Data modeling and transformation             |
| YOLOv8 (Ultralytics)| Image detection for data enrichment         |
| FastAPI            | Analytical API interface                     |
| Dagster            | Orchestration and scheduling                 |
| Docker + Compose   | Environment & container management           |
| python-dotenv      | Secure secret management                     |

## Project Structure

kara_medical_pipeline/
│
├── .env # Environment secrets
├── docker-compose.yml # Docker setup for PostgreSQL + App
├── requirements.txt # Python dependencies
├── Dockerfile # Container for the Python app
│
├── src/ # Core source code
│ ├── scraper/ # Telegram data scraping scripts
│ ├── loader/ # JSON to PostgreSQL loading logic
│ ├── enrichment/ # YOLO image detection and processing
│ └── api/ # FastAPI application for analytics
│
├── data/ # Data lake (raw and processed)
│ └── raw/telegram_messages/YYYY-MM-DD/channel_name.json
│
├── kara_dbt/ # dbt project folder
│ ├── models/
│ │ ├── staging/ # Staging transformations
│ │ ├── marts/ # Final star schema models
│ │ └── tests/ # Custom SQL tests
│ └── dbt_project.yml
│
└── dagster_project/ # Dagster orchestration jobs
├── jobs/
├── ops/
└── workspace.yaml

markdown
Copy
Edit

## How It Works

### Task 0: Environment & Setup
- Virtual environment via `venv`
- Containerized with Docker (Python + PostgreSQL)
- Secure `.env` file for secrets
- Dependency management via `requirements.txt`

### Task 1: Telegram Scraping & Raw Storage
- Channels scraped: `@lobelia4cosmetics`, `@tikvahpharma`, etc.
- Raw JSON messages saved to `data/raw/telegram_messages/YYYY-MM-DD/`

### Task 2: Data Modeling & dbt
- Raw data loaded into PostgreSQL `raw` schema
- dbt used to:
  - Create staging models (cast, clean)
  - Build a star schema with:
    - `dim_channels`
    - `dim_dates`
    - `fct_messages`

### Task 3: YOLO Image Enrichment
- Images from messages passed to YOLOv8
- Detected objects logged with confidence scores
- Stored in `fct_image_detections` fact table

### Task 4: Analytical API
- Built with FastAPI
- Endpoints include:
  - `/api/reports/top-products`
  - `/api/channels/{channel}/activity`
  - `/api/search/messages?query=...`

### Task 5: Pipeline Orchestration
- Dagster manages:
  - `scrape_telegram_data`
  - `load_raw_to_postgres`
  - `run_dbt_transformations`
  - `run_yolo_enrichment`
- Configurable schedules and job monitoring

## Running Locally

### 1. Clone Repo and Setup

```bash
git clone https://github.com/your-username/kara_medical_pipeline.git
cd kara_medical_pipeline
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

2. Setup Environment
Create a .env file based on the example below:

TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

POSTGRES_USER=dev
POSTGRES_PASSWORD=1234
POSTGRES_DB=kara_dbt
POSTGRES_PORT=5432

3. Run with Docker
dagster dev -w dagster_project/workspace.yaml

4. Start Dagster UI
bash
Copy
Edit
dagster dev -w dagster_project/workspace.yaml
5. Run dbt Models
bash
Copy
Edit
cd kara_dbt
dbt run
6. Start FastAPI Server
bash
Copy
Edit
uvicorn src.api.main:app --reload