# yaml_grading.py
# YAML for Infrastructure as Code — Grader
# Cisco IaC Perspective
#
# HOW IT WORKS:
# 1. Write your solution in yaml_solution.py
# 2. Run this script: python3 yaml_grading.py
# 3. Fix any hints and re-run until you get Good Job!

import os
import sys
import yaml
import json
import shutil
import tempfile
import traceback

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

def fail(text):
    print(f"    {RED}✘  {text}{RESET}")

def hint(text):
    print(f"    {YELLOW}💡 Hint: {text}{RESET}")

def explain(text):
    print(f"  {WHITE}{text}{RESET}")

def blank():
    print()

def pretty(value):
    if isinstance(value, str):
        return value
    return repr(value)

# ─────────────────────────────────────────────────────────────────────────────
# DATA — same as challenge and solution
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

# ─────────────────────────────────────────────────────────────────────────────
# GRADER HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def run_solution(work_dir):
    filename = "yaml_solution.py"
    solution_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    if not os.path.exists(solution_path):
        blank()
        fail(f"File '{filename}' not found.")
        blank()
        explain(f"Create '{filename}' in the same folder as this grader.")
        blank()
        sys.exit(1)

    namespace = {
        "yaml": yaml,
        "json": json,
        "os": os,
        "DEVICE_YAML": DEVICE_YAML,
        "INVENTORY_YAML": INVENTORY_YAML,
        "DESIRED_STATE": DESIRED_STATE,
    }
    try:
        with open(solution_path) as f:
            code = f.read()
        import textwrap
        code = textwrap.dedent(code)
        old_cwd = os.getcwd()
        os.chdir(work_dir)
        try:
            exec(compile(code, filename, "exec"), namespace)
        finally:
            os.chdir(old_cwd)
        return namespace
    except Exception:
        blank()
        fail("Your script raised an error:")
        print()
        traceback.print_exc()
        blank()
        return None


def show_task_review(task_label, label, passed, actual, expected, hint_text, solution_ways, var_name):
    status = f"{GREEN}✔  PASSED{RESET}" if passed else f"{RED}✘  FAILED{RESET}"
    print(f"{BOLD}{'─' * 62}{RESET}")
    print(f"{BOLD}  {task_label}: {label}{RESET}")
    print(f"  {status}")
    print(f"{BOLD}{'─' * 62}{RESET}")
    blank()

    if not passed:
        hint(hint_text)
        blank()
        print(f"    {YELLOW}What your code produced:{RESET}")
        print(f"    {CYAN}>>> print({var_name}){RESET}")
        print(f"    {RED}{pretty(actual)}{RESET}")
        blank()

    print(f"    {YELLOW}Ways to write the solution:{RESET}")
    for way_label, way_code in solution_ways:
        print(f"    {YELLOW}  ▸ {way_label}{RESET}")
        for line in way_code:
            print(f"    {CYAN}    {line}{RESET}")
        blank()

    print(f"    {YELLOW}Correct output:{RESET}")
    print(f"    {CYAN}>>> print({var_name}){RESET}")
    print(f"    {GREEN}{pretty(expected)}{RESET}")
    blank()


