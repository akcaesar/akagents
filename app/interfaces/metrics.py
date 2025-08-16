"""
Author: Akshay NS
Contains: Prometheus metrics definitions for summarization service
"""

from prometheus_client import Counter, Histogram

# Counter for total requests by model
REQUESTS_TOTAL = Counter(
    'summarization_requests_total',
    'Total summarization requests',
    ['model_name']
)

# Histogram for response times by model
RESPONSE_TIME = Histogram(
    'summarization_duration_seconds',
    'Time spent processing request',
    ['model_name'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]  # buckets based on your latency patterns
)

# Counter for successful requests
SUCCESS_TOTAL = Counter(
    'summarization_success_total',
    'Successful summarization requests',
    ['model_name']
)

# Counter for failed requests
FAILURE_TOTAL = Counter(
    'summarization_failure_total',
    'Failed summarization requests',
    ['model_name']
)

# Histogram for input/output length ratios
LENGTH_RATIO = Histogram(
    'summarization_length_ratio',
    'Ratio of output length to input length',
    ['model_name'],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]
)
