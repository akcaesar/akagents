"""
Author: Akshay NS
Contains: FastAPI application setup
    
"""

from fastapi import FastAPI
from .routes.summarize import router as summarize_router
from .routes.email_processing import router as email_processing_router
def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(summarize_router, prefix="/api", tags=["summarization"])
    app.include_router(email_processing_router, prefix="/api", tags=["email_processing"])
    return app

