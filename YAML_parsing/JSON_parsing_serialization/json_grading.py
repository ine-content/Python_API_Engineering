# json_grading.py
# JSON for Infrastructure as Code — Grader
# Cisco IaC Perspective
#
# HOW IT WORKS:
# 1. Write your solution in json_solution.py
# 2. Run this script: python3 json_grading.py
# 3. Fix any hints and re-run until you get Good Job!

import os
import sys
import json
import copy
import traceback
from datetime import datetime

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
    return json.dumps(value, indent=2, sort_keys=True)

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

def run_solution():
    filename = "json_solution.py"
    if not os.path.exists(filename):
        blank()
        fail(f"File '{filename}' not found.")
        blank()
        explain(f"Create '{filename}' in the same folder as this grader.")
        blank()
        sys.exit(1)

    namespace = {
        "json": json,
        "copy": copy,
        "datetime": datetime,
        "payload": payload,
        "api_response": api_response,
        "nxos_json": nxos_json,
        "desired_state": desired_state,
    }
    try:
        with open(filename) as f:
            code = f.read()
        exec(compile(code, filename, "exec"), namespace)
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
    if isinstance(expected, str):
        for line in expected.splitlines():
            print(f"    {GREEN}{line}{RESET}")
    else:
        for line in json.dumps(expected, indent=2, sort_keys=True).splitlines():
            print(f"    {GREEN}{line}{RESET}")
    blank()

def grade(checks):
    total = len(checks)
    passed = 0
    results = []
    for task_label, label, actual, expected, hint_text, solution_ways, var_name in checks:
        ok = actual == expected
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

print()
bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         JSON FOR INFRASTRUCTURE AS CODE — GRADER{RESET}")
print(f"{BOLD}         Cisco IaC Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("Grading your json_solution.py ...")
blank()

ns = run_solution()
if ns:
    exp_payload_pretty_json = json.dumps(payload, indent=2, sort_keys=True)
    exp_device = json.loads(api_response)
    exp_device_hostname = exp_device["hostname"]
    exp_first_interface_name = exp_device["interfaces"][0]["name"]
    exp_rows = json.loads(nxos_json)["TABLE_interface"]["ROW_interface"]
    exp_normalized = [
        {"name": i["interface"], "state": i["state"], "vlan": int(i["vlan"]), "ip": i["eth_ip_addr"]}
        for i in exp_rows
    ]
    exp_up_interfaces = [i for i in exp_normalized if i["state"] == "up"]
    exp_up_vlans = sorted({i["vlan"] for i in exp_up_interfaces})
    exp_desired_state_pretty_json = json.dumps(desired_state, indent=2, sort_keys=True)
    exp_compact_payload = json.dumps(desired_state, separators=(",", ":"))
    def _iac_default(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Cannot serialize {type(obj)}")
    exp_report = copy.deepcopy(desired_state)
    exp_report["checked_at"] = datetime(2024, 1, 15, 10, 30)
    exp_report["compliant"] = True
    exp_report_json = json.dumps(exp_report, default=_iac_default, indent=2, sort_keys=True)

    grade([
        ("Task 1", "payload_pretty_json — readable inventory JSON", ns.get("payload_pretty_json"), exp_payload_pretty_json, "Use json.dumps(payload, indent=2, sort_keys=True).", [("Pretty json.dumps", ["payload_pretty_json = json.dumps(payload, indent=2, sort_keys=True)"])], "payload_pretty_json"),
        ("Task 2", "device — parsed API response dict", ns.get("device"), exp_device, "Use json.loads(api_response).", [("Parse the JSON string", ["device = json.loads(api_response)"])], "json.dumps(device, indent=2, sort_keys=True)"),
        ("Task 3", "device_hostname and first_interface_name — extracted fields", (ns.get("device_hostname"), ns.get("first_interface_name")), (exp_device_hostname, exp_first_interface_name), "Use device['hostname'] and device['interfaces'][0]['name'].", [("Read dict/list fields", ["device_hostname = device['hostname']", "first_interface_name = device['interfaces'][0]['name']"])], "(device_hostname, first_interface_name)"),
        ("Task 4", "rows — NX-OS TABLE/ROW interface rows", ns.get("rows"), exp_rows, "Parse nxos_json, then navigate TABLE_interface → ROW_interface.", [("Parse then navigate TABLE/ROW", ["data = json.loads(nxos_json)", "rows = data['TABLE_interface']['ROW_interface']"])], "json.dumps(rows, indent=2, sort_keys=True)"),
        ("Task 5", "normalized — standard interface model", ns.get("normalized"), exp_normalized, "Rename fields and convert VLAN with int(i['vlan']).", [("List comprehension", ["normalized = [", "    {'name': i['interface'], 'state': i['state'],", "     'vlan': int(i['vlan']), 'ip': i['eth_ip_addr']}", "    for i in rows", "]"])], "json.dumps(normalized, indent=2, sort_keys=True)"),
        ("Task 6", "up_interfaces and up_vlans — filtered automation decision data", (ns.get("up_interfaces"), ns.get("up_vlans")), (exp_up_interfaces, exp_up_vlans), "Filter state == 'up', then build sorted unique VLANs.", [("Filter and summarize", ["up_interfaces = [i for i in normalized if i['state'] == 'up']", "up_vlans = sorted({i['vlan'] for i in up_interfaces})"])], "(up_interfaces, up_vlans)"),
        ("Task 7", "desired_state_pretty_json and compact_payload — two JSON forms", (ns.get("desired_state_pretty_json"), ns.get("compact_payload")), (exp_desired_state_pretty_json, exp_compact_payload), "Use indent/sort_keys for pretty output and separators=(',', ':') for compact output.", [("Pretty and compact serialization", ["desired_state_pretty_json = json.dumps(desired_state, indent=2, sort_keys=True)", "compact_payload = json.dumps(desired_state, separators=(',', ':'))"])], "(desired_state_pretty_json, compact_payload)"),
        ("Task 8", "report_json — compliance report with serialized datetime", ns.get("report_json"), exp_report_json, "Use copy.deepcopy, add checked_at and compliant, and serialize datetime with default=.", [("Deep copy plus default", ["def iac_default(obj):", "    if isinstance(obj, datetime):", "        return obj.isoformat()", "    raise TypeError(f'Cannot serialize {type(obj)}')", "", "report = copy.deepcopy(desired_state)", "report['checked_at'] = datetime(2024, 1, 15, 10, 30)", "report['compliant'] = True", "report_json = json.dumps(report, default=iac_default, indent=2, sort_keys=True)"])], "report_json"),
    ])

pause()
