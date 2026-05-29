# JSON for Infrastructure as Code — 3-Chapter Deep Dive
# Cisco IaC Perspective
# Press ENTER to advance through each step

import json
import copy
from datetime import datetime

# ── ANSI colors ───────────────────────────────────────────────────────────────
RESET  = "\033[0m"
CYAN   = "\033[96m"    # >>> commands
GREEN  = "\033[92m"    # output values
YELLOW = "\033[93m"    # highlights
WHITE  = "\033[97m"    # explanations
RED    = "\033[91m"    # warnings / errors
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

def print_json(value):
    """Pretty-print Python data as JSON for readable IaC examples."""
    print(json.dumps(value, indent=2, sort_keys=True))

def show_json(value):
    """Pretty-print JSON with the same green output style as out()."""
    for line in json.dumps(value, indent=2, sort_keys=True).splitlines():
        out(line)

# ─────────────────────────────────────────────────────────────────────────────
bar = "█" * 62
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         JSON FOR INFRASTRUCTURE AS CODE{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco IaC Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")

pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — JSON Fundamentals for IaC
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "JSON Fundamentals for IaC")

section("1.1 — Why JSON matters in IaC")

explain("JSON is the language most APIs use to exchange structured data.")
explain("In infrastructure automation, you use JSON for:")
blank()
explain("  — REST API request payloads")
explain("  — RESTCONF/YANG responses")
explain("  — cloud resource definitions")
explain("  — device inventory files")
explain("  — compliance reports and config snapshots")
blank()
explain("Your IaC workflow is usually:")
blank()
explain("  1. Parse JSON from an API or file")
explain("  2. Read or transform the data")
explain("  3. Serialize clean JSON back to an API or file")
blank()

pause()

section("1.2 — JSON types map directly to Python types")

explain("JSON has six core data types.")
explain("Python's json module converts them automatically.")
blank()
explain("  JSON object  → Python dict")
explain("  JSON array   → Python list")
explain("  JSON string  → Python str")
explain("  JSON number  → Python int or float")
explain("  JSON true/false → Python True/False")
explain("  JSON null    → Python None")
blank()
explain("Scenario: You are building an IaC inventory record for one router.")
explain("Before saving it or sending it to an API, you need to understand")
explain("how Python values will appear when converted into JSON.")
blank()

payload = {
    "hostname": "nyc-rtr-01",
    "platform": "IOS-XE",
    "enabled": True,
    "mgmt_ip": "10.0.0.1",
    "vlans": [10, 20, 30],
    "last_backup": None,
}
cmd("payload = {'hostname': 'nyc-rtr-01', 'platform': 'IOS-XE', ...}")
cmd("print(json.dumps(payload, indent=2, sort_keys=True))")
blank()
show_json(payload)
blank()

pause()

section("1.3 — Parse API JSON with json.loads()")

explain("Scenario: Your automation script calls a device API and receives")
explain("a JSON response body as text. You need to parse that text before")
explain("you can read fields like hostname or interface name.")
blank()

api_response = '''{
  "hostname": "nyc-rtr-01",
  "platform": "IOS-XE",
  "status": "up",
  "interfaces": [
    {"name": "Gi0/0", "state": "up", "vlan": 10},
    {"name": "Gi0/1", "state": "down", "vlan": 20}
  ]
}'''

explain("API response bodies usually arrive as strings.")
explain("Use json.loads() to turn a JSON string into Python data.")
blank()
cmd("device = json.loads(api_response)")
device = json.loads(api_response)
cmd("print(json.dumps(device, indent=2, sort_keys=True))")
blank()
show_json(device)
blank()
cmd("print(device['hostname'])")
out(device["hostname"])
cmd("print(device['interfaces'][0]['name'])")
out(device["interfaces"][0]["name"])
blank()

pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Reading and Normalizing IaC JSON
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "Reading and Normalizing IaC JSON")

section("2.1 — Navigate nested device responses")

explain("Scenario: An NX-OS command returns interface data wrapped inside")
explain("TABLE_interface and ROW_interface. Your first job is to navigate")
explain("through the wrapper and reach the useful interface rows.")
blank()

nxos_json = json.dumps({
    "TABLE_interface": {
        "ROW_interface": [
            {"interface": "Ethernet1/1", "state": "up", "vlan": "10", "eth_ip_addr": "10.0.0.1"},
            {"interface": "Ethernet1/2", "state": "down", "vlan": "20", "eth_ip_addr": "10.0.1.1"},
            {"interface": "Ethernet1/3", "state": "up", "vlan": "30", "eth_ip_addr": "10.0.2.1"},
        ]
    }
})

explain("Vendor APIs often wrap useful data inside nested keys.")
explain("NX-OS commonly uses TABLE_* and ROW_* keys.")
blank()
cmd("data = json.loads(nxos_json)")
data = json.loads(nxos_json)
cmd("rows = data['TABLE_interface']['ROW_interface']")
rows = data["TABLE_interface"]["ROW_interface"]
cmd("print(json.dumps(rows, indent=2, sort_keys=True))")
blank()
show_json(rows)
blank()

pause()

section("2.2 — Normalize vendor data into your internal model")

