# End-to-End API Workflow — Your Solution File
# Cisco CAT8k / Nexus 9k Lab Perspective
#
# HOW TO USE:
# 1. Complete the tasks below
# 2. Run api_workflow_grading.py:
#    python3 api_workflow_grading.py
#
# LIVE LAB TESTING:
# Set environment variables before running live mode:
#   export CAT8K_HOST='your-cat8k-host-or-ip'
#   export CAT8K_USERNAME='your-username'
#   export CAT8K_PASSWORD='your-password'
#   export NEXUS9K_HOST='your-n9k-host-or-ip'
#   export NEXUS9K_USERNAME='your-username'
#   export NEXUS9K_PASSWORD='your-password'
#
# The grader uses live=False and sample responses, so it does not require
# live device access.

# DATA — do not edit this
# -----------------------------------------------------------------------------
import os
import json
import time

CAT8K_CONFIG = {
    "host": os.getenv("CAT8K_HOST", "cat8k-lab.example.com"),
    "username": os.getenv("CAT8K_USERNAME", "admin"),
    "password": os.getenv("CAT8K_PASSWORD", "password"),
    "verify_ssl": os.getenv("CAT8K_VERIFY_SSL", "false").lower() == "true",
    "timeout": int(os.getenv("CAT8K_TIMEOUT", "10")),
    "max_attempts": int(os.getenv("CAT8K_MAX_ATTEMPTS", "3")),
    "base_delay": int(os.getenv("CAT8K_BASE_DELAY", "1")),
    "interfaces_path": "/restconf/data/ietf-interfaces:interfaces",
}

NEXUS9K_CONFIG = {
    "host": os.getenv("NEXUS9K_HOST", "n9k-lab.example.com"),
    "username": os.getenv("NEXUS9K_USERNAME", "admin"),
    "password": os.getenv("NEXUS9K_PASSWORD", "password"),
    "verify_ssl": os.getenv("NEXUS9K_VERIFY_SSL", "false").lower() == "true",
    "timeout": int(os.getenv("NEXUS9K_TIMEOUT", "10")),
    "max_attempts": int(os.getenv("NEXUS9K_MAX_ATTEMPTS", "3")),
    "base_delay": int(os.getenv("NEXUS9K_BASE_DELAY", "1")),
    "nxapi_path": "/ins",
}

RETRYABLE_STATUS_CODES = [408, 429, 500, 502, 503, 504]
REQUIRED_REQUEST_KEYS = ["method", "url", "headers", "timeout", "max_attempts"]

CAT8K_SAMPLE_RESPONSE = {
    "ietf-interfaces:interfaces": {
        "interface": [
            {"name": "GigabitEthernet1", "enabled": True, "type": "iana-if-type:ethernetCsmacd"},
            {"name": "Loopback0", "enabled": True, "type": "iana-if-type:softwareLoopback"},
        ]
    }
}

NEXUS9K_SAMPLE_RESPONSE = {
    "ins_api": {
        "outputs": {
            "output": {
                "code": "200",
                "msg": "Success",
                "body": {
                    "TABLE_interface": {
                        "ROW_interface": [
                            {"interface": "Ethernet1/1", "state": "up"},
                            {"interface": "Ethernet1/2", "state": "down"},
                        ]
                    }
                },
            }
        }
    }
}

# -----------------------------------------------------------------------------
# YOUR ANSWERS
# -----------------------------------------------------------------------------

# Task 1 — Build a script that authenticates, retrieves data, handles timeouts/retries, and logs results


# Task 2 — Design a reusable API workflow with validation, retry logic, and safe request handling
