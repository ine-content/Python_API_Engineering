# Safety — Your Solution File
# Cisco API Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run safety_grading.py to check your answers:
#    python3 safety_grading.py

# DATA — do not edit this
# -----------------------------------------------------------------------------
import json
import os

CHANGE_REQUEST = {
    "hostname": "nyc-rtr-01",
    "interface": "GigabitEthernet1",
    "description": "WAN uplink",
}

REQUIRED_FIELDS = ["hostname", "interface", "description"]
ALLOWED_INTERFACES = ["GigabitEthernet1", "GigabitEthernet2", "Loopback0"]

ERROR_RESPONSE = {
    "status_code": 400,
    "body": {
        "error": "invalid interface",
        "detail": "Interface GigabitEthernet99 does not exist",
    },
}

REQUEST_CONTEXT = {
    "method": "PATCH",
    "url": "https://controller.example.local/api/v1/interfaces/GigabitEthernet99",
    "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer secret-token-value",
    },
}

RECOVERY_MAP = {
    400: "stop_and_fix_payload",
    401: "stop_and_refresh_credentials",
    403: "stop_and_check_permissions",
    404: "skip_missing_resource",
    409: "stop_and_review_conflict",
    500: "retry_or_escalate",
    503: "retry_with_backoff",
}

CHANGE_PLAN = {
    "device": "nyc-rtr-01",
    "interface": "GigabitEthernet1",
    "new_description": "WAN uplink",
    "previous_description": "old description",
}

# -----------------------------------------------------------------------------
# YOUR ANSWERS
# -----------------------------------------------------------------------------

# Task 1 — Validate required fields before a request


# Task 2 — Validate allowed values before a request


# Task 3 — Build a safe error summary


# Task 4 — Choose a recovery action and rollback plan


# Task 5 — Build a safety summary JSON string