explain("IaC code is easier when every vendor response becomes a standard shape.")
explain("Here, VLAN is converted from string to integer and fields are renamed.")
blank()
explain("Scenario: Different vendors use different field names. Your IaC")
explain("system should not care about vendor-specific names, so you convert")
explain("the response into a clean internal model.")
blank()
cmd("normalized = [")
cmd("    {'name': i['interface'], 'state': i['state'],")
cmd("     'vlan': int(i['vlan']), 'ip': i['eth_ip_addr']}")
cmd("    for i in rows")
cmd("]")
normalized = [
    {
        "name": i["interface"],
        "state": i["state"],
        "vlan": int(i["vlan"]),
        "ip": i["eth_ip_addr"],
    }
    for i in rows
]
cmd("print(json.dumps(normalized, indent=2, sort_keys=True))")
blank()
show_json(normalized)
blank()

pause()

section("2.3 — Filter parsed JSON for automation decisions")

explain("After parsing, JSON data is normal Python data.")
explain("Use normal list/dict logic to decide what IaC should change.")
blank()
explain("Scenario: Before making changes, your automation needs to know")
explain("which interfaces are currently usable. You filter the normalized")
explain("data so later tasks only act on interfaces that are up.")
blank()
cmd("up_interfaces = [i for i in normalized if i['state'] == 'up']")
up_interfaces = [i for i in normalized if i["state"] == "up"]
cmd("print(json.dumps(up_interfaces, indent=2, sort_keys=True))")
blank()
show_json(up_interfaces)
blank()
cmd("up_vlans = sorted({i['vlan'] for i in up_interfaces})")
up_vlans = sorted({i["vlan"] for i in up_interfaces})
cmd("print(json.dumps(up_vlans, indent=2))")
blank()
show_json(up_vlans)
blank()

pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — Writing JSON Payloads for IaC
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "Writing JSON Payloads for IaC")

section("3.1 — Build a desired-state payload")

explain("IaC usually means describing desired state, not typing commands manually.")
explain("Create Python data first, then serialize it to JSON for an API.")
blank()
explain("Scenario: Instead of logging into the router and typing commands,")
explain("you describe the intended configuration as structured data. That")
explain("desired state can then be sent to an API or stored in Git.")
blank()

desired_state = {
    "site": "NYC",
    "device": "nyc-rtr-01",
    "intended_config": {
        "ntp_servers": ["10.0.0.100", "10.0.0.101"],
        "dns_servers": ["8.8.8.8", "1.1.1.1"],
        "vlans": [10, 20, 30],
    },
}
cmd("desired_state = {'site': 'NYC', 'device': 'nyc-rtr-01', ...}")
cmd("payload_json = json.dumps(desired_state, indent=2, sort_keys=True)")
payload_json = json.dumps(desired_state, indent=2, sort_keys=True)
cmd("print(payload_json)")
blank()
for line in payload_json.splitlines():
    out(line)
blank()

pause()

section("3.2 — Compact JSON for API transport")

explain("Pretty JSON is best for humans and git diffs.")
explain("Compact JSON is useful when sending API payloads.")
blank()
explain("Scenario: The same desired-state data may be sent over HTTP.")
explain("For transport, you may not need spaces or indentation, so you")
explain("serialize the payload in compact form.")
blank()
cmd("compact_payload = json.dumps(desired_state, separators=(',', ':'))")
compact_payload = json.dumps(desired_state, separators=(",", ":"))
cmd("print(compact_payload)")
out(compact_payload)
blank()

pause()

section("3.3 — Serialize datetime safely")

explain("Some Python objects are not valid JSON by default.")
explain("For IaC reports, datetime must be converted to a string.")
blank()
explain("Scenario: A compliance report often includes the time when the")
explain("check was performed. Python datetime objects are useful in code,")
explain("but JSON needs them converted into text before serialization.")
blank()
cmd("def iac_default(obj):")
cmd("    if isinstance(obj, datetime):")
cmd("        return obj.isoformat()")
cmd("    raise TypeError(f'Cannot serialize {type(obj)}')")
blank()

def iac_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Cannot serialize {type(obj)}")

report = copy.deepcopy(desired_state)
report["checked_at"] = datetime(2024, 1, 15, 10, 30)
report["compliant"] = True
cmd("report['checked_at'] = datetime(2024, 1, 15, 10, 30)")
cmd("report_json = json.dumps(report, default=iac_default, indent=2, sort_keys=True)")
report_json = json.dumps(report, default=iac_default, indent=2, sort_keys=True)
cmd("print(report_json)")
blank()
for line in report_json.splitlines():
    out(line)
blank()

pause()

# ═════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — JSON FOR IAC{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   JSON fundamentals: types, loads(), and API strings")
print(f"  {BOLD}Ch 2{RESET}   Reading JSON: navigate, normalize, and filter data")
print(f"  {BOLD}Ch 3{RESET}   Writing JSON: desired state, compact payloads, datetime")
blank()
print(f"  {WHITE}Every printed JSON example used pretty formatting with")
print(f"  json.dumps(..., indent=2, sort_keys=True) wherever readability mattered.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
