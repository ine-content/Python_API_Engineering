# YAML for Infrastructure as Code — 3-Chapter Deep Dive
# Cisco IaC Perspective
# Press ENTER to advance through each step

import yaml
import json
import os
import shutil
import tempfile

# ── ANSI colors ───────────────────────────────────────────────────────────────
RESET  = "\033[0m"
CYAN   = "\033[96m"    # >>> commands / YAML snippets
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


def yaml_block(text):
    """Print a YAML snippet in cyan with no >>> prefix."""
    for line in text.splitlines():
        print(f"    {CYAN}{line}{RESET}")


def show_yaml(value):
    """Pretty-print Python data as YAML using readable block style."""
    text = yaml.dump(value, default_flow_style=False, sort_keys=False)
    for line in text.splitlines():
        out(line)


def show_json(value):
    """Pretty-print Python data as JSON for YAML↔JSON conversion demos."""
    text = json.dumps(value, indent=2, sort_keys=True)
    for line in text.splitlines():
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


# ── Working directory for demo files ─────────────────────────────────────────
DEMO_DIR = tempfile.mkdtemp(prefix="yaml_3ch_demo_")


def demo(filename):
    return os.path.join(DEMO_DIR, filename)


# ─────────────────────────────────────────────────────────────────────────────
bar = "█" * 62
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         YAML FOR INFRASTRUCTURE AS CODE{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco IaC Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")

pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — YAML Format Fundamentals
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "YAML Format Fundamentals")

section("1.1 — What YAML is and why IaC uses it")

explain("YAML means YAML Ain't Markup Language.")
explain("It is a human-readable data format used heavily for config files.")
blank()
explain("In Cisco IaC, YAML commonly appears in:")
blank()
explain("  — Ansible playbooks, inventory, host_vars, and group_vars")
explain("  — Nornir hosts.yaml, groups.yaml, and defaults.yaml")
explain("  — intent files for sites, VLANs, routing, and services")
explain("  — config snapshots, templates, and deployment inputs")
blank()
explain("Rule of thumb:")
explain("  Humans write YAML. APIs usually send and receive JSON.")
blank()
explain("Scenario: A network engineer wants to define router intent in a")
explain("file that is easy to read, edit, review, and store in Git.")
blank()
yaml_block("""hostname: nyc-rtr-01
platform: IOS-XE
status: up
mgmt_ip: 10.0.0.1""")
blank()
explain("This is valid YAML: key-value pairs, no braces, no commas.")

pause()

section("1.2 — Mappings, sequences, scalars, and indentation")

explain("YAML has three basic building blocks you must recognize:")
blank()
explain("  Scalar   — one value, like a string, number, boolean, or null")
explain("  Mapping  — key-value pairs, like a Python dict")
explain("  Sequence — a list of items, like a Python list")
blank()
explain("Scenario: You are defining one device with nested config and VLANs.")
explain("Indentation tells YAML which values belong together.")
blank()

yaml_str = """\
hostname: nyc-rtr-01
platform: IOS-XE
enabled: true
last_backup: null
vlans:
  - 10
  - 20
  - 30
config:
  ntp: 10.0.0.100
  dns: 8.8.8.8
"""
cmd('yaml_str = """')
yaml_block(yaml_str.rstrip())
cmd('"""')
blank()
cmd("device = yaml.safe_load(yaml_str)")
device = yaml.safe_load(yaml_str)
cmd("print(device)")
out(device)
blank()
cmd("print(type(device))")
out(type(device))
cmd("print(type(device['vlans']))")
out(type(device["vlans"]))
cmd("print(device['config']['ntp'])")
out(device["config"]["ntp"])
blank()
explain("YAML indentation becomes nested Python dictionaries and lists.")

pause()

section("1.3 — YAML vs JSON: same data, different audience")

