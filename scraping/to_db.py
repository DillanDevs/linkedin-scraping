import pandas as pd
from dotenv import load_dotenv
from backend.config.config_db import SessionLocal, init_db
from backend.repository.job_repository import JobRepository

load_dotenv()

def load_csv_to_db(csv_path: str = "dataset_linkedin.csv") -> None:
    init_db()
    df = pd.read_csv(csv_path, parse_dates=["date_posted"])
    records = []
    for row in df.to_dict(orient="records"):
        applicants_val = row.get("applicants")
        days_val = row.get("days_since_posted")
        records.append({
            "title":             row["title"],
            "company":           row["company"],
            "location":          row["location"],
            "date_posted":       row["date_posted"].date() if row["date_posted"] else None,
            "days_since_posted": int(days_val) if days_val is not None and not pd.isna(days_val) else None,
            "applicants":        int(applicants_val) if applicants_val is not None and not pd.isna(applicants_val) else None,
            "job_url":           row["job_url"],
        })
    with SessionLocal() as db:
        repo = JobRepository(db)
        repo.upsert_batch(records)
