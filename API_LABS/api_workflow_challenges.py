# End-to-End API Workflow — Student Challenges
# Cisco CAT8k / Nexus 9k Lab Perspective
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: api_workflow_solution.py
# 3. Run: python3 api_workflow_grading.py
#
# LIVE LAB NOTE:
# These tasks are designed to work against real lab devices when environment
# variables are set. The grader validates structure and logic without requiring
# live device access.

import os
import json

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
    explain("Available in api_workflow_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# DATA — same data shapes used by solution and grader
# -----------------------------------------------------------------------------

CAT8K_CONFIG = {
    "host": os.getenv("CAT8K_HOST", "cat8k-lab.example.com"),
    "username": os.getenv("CAT8K_USERNAME", "admin"),
    "password": os.getenv("CAT8K_PASSWORD", "password"),
    "verify_ssl": os.getenv("CAT8K_VERIFY_SSL", "false").lower() == "true",
    "timeout": int(os.getenv("CAT8K_TIMEOUT", "10")),
    "max_attempts": int(os.getenv("CAT8K_MAX_ATTEMPTS", "3")),
    "base_delay": int(os.getenv("CAT8K_BASE_DELAY", "1")),
    "interfaces_path": "/restconf/data/ietf-interfaces:interfaces",
}

NEXUS9K_CONFIG = {
    "host": os.getenv("NEXUS9K_HOST", "n9k-lab.example.com"),
    "username": os.getenv("NEXUS9K_USERNAME", "admin"),
    "password": os.getenv("NEXUS9K_PASSWORD", "password"),
    "verify_ssl": os.getenv("NEXUS9K_VERIFY_SSL", "false").lower() == "true",
    "timeout": int(os.getenv("NEXUS9K_TIMEOUT", "10")),
    "max_attempts": int(os.getenv("NEXUS9K_MAX_ATTEMPTS", "3")),
    "base_delay": int(os.getenv("NEXUS9K_BASE_DELAY", "1")),
    "nxapi_path": "/ins",
}

RETRYABLE_STATUS_CODES = [408, 429, 500, 502, 503, 504]
REQUIRED_REQUEST_KEYS = ["method", "url", "headers", "timeout", "max_attempts"]

CAT8K_SAMPLE_RESPONSE = {
    "ietf-interfaces:interfaces": {
        "interface": [
            {"name": "GigabitEthernet1", "enabled": True, "type": "iana-if-type:ethernetCsmacd"},
            {"name": "Loopback0", "enabled": True, "type": "iana-if-type:softwareLoopback"},
        ]
    }
}

NEXUS9K_SAMPLE_RESPONSE = {
    "ins_api": {
        "outputs": {
            "output": {
                "code": "200",
                "msg": "Success",
                "body": {
                    "TABLE_interface": {
                        "ROW_interface": [
                            {"interface": "Ethernet1/1", "state": "up"},
                            {"interface": "Ethernet1/2", "state": "down"},
                        ]
                    }
                },
            }
        }
    }
}

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         END-TO-END API WORKFLOW — CHALLENGES{RESET}")
print(f"{BOLD}         Cisco CAT8k / Nexus 9k Lab Practice{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("2 end-to-end scenario tasks.")
explain("Students will build reusable request workflows with authentication,")
explain("validation, timeout/retry handling, response parsing, and logging.")
blank()
explain("Write answers in: api_workflow_solution.py")
explain("Then run: python3 api_workflow_grading.py")
blank()
explain("For live testing, set these environment variables before running:")
header("export CAT8K_HOST='your-cat8k-host-or-ip'")
header("export CAT8K_USERNAME='your-username'")
header("export CAT8K_PASSWORD='your-password'")
header("export NEXUS9K_HOST='your-n9k-host-or-ip'")
header("export NEXUS9K_USERNAME='your-username'")
header("export NEXUS9K_PASSWORD='your-password'")
blank()
explain("The grader does not require live device access, but the final functions")
explain("should be capable of making real requests when the lab is reachable.")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Build a script that authenticates, retrieves data, handles timeouts/retries, and logs results", "Medium")
explain("Scenario: You need to retrieve interface data from a Cisco CAT8k using")
explain("RESTCONF. The script must authenticate with Basic Auth, use a timeout,")
explain("retry temporary failures, parse the JSON response, and write a run log.")
blank()
available("CAT8K_CONFIG", "RETRYABLE_STATUS_CODES", "CAT8K_SAMPLE_RESPONSE")
explain("Your task: Create the following:")
explain("  • cat8k_request")
explain("  • cat8k_backoff_delays")
explain("  • parse_cat8k_interfaces(response_json)")
explain("  • run_cat8k_workflow(live=False)")
blank()
explain("Requirements:")
explain("  • cat8k_request must include method, url, auth, headers, timeout, max_attempts.")
explain("  • method must be GET.")
explain("  • url must be https://<CAT8K_HOST><interfaces_path>.")
explain("  • headers must include Accept: application/yang-data+json.")
explain("  • auth must be a tuple: (username, password).")
explain("  • cat8k_backoff_delays must use exponential backoff.")
explain("  • parse_cat8k_interfaces must return a list of interface names.")
explain("  • run_cat8k_workflow(live=False) must use CAT8K_SAMPLE_RESPONSE.")
explain("  • run_cat8k_workflow(live=True) should make the real RESTCONF request.")
explain("  • The workflow must return a dict with device, success, interfaces, attempts, and log.")
blank()
hint("Use requests.get() only inside run_cat8k_workflow when live=True.")
blank()
output_intro()
header(">>> print(cat8k_request['method'])")
header("GET")
header(">>> print(parse_cat8k_interfaces(CAT8K_SAMPLE_RESPONSE))")
header("['GigabitEthernet1', 'Loopback0']")
header(">>> result = run_cat8k_workflow(live=False)")
header(">>> print(result['success'], result['interfaces'])")
header("True ['GigabitEthernet1', 'Loopback0']")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Design a reusable API workflow with validation, retry logic, and safe request handling", "Hard")
explain("Scenario: You need a reusable workflow for a Cisco Nexus 9k NX-API call.")
explain("Before sending the request, the script must validate the request shape.")
explain("It must retry temporary failures, avoid leaking passwords in logs,")
explain("and parse the NX-API response into useful interface data.")
blank()
available("NEXUS9K_CONFIG", "REQUIRED_REQUEST_KEYS", "RETRYABLE_STATUS_CODES", "NEXUS9K_SAMPLE_RESPONSE")
explain("Your task: Create the following:")
explain("  • nexus_command_payload")
explain("  • nexus_request")
explain("  • validate_request(request)")
explain("  • sanitize_log_entry(entry)")
explain("  • parse_nexus_interfaces(response_json)")
explain("  • run_reusable_nexus_workflow(live=False)")
blank()
explain("Requirements:")
explain("  • nexus_command_payload must send the command show interface brief.")
explain("  • nexus_request must include method, url, auth, headers, body, timeout, max_attempts.")
explain("  • method must be POST.")
explain("  • url must be https://<NEXUS9K_HOST>/ins.")
explain("  • headers must include Content-Type: application/json.")
explain("  • validate_request must return {'valid': bool, 'missing_keys': list}.")
explain("  • sanitize_log_entry must remove or mask auth/password data.")
explain("  • parse_nexus_interfaces must return interface names from NX-API JSON.")
explain("  • run_reusable_nexus_workflow(live=False) must use NEXUS9K_SAMPLE_RESPONSE.")
explain("  • run_reusable_nexus_workflow(live=True) should make the real NX-API request.")
explain("  • The workflow must return a dict with device, validation, success, interfaces, attempts, and log.")
blank()
hint("Use requests.post() only inside run_reusable_nexus_workflow when live=True.")
blank()
output_intro()
header(">>> print(validate_request(nexus_request)['valid'])")
header("True")
header(">>> print(parse_nexus_interfaces(NEXUS9K_SAMPLE_RESPONSE))")
header("['Ethernet1/1', 'Ethernet1/2']")
header(">>> result = run_reusable_nexus_workflow(live=False)")
header(">>> print(result['success'], result['interfaces'])")
header("True ['Ethernet1/1', 'Ethernet1/2']")
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
print(f"{BOLD}{CYAN}    api_workflow_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 api_workflow_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