explain("YAML and JSON can represent the same structured data.")
explain("YAML is usually better for humans. JSON is usually better for APIs.")
blank()
explain("Scenario: The same device data may live in Git as YAML, but later")
explain("be converted into JSON before being sent to an API.")
blank()

same_data = {
    "hostname": "nyc-rtr-01",
    "platform": "IOS-XE",
    "vlans": [10, 20, 30],
}
explain("YAML form:")
blank()
show_yaml(same_data)
blank()
explain("JSON form:")
blank()
show_json(same_data)
blank()
explain("The structure is the same. Only the syntax is different.")

pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Reading and Writing YAML with PyYAML
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "Reading and Writing YAML with PyYAML")

section("2.1 — Parse YAML strings with yaml.safe_load()")

explain("yaml.safe_load() parses a YAML string into Python data.")
explain("Use safe_load(), not yaml.load(), when reading IaC input.")
blank()
explain("Scenario: Your automation script receives a YAML intent string")
explain("for a device and needs to inspect the hostname, platform, and VLANs.")
blank()

intent_yaml = """\
hostname: nyc-rtr-01
platform: IOS-XE
status: up
vlans: [10, 20, 30]
config:
  ntp: 10.0.0.100
  dns: 8.8.8.8
"""
cmd('intent_yaml = """')
yaml_block(intent_yaml.rstrip())
cmd('"""')
blank()
cmd("intent = yaml.safe_load(intent_yaml)")
intent = yaml.safe_load(intent_yaml)
cmd("print(intent['hostname'])")
out(intent["hostname"])
cmd("print(intent['vlans'])")
out(intent["vlans"])
cmd("print(intent['config']['dns'])")
out(intent["config"]["dns"])
blank()

pause()

section("2.2 — Load YAML from files and filter inventory")

explain("Most IaC YAML lives in files, not Python strings.")
explain("Use open() with yaml.safe_load() to read those files.")
blank()
explain("Scenario: A file called inventory.yaml contains multiple devices.")
explain("Automation needs to load the file and find devices that are up.")
blank()

inventory_yaml = """\
devices:
  - hostname: nyc-rtr-01
    platform: IOS-XE
    status: up
    ip: 10.0.0.1
    vlans: [10, 20, 30]
  - hostname: lon-sw-01
    platform: NX-OS
    status: down
    ip: 10.1.0.1
    vlans: [10, 20]
  - hostname: sin-fw-01
    platform: ASA
    status: up
    ip: 10.2.0.1
    vlans: [30, 40, 50]
"""
cmd('inventory_yaml = """')
yaml_block(inventory_yaml.rstrip())
cmd('"""')
blank()

inv_path = demo("inventory.yaml")
with open(inv_path, "w") as f:
    f.write(inventory_yaml)

cmd("with open('inventory.yaml') as f:")
cmd("    inventory = yaml.safe_load(f)")
with open(inv_path) as f:
    inventory = yaml.safe_load(f)
blank()
cmd("up_hostnames = [d['hostname'] for d in inventory['devices'] if d['status'] == 'up']")
up_hostnames = [d["hostname"] for d in inventory["devices"] if d["status"] == "up"]
cmd("print(up_hostnames)")
out(up_hostnames)
blank()

pause()

section("2.3 — Write Python data back to YAML with yaml.dump()")

explain("yaml.dump() serializes Python data back into YAML.")
explain("Use default_flow_style=False for readable block-style YAML.")
explain("Use sort_keys=False when you want key order to stay natural.")
blank()
explain("Scenario: Automation enriches device data with a VLAN count and")
explain("writes a new YAML report that humans can review.")
blank()

cmd("inventory['devices'] =")
show_yaml(inventory["devices"])
blank()

report = []
for d in inventory["devices"]:
    item = dict(d)
    item["vlan_count"] = len(d["vlans"])
    report.append(item)

