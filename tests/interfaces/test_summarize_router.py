"""
Author: Akshay NS    # Use the correct endpoint with /api prefix
    response = client.post("/api/summarize", params={"text": "This is some long text."})
    assert response.status_code == 200
    assert response.json() == {"summary": "fake summary"}ntains: test for summarize router (Only tests the routing + serialization logic, not the heavy model calls.)
    
"""

# tests/interfaces/api/test_summarize_router.py
from fastapi.testclient import TestClient
from app.interfaces.api.fastapi_app import create_app
from app.domain.services.summarization_service import SummarizationService

class FakeSummarizer(SummarizationService):
    def summarize(self, text: str) -> str:
        return "fake summary"

def test_summarize_endpoint(monkeypatch):
    app = create_app()
    client = TestClient(app)

    # Monkeypatch the OllamaSummarizer used in the route
    from app.interfaces.api.routes import summarize
    summarize.OllamaSummarizer = lambda model_name: FakeSummarizer()

    response = client.post("api/summarize", params={"text": "This is some long text."})
    assert response.status_code == 200
    assert response.json() == {"summary": "fake summary"}
