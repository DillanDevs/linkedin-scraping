from typing import Iterable
from sqlalchemy.orm import Session
from backend.models.job_listing import JobListing

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_batch(self, records: Iterable[dict]) -> None:
        for rec in records:
            job = JobListing(**rec)
            self.db.merge(job)
        self.db.commit()