cmd("for d in inventory['devices']:")
cmd("    item = dict(d)")
cmd("    item['vlan_count'] = len(d['vlans'])")
cmd("    report.append(item)")
blank()
cmd("report_yaml = yaml.dump(report, default_flow_style=False, sort_keys=False)")
report_yaml = yaml.dump(report, default_flow_style=False, sort_keys=False)
cmd("print(report_yaml)")
blank()
for line in report_yaml.splitlines():
    out(line)
blank()

pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — YAML Patterns in IaC
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "YAML Patterns in IaC")

section("3.1 — Ansible-style host_vars")

explain("Ansible often stores per-device variables in host_vars/.")
explain("One YAML file usually represents one device.")
blank()
explain("Scenario: Your inventory has device IPs, platforms, NTP, and VLANs.")
explain("You need to generate host_vars files that Ansible can consume.")
blank()

inventory_devices = [
    {
        "hostname": "nyc-rtr-01",
        "platform": "IOS-XE",
        "ip": "10.0.0.1",
        "config": {"ntp": "10.0.0.100"},
        "vlans": [10, 20, 30],
    },
    {
        "hostname": "lon-sw-01",
        "platform": "NX-OS",
        "ip": "10.1.0.1",
        "config": {"ntp": "10.1.0.100"},
        "vlans": [10, 20],
    },
]
platform_map = {"IOS-XE": "ios", "NX-OS": "nxos", "ASA": "asa"}
host_vars_dir = demo("host_vars")
os.makedirs(host_vars_dir, exist_ok=True)

cmd("platform_map = {'IOS-XE': 'ios', 'NX-OS': 'nxos', 'ASA': 'asa'}")
cmd("os.makedirs('host_vars', exist_ok=True)")
cmd("for d in inventory_devices:")
cmd("    host_vars = {")
cmd("        'ansible_host': d['ip'],")
cmd("        'ansible_network_os': platform_map[d['platform']],")
cmd("        'ntp': d['config']['ntp'],")
cmd("        'vlans': d['vlans'],")
cmd("    }")
cmd("    with open(f\"host_vars/{d['hostname']}.yaml\", 'w') as f:")
cmd("        yaml.dump(host_vars, f, default_flow_style=False, sort_keys=False)")
blank()

for d in inventory_devices:
    host_vars = {
        "ansible_host": d["ip"],
        "ansible_network_os": platform_map[d["platform"]],
        "ntp": d["config"]["ntp"],
        "vlans": d["vlans"],
    }
    with open(os.path.join(host_vars_dir, f"{d['hostname']}.yaml"), "w") as f:
        yaml.dump(host_vars, f, default_flow_style=False, sort_keys=False)

cmd("print(sorted(os.listdir('host_vars')))")
host_var_files = sorted(os.listdir(host_vars_dir))
out(host_var_files)
blank()
cmd("with open('host_vars/nyc-rtr-01.yaml') as f:")
cmd("    print(f.read())")
blank()
with open(os.path.join(host_vars_dir, "nyc-rtr-01.yaml")) as f:
    for line in f.read().splitlines():
        out(line)
blank()

pause()

section("3.2 — Multi-document YAML with yaml.safe_load_all()")

explain("A single YAML file can contain multiple documents separated by ---. ")
explain("This pattern is common in Kubernetes, Ansible, and deployment batches.")
blank()
explain("Scenario: A deployment batch contains one YAML document per device.")
explain("Automation needs to load all documents and summarize platforms.")
blank()

multi_doc_yaml = """\
---
hostname: nyc-rtr-01
platform: IOS-XE
status: up
vlans: [10, 20, 30]
---
hostname: lon-sw-01
platform: NX-OS
status: down
vlans: [10, 20]
---
hostname: sin-fw-01
platform: ASA
status: up
vlans: [30, 40, 50]
"""
cmd('multi_doc_yaml = """')
yaml_block(multi_doc_yaml.rstrip())
cmd('"""')
blank()
cmd("devices = list(yaml.safe_load_all(multi_doc_yaml))")
devices = list(yaml.safe_load_all(multi_doc_yaml))
cmd("print(len(devices))")
out(len(devices))
blank()
cmd("platform_counts = {}")
cmd("for d in devices:")
cmd("    platform_counts[d['platform']] = platform_counts.get(d['platform'], 0) + 1")
platform_counts = {}
for d in devices:
    platform_counts[d["platform"]] = platform_counts.get(d["platform"], 0) + 1
