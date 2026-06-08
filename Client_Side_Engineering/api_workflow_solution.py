# Client Side Engineering — Your Solution File
# Cisco API Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run api_workflow_grading.py to check your answers:
#    python3 api_workflow_grading.py

import json
import os

API_CONFIG = {
    "base_url": "https://sandboxdnac.cisco.com",
    "devices_path": "/dna/intent/api/v1/network-device",
    "token": "abc123sandbox-token",
    "accept": "application/json",
}

NEW_DEVICE = {
    "hostname": "sfo-rtr-01",
    "platform": "IOS-XE",
    "mgmt_ip": "10.3.0.1",
}

RAW_DEVICE_RESPONSE = """\
{
  "hostname": "nyc-rtr-01",
  "id": "device-101",
  "status": "reachable"
}
"""

API_RESPONSES = [
    {"method": "GET", "path": "/devices", "status_code": 200, "body": '{"count": 2}'},
    {"method": "POST", "path": "/devices", "status_code": 201, "body": '{"id": "device-999"}'},
    {"method": "GET", "path": "/devices/missing", "status_code": 404, "body": '{"error": "not found"}'},
    {"method": "PATCH", "path": "/devices/nyc-rtr-01", "status_code": 500, "body": '{"error": "server error"}'},
]

# -----------------------------------------------------------------------------
# YOUR ANSWERS
# -----------------------------------------------------------------------------

# Task 1 — Build a GET request dictionary


# Task 2 — Build a POST request and serialize the body


# Task 3 — Deserialize a raw JSON response


# Task 4 — Separate successful and failed API responses


# Task 5 — Build a JSON API run summary
