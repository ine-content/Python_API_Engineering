# Payload Handling for Network Automation — Student Challenges
# Cisco API Perspective
# Scenario-based tasks mapped directly to payload_deepdive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: payload_solution.py
# 3. Run: python3 payload_grading.py

import json
import os
import yaml

RESET  = "\033[0m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

def pause():
    input(f"\n{DIM}  [ Press ENTER to continue ]{RESET} ")
    print()

def header(text):
    print(f"    {CYAN}{text}{RESET}")

def explain(text):
    print(f"  {WHITE}{text}{RESET}")

def hint(text):
    print(f"  {YELLOW}Hint: {text}{RESET}")

def blank():
    print()

def task_section(num, title, difficulty):
    stars = {"Easy": "★☆☆", "Medium": "★★☆", "Hard": "★★★"}
    label = f"Task {num:02d} — {title}  |  {difficulty} {stars[difficulty]}"
    print(f"{BOLD}{'─' * 70}{RESET}")
    print(f"{BOLD}  {label}{RESET}")
    print(f"{BOLD}{'─' * 70}{RESET}")
    blank()

def available(*names):
    explain("Available in payload_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# DATA — same data shapes used in the deep dive examples
# -----------------------------------------------------------------------------

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

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         PAYLOAD HANDLING FOR NETWORK AUTOMATION — CHALLENGES{RESET}")
print(f"{BOLD}         3-Chapter Scenario Practice — Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("8 scenario-based tasks mapped directly to the DeepDive examples.")
explain("For each task, read the scenario, use the available variable shown,")
explain("and create the required variable in payload_solution.py.")
blank()
explain("Write answers in: payload_solution.py")
explain("Then run: python3 payload_grading.py")
blank()
explain("Use json.loads() for JSON strings, yaml.safe_load() for YAML strings,")
explain("and json.dump/json.load when the task requires file-based JSON handling.")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Parse JSON and YAML payloads", "Easy")
explain("Scenario: Your automation receives the same device record in two")
explain("common payload formats: JSON from an API and YAML from an IaC file.")
explain("Before your code can compare or inspect them, both payloads must be")
explain("converted into Python dictionaries.")
blank()
available("DEVICE_JSON", "DEVICE_YAML")
explain("Your task: Create device_from_json and device_from_yaml.")
explain("device_from_json must come from json.loads(DEVICE_JSON).")
explain("device_from_yaml must come from yaml.safe_load(DEVICE_YAML).")
blank()
hint("Refer DeepDive Chapter 1.2 — Reading JSON and YAML.")
blank()
output_intro()
header(">>> print(device_from_json['hostname'], device_from_yaml['hostname'])")
header("nyc-rtr-01 nyc-rtr-01")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Extract structured values", "Easy")
explain("Scenario: After parsing the JSON payload, your workflow needs a few")
explain("specific values for validation and reporting: the hostname, the first")
explain("tag, and the number of interfaces in the payload.")
blank()
available("device_from_json  (created in Task 1)")
explain("Your task: Create payload_hostname, first_tag, and interface_count.")
explain("payload_hostname must come from device_from_json['hostname'].")
explain("first_tag must be the first item in device_from_json['tags'].")
explain("interface_count must be the length of device_from_json['interfaces'].")
blank()
hint("Refer DeepDive Chapter 1.3 — Structured inputs and outputs.")
blank()
output_intro()
header(">>> print(payload_hostname, first_tag, interface_count)")
header("nyc-rtr-01 edge 2")
blank()

pause()

# ── Task 3 ────────────────────────────────────────────────────────────────────
task_section(3, "Handle nested payload data", "Easy")
explain("Scenario: Device payloads often contain nested objects. Your script")
explain("needs to inspect the first interface object and extract the fields that")
explain("matter for automation decisions.")
blank()
available("device_from_json  (created in Task 1)")
explain("Your task: Create first_interface, first_interface_name, and first_interface_enabled.")
explain("first_interface must be device_from_json['interfaces'][0].")
explain("first_interface_name must come from first_interface['name'].")
explain("first_interface_enabled must come from first_interface['enabled'].")
blank()
hint("Refer DeepDive Chapter 2.1 — Handling nested payloads.")
blank()
output_intro()
header(">>> print(first_interface_name, first_interface_enabled)")
header("GigabitEthernet1 True")
blank()

pause()

# ── Task 4 ────────────────────────────────────────────────────────────────────
task_section(4, "Filter a larger dataset", "Medium")
explain("Scenario: Your inventory contains devices across several sites.")
explain("The automation should only target devices that are currently up, while")
explain("keeping the same order as the source inventory.")
blank()
available("LARGE_INVENTORY")
explain("Your task: Create up_device_hostnames.")
explain("It must contain hostnames from LARGE_INVENTORY['devices'] where status == 'up'.")
explain("Preserve the original order from the inventory.")
blank()
hint("Refer DeepDive Chapter 2.2 — Handling large datasets.")
blank()
output_intro()
header(">>> print(up_device_hostnames)")
header("['nyc-rtr-01', 'sin-fw-01', 'sfo-rtr-01']")
blank()

pause()

# ── Task 5 ────────────────────────────────────────────────────────────────────
task_section(5, "Summarize a larger dataset", "Medium")
explain("Scenario: Before taking action on an inventory, your automation needs")
explain("a quick summary of how many devices are up, down, or in maintenance.")
blank()
available("LARGE_INVENTORY")
explain("Your task: Create a dictionary named status_counts.")
explain("Count every device in LARGE_INVENTORY['devices'] by its status value.")
explain("Expected keys are up, down, and maintenance.")
blank()
hint("Refer DeepDive Chapter 2.2 — Handling large datasets.")
blank()
output_intro()
header(">>> print(status_counts)")
header("{'up': 3, 'down': 1, 'maintenance': 1}")
blank()

pause()

# ── Task 6 ────────────────────────────────────────────────────────────────────
task_section(6, "Raw to structured transformation", "Medium")
explain("Scenario: A legacy monitoring system exports pipe-delimited event")
explain("strings. To use those events in modern automation, each string must be")
explain("converted into a structured dictionary.")
blank()
available("RAW_EVENTS")
explain("Your task: Create structured_events.")
explain("Split each raw event on '|'.")
explain("Use the keys hostname, platform, status, interface, and mgmt_ip.")
blank()
hint("Refer DeepDive Chapter 3.1 — Raw to structured transformation.")
blank()
output_intro()
header(">>> print(structured_events[0]['interface'])")
header("GigabitEthernet1")
blank()

pause()

# ── Task 7 ────────────────────────────────────────────────────────────────────
task_section(7, "Write and read JSON payloads", "Medium")
explain("Scenario: After transforming raw events, your workflow needs to save")
explain("the structured data to a JSON file and then prove it can be loaded back")
explain("without changing the data.")
blank()
available("structured_events  (created in Task 6)")
explain("Your task: Create events_from_file.")
explain("Write structured_events to the relative path events.json.")
explain("Use json.dump(..., indent=2, sort_keys=True).")
explain("Then read events.json back with json.load().")
blank()
hint("Refer DeepDive Chapter 3.3 — Writing structured output to files.")
blank()
output_intro()
header(">>> print(events_from_file == structured_events)")
header("True")
blank()

pause()

# ── Task 8 ────────────────────────────────────────────────────────────────────
task_section(8, "Build API-ready payload and YAML report", "Medium")
explain("Scenario: Your automation needs an API-ready object containing the")
explain("structured device events, plus a YAML report that humans can review.")
blank()
available("structured_events  (created in Task 6)")
explain("Your task: Create api_payload and report_yaml.")
explain("api_payload must be {'devices': structured_events, 'count': len(structured_events)}.")
explain("report_yaml must serialize api_payload with block style and sort_keys=False.")
explain("Use yaml.dump(api_payload, default_flow_style=False, sort_keys=False).")
blank()
hint("Refer DeepDive Chapter 3.2 — Building API-ready output.")
blank()
output_intro()
header(">>> print(api_payload['count'])")
header("3")
header(">>> print(report_yaml.splitlines()[0])")
header("devices:")
blank()

pause()

# ═════════════════════════════════════════════════════════════════════════════
# DONE
# ═════════════════════════════════════════════════════════════════════════════
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}  All tasks read. Write your answers in:{RESET}")
print()
print(f"{BOLD}{CYAN}    payload_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 payload_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
