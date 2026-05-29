# End-to-End API Workflow — Grader
# Cisco CAT8k / Nexus 9k Lab Perspective
#
# HOW IT WORKS:
# 1. Complete api_workflow_solution.py
# 2. Run this script: python3 api_workflow_grading.py
# 3. Fix hints and re-run until you get Good Job!

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

def run_solution(work_dir):
    filename = "api_workflow_solution.py"
    solution_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    if not os.path.exists(solution_path):
        blank()
        fail(f"File '{filename}' not found.")
        blank()
        explain(f"Create '{filename}' in the same folder as this grader.")
        blank()
        sys.exit(1)

    namespace = {
        "os": os,
        "json": json,
        "time": __import__("time"),
        "CAT8K_CONFIG": CAT8K_CONFIG,
        "NEXUS9K_CONFIG": NEXUS9K_CONFIG,
        "RETRYABLE_STATUS_CODES": RETRYABLE_STATUS_CODES,
        "REQUIRED_REQUEST_KEYS": REQUIRED_REQUEST_KEYS,
        "CAT8K_SAMPLE_RESPONSE": CAT8K_SAMPLE_RESPONSE,
        "NEXUS9K_SAMPLE_RESPONSE": NEXUS9K_SAMPLE_RESPONSE,
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
    score_color = GREEN if passed == total else YELLOW if passed >= 1 else RED
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

def sanitized_has_no_secret(value):
    text = repr(value).lower()
    return "password" not in text and "auth': (" not in text and '"auth": (' not in text

print()
bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         END-TO-END API WORKFLOW — GRADER{RESET}")
print(f"{BOLD}         Cisco CAT8k / Nexus 9k Lab Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("Grading your api_workflow_solution.py ...")
blank()

work_dir = tempfile.mkdtemp(prefix="e2e_api_workflow_grade_")
ns = run_solution(work_dir)

if ns:
    exp_cat8k_request = {
        "method": "GET",
        "url": f"https://{CAT8K_CONFIG['host']}{CAT8K_CONFIG['interfaces_path']}",
        "auth": (CAT8K_CONFIG["username"], CAT8K_CONFIG["password"]),
        "headers": {"Accept": "application/yang-data+json"},
        "timeout": CAT8K_CONFIG["timeout"],
        "max_attempts": CAT8K_CONFIG["max_attempts"],
    }
    exp_cat8k_backoff_delays = [CAT8K_CONFIG["base_delay"] * (2 ** attempt) for attempt in range(CAT8K_CONFIG["max_attempts"])]
    exp_cat8k_interfaces = ["GigabitEthernet1", "Loopback0"]

    cat8k_parse = ns.get("parse_cat8k_interfaces")
    cat8k_run = ns.get("run_cat8k_workflow")
    cat8k_interfaces = cat8k_parse(CAT8K_SAMPLE_RESPONSE) if callable(cat8k_parse) else None
    cat8k_result = cat8k_run(live=False) if callable(cat8k_run) else None

    exp_cat8k_result_core = {
        "device": "CAT8k",
        "success": True,
        "interfaces": exp_cat8k_interfaces,
        "attempts": 1,
    }
    actual_cat8k_result_core = None
    if isinstance(cat8k_result, dict):
        actual_cat8k_result_core = {
            "device": cat8k_result.get("device"),
            "success": cat8k_result.get("success"),
            "interfaces": cat8k_result.get("interfaces"),
            "attempts": cat8k_result.get("attempts"),
        }

    exp_nexus_command_payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show interface brief",
            "output_format": "json",
        }
    }
    exp_nexus_request = {
        "method": "POST",
        "url": f"https://{NEXUS9K_CONFIG['host']}{NEXUS9K_CONFIG['nxapi_path']}",
        "auth": (NEXUS9K_CONFIG["username"], NEXUS9K_CONFIG["password"]),
        "headers": {"Content-Type": "application/json"},
        "body": exp_nexus_command_payload,
        "timeout": NEXUS9K_CONFIG["timeout"],
        "max_attempts": NEXUS9K_CONFIG["max_attempts"],
    }

    validate_request = ns.get("validate_request")
    sanitize_log_entry = ns.get("sanitize_log_entry")
    parse_nexus = ns.get("parse_nexus_interfaces")
    run_nexus = ns.get("run_reusable_nexus_workflow")

    validation = validate_request(ns.get("nexus_request")) if callable(validate_request) else None
    sanitized = sanitize_log_entry({"auth": ("admin", "password"), "password": "secret", "status_code": 200}) if callable(sanitize_log_entry) else None
    nexus_interfaces = parse_nexus(NEXUS9K_SAMPLE_RESPONSE) if callable(parse_nexus) else None
    nexus_result = run_nexus(live=False) if callable(run_nexus) else None

    exp_validation = {"valid": True, "missing_keys": []}
    exp_nexus_interfaces = ["Ethernet1/1", "Ethernet1/2"]

    exp_nexus_result_core = {
        "device": "Nexus9k",
        "validation": exp_validation,
        "success": True,
        "interfaces": exp_nexus_interfaces,
        "attempts": 1,
    }
    actual_nexus_result_core = None
    if isinstance(nexus_result, dict):
        actual_nexus_result_core = {
            "device": nexus_result.get("device"),
            "validation": nexus_result.get("validation"),
            "success": nexus_result.get("success"),
            "interfaces": nexus_result.get("interfaces"),
            "attempts": nexus_result.get("attempts"),
        }

    ways = {
        "cat8k": [("CAT8k workflow shape", [
            "cat8k_request = {'method': 'GET', 'url': f\"https://{CAT8K_CONFIG['host']}{CAT8K_CONFIG['interfaces_path']}\", 'auth': (CAT8K_CONFIG['username'], CAT8K_CONFIG['password']), 'headers': {'Accept': 'application/yang-data+json'}, 'timeout': CAT8K_CONFIG['timeout'], 'max_attempts': CAT8K_CONFIG['max_attempts']}",
            "cat8k_backoff_delays = [CAT8K_CONFIG['base_delay'] * (2 ** attempt) for attempt in range(CAT8K_CONFIG['max_attempts'])]",
            "def parse_cat8k_interfaces(response_json):",
            "    return [item['name'] for item in response_json['ietf-interfaces:interfaces']['interface']]",
            "def run_cat8k_workflow(live=False):",
            "    # live=False uses CAT8K_SAMPLE_RESPONSE; live=True uses requests.get with timeout/retries",
            "    return {'device': 'CAT8k', 'success': True, 'interfaces': parse_cat8k_interfaces(CAT8K_SAMPLE_RESPONSE), 'attempts': 1, 'log': []}",
        ])],
        "nexus": [("Reusable Nexus workflow shape", [
            "nexus_command_payload = {'ins_api': {'version': '1.0', 'type': 'cli_show', 'chunk': '0', 'sid': '1', 'input': 'show interface brief', 'output_format': 'json'}}",
            "nexus_request = {'method': 'POST', 'url': f\"https://{NEXUS9K_CONFIG['host']}{NEXUS9K_CONFIG['nxapi_path']}\", 'auth': (NEXUS9K_CONFIG['username'], NEXUS9K_CONFIG['password']), 'headers': {'Content-Type': 'application/json'}, 'body': nexus_command_payload, 'timeout': NEXUS9K_CONFIG['timeout'], 'max_attempts': NEXUS9K_CONFIG['max_attempts']}",
            "def validate_request(request):",
            "    missing = [key for key in REQUIRED_REQUEST_KEYS if key not in request]",
            "    return {'valid': len(missing) == 0, 'missing_keys': missing}",
            "def sanitize_log_entry(entry):",
            "    # remove auth/password before logging",
            "    ...",
            "def parse_nexus_interfaces(response_json):",
            "    return [row['interface'] for row in response_json['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']]",
        ])],
    }

    actual_task1 = (
        ns.get("cat8k_request"),
        ns.get("cat8k_backoff_delays"),
        cat8k_interfaces,
        actual_cat8k_result_core,
        isinstance(cat8k_result, dict) and "log" in cat8k_result,
    )
    expected_task1 = (
        exp_cat8k_request,
        exp_cat8k_backoff_delays,
        exp_cat8k_interfaces,
        exp_cat8k_result_core,
        True,
    )

    actual_task2 = (
        ns.get("nexus_command_payload"),
        ns.get("nexus_request"),
        validation,
        sanitized_has_no_secret(sanitized),
        nexus_interfaces,
        actual_nexus_result_core,
        isinstance(nexus_result, dict) and "log" in nexus_result,
    )
    expected_task2 = (
        exp_nexus_command_payload,
        exp_nexus_request,
        exp_validation,
        True,
        exp_nexus_interfaces,
        exp_nexus_result_core,
        True,
    )

    grade([
        ("Task 1", "CAT8k end-to-end request, retry, parse, and log workflow", actual_task1, expected_task1, "Build CAT8k request data, exponential backoff, parser, and run_cat8k_workflow(live=False).", ways["cat8k"], "(cat8k_request, cat8k_backoff_delays, parse result, workflow result, has log)"),
        ("Task 2", "Reusable Nexus 9k workflow with validation and safe handling", actual_task2, expected_task2, "Build Nexus request data, validate request shape, sanitize logs, parse NX-API output, and run reusable workflow.", ways["nexus"], "(payload, request, validation, sanitized, parse result, workflow result, has log)"),
    ])

shutil.rmtree(work_dir, ignore_errors=True)
pause()
