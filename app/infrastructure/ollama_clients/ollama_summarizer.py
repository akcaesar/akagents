""" 
Author: Akshay NS
Contains: Ollama Adapter

"""

import subprocess
import sys
import os

# Add project root to Python path when running directly
if __name__ == "__main__" or __name__ == "__mp_main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    sys.path.insert(0, project_root)

from app.domain.services.summarization_service import SummarizationService


class OllamaSummarizer(SummarizationService):
    def __init__(self, model_name: str):
        self.model_name = model_name
        
    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text: {text}"
        command = ["ollama", "run", self.model_name, prompt]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "Error in summarization" 