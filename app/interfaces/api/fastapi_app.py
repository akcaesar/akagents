"""
Author: Akshay NS
Contains: FastAPI application setup
    
"""

from fastapi import FastAPI
from .routes.summarize import router as summarize_router
from prometheus_client import make_asgi_app

def create_app() -> FastAPI:
    app = FastAPI(title="AK Agents API")
    
    # Add routes
    app.include_router(summarize_router, prefix="/api", tags=["summarization"])
    
    # Add Prometheus metrics endpoint
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    return app