cmd("print(platform_counts)")
out(platform_counts)
blank()

pause()

section("3.3 — Convert YAML to JSON for API workflows")

explain("IaC often uses YAML for human-authored intent and JSON for APIs.")
explain("The bridge is: YAML → Python object → JSON string.")
blank()
explain("Scenario: A YAML intent file defines desired state. Before sending")
explain("it to a REST API, automation converts it into pretty JSON.")
blank()

desired_yaml = """\
site: NYC
device: nyc-rtr-01
intended_config:
  ntp_servers:
    - 10.0.0.100
    - 10.0.0.101
  dns_servers:
    - 8.8.8.8
    - 1.1.1.1
  vlans:
    - 10
    - 20
    - 30
"""
cmd('desired_yaml = """')
yaml_block(desired_yaml.rstrip())
cmd('"""')
blank()
cmd("desired_state = yaml.safe_load(desired_yaml)")
desired_state = yaml.safe_load(desired_yaml)
cmd("api_payload = json.dumps(desired_state, indent=2, sort_keys=True)")
api_payload = json.dumps(desired_state, indent=2, sort_keys=True)
cmd("print(api_payload)")
blank()
for line in api_payload.splitlines():
    out(line)
blank()

pause()

section("3.4 — Common YAML pitfalls")

explain("YAML is readable, but it has sharp edges.")
blank()
explain("Pitfall 1: Tabs are illegal for indentation.")
explain("Pitfall 2: Indentation controls nesting, so spacing matters.")
explain("Pitfall 3: yes/no/on/off can become booleans in YAML 1.1 parsers.")
blank()
explain("Scenario: A field that looks like a string may be parsed as a boolean.")
blank()

bad_yaml = "country: NO\nenabled: yes\nport_state: on"
cmd("bad_yaml = \"country: NO\\\\nenabled: yes\\\\nport_state: on\"")
yaml_block(bad_yaml)
blank()
cmd("parsed = yaml.safe_load('country: NO\\nenabled: yes\\nport_state: on')")
parsed_bad = yaml.safe_load(bad_yaml)
cmd("print(parsed)")
warn(parsed_bad)
blank()
explain("Fix: quote values that must stay strings.")
blank()
fixed_yaml = "country: 'NO'\nenabled: 'yes'\nport_state: 'on'"
cmd("fixed_yaml = \"country: 'NO'\\\\nenabled: 'yes'\\\\nport_state: 'on'\"")
yaml_block(fixed_yaml)
blank()
cmd("parsed = yaml.safe_load(\"country: 'NO'\\nenabled: 'yes'\\nport_state: 'on'\")")
parsed_fixed = yaml.safe_load(fixed_yaml)
cmd("print(parsed)")
out(parsed_fixed)
blank()

pause()

# ── Clean up demo files ───────────────────────────────────────────────────────
shutil.rmtree(DEMO_DIR, ignore_errors=True)

# ═════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — YAML FOR IAC{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   YAML format: scalars, mappings, sequences, indentation")
print(f"  {BOLD}Ch 2{RESET}   PyYAML: safe_load, file loading, dump output")
print(f"  {BOLD}Ch 3{RESET}   IaC patterns: host_vars, multi-doc YAML, YAML→JSON")
blank()
print(f"  {WHITE}The goal is not just to parse YAML — it is to understand")
print(f"  how human-readable YAML becomes Python data your automation")
print(f"  can validate, transform, write back, or convert into JSON.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
