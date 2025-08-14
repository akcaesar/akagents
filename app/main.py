"""  
Author: Akshay NS
Contains: Main entry point for the FastAPI application.
"""
import uvicorn
from app.interfaces.api.fastapi_app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )