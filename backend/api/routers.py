from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.config.config_db import get_db
from backend.schemas.job_schema import JobCreate
from backend.services.job_service import JobService
from typing import List
from backend.schemas.response_schemas import ResponseModel, ListResponseModel, SingleResponseModel

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel,
    summary="Bulk create or update job listings",
    responses={
        status.HTTP_201_CREATED: {"description": "Jobs successfully created or updated"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error"}
    }
)
async def create_jobs(
    payload: List[JobCreate],
    db: Session = Depends(get_db)
) -> ResponseModel:
    """
    Create or update multiple job listings.
    """
    JobService(db).create_jobs(payload)
    return ResponseModel(
        message=f"{len(payload)} job(s) added or updated"
    )

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ListResponseModel,
    summary="Retrieve all job listings"
)
async def read_jobs(
    db: Session = Depends(get_db)
) -> ListResponseModel:
    """
    Get a list of all job listings.
    """
    jobs = JobService(db).get_jobs()
    return ListResponseModel(data=jobs)

@router.get(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=SingleResponseModel,
    summary="Get a single job listing by ID",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Job not found"}}
)
async def read_job(
    job_id: int,
    db: Session = Depends(get_db)
) -> SingleResponseModel:
    """
    Get a job listing by its ID.
    """
    job = JobService(db).get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return SingleResponseModel(data=job)

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
    summary="Delete a job listing by ID",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Job not found"}}
)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
) -> ResponseModel:
    """
    Delete a job listing by its ID.
    Returns a confirmation message upon successful deletion.
    """
    success = JobService(db).delete_job(job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return ResponseModel(
        message=f"Job with id {job_id} successfully deleted"
    )
