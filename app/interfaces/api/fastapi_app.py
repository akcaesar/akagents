"""
Author: Akshay NS
Contains: FastAPI application setup
    
"""

from fastapi import FastAPI
from .routes.summarize import router as summarize_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(summarize_router, prefix="/api", tags=["summarization"])
    return app

