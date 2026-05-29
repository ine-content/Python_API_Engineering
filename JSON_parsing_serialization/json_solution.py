# json_solution.py
# JSON for Infrastructure as Code — Your Solution File
# Cisco IaC Perspective
#
# HOW TO USE:
# 1. Write your answer for each task below
# 2. Run json_grading.py to check your answers:
#    python3 json_grading.py

import json
import copy
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# DATA — do not edit this
# ─────────────────────────────────────────────────────────────────────────────
payload = {
    "hostname": "nyc-rtr-01",
    "platform": "IOS-XE",
    "enabled": True,
    "mgmt_ip": "10.0.0.1",
    "vlans": [10, 20, 30],
    "last_backup": None,
}

api_response = '''{
  "hostname": "nyc-rtr-01",
  "platform": "IOS-XE",
  "status": "up",
  "interfaces": [
    {"name": "Gi0/0", "state": "up", "vlan": 10},
    {"name": "Gi0/1", "state": "down", "vlan": 20}
  ]
}'''

nxos_json = json.dumps({
    "TABLE_interface": {
        "ROW_interface": [
            {"interface": "Ethernet1/1", "state": "up", "vlan": "10", "eth_ip_addr": "10.0.0.1"},
            {"interface": "Ethernet1/2", "state": "down", "vlan": "20", "eth_ip_addr": "10.0.1.1"},
            {"interface": "Ethernet1/3", "state": "up", "vlan": "30", "eth_ip_addr": "10.0.2.1"},
        ]
    }
})

desired_state = {
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

# Task 1 — Serialize the IaC inventory payload as pretty JSON
# Variable name: payload_pretty_json


# Task 2 — Parse an API JSON response string
# Variable name: device


# Task 3 — Extract fields from parsed API JSON
# Variable names: device_hostname / first_interface_name


# Task 4 — Navigate NX-OS TABLE/ROW JSON
# Variable name: rows


# Task 5 — Normalize vendor-specific interface rows
# Variable name: normalized


# Task 6 — Filter normalized data for automation decisions
# Variable names: up_interfaces / up_vlans


# Task 7 — Serialize desired state as pretty and compact JSON
# Variable names: desired_state_pretty_json / compact_payload


# Task 8 — Serialize a compliance report with datetime safely
# Variable name: report_json

