from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from backend.api.routers import router as jobs_router, ResponseModel
from backend.config.config_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="LinkedIn Scraper API",
    version="0.1.0",
    description="API to access and manage LinkedIn job listings",
    lifespan=lifespan,
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            status="error",
            message=str(exc.detail),
            data=None
        ).dict()
    )

app.include_router(jobs_router)