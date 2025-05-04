from sqlalchemy import Column, Integer, String, Date
from backend.db.base import Base

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    company = Column(String(128), nullable=False)
    location = Column(String(128), nullable=False)
    date_posted = Column(Date, nullable=True)
    days_since_posted = Column(Integer, nullable=True)
    job_url = Column(String(512), nullable=False, unique=True, index=True)
    applicants = Column(Integer, nullable=True)

    def __repr__(self):
        return (
            f"<JobListing(id={self.id!r}, title={self.title!r}, company={self.company!r})>"
        )