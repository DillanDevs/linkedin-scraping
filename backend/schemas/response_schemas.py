from pydantic import BaseModel
from typing import Optional, List
from .job_schema import JobRead

class ResponseModel(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[dict] = None

class ListResponseModel(BaseModel):
    status: str = "success"
    data: List[JobRead]

class SingleResponseModel(BaseModel):
    status: str = "success"
    data: JobRead
