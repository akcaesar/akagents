from app.application.use_cases.run_summarization import RunSummarization
from app.domain.services.summarization_service import SummarizationService
from app.infrastructure.ollama_clients.ollama_summarizer import OllamaSummarizer
# class FakeSummarizer(SummarizationService):
#     def summarize(self, text: str) -> str:
#         return "This is a fake summary."
    
    
    
    
    

def test_run_summarization():
    # Initialize the summarizer with your model
    summarizer = OllamaSummarizer(model_name="gemma3:1b")
    use_case = RunSummarization(summarizer)
    
    # Test text that should be summarized
    test_text = "This is a test text. My name is akshay ns. The sky is blue. " * 3
    
    # Get the summary
    summary = use_case.execute(test_text)
    
    # Test that we got a non-empty response
    assert summary is not None
    assert len(summary) > 0
    
    # Print both original text and summary for comparison
    print("\nOriginal text:")
    print("-" * 80)
    print(test_text)
    print("\nGenerated Summary:")
    print("-" * 80)
    print(summary)
    print("-" * 80)
    
    # Test that the summary is shorter than the original text
    assert len(summary) < len(test_text)
    
    # # Test that some key information is preserved (optional)
    # assert any(word in summary.lower() for word in ["akshay", "test", "sky"])