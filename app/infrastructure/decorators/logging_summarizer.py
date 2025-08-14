"""
Author: Akshay NS
Module: LoggingSummarizer
Description:
    A logging decorator which wraps any SummarizationService implementation
    to log inputs, outputs, execution time, and model metadata. Supports
    console and JSON file logging.

"""

import time
import logging
import json
from app.domain.services.summarization_service import SummarizationService
from pathlib import Path

# Create log directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Logger setup
logger = logging.getLogger("summarization_logger")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)

# File handler (JSON logs)
file_handler = logging.FileHandler(log_dir / "summarizer.jsonl")
file_handler.setFormatter(logging.Formatter('%(message)s'))  # we'll log JSON strings manually

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class LoggingSummarizer(SummarizationService):
    """
    Decorator for SummarizationService to log input, output, duration, errors,
    and model metadata to console and JSON file.
    """

    def __init__(self, wrapped: SummarizationService):
        self._wrapped = wrapped

    def summarize(self, text: str | None) -> str:
        start = time.time()
        log_data = {
            "input_length": len(text) if text else 0,
            "model_name": getattr(self._wrapped, "model_name", "unknown"),
            "timestamp": time.time()
        }

        try:
            result = self._wrapped.summarize(text)
            duration = time.time() - start
            log_data.update({
                "output_length": len(result),
                "duration_sec": round(duration, 4),
                "status": "success"
            })

            # Log to console (formatted)
            logger.info(f"Summarization completed in {duration:.2f}s, output length: {len(result)}, model: {log_data['model_name']}")
            
            # Log to JSON file
            logger.info(json.dumps(log_data))

            return result

        except Exception as e:
            log_data.update({
                "status": "error",
                "error": str(e)
            })
            logger.exception("Error during summarization")
            logger.info(json.dumps(log_data))  # log error in JSON file
            raise
