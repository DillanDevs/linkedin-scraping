from collections.abc import Iterable
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.job_listing import JobListing

class JobRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[JobListing]:
        """
        Devuelve todas las ofertas de trabajo.
        """
        return self.db.query(JobListing).all()

    def get_by_id(self, job_id: int) -> Optional[JobListing]:
        """
        Busca una oferta por su ID.
        """
        return (
            self.db
            .query(JobListing)
            .filter(JobListing.id == job_id)
            .first()
        )

    def upsert_batch(self, records: Iterable[dict]) -> None:
        """
        Inserta o actualiza (merge) una lista de registros de ofertas.
        """
        for rec in records:
            job = JobListing(**rec)
            self.db.merge(job)
        self.db.commit()

    def delete(self, job_id: int) -> bool:
        """
        Elimina la oferta con el ID dado.
        Retorna True si se eliminó, False si no existía.
        """
        count = (
            self.db
            .query(JobListing)
            .filter(JobListing.id == job_id)
            .delete()
        )
        if count:
            self.db.commit()
            return True
        return False
