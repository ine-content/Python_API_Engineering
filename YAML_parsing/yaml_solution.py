# yaml_solution.py
# YAML for Infrastructure as Code — Your Solution File
# Cisco IaC Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run yaml_grading.py to check your answers:
#    python3 yaml_grading.py
#
# IMPORTANT:
# - Tasks 5 and 7 involve file I/O — use RELATIVE paths
# - The grader runs your script from a temporary working directory

# ─────────────────────────────────────────────────────────────────────────────
# DATA — do not edit this
# ─────────────────────────────────────────────────────────────────────────────
import yaml
import json
import os

DEVICE_YAML = """\
hostname: nyc-rtr-01
platform: IOS-XE
status: up
mgmt_ip: 10.0.0.1
vlans:
  - 10
  - 20
  - 30
last_backup: null
"""

INVENTORY_YAML = """\
devices:
  - hostname: nyc-rtr-01
    platform: IOS-XE
    status: up
    mgmt_ip: 10.0.0.1
    vlans: [10, 20, 30]
  - hostname: lon-sw-01
    platform: NX-OS
    status: down
    mgmt_ip: 10.1.0.1
    vlans: [10, 20]
  - hostname: sin-fw-01
    platform: ASA
    status: up
    mgmt_ip: 10.2.0.1
    vlans: [30, 40, 50]
"""

DESIRED_STATE = {
    "site": "NYC",
    "device": "nyc-rtr-01",
    "intended_config": {
        "ntp_servers": ["10.0.0.100", "10.0.0.101"],
        "dns_servers": ["8.8.8.8", "1.1.1.1"],
        "vlans": [10, 20, 30],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# YOUR ANSWERS
# ─────────────────────────────────────────────────────────────────────────────

# Task 1 — Parse a YAML device record


# Task 2 — Extract scalar and list values


# Task 3 — Convert parsed YAML to pretty JSON


# Task 4 — Parse inventory YAML and filter UP devices


# Task 5 — Load inventory YAML from a file


# Task 6 — Serialize desired state to YAML


# Task 7 — Write desired state YAML and read it back


# Task 8 — Convert YAML inventory devices to JSON
