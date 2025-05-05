from collections.abc import Iterable
from typing import Optional
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from backend.models.job_listing import JobListing


class JobRepository:

    def __init__(self, db: Session) -> None:
        """
        Initialize the repository with a database session.

        Args:
            db (Session): SQLAlchemy session.
        """
        self.db = db

    def list_all(self) -> list[JobListing]:
        """
        Retrieve all job listings from the database.

        Returns:
            list[JobListing]: A list of all JobListing instances.
        """
        return self.db.query(JobListing).all()

    def get_by_id(self, job_id: int) -> Optional[JobListing]:
        """
        Find a job listing by its ID.

        Args:
            job_id (int): The ID of the job listing to retrieve.

        Returns:
            Optional[JobListing]: The JobListing if found, else None.
        """
        return self.db.query(JobListing).filter(JobListing.id == job_id).first()

    def upsert_batch(self, records: Iterable[dict]) -> None:
        """
        Bulk insert or update job listings in a single statement.
        On conflict of 'job_url', all other columns are updated.

        Args:
            records (Iterable[dict]): An iterable of dicts representing job data.
        """
        stmt = insert(JobListing).values(list(records))

        # Build a dict of columns to update on conflict, excluding 'id'
        update_columns = {
            col.name: getattr(stmt.excluded, col.name)
            for col in JobListing.__table__.columns
            if col.name != "id"
        }

        stmt = stmt.on_conflict_do_update(
            index_elements=["job_url"], set_=update_columns
        )

        self.db.execute(stmt)
        self.db.commit()

    def delete(self, job_id: int) -> bool:
        """
        Delete a job listing by its ID.

        Args:
            job_id (int): The ID of the job listing to delete.

        Returns:
            bool: True if a record was deleted, False otherwise.
        """
        deleted_count = (
            self.db.query(JobListing).filter(JobListing.id == job_id).delete()
        )
        if deleted_count:
            self.db.commit()
            return True
        return False
