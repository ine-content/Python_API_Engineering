# payload_grading.py
# Payload Handling for Network Automation — Grader
# Cisco API Perspective
#
# HOW IT WORKS:
# 1. Write your solution in payload_solution.py
# 2. Run this script: python3 payload_grading.py
# 3. Fix any hints and re-run until you get Good Job!

import os
import sys
import yaml
import json
import shutil
import tempfile
import traceback

RESET  = "\033[0m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

def pause(): input(f"\n{DIM}  [ Press ENTER to continue ]{RESET} "); print()
def fail(text): print(f"    {RED}✘  {text}{RESET}")
def hint(text): print(f"    {YELLOW}💡 Hint: {text}{RESET}")
def explain(text): print(f"  {WHITE}{text}{RESET}")
def blank(): print()
def pretty(value): return value if isinstance(value, str) else repr(value)

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
# GRADER HELPERS
# -----------------------------------------------------------------------------
def run_solution(work_dir):
    filename = "payload_solution.py"
    solution_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(solution_path):
        blank(); fail(f"File '{filename}' not found."); blank(); explain(f"Create '{filename}' in the same folder as this grader."); blank(); sys.exit(1)
    namespace = {"yaml": yaml, "json": json, "os": os, "DEVICE_JSON": DEVICE_JSON, "DEVICE_YAML": DEVICE_YAML, "RAW_EVENTS": RAW_EVENTS, "LARGE_INVENTORY": LARGE_INVENTORY}
    try:
        with open(solution_path) as f:
            code = f.read()
        import textwrap
        code = textwrap.dedent(code)
        old_cwd = os.getcwd(); os.chdir(work_dir)
        try:
            exec(compile(code, filename, "exec"), namespace)
        finally:
            os.chdir(old_cwd)
        return namespace
    except Exception:
        blank(); fail("Your script raised an error:"); print(); traceback.print_exc(); blank(); return None

def show_task_review(task_label, label, passed, actual, expected, hint_text, solution_ways, var_name):
    status = f"{GREEN}✔  PASSED{RESET}" if passed else f"{RED}✘  FAILED{RESET}"
    print(f"{BOLD}{'─' * 62}{RESET}"); print(f"{BOLD}  {task_label}: {label}{RESET}"); print(f"  {status}"); print(f"{BOLD}{'─' * 62}{RESET}"); blank()
    if not passed:
        hint(hint_text); blank(); print(f"    {YELLOW}What your code produced:{RESET}"); print(f"    {CYAN}>>> print({var_name}){RESET}"); print(f"    {RED}{pretty(actual)}{RESET}"); blank()
    print(f"    {YELLOW}Ways to write the solution:{RESET}")
    for way_label, way_code in solution_ways:
        print(f"    {YELLOW}  ▸ {way_label}{RESET}")
        for line in way_code:
            print(f"    {CYAN}    {line}{RESET}")
        blank()
    print(f"    {YELLOW}Correct output:{RESET}"); print(f"    {CYAN}>>> print({var_name}){RESET}"); print(f"    {GREEN}{pretty(expected)}{RESET}"); blank()

def grade(checks):
    total = len(checks); passed = 0; results = []
    for task_label, label, actual, expected, hint_text, solution_ways, var_name in checks:
        ok = (actual == expected); passed += 1 if ok else 0
        results.append((task_label, label, ok, actual, expected, hint_text, solution_ways, var_name))
    blank(); bar = "█" * 62; score_color = GREEN if passed >= 7 else YELLOW if passed >= 5 else RED
    print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print(); print(f"{BOLD}  YOUR SCORE:  {score_color}{passed} / {total}{RESET}"); print()
    for task_label, label, ok, *_ in results:
        mark = f"{GREEN}✔{RESET}" if ok else f"{RED}✘{RESET}"
        print(f"    {mark}  {task_label}: {label}")
    print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}")
    blank(); explain("Press ENTER to review each task — solutions are shown for all tasks.")
    for result in results:
        pause(); show_task_review(*result)
    blank(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
    if passed == total: print(f"{BOLD}{GREEN}  ✔  PERFECT SCORE! You scored {passed}/{total}.{RESET}")
    elif passed >= 7: print(f"{BOLD}{GREEN}  ✔  GOOD JOB! You scored {passed}/{total}.{RESET}")
    else: print(f"{BOLD}{YELLOW}  You scored {passed}/{total}. Review, fix, and re-run.{RESET}")
    print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); return passed

print(); bar = "█" * 62
print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
print(f"{BOLD}         PAYLOAD HANDLING FOR NETWORK AUTOMATION — GRADER{RESET}")
print(f"{BOLD}         Cisco API Perspective{RESET}")
print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank(); explain("Grading your payload_solution.py ..."); blank()

work_dir = tempfile.mkdtemp(prefix="payload_grade_")
ns = run_solution(work_dir)

