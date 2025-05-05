from typing import List, Optional
from sqlalchemy.orm import Session
from backend.repository.job_repository import JobRepository
from backend.schemas.job_schema import JobCreate, JobRead

class JobService:

    def __init__(self, db: Session) -> None:
        """
        Initialize the service with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.repo = JobRepository(db)

    def create_jobs(self, jobs_in: List[JobCreate]) -> None:
        """
        Bulk create or update job listings.

        Converts Pydantic HttpUrl to plain string before persisting.

        Args:
            jobs_in (List[JobCreate]): List of validated job creation schemas.
        """
        records = []
        for job in jobs_in:
            data = job.dict()
            data["job_url"] = str(data["job_url"])
            records.append(data)
        self.repo.upsert_batch(records)

    def get_jobs(self) -> List[JobRead]:
        """
        Retrieve all stored job listings.

        Returns:
            List[JobRead]: List of job reading schemas.
        """
        jobs = self.repo.list_all()
        return [JobRead.from_orm(job) for job in jobs]

    def get_job(self, job_id: int) -> Optional[JobRead]:
        """
        Retrieve a single job listing by its ID.

        Args:
            job_id (int): The ID of the job to retrieve.

        Returns:
            Optional[JobRead]: The job reading schema if found, else None.
        """
        job = self.repo.get_by_id(job_id)
        return JobRead.from_orm(job) if job else None

    def delete_job(self, job_id: int) -> bool:
        """
        Delete a job listing by its ID.

        Args:
            job_id (int): The ID of the job to delete.

        Returns:
            bool: True if deletion succeeded, False if no record was found.
        """
        return self.repo.delete(job_id)