def grade(checks):
    total = len(checks)
    passed = 0
    results = []
    for task_label, label, actual, expected, hint_text, solution_ways, var_name in checks:
        ok = (actual == expected)
        if ok:
            passed += 1
        results.append((task_label, label, ok, actual, expected, hint_text, solution_ways, var_name))

    blank()
    bar = "█" * 62
    score_color = GREEN if passed >= 7 else YELLOW if passed >= 5 else RED
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    print()
    print(f"{BOLD}  YOUR SCORE:  {score_color}{passed} / {total}{RESET}")
    print()
    for task_label, label, ok, *_ in results:
        mark = f"{GREEN}✔{RESET}" if ok else f"{RED}✘{RESET}"
        print(f"    {mark}  {task_label}: {label}")
    print()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")

    blank()
    explain("Press ENTER to review each task — solutions are shown for all tasks.")
    for result in results:
        pause()
        show_task_review(*result)

    blank()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    print()
    if passed == total:
        print(f"{BOLD}{GREEN}  ✔  PERFECT SCORE! You scored {passed}/{total}.{RESET}")
    elif passed >= 7:
        print(f"{BOLD}{GREEN}  ✔  GOOD JOB! You scored {passed}/{total}.{RESET}")
    else:
        print(f"{BOLD}{YELLOW}  You scored {passed}/{total}. Review, fix, and re-run.{RESET}")
    print()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    return passed


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         YAML FOR INFRASTRUCTURE AS CODE — GRADER{RESET}")
print(f"{BOLD}         Cisco IaC Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("Grading your yaml_solution.py ...")
blank()

work_dir = tempfile.mkdtemp(prefix="yaml_iac_grade_")
ns = run_solution(work_dir)

if ns:
    exp_device = yaml.safe_load(DEVICE_YAML)
    exp_device_hostname = exp_device["hostname"]
    exp_first_vlan = exp_device["vlans"][0]
    exp_last_backup_value = exp_device["last_backup"]
    exp_device_json = json.dumps(exp_device, indent=2, sort_keys=True)

    exp_parsed_inventory = yaml.safe_load(INVENTORY_YAML)
    exp_up_hostnames = [d["hostname"] for d in exp_parsed_inventory["devices"] if d["status"] == "up"]

    inventory_file_path = os.path.join(work_dir, "inventory.yaml")
    inventory_from_file_actual = None
    if os.path.exists(inventory_file_path):
        with open(inventory_file_path) as f:
            inventory_from_file_actual = yaml.safe_load(f)

    exp_desired_yaml = yaml.dump(DESIRED_STATE, default_flow_style=False, sort_keys=False)

    desired_file_path = os.path.join(work_dir, "desired_state.yaml")
    reloaded_desired_actual = None
    if os.path.exists(desired_file_path):
        with open(desired_file_path) as f:
            reloaded_desired_actual = yaml.safe_load(f)

    exp_devices_json = json.dumps(exp_parsed_inventory["devices"], indent=2, sort_keys=True)
    devices_json_parsed = None
    if ns.get("devices_json"):
        try:
            devices_json_parsed = json.loads(ns.get("devices_json"))
        except Exception:
            devices_json_parsed = "invalid json"

    ways = {
        "device": [("safe_load", ["device = yaml.safe_load(DEVICE_YAML)"])],
        "extract": [("dict/list access", ["device_hostname = device['hostname']", "first_vlan = device['vlans'][0]", "last_backup_value = device['last_backup']"])],
        "json": [("json.dumps", ["device_json = json.dumps(device, indent=2, sort_keys=True)"])],
        "inventory": [("parse and filter", ["parsed_inventory = yaml.safe_load(INVENTORY_YAML)", "up_hostnames = [d['hostname'] for d in parsed_inventory['devices'] if d['status'] == 'up']"])],
        "fileload": [("write string then load file", ["with open('inventory.yaml', 'w') as f:", "    f.write(INVENTORY_YAML)", "with open('inventory.yaml') as f:", "    inventory_from_file = yaml.safe_load(f)"])],
        "dump": [("yaml.dump options", ["desired_yaml = yaml.dump(DESIRED_STATE, default_flow_style=False, sort_keys=False)"])],
        "roundtrip": [("dump then safe_load", ["with open('desired_state.yaml', 'w') as f:", "    yaml.dump(DESIRED_STATE, f, default_flow_style=False, sort_keys=False)", "with open('desired_state.yaml') as f:", "    reloaded_desired_state = yaml.safe_load(f)"])],
        "devicesjson": [("YAML to JSON", ["devices = yaml.safe_load(INVENTORY_YAML)['devices']", "devices_json = json.dumps(devices, indent=2, sort_keys=True)"])],
    }

    grade([
        ("Task 1", "device — parsed YAML device dict",
         ns.get("device"), exp_device,
         "Use yaml.safe_load(DEVICE_YAML).", ways["device"], "device"),
        ("Task 2", "device_hostname, first_vlan, last_backup_value — extracted values",
         (ns.get("device_hostname"), ns.get("first_vlan"), ns.get("last_backup_value")),
         (exp_device_hostname, exp_first_vlan, exp_last_backup_value),
         "Extract values from device after Task 1.", ways["extract"], "(device_hostname, first_vlan, last_backup_value)"),
        ("Task 3", "device_json — parsed YAML converted to pretty JSON",
         ns.get("device_json"), exp_device_json,
         "Use json.dumps(device, indent=2, sort_keys=True).", ways["json"], "device_json"),
        ("Task 4", "parsed_inventory and up_hostnames — filtered UP devices",
         (ns.get("parsed_inventory"), ns.get("up_hostnames")),
         (exp_parsed_inventory, exp_up_hostnames),
         "Parse INVENTORY_YAML, then filter devices where status == 'up'.", ways["inventory"], "(parsed_inventory, up_hostnames)"),
        ("Task 5", "inventory_from_file — inventory.yaml loaded back",
         inventory_from_file_actual, exp_parsed_inventory,
         "Write INVENTORY_YAML to inventory.yaml, then safe_load the file.", ways["fileload"], "inventory_from_file"),
        ("Task 6", "desired_yaml — DESIRED_STATE serialized to YAML",
         ns.get("desired_yaml"), exp_desired_yaml,
         "Use yaml.dump(DESIRED_STATE, default_flow_style=False, sort_keys=False).", ways["dump"], "desired_yaml"),
        ("Task 7", "reloaded_desired_state — desired_state.yaml round trip",
         reloaded_desired_actual, DESIRED_STATE,
         "Dump DESIRED_STATE to desired_state.yaml and load it back.", ways["roundtrip"], "reloaded_desired_state"),
        ("Task 8", "devices_json — YAML devices converted to pretty JSON",
         devices_json_parsed, exp_parsed_inventory["devices"],
         "Parse INVENTORY_YAML, extract ['devices'], then json.dumps(...).", ways["devicesjson"], "json.loads(devices_json)"),
    ])

shutil.rmtree(work_dir, ignore_errors=True)
pause()
