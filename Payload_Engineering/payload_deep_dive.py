# Payload Handling for Network Automation — 3-Chapter Deep Dive
# Cisco IaC / API Perspective
# Press ENTER to advance through each step

import json
import os
import shutil
import tempfile
import yaml

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

def cmd(command):
    print(f"    {CYAN}>>> {command}{RESET}")

def out(value):
    print(f"    {GREEN}{value}{RESET}")

def warn(value):
    print(f"    {RED}{value}{RESET}")

def explain(text):
    print(f"  {WHITE}{text}{RESET}")

def blank():
    print()

def block(text):
    for line in text.splitlines():
        print(f"    {CYAN}{line}{RESET}")

def show_json(value):
    for line in json.dumps(value, indent=2, sort_keys=True).splitlines():
        out(line)

def show_yaml(value):
    for line in yaml.dump(value, default_flow_style=False, sort_keys=False).splitlines():
        out(line)

def section(title):
    print(f"{BOLD}{'─' * 62}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{BOLD}{'─' * 62}{RESET}")
    blank()

def chapter(num, title):
    bar = "█" * 62
    print()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    print()
    print(f"{BOLD}   CHAPTER {num}{RESET}")
    print(f"{BOLD}   {title}{RESET}")
    print()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    blank()

DEMO_DIR = tempfile.mkdtemp(prefix="payload_3ch_demo_")
def demo(filename):
    return os.path.join(DEMO_DIR, filename)

bar = "█" * 62
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         PAYLOAD HANDLING FOR NETWORK AUTOMATION{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — Payload Fundamentals
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "Payload Fundamentals")

section("1.1 — What a payload is")
explain("A payload is structured data your automation reads, transforms, or sends.")
explain("In network automation, payloads commonly appear as JSON from APIs")
explain("and YAML from human-authored intent files.")
blank()
explain("Scenario: A controller API returns one raw JSON payload for a device.")
explain("Before you parse anything, look at the actual payload text your script received.")
blank()
received_payload = """\
{
  "hostname": "nyc-rtr-01",
  "platform": "IOS-XE",
  "status": "up",
  "mgmt_ip": "10.0.0.1",
  "interfaces": [
    {
      "name": "GigabitEthernet1",
      "admin_status": "up",
      "oper_status": "up"
    },
    {
      "name": "GigabitEthernet2",
      "admin_status": "down",
      "oper_status": "down"
    }
  ]
}
"""
cmd("received_payload = " + '"""')
block(received_payload.rstrip())
cmd('"""')
blank()
explain("At this point, it is still just text — the same kind of string an API response body may contain.")
blank()
cmd("device = json.loads(received_payload)")
device = json.loads(received_payload)
cmd("print(device['hostname'])")
out(device["hostname"])
cmd("print(device['interfaces'][0]['name'])")
out(device["interfaces"][0]["name"])
cmd("print(type(device))")
out(type(device))
blank()
explain("The raw payload string becomes a Python dict your code can inspect.")
explain("Nested JSON objects become dictionaries; JSON arrays become lists.")
pause()

section("1.2 — Reading JSON and YAML")
explain("JSON and YAML can represent the same payload shape.")
explain("json.loads() reads JSON strings. yaml.safe_load() reads YAML strings.")
blank()
yaml_text = """\
hostname: nyc-rtr-01
platform: IOS-XE
status: up
vlans:
  - 10
  - 20
  - 30
"""
json_text = '{"hostname":"nyc-rtr-01","platform":"IOS-XE","status":"up","vlans":[10,20,30]}'
cmd("from_json = json.loads(json_text)")
from_json = json.loads(json_text)
cmd("from_yaml = yaml.safe_load(yaml_text)")
from_yaml = yaml.safe_load(yaml_text)
cmd("print(from_json == from_yaml)")
out(from_json == from_yaml)
blank()
show_json(from_json)
blank()
explain("Different syntax. Same Python data model.")
pause()

section("1.3 — Structured inputs and outputs")
explain("Good automation does not pass around random strings forever.")
explain("It converts input into predictable dictionaries and lists, then")
explain("returns structured output that another tool can consume.")
blank()
raw_line = "nyc-rtr-01|IOS-XE|up|10.0.0.1"
cmd("hostname, platform, status, ip = raw_line.split('|')")
hostname, platform, status, ip = raw_line.split('|')
cmd("structured = {'hostname': hostname, 'platform': platform, 'status': status, 'mgmt_ip': ip}")
structured = {"hostname": hostname, "platform": platform, "status": status, "mgmt_ip": ip}
cmd("print(structured)")
out(structured)
blank()
explain("Raw text is fragile. Structured data is easier to validate and transform.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Working with Real Payload Shapes
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "Working with Real Payload Shapes")

section("2.1 — Handling nested payloads")
explain("API responses often contain dictionaries inside lists inside dictionaries.")
explain("Use bracket access step by step, and keep the path readable.")
blank()
payload = {
    "device": {
        "hostname": "nyc-rtr-01",
        "interfaces": [
            {"name": "GigabitEthernet1", "enabled": True, "ip": "10.0.0.1"},
            {"name": "GigabitEthernet2", "enabled": False, "ip": None},
        ],
    }
}
cmd("first_interface = payload['device']['interfaces'][0]")
first_interface = payload["device"]["interfaces"][0]
cmd("print(first_interface['name'])")
out(first_interface["name"])
cmd("print(first_interface['ip'])")
out(first_interface["ip"])
blank()
explain("Read nested payloads from the outside in: dict key, dict key, list index.")
pause()

