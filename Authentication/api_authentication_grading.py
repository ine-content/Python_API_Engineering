# API Authentication — Grader
# Cisco API Perspective
#
# HOW IT WORKS:
# 1. Write your solution in api_authentication_solution.py
# 2. Run this script: python3 api_authentication_grading.py
# 3. Fix any hints and re-run until you get Good Job!

import os
import sys
import json
import base64
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

# DATA — do not edit this
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

def run_solution(work_dir):
    filename = "api_authentication_solution.py"
    solution_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    if not os.path.exists(solution_path):
        blank()
        fail(f"File '{filename}' not found.")
        blank()
        explain(f"Create '{filename}' in the same folder as this grader.")
        blank()
        sys.exit(1)

    namespace = {
        "json": json,
        "os": os,
        "base64": base64,
        "IOSXE_SANDBOX": IOSXE_SANDBOX,
        "CATALYST_CENTER_SANDBOX": CATALYST_CENTER_SANDBOX,
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
        ok = actual == expected
        if ok:
            passed += 1
        results.append((task_label, label, ok, actual, expected, hint_text, solution_ways, var_name))

    blank()
    bar = "█" * 62
    score_color = GREEN if passed == total else YELLOW
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
    else:
        print(f"{BOLD}{YELLOW}  You scored {passed}/{total}. Review, fix, and re-run.{RESET}")

    print()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    return passed

print()
bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         API AUTHENTICATION — GRADER{RESET}")
print(f"{BOLD}         Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("Grading your api_authentication_solution.py ...")
blank()

work_dir = tempfile.mkdtemp(prefix="api_auth_easy_grade_")
ns = run_solution(work_dir)

if ns:
    credential = f"{IOSXE_SANDBOX['username']}:{IOSXE_SANDBOX['password']}"
    encoded = base64.b64encode(credential.encode()).decode()
    exp_iosxe_basic_auth_header = "Basic " + encoded
    exp_iosxe_request = {
        "method": "GET",
        "url": IOSXE_SANDBOX["url"],
        "headers": {
            "Accept": IOSXE_SANDBOX["accept"],
            "Authorization": exp_iosxe_basic_auth_header,
        },
    }

    exp_catalyst_token_header = CATALYST_CENTER_SANDBOX["token"]
    exp_catalyst_request = {
        "method": "GET",
        "url": CATALYST_CENTER_SANDBOX["devices_url"],
        "headers": {
            "Accept": CATALYST_CENTER_SANDBOX["accept"],
            "X-Auth-Token": exp_catalyst_token_header,
        },
    }

    ways = {
        "basic": [("build Basic Auth header and request", [
            "credential = f\"{IOSXE_SANDBOX['username']}:{IOSXE_SANDBOX['password']}\"",
            "encoded = base64.b64encode(credential.encode()).decode()",
            "iosxe_basic_auth_header = 'Basic ' + encoded",
            "iosxe_request = {'method': 'GET', 'url': IOSXE_SANDBOX['url'], 'headers': {'Accept': IOSXE_SANDBOX['accept'], 'Authorization': iosxe_basic_auth_header}}",
        ])],
        "token": [("build X-Auth-Token header and request", [
            "catalyst_token_header = CATALYST_CENTER_SANDBOX['token']",
            "catalyst_request = {'method': 'GET', 'url': CATALYST_CENTER_SANDBOX['devices_url'], 'headers': {'Accept': CATALYST_CENTER_SANDBOX['accept'], 'X-Auth-Token': catalyst_token_header}}",
        ])],
    }

    grade([
        ("Task 1", "iosxe_basic_auth_header and iosxe_request — Basic Auth", (ns.get("iosxe_basic_auth_header"), ns.get("iosxe_request")), (exp_iosxe_basic_auth_header, exp_iosxe_request), "Build username:password, Base64 encode it, prefix with Basic, and build the GET request dictionary.", ways["basic"], "(iosxe_basic_auth_header, iosxe_request)"),
        ("Task 2", "catalyst_token_header and catalyst_request — X-Auth-Token", (ns.get("catalyst_token_header"), ns.get("catalyst_request")), (exp_catalyst_token_header, exp_catalyst_request), "Use the provided token as X-Auth-Token and build the GET request dictionary.", ways["token"], "(catalyst_token_header, catalyst_request)"),
    ])

shutil.rmtree(work_dir, ignore_errors=True)
pause()
