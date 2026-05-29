# API Authentication — Student Challenges
# Cisco API Perspective
# Scenario-based tasks mapped directly to api_authentication_deep_dive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: api_authentication_solution.py
# 3. Run: python3 api_authentication_grading.py

import base64
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
    explain("Available in api_authentication_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# DATA — same data shapes used in the deep dive examples
# -----------------------------------------------------------------------------

IOSXE_SANDBOX = {
    "url": "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/ietf-interfaces:interfaces",
    "username": "devnetuser",
    "password": "Cisco123!",
    "accept": "application/yang-data+json",
}

CATALYST_CENTER_SANDBOX = {
    "devices_url": "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device",
    "token": "abc123sandbox-token",
    "accept": "application/json",
}

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         API AUTHENTICATION — CHALLENGES{RESET}")
print(f"{BOLD}         Cisco Sandbox Scenario Practice{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("2 easier scenario-based tasks mapped directly to the DeepDive examples.")
explain("Each task focuses on building authentication headers and request dictionaries.")
blank()
explain("Write answers in: api_authentication_solution.py")
explain("Then run: python3 api_authentication_grading.py")
blank()
explain("These tasks prepare students for Cisco Sandbox testing, but the grader")
explain("does not require live internet access.")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Build a Basic Auth header for IOS XE Sandbox", "Easy")
explain("Scenario: You are preparing to call the Cisco IOS XE RESTCONF Sandbox.")
explain("The sandbox uses Basic authentication, so your code needs to build the")
explain("Authorization header before a GET request can be sent.")
blank()
available("IOSXE_SANDBOX")
explain("Your task: Create iosxe_basic_auth_header and iosxe_request.")
blank()
explain("Requirements:")
explain("  • Combine username and password as username:password.")
explain("  • Base64 encode that credential.")
explain("  • Prefix the encoded value with 'Basic '.")
explain("  • Build iosxe_request with method, url, and headers.")
explain("  • Headers must include Accept and Authorization.")
blank()
hint("Refer DeepDive Chapter 2.2 and 2.3 — Build a Basic Auth header step by step.")
blank()
output_intro()
header(">>> print(iosxe_basic_auth_header)")
header("Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE=")
header(">>> print(iosxe_request['method'])")
header("GET")
header(">>> print(iosxe_request['headers']['Authorization'])")
header("Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE=")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Build a token header for Catalyst Center Sandbox", "Easy")
explain("Scenario: You are preparing to call a Cisco Catalyst Center Sandbox API.")
explain("The API call will use a token. In this simplified lab, the token is")
explain("already provided so you can focus on building the correct header.")
blank()
available("CATALYST_CENTER_SANDBOX")
explain("Your task: Create catalyst_token_header and catalyst_request.")
blank()
explain("Requirements:")
explain("  • catalyst_token_header must be the token from CATALYST_CENTER_SANDBOX.")
explain("  • Build catalyst_request with method, url, and headers.")
explain("  • Headers must include Accept and X-Auth-Token.")
blank()
hint("Refer DeepDive Chapter 2.6 — Cisco Catalyst Center X-Auth-Token style.")
blank()
output_intro()
header(">>> print(catalyst_token_header)")
header("abc123sandbox-token")
header(">>> print(catalyst_request['method'])")
header("GET")
header(">>> print(catalyst_request['headers']['X-Auth-Token'])")
header("abc123sandbox-token")
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
print(f"{BOLD}{CYAN}    api_authentication_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 api_authentication_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
