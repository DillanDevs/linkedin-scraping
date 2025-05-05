from datetime import date
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    company: str = Field(..., min_length=1, max_length=128)
    location: str = Field(..., min_length=1, max_length=128)
    date_posted: date | None = Field(
        None,
        description="ISO date when the job was posted"
    )
    days_since_posted: int | None = Field(
        None,
        ge=0,
        description="Days since the job was posted"
    )
    applicants: int | None = Field(
        None,
        ge=0,
        description="Number of applicants"
    )
    job_url: HttpUrl = Field(
        ...,
        description="LinkedIn URL of the job listing"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )

class JobCreate(JobBase):
    """Schema for creating or updating a job listing"""

class JobRead(JobBase):
    id: int = Field(..., ge=1)

    model_config = ConfigDict(
        from_attributes=True
    )