section("2.2 — Handling large datasets")
explain("Large datasets should be filtered and summarized instead of printed blindly.")
blank()
inventory = {
    "devices": [
        {"hostname": "nyc-rtr-01", "site": "NYC", "status": "up", "vlans": [10, 20, 30]},
        {"hostname": "lon-sw-01", "site": "LON", "status": "down", "vlans": [10, 20]},
        {"hostname": "sin-fw-01", "site": "SIN", "status": "up", "vlans": [30, 40, 50]},
        {"hostname": "sfo-rtr-01", "site": "SFO", "status": "up", "vlans": [10, 60]},
    ]
}
cmd("up_devices = [d for d in inventory['devices'] if d['status'] == 'up']")
up_devices = [d for d in inventory["devices"] if d["status"] == "up"]
cmd("hostnames = [d['hostname'] for d in up_devices]")
hostnames = [d["hostname"] for d in up_devices]
cmd("print(hostnames)")
out(hostnames)
blank()
cmd("site_counts = {}")
cmd("for d in inventory['devices']:")
cmd("    site_counts[d['site']] = site_counts.get(d['site'], 0) + 1")
site_counts = {}
for d in inventory["devices"]:
    site_counts[d["site"]] = site_counts.get(d["site"], 0) + 1
cmd("print(site_counts)")
out(site_counts)
pause()

section("2.3 — Validating expected keys")
explain("Before transforming a payload, confirm the fields you depend on exist.")
blank()
required_keys = ["hostname", "platform", "status", "mgmt_ip"]
cmd("missing = [key for key in required_keys if key not in structured]")
missing = [key for key in required_keys if key not in structured]
cmd("print(missing)")
out(missing)
blank()
if not missing:
    out("payload has the required keys")
else:
    warn("payload is missing required keys")
blank()
explain("Validation catches bad input before your automation sends bad output.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — Payload Transformation Patterns
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "Payload Transformation Patterns")

section("3.1 — Raw to structured transformation")
explain("Many systems export logs, CSV-style strings, or pipe-delimited records.")
explain("Your job is to normalize that raw input into dictionaries.")
blank()
raw_events = [
    "nyc-rtr-01|IOS-XE|up|GigabitEthernet1|10.0.0.1",
    "lon-sw-01|NX-OS|down|Ethernet1/1|10.1.0.1",
]
cmd("records = []")
cmd("for line in raw_events:")
cmd("    hostname, platform, status, interface, ip = line.split('|')")
cmd("    records.append({'hostname': hostname, 'platform': platform, 'status': status, 'interface': interface, 'mgmt_ip': ip})")
records = []
for line in raw_events:
    hostname, platform, status, interface, ip = line.split("|")
    records.append({"hostname": hostname, "platform": platform, "status": status, "interface": interface, "mgmt_ip": ip})
cmd("print(records[0])")
out(records[0])
pause()

section("3.2 — Building API-ready output")
explain("APIs usually expect specific keys, nesting, and JSON serialization.")
blank()
cmd("api_payload = {'devices': records, 'count': len(records)}")
api_payload = {"devices": records, "count": len(records)}
cmd("api_payload_json = json.dumps(api_payload, indent=2, sort_keys=True)")
api_payload_json = json.dumps(api_payload, indent=2, sort_keys=True)
cmd("print(api_payload_json)")
blank()
for line in api_payload_json.splitlines():
    out(line)
pause()

section("3.3 — Writing structured output to files")
explain("Payload workflows often read one format and write another.")
explain("For example: raw lines → Python objects → JSON file and YAML report.")
blank()
json_path = demo("devices.json")
yaml_path = demo("devices.yaml")
cmd("with open('devices.json', 'w') as f:")
cmd("    json.dump(records, f, indent=2, sort_keys=True)")
with open(json_path, "w") as f:
    json.dump(records, f, indent=2, sort_keys=True)
cmd("with open('devices.yaml', 'w') as f:")
cmd("    yaml.dump(records, f, default_flow_style=False, sort_keys=False)")
with open(yaml_path, "w") as f:
    yaml.dump(records, f, default_flow_style=False, sort_keys=False)
cmd("print(os.path.exists('devices.json'))")
out(os.path.exists(json_path))
cmd("print(os.path.exists('devices.yaml'))")
out(os.path.exists(yaml_path))
blank()
explain("The structured object is the bridge between file formats and APIs.")
pause()

shutil.rmtree(DEMO_DIR, ignore_errors=True)

bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — PAYLOAD HANDLING{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   Payload basics: JSON, YAML, structured I/O")
print(f"  {BOLD}Ch 2{RESET}   Nested data, large datasets, validation")
print(f"  {BOLD}Ch 3{RESET}   Raw → structured → API/file output")
blank()
print(f"  {WHITE}The goal is not just to read payloads — it is to turn messy")
print(f"  input into predictable Python data your automation can filter,")
print(f"  validate, transform, serialize, and send safely.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
