# JSON for Infrastructure as Code — Student Challenges
# Cisco IaC Perspective
# Scenario-based tasks mapped directly to json_deep_dive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: json_solution.py
# 3. Run: python3 json_grading.py

import json
import copy
from datetime import datetime

# ── ANSI colors ───────────────────────────────────────────────────────────────
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
    explain("Available in json_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# ─────────────────────────────────────────────────────────────────────────────
# DATA — same data shapes used in the deep dive examples
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

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         JSON FOR INFRASTRUCTURE AS CODE — CHALLENGES{RESET}")
print(f"{BOLD}         3-Chapter Scenario Practice — Cisco IaC Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("8 scenario-based tasks mapped directly to the DeepDive examples.")
explain("For each task, read the scenario, use the available variable shown,")
explain("and create the required variable in json_solution.py.")
blank()
explain("Write answers in: json_solution.py")
explain("Then run: python3 json_grading.py")
blank()
explain("Printed JSON should use json.dumps(..., indent=2, sort_keys=True)")
explain("unless the task specifically asks for compact JSON.")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Serialize the IaC inventory payload as pretty JSON", "Easy")
explain("Scenario: You built a Python dictionary for a router inventory record.")
explain("Before saving it to Git, you need a readable JSON string that a")
explain("teammate can review in a pull request.")
blank()
available("payload")
explain("Your task: Create a variable named payload_pretty_json.")
explain("It must contain payload serialized with json.dumps(payload, indent=2, sort_keys=True).")
blank()
hint("Refer DeepDive Chapter 1.2 — JSON types map directly to Python types.")
blank()
output_intro()
header(">>> print(payload_pretty_json)")
header("{")
header('  "enabled": true,')
header('  "hostname": "nyc-rtr-01",')
header('  "last_backup": null,')
header('  "mgmt_ip": "10.0.0.1",')
header('  "platform": "IOS-XE",')
header('  "vlans": [')
header("    10,")
header("    20,")
header("    30")
header("  ]")
header("}")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Parse an API JSON response string", "Easy")
explain("Scenario: A device API returned JSON as text. Your automation cannot")
explain("inspect fields such as hostname or interfaces until that text becomes")
explain("a Python dictionary.")
blank()
available("api_response")
explain("Your task: Create a variable named device by parsing api_response with json.loads().")
blank()
hint("Refer DeepDive Chapter 1.3 — Parse API JSON with json.loads().")
blank()
output_intro()
header(">>> print(json.dumps(device, indent=2, sort_keys=True))")
header("{")
header('  "hostname": "nyc-rtr-01",')
header('  "interfaces": [')
header("    {...}")
header("  ],")
header('  "platform": "IOS-XE",')
header('  "status": "up"')
header("}")
blank()

pause()

# ── Task 3 ────────────────────────────────────────────────────────────────────
task_section(3, "Extract fields from parsed API JSON", "Easy")
explain("Scenario: After parsing the API response, your workflow needs two")
explain("specific values for the next automation step: the device hostname and")
explain("the first interface name.")
blank()
available("device")
explain("Your task: Create device_hostname and first_interface_name from device.")
blank()
hint("Refer DeepDive Chapter 1.3 — Parse API JSON with json.loads().")
blank()
output_intro()
header(">>> print(device_hostname)")
header("nyc-rtr-01")
header(">>> print(first_interface_name)")
header("Gi0/0")
blank()

pause()

# ── Task 4 ────────────────────────────────────────────────────────────────────
task_section(4, "Navigate NX-OS TABLE/ROW JSON", "Medium")
explain("Scenario: NX-OS wraps useful interface records inside TABLE_interface")
explain("and ROW_interface. Before normalizing the data, you need to reach the")
explain("actual list of interface rows.")
blank()
available("nxos_json")
explain("Your task: Parse nxos_json and create rows from TABLE_interface → ROW_interface.")
blank()
hint("Refer DeepDive Chapter 2.1 — Navigate nested device responses.")
blank()
output_intro()
header(">>> print(json.dumps(rows, indent=2, sort_keys=True))")
header("[")
header('  {"eth_ip_addr": "10.0.0.1", ...},')
header('  {"eth_ip_addr": "10.0.1.1", ...},')
header('  {"eth_ip_addr": "10.0.2.1", ...}')
header("]")
blank()

pause()

# ── Task 5 ────────────────────────────────────────────────────────────────────
task_section(5, "Normalize vendor-specific interface rows", "Medium")
explain("Scenario: Your IaC system should not depend on NX-OS field names.")
explain("Convert the vendor-specific rows into your standard internal shape so")
explain("later code can work the same way across platforms.")
blank()
available("rows")
explain("Your task: Create normalized as a list of dictionaries with name, state, vlan, and ip.")
explain("The vlan value must be an integer, not a string.")
blank()
hint("Refer DeepDive Chapter 2.2 — Normalize vendor data into your internal model.")
blank()
output_intro()
header(">>> print(json.dumps(normalized, indent=2, sort_keys=True))")
header("[")
header('  {"ip": "10.0.0.1", "name": "Ethernet1/1", "state": "up", "vlan": 10},')
header("  ...")
header("]")
blank()

pause()

# ── Task 6 ────────────────────────────────────────────────────────────────────
task_section(6, "Filter normalized data for automation decisions", "Medium")
explain("Scenario: Your automation should only act on interfaces that are up.")
explain("You also need a clean VLAN summary for those usable interfaces.")
blank()
available("normalized")
explain("Your task: Create up_interfaces and up_vlans.")
explain("up_interfaces must include only records where state == 'up'.")
explain("up_vlans must be a sorted list of unique VLAN integers from up_interfaces.")
blank()
hint("Refer DeepDive Chapter 2.3 — Filter parsed JSON for automation decisions.")
blank()
output_intro()
header(">>> print(json.dumps(up_interfaces, indent=2, sort_keys=True))")
header("[")
header('  {"ip": "10.0.0.1", "name": "Ethernet1/1", "state": "up", "vlan": 10},')
header('  {"ip": "10.0.2.1", "name": "Ethernet1/3", "state": "up", "vlan": 30}')
header("]")
header(">>> print(json.dumps(up_vlans, indent=2))")
header("[")
header("  10,")
header("  30")
header("]")
blank()

pause()

# ── Task 7 ────────────────────────────────────────────────────────────────────
task_section(7, "Serialize desired state as pretty and compact JSON", "Medium")
explain("Scenario: The same desired-state object is needed in two forms:")
explain("readable JSON for humans and compact JSON for API transport.")
blank()
available("desired_state")
explain("Your task: Create desired_state_pretty_json and compact_payload.")
explain("The pretty version must use indent=2 and sort_keys=True.")
explain("The compact version must use separators=(',', ':').")
blank()
hint("Refer DeepDive Chapter 3.1 and 3.2 — Build desired-state payloads and compact JSON.")
blank()
output_intro()
header(">>> print(desired_state_pretty_json)")
header("{")
header('  "device": "nyc-rtr-01",')
header('  "intended_config": { ... },')
header('  "site": "NYC"')
header("}")
header(">>> print(compact_payload[:40])")
header('{"site":"NYC","device":"nyc-rtr-01"')
blank()

pause()

# ── Task 8 ────────────────────────────────────────────────────────────────────
task_section(8, "Serialize a compliance report with datetime safely", "Medium")
explain("Scenario: A compliance report includes the desired state plus the time")
explain("the check was performed. Python datetime objects cannot be serialized")
explain("to JSON directly, so your script needs a safe conversion function.")
blank()
available("desired_state", "copy", "datetime")
explain("Your task: Create report_json.")
explain("Deep-copy desired_state into report, add checked_at and compliant, then serialize it.")
explain("Use datetime(2026, 1, 15, 10, 30), compliant=True, default=your function,")
explain("indent=2, and sort_keys=True.")
blank()
hint("Refer DeepDive Chapter 3.3 — Serialize datetime safely.")
blank()
output_intro()
header(">>> parsed = json.loads(report_json)")
header(">>> print(parsed['checked_at'])")
header("2026-01-15T10:30:00")
header(">>> print(parsed['compliant'])")
header("True")
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
print(f"{BOLD}{CYAN}    json_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 json_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
