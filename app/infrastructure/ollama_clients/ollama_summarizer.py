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
        try:
            # Set encoding explicitly and handle errors
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Error output: {result.stderr}")
                return "Error in summarization"
        except Exception as e:
            print(f"Exception during summarization: {str(e)}")
            return "Error in summarization" 