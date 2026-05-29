# Reliability & Resilience — Grader
# Cisco API Perspective
#
# HOW IT WORKS:
# 1. Write your solution in reliability_resilience_solution.py
# 2. Run this script: python3 reliability_resilience_grading.py
# 3. Fix any hints and re-run until you get Good Job!

import os
import sys
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

API_REQUEST = {
    "method": "GET",
    "url": "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device",
    "headers": {
        "Accept": "application/json",
        "X-Auth-Token": "abc123sandbox-token",
    },
}

RETRY_POLICY = {
    "max_attempts": 4,
    "base_delay": 1,
    "retryable_status_codes": [408, 429, 500, 502, 503, 504],
}

SIMULATED_RESPONSES = [
    {"attempt": 1, "status_code": 503},
    {"attempt": 2, "status_code": 503},
    {"attempt": 3, "status_code": 200},
]

CREATE_JOB_REQUEST = {
    "method": "POST",
    "url": "https://controller.example.local/api/v1/jobs",
    "body": {
        "device": "nyc-rtr-01",
        "operation": "backup",
    },
}

def run_solution(work_dir):
    filename = "reliability_resilience_solution.py"
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
        "API_REQUEST": API_REQUEST,
        "RETRY_POLICY": RETRY_POLICY,
        "SIMULATED_RESPONSES": SIMULATED_RESPONSES,
        "CREATE_JOB_REQUEST": CREATE_JOB_REQUEST,
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
    score_color = GREEN if passed >= 4 else YELLOW if passed >= 3 else RED
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
    elif passed >= 4:
        print(f"{BOLD}{GREEN}  ✔  GOOD JOB! You scored {passed}/{total}.{RESET}")
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
print(f"{BOLD}         RELIABILITY & RESILIENCE — GRADER{RESET}")
print(f"{BOLD}         Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("Grading your reliability_resilience_solution.py ...")
blank()

work_dir = tempfile.mkdtemp(prefix="reliability_grade_")
ns = run_solution(work_dir)

if ns:
    exp_request_with_timeout = dict(API_REQUEST)
    exp_request_with_timeout["timeout"] = 10

    exp_backoff_delays = [RETRY_POLICY["base_delay"] * (2 ** attempt) for attempt in range(RETRY_POLICY["max_attempts"])]

    exp_retryable_responses = [r for r in SIMULATED_RESPONSES if r["status_code"] in RETRY_POLICY["retryable_status_codes"]]
    exp_final_status_code = SIMULATED_RESPONSES[-1]["status_code"]

    exp_idempotent_create_request = {
        "method": CREATE_JOB_REQUEST["method"],
        "url": CREATE_JOB_REQUEST["url"],
        "headers": {
            "Content-Type": "application/json",
            "Idempotency-Key": "backup-nyc-rtr-01",
        },
        "body": CREATE_JOB_REQUEST["body"],
    }

    exp_resilience_summary = {
        "timeout": exp_request_with_timeout["timeout"],
        "max_attempts": RETRY_POLICY["max_attempts"],
        "backoff_delays": exp_backoff_delays,
        "retryable_attempts": [r["attempt"] for r in exp_retryable_responses],
        "final_status_code": exp_final_status_code,
    }
    exp_resilience_summary_json = json.dumps(exp_resilience_summary, indent=2, sort_keys=True)

    ways = {
        "timeout": [("copy and add timeout", ["request_with_timeout = dict(API_REQUEST)", "request_with_timeout['timeout'] = 10"])],
        "backoff": [("exponential backoff list", ["backoff_delays = [RETRY_POLICY['base_delay'] * (2 ** attempt) for attempt in range(RETRY_POLICY['max_attempts'])]"])],
        "retryable": [("filter retryable status codes", ["retryable_responses = [r for r in SIMULATED_RESPONSES if r['status_code'] in RETRY_POLICY['retryable_status_codes']]", "final_status_code = SIMULATED_RESPONSES[-1]['status_code']"])],
        "idempotent": [("add idempotency key", ["idempotent_create_request = {'method': CREATE_JOB_REQUEST['method'], 'url': CREATE_JOB_REQUEST['url'], 'headers': {'Content-Type': 'application/json', 'Idempotency-Key': 'backup-nyc-rtr-01'}, 'body': CREATE_JOB_REQUEST['body']}"])],
        "summary": [("build and serialize summary", ["resilience_summary = {'timeout': request_with_timeout['timeout'], 'max_attempts': RETRY_POLICY['max_attempts'], 'backoff_delays': backoff_delays, 'retryable_attempts': [r['attempt'] for r in retryable_responses], 'final_status_code': final_status_code}", "resilience_summary_json = json.dumps(resilience_summary, indent=2, sort_keys=True)"])],
    }

    grade([
        ("Task 1", "request_with_timeout — timeout added to request", ns.get("request_with_timeout"), exp_request_with_timeout, "Copy API_REQUEST and add timeout = 10.", ways["timeout"], "request_with_timeout"),
        ("Task 2", "backoff_delays — exponential backoff schedule", ns.get("backoff_delays"), exp_backoff_delays, "Use base_delay * (2 ** attempt) for max_attempts attempts.", ways["backoff"], "backoff_delays"),
        ("Task 3", "retryable_responses and final_status_code — retry decision data", (ns.get("retryable_responses"), ns.get("final_status_code")), (exp_retryable_responses, exp_final_status_code), "Filter responses whose status_code is retryable and capture the final status.", ways["retryable"], "(retryable_responses, final_status_code)"),
        ("Task 4", "idempotent_create_request — POST with idempotency key", ns.get("idempotent_create_request"), exp_idempotent_create_request, "Build the POST request with Content-Type and Idempotency-Key headers.", ways["idempotent"], "idempotent_create_request"),
        ("Task 5", "resilience_summary and JSON — final report", (ns.get("resilience_summary"), ns.get("resilience_summary_json")), (exp_resilience_summary, exp_resilience_summary_json), "Build the summary dictionary and serialize it with json.dumps(...).", ways["summary"], "(resilience_summary, resilience_summary_json)"),
    ])

shutil.rmtree(work_dir, ignore_errors=True)
pause()
