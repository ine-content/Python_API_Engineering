# API Authentication — Your Solution File
# Cisco API Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run api_authentication_grading.py to check your answers:
#    python3 api_authentication_grading.py

# DATA — do not edit this
# -----------------------------------------------------------------------------
import base64
import json
import os

IOSXE_SANDBOX = {
    "url": "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/ietf-interfaces:interfaces",
    "username": "devnetuser",
    "password": "Cisco123!",
    "accept": "application/yang-data+json",
}

CATALYST_CENTER_SANDBOX = {
    "devices_url": "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device",
    "token": "abc123sandbox-token",
    "accept": "application/json",
}

# -----------------------------------------------------------------------------
# YOUR ANSWERS
# -----------------------------------------------------------------------------

# Task 1 — Build a Basic Auth header for IOS XE Sandbox


# Task 2 — Build a token header for Catalyst Center Sandbox