if ns:
    exp_json = json.loads(DEVICE_JSON)
    exp_yaml = yaml.safe_load(DEVICE_YAML)
    exp_payload_hostname = exp_json["hostname"]
    exp_first_tag = exp_json["tags"][0]
    exp_interface_count = len(exp_json["interfaces"])
    exp_first_interface = exp_json["interfaces"][0]
    exp_first_interface_name = exp_first_interface["name"]
    exp_first_interface_enabled = exp_first_interface["enabled"]
    exp_up_device_hostnames = [d["hostname"] for d in LARGE_INVENTORY["devices"] if d["status"] == "up"]
    exp_status_counts = {}
    for d in LARGE_INVENTORY["devices"]:
        exp_status_counts[d["status"]] = exp_status_counts.get(d["status"], 0) + 1
    exp_structured_events = []
    for line in RAW_EVENTS:
        hostname, platform, status, interface, mgmt_ip = line.split("|")
        exp_structured_events.append({"hostname": hostname, "platform": platform, "status": status, "interface": interface, "mgmt_ip": mgmt_ip})
    events_file_path = os.path.join(work_dir, "events.json")
    events_from_file_actual = None
    if os.path.exists(events_file_path):
        with open(events_file_path) as f:
            try:
                events_from_file_actual = json.load(f)
            except Exception:
                events_from_file_actual = "invalid json file"
    exp_api_payload = {"devices": exp_structured_events, "count": len(exp_structured_events)}
    exp_report_yaml = yaml.dump(exp_api_payload, default_flow_style=False, sort_keys=False)

    ways = {
        "parse": [("loads", ["device_from_json = json.loads(DEVICE_JSON)", "device_from_yaml = yaml.safe_load(DEVICE_YAML)"])],
        "extract": [("dict/list access", ["payload_hostname = device_from_json['hostname']", "first_tag = device_from_json['tags'][0]", "interface_count = len(device_from_json['interfaces'])"])],
        "nested": [("nested access", ["first_interface = device_from_json['interfaces'][0]", "first_interface_name = first_interface['name']", "first_interface_enabled = first_interface['enabled']"])],
        "filter": [("list comprehension", ["up_device_hostnames = [d['hostname'] for d in LARGE_INVENTORY['devices'] if d['status'] == 'up']"])],
        "count": [("loop and increment", ["status_counts = {}", "for d in LARGE_INVENTORY['devices']:", "    status_counts[d['status']] = status_counts.get(d['status'], 0) + 1"])],
        "transform": [("split lines", ["structured_events = []", "for line in RAW_EVENTS:", "    hostname, platform, status, interface, mgmt_ip = line.split('|')", "    structured_events.append({'hostname': hostname, 'platform': platform, 'status': status, 'interface': interface, 'mgmt_ip': mgmt_ip})"])],
        "jsonfile": [("dump then load", ["with open('events.json', 'w') as f:", "    json.dump(structured_events, f, indent=2, sort_keys=True)", "with open('events.json') as f:", "    events_from_file = json.load(f)"])],
        "apiyaml": [("build and dump", ["api_payload = {'devices': structured_events, 'count': len(structured_events)}", "report_yaml = yaml.dump(api_payload, default_flow_style=False, sort_keys=False)"])],
    }

    grade([
        ("Task 1", "device_from_json and device_from_yaml — parsed payloads", (ns.get("device_from_json"), ns.get("device_from_yaml")), (exp_json, exp_yaml), "Use json.loads() and yaml.safe_load().", ways["parse"], "(device_from_json, device_from_yaml)"),
        ("Task 2", "payload_hostname, first_tag, interface_count — extracted values", (ns.get("payload_hostname"), ns.get("first_tag"), ns.get("interface_count")), (exp_payload_hostname, exp_first_tag, exp_interface_count), "Extract values from device_from_json after Task 1.", ways["extract"], "(payload_hostname, first_tag, interface_count)"),
        ("Task 3", "first_interface fields — nested payload access", (ns.get("first_interface"), ns.get("first_interface_name"), ns.get("first_interface_enabled")), (exp_first_interface, exp_first_interface_name, exp_first_interface_enabled), "Access device_from_json['interfaces'][0] first.", ways["nested"], "(first_interface, first_interface_name, first_interface_enabled)"),
        ("Task 4", "up_device_hostnames — filtered large dataset", ns.get("up_device_hostnames"), exp_up_device_hostnames, "Filter LARGE_INVENTORY['devices'] where status == 'up'.", ways["filter"], "up_device_hostnames"),
        ("Task 5", "status_counts — summarized large dataset", ns.get("status_counts"), exp_status_counts, "Loop through LARGE_INVENTORY['devices'] and count each status.", ways["count"], "status_counts"),
        ("Task 6", "structured_events — raw strings transformed to dicts", ns.get("structured_events"), exp_structured_events, "Split each RAW_EVENTS line on '|'.", ways["transform"], "structured_events"),
        ("Task 7", "events_from_file — JSON file round trip", events_from_file_actual, exp_structured_events, "Write structured_events to events.json, then json.load it back.", ways["jsonfile"], "events_from_file"),
        ("Task 8", "api_payload and report_yaml — structured output", (ns.get("api_payload"), ns.get("report_yaml")), (exp_api_payload, exp_report_yaml), "Build api_payload, then serialize it with yaml.dump(..., sort_keys=False).", ways["apiyaml"], "(api_payload, report_yaml)"),
    ])

shutil.rmtree(work_dir, ignore_errors=True)
pause()
