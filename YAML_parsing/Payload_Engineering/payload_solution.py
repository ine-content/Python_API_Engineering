# payload_solution.py
# Payload Handling for Network Automation — Your Solution File
# Cisco API Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run payload_grading.py to check your answers:
#    python3 payload_grading.py
#
# IMPORTANT:
# - Tasks 7 and 8 involve file I/O — use RELATIVE paths
# - The grader runs your script from a temporary working directory

# DATA — do not edit this
# -----------------------------------------------------------------------------
import json
import os
import yaml

DEVICE_JSON = """\
{
  "hostname": "nyc-rtr-01",
  "platform": "IOS-XE",
  "status": "up",
  "mgmt_ip": "10.0.0.1",
  "interfaces": [
    {"name": "GigabitEthernet1", "enabled": true, "description": "WAN"},
    {"name": "GigabitEthernet2", "enabled": false, "description": "LAN"}
  ],
  "tags": ["edge", "wan", "production"]
}
"""

DEVICE_YAML = """\
hostname: nyc-rtr-01
platform: IOS-XE
status: up
mgmt_ip: 10.0.0.1
interfaces:
  - name: GigabitEthernet1
    enabled: true
    description: WAN
  - name: GigabitEthernet2
    enabled: false
    description: LAN
tags:
  - edge
  - wan
  - production
"""

RAW_EVENTS = [
    "nyc-rtr-01|IOS-XE|up|GigabitEthernet1|10.0.0.1",
    "lon-sw-01|NX-OS|down|Ethernet1/1|10.1.0.1",
    "sin-fw-01|ASA|up|Management0/0|10.2.0.1",
]

LARGE_INVENTORY = {
    "devices": [
        {"hostname": "nyc-rtr-01", "site": "NYC", "status": "up", "vlans": [10, 20, 30], "interfaces": {"wan": {"ip": "10.0.0.1", "enabled": True}}},
        {"hostname": "lon-sw-01", "site": "LON", "status": "down", "vlans": [10, 20], "interfaces": {"wan": {"ip": "10.1.0.1", "enabled": False}}},
        {"hostname": "sin-fw-01", "site": "SIN", "status": "up", "vlans": [30, 40, 50], "interfaces": {"wan": {"ip": "10.2.0.1", "enabled": True}}},
        {"hostname": "sfo-rtr-01", "site": "SFO", "status": "up", "vlans": [10, 60], "interfaces": {"wan": {"ip": "10.3.0.1", "enabled": True}}},
        {"hostname": "dal-sw-01", "site": "DAL", "status": "maintenance", "vlans": [70], "interfaces": {"wan": {"ip": "10.4.0.1", "enabled": False}}},
    ]
}

# -----------------------------------------------------------------------------
# YOUR ANSWERS
# -----------------------------------------------------------------------------

# Task 1 — Parse JSON and YAML payloads


# Task 2 — Extract structured values


# Task 3 — Handle nested payload data


# Task 4 — Filter a larger dataset


# Task 5 — Summarize a larger dataset


# Task 6 — Transform raw strings into structured records


# Task 7 — Write structured records to JSON and read them back


# Task 8 — Build an API-ready payload and YAML report
