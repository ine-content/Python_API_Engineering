# YAML for Infrastructure as Code — Student Challenges
# Cisco IaC Perspective
# Scenario-based tasks mapped directly to yaml_deep_dive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: yaml_solution.py
# 3. Run: python3 yaml_grading.py

import os
import yaml
import json

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
    explain("Available in yaml_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# ─────────────────────────────────────────────────────────────────────────────
# DATA — same data shapes used in the deep dive examples
# ─────────────────────────────────────────────────────────────────────────────

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

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         YAML FOR INFRASTRUCTURE AS CODE — CHALLENGES{RESET}")
print(f"{BOLD}         3-Chapter Scenario Practice — Cisco IaC Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("8 scenario-based tasks mapped directly to the DeepDive examples.")
explain("For each task, read the scenario, use the available variable shown,")
explain("and create the required variable in yaml_solution.py.")
blank()
explain("Write answers in: yaml_solution.py")
explain("Then run: python3 yaml_grading.py")
blank()
explain("Use yaml.safe_load() when parsing YAML.")
explain("Use yaml.dump(..., default_flow_style=False, sort_keys=False)")
explain("when the task asks for readable YAML output.")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Parse a YAML device record", "Easy")
explain("Scenario: A network automation workflow receives a YAML device record")
explain("for a branch router. Before your Python code can inspect fields such as")
explain("hostname, platform, or VLANs, the YAML text must become a Python dictionary.")
blank()
available("DEVICE_YAML")
explain("Your task: Create a variable named device.")
explain("It must contain DEVICE_YAML parsed with yaml.safe_load(DEVICE_YAML).")
blank()
hint("Refer DeepDive Chapter 2.1 — Parse a YAML String with yaml.safe_load().")
blank()
output_intro()
header(">>> print(device['hostname'])")
header("nyc-rtr-01")
header(">>> print(type(device))")
header("<class 'dict'>")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Extract scalar and list values", "Easy")
explain("Scenario: After parsing the device YAML, your automation needs a few")
explain("specific values for downstream validation: the hostname, the first VLAN,")
explain("and the backup status.")
blank()
available("device")
explain("Your task: Create device_hostname, first_vlan, and last_backup_value.")
explain("device_hostname must come from device['hostname'].")
explain("first_vlan must be the first item in device['vlans'].")
explain("last_backup_value must be the parsed value of device['last_backup'].")
blank()
hint("Refer DeepDive Chapter 1.2 — Mappings, Sequences, and Scalars.")
blank()
output_intro()
header(">>> print(device_hostname, first_vlan, last_backup_value)")
header("nyc-rtr-01 10 None")
blank()

pause()

# ── Task 3 ────────────────────────────────────────────────────────────────────
task_section(3, "Convert parsed YAML to pretty JSON", "Easy")
explain("Scenario: Another system accepts JSON, not YAML. You already have the")
explain("device data as a Python dictionary, so now you need to serialize it into")
explain("a readable JSON string for review or API handoff.")
blank()
available("device")
explain("Your task: Create a variable named device_json.")
explain("It must contain json.dumps(device, indent=2, sort_keys=True).")
blank()
hint("Refer DeepDive Chapter 1.3 — YAML vs JSON: Same Data, Different Format.")
blank()
output_intro()
header(">>> print(device_json[:40])")
header("{")
header('  "hostname": "nyc-rtr-01",')
blank()

pause()

# ── Task 4 ────────────────────────────────────────────────────────────────────
task_section(4, "Parse inventory YAML and filter UP devices", "Medium")
explain("Scenario: Your inventory file contains devices across multiple sites.")
explain("The automation should only target devices that are currently marked up,")
explain("while preserving the inventory order.")
blank()
available("INVENTORY_YAML")
explain("Your task: Create parsed_inventory and up_hostnames.")
explain("parsed_inventory must contain INVENTORY_YAML parsed with yaml.safe_load().")
explain("up_hostnames must include only hostnames where status == 'up'.")
blank()
hint("Refer DeepDive Chapter 2.2 — Parse an Inventory and Filter Devices.")
blank()
output_intro()
header(">>> print(up_hostnames)")
header("['nyc-rtr-01', 'sin-fw-01']")
blank()

pause()

# ── Task 5 ────────────────────────────────────────────────────────────────────
task_section(5, "Load inventory YAML from a file", "Medium")
explain("Scenario: In real IaC workflows, inventory data is usually stored in")
explain("files instead of hardcoded strings. Your script needs to write the YAML")
explain("inventory to disk and then load it back as Python data.")
blank()
available("INVENTORY_YAML")
explain("Your task: Create inventory_from_file.")
explain("Write INVENTORY_YAML to the relative path inventory.yaml.")
explain("Then load inventory.yaml back with yaml.safe_load().")
blank()
hint("Refer DeepDive Chapter 2.3 — Load YAML from a File.")
blank()
output_intro()
header(">>> print(len(inventory_from_file['devices']))")
header("3")
blank()

pause()

# ── Task 6 ────────────────────────────────────────────────────────────────────
task_section(6, "Serialize desired state to YAML", "Medium")
explain("Scenario: Your intended network configuration exists as Python data.")
explain("To store it in an IaC repository, you need to export it as readable YAML")
explain("while preserving the key order.")
blank()
available("DESIRED_STATE")
explain("Your task: Create a variable named desired_yaml.")
explain("It must contain yaml.dump(DESIRED_STATE, default_flow_style=False, sort_keys=False).")
blank()
hint("Refer DeepDive Chapter 3.1 — Serialize Python Data with yaml.dump().")
blank()
output_intro()
header(">>> print(type(desired_yaml))")
header("<class 'str'>")
header(">>> print(desired_yaml.splitlines()[0])")
header("site: NYC")
blank()

pause()

# ── Task 7 ────────────────────────────────────────────────────────────────────
task_section(7, "Write desired state YAML and read it back", "Medium")
explain("Scenario: Before trusting generated YAML in an automation pipeline,")
explain("you want to prove the desired-state data survives a write/read round trip")
explain("without changing its structure or values.")
blank()
available("DESIRED_STATE")
explain("Your task: Create reloaded_desired_state.")
explain("Write DESIRED_STATE to the relative path desired_state.yaml using")
explain("yaml.dump(..., default_flow_style=False, sort_keys=False).")
explain("Then read desired_state.yaml back with yaml.safe_load().")
blank()
hint("Refer DeepDive Chapter 3.2 — Write YAML to a File and Read It Back.")
blank()
output_intro()
header(">>> print(reloaded_desired_state == DESIRED_STATE)")
header("True")
blank()

pause()

# ── Task 8 ────────────────────────────────────────────────────────────────────
task_section(8, "Convert YAML inventory devices to JSON", "Medium")
explain("Scenario: A REST API does not need the full inventory wrapper. It only")
explain("expects the devices list from the YAML inventory, serialized as pretty JSON.")
blank()
available("INVENTORY_YAML")
explain("Your task: Create a variable named devices_json.")
explain("Parse INVENTORY_YAML, extract the devices list, and serialize that list")
explain("with json.dumps(..., indent=2, sort_keys=True).")
blank()
hint("Refer DeepDive Chapter 3.3 — Convert YAML Inventory to JSON for an API.")
blank()
output_intro()
header(">>> data = json.loads(devices_json)")
header(">>> print(type(data), len(data), data[0]['hostname'])")
header("<class 'list'> 3 nyc-rtr-01")
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
print(f"{BOLD}{CYAN}    yaml_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 yaml_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
