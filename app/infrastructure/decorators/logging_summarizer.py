"""  
Author: Akshay NS
Contains: a logging decorator which wraps the summarization service to log the input and output of the summarization process.

"""

import time, logging
from app.domain.services.summarization_service import SummarizationService

logger = logging.getLogger('summarization_logger')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = ("[%(asctime)s] %(levelname)s: %(message)s")
handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(handler)


class LoggingSummarizer(SummarizationService):
    def __init__(self, wrapped: SummarizationService):
        self._wrapped = wrapped
        
    def summarize(self, text: str | None) -> str:
        start = time.time()
        try:
            logger.info(f"Input text length: {len(text) if text else 0}")
            result = self._wrapped.summarize(text)
            duration = time.time() - start
            logger.info(f"Summarization completed in {duration:.2f}s, output length: {len(result)}, model used : {self._wrapped.model_name}")
            return result
        except Exception as e:
            logger.exception("Error during summarization")
            raise