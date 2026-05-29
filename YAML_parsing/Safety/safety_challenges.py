# Safety — Student Challenges
# Cisco API Perspective
# Scenario-based tasks mapped directly to safety_deep_dive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: safety_solution.py
# 3. Run: python3 safety_grading.py

import json
import os

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
    explain("Available in safety_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# DATA — same data shapes used in the deep dive examples
# -----------------------------------------------------------------------------

CHANGE_REQUEST = {
    "hostname": "nyc-rtr-01",
    "interface": "GigabitEthernet1",
    "description": "WAN uplink",
}

REQUIRED_FIELDS = ["hostname", "interface", "description"]
ALLOWED_INTERFACES = ["GigabitEthernet1", "GigabitEthernet2", "Loopback0"]

ERROR_RESPONSE = {
    "status_code": 400,
    "body": {
        "error": "invalid interface",
        "detail": "Interface GigabitEthernet99 does not exist",
    },
}

REQUEST_CONTEXT = {
    "method": "PATCH",
    "url": "https://controller.example.local/api/v1/interfaces/GigabitEthernet99",
    "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer secret-token-value",
    },
}

RECOVERY_MAP = {
    400: "stop_and_fix_payload",
    401: "stop_and_refresh_credentials",
    403: "stop_and_check_permissions",
    404: "skip_missing_resource",
    409: "stop_and_review_conflict",
    500: "retry_or_escalate",
    503: "retry_with_backoff",
}

CHANGE_PLAN = {
    "device": "nyc-rtr-01",
    "interface": "GigabitEthernet1",
    "new_description": "WAN uplink",
    "previous_description": "old description",
}

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         SAFETY — CHALLENGES{RESET}")
print(f"{BOLD}         Cisco API Scenario Practice{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("5 scenario-based tasks mapped directly to the DeepDive examples.")
explain("You will validate input before requests, build safe error summaries,")
explain("and create recovery and rollback data.")
blank()
explain("Write answers in: safety_solution.py")
explain("Then run: python3 safety_grading.py")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Validate required fields before a request", "Easy")
explain("Scenario: Your script is about to update an interface description.")
explain("Before sending the API request, verify that the payload includes all")
explain("required fields.")
blank()
available("CHANGE_REQUEST", "REQUIRED_FIELDS")
explain("Your task: Create missing_fields and has_required_fields.")
explain("missing_fields must list any required fields missing from CHANGE_REQUEST.")
explain("has_required_fields must be True when no fields are missing.")
blank()
hint("Refer DeepDive Chapter 1.2 — Required field validation.")
blank()
output_intro()
header(">>> print(missing_fields)")
header("[]")
header(">>> print(has_required_fields)")
header("True")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Validate allowed values before a request", "Easy")
explain("Scenario: The request has an interface name, but your automation should")
explain("only allow changes to approved interfaces.")
blank()
available("CHANGE_REQUEST", "ALLOWED_INTERFACES")
explain("Your task: Create interface_is_allowed and validation_report.")
explain("interface_is_allowed must check whether CHANGE_REQUEST['interface']")
explain("exists in ALLOWED_INTERFACES.")
explain("validation_report must include valid, missing_fields, and interface_is_allowed.")
blank()
hint("Refer DeepDive Chapter 1.3 and 1.4 — Value validation and validation report.")
blank()
output_intro()
header(">>> print(interface_is_allowed)")
header("True")
header(">>> print(validation_report['valid'])")
header("True")
blank()

pause()

# ── Task 3 ────────────────────────────────────────────────────────────────────
task_section(3, "Build a safe error summary", "Medium")
explain("Scenario: An API request failed. You need to report the error without")
explain("leaking sensitive headers such as Authorization.")
blank()
available("ERROR_RESPONSE", "REQUEST_CONTEXT")
explain("Your task: Create safe_error_summary.")
explain("It must include method, url, status_code, error, and detail.")
explain("Do not include REQUEST_CONTEXT['headers'] in the summary.")
blank()
hint("Refer DeepDive Chapter 2.2 and 2.3 — Safe error summary.")
blank()
output_intro()
header(">>> print(safe_error_summary['status_code'])")
header("400")
header(">>> print('headers' in safe_error_summary)")
header("False")
blank()

pause()

# ── Task 4 ────────────────────────────────────────────────────────────────────
task_section(4, "Choose a recovery action and rollback plan", "Medium")
explain("Scenario: After a failed request, your script should decide what to do")
explain("next and prepare rollback data in case the change must be undone.")
blank()
available("ERROR_RESPONSE", "RECOVERY_MAP", "CHANGE_PLAN")
explain("Your task: Create recovery_action and rollback_plan.")
explain("recovery_action must use ERROR_RESPONSE['status_code'] to look up RECOVERY_MAP.")
explain("rollback_plan must restore the previous description from CHANGE_PLAN.")
blank()
hint("Refer DeepDive Chapter 3.2 and 3.3 — Recovery actions and rollback planning.")
blank()
output_intro()
header(">>> print(recovery_action)")
header("stop_and_fix_payload")
header(">>> print(rollback_plan['restore_description'])")
header("old description")
blank()

pause()

# ── Task 5 ────────────────────────────────────────────────────────────────────
task_section(5, "Build a safety summary JSON string", "Medium")
explain("Scenario: At the end of the safety check, your automation should")
explain("produce a JSON summary of validation, error handling, and recovery.")
blank()
available("validation_report  (created in Task 2)", "safe_error_summary  (created in Task 3)", "recovery_action  (created in Task 4)", "rollback_plan  (created in Task 4)")
explain("Your task: Create safety_summary and safety_summary_json.")
explain("safety_summary must include validation_passed, status_code, recovery_action,")
explain("and rollback_available.")
explain("safety_summary_json must use json.dumps(..., indent=2, sort_keys=True).")
blank()
hint("Refer DeepDive Chapter 3.4 — Safety summary.")
blank()
output_intro()
header(">>> print(safety_summary['validation_passed'])")
header("True")
header(">>> print(safety_summary['rollback_available'])")
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
print(f"{BOLD}{CYAN}    safety_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 safety_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
