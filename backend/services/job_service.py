from sqlalchemy.orm import Session
from backend.repository.job_repository import JobRepository
from backend.schemas.job_schema import JobCreate, JobRead

class JobService:
    def __init__(self, db: Session) -> None:
        self.repo = JobRepository(db)

    def create_jobs(self, jobs_in: list[JobCreate]) -> None:
        records = []
        for job in jobs_in:
            data = job.dict()
            # Asegura que job_url sea str, no HttpUrl
            data["job_url"] = str(data.get("job_url"))
            records.append(data)
        self.repo.upsert_batch(records)

    def get_jobs(self) -> list[JobRead]:
        return [JobRead.from_orm(job) for job in self.repo.list_all()]

    def get_job(self, job_id: int) -> JobRead | None:
        job = self.repo.get_by_id(job_id)
        return JobRead.from_orm(job) if job else None

    def delete_job(self, job_id: int) -> bool:
        return self.repo.delete(job_id)
