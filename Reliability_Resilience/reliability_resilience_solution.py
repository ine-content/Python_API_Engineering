# Reliability & Resilience — Your Solution File
# Cisco API Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run reliability_resilience_grading.py to check your answers:
#    python3 reliability_resilience_grading.py

# DATA — do not edit this
# -----------------------------------------------------------------------------
import json
import os

API_REQUEST = {
    "method": "GET",
    "url": "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device",
    "headers": {
        "Accept": "application/json",
        "X-Auth-Token": "abc123sandbox-token",
    },
}

RETRY_POLICY = {
    "max_attempts": 4,
    "base_delay": 1,
    "retryable_status_codes": [408, 429, 500, 502, 503, 504],
}

SIMULATED_RESPONSES = [
    {"attempt": 1, "status_code": 503},
    {"attempt": 2, "status_code": 503},
    {"attempt": 3, "status_code": 200},
]

CREATE_JOB_REQUEST = {
    "method": "POST",
    "url": "https://controller.example.local/api/v1/jobs",
    "body": {
        "device": "nyc-rtr-01",
        "operation": "backup",
    },
}

# -----------------------------------------------------------------------------
# YOUR ANSWERS
# -----------------------------------------------------------------------------

# Task 1 — Add timeout settings to an API request


# Task 2 — Build exponential backoff delays


# Task 3 — Identify retryable responses


# Task 4 — Add an idempotency key to a POST request


# Task 5 — Build a resilience summary JSON string
