# Safety — Grader
# Cisco API Perspective
#
# HOW IT WORKS:
# 1. Write your solution in safety_solution.py
# 2. Run this script: python3 safety_grading.py
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

def run_solution(work_dir):
    filename = "safety_solution.py"
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
        "CHANGE_REQUEST": CHANGE_REQUEST,
        "REQUIRED_FIELDS": REQUIRED_FIELDS,
        "ALLOWED_INTERFACES": ALLOWED_INTERFACES,
        "ERROR_RESPONSE": ERROR_RESPONSE,
        "REQUEST_CONTEXT": REQUEST_CONTEXT,
        "RECOVERY_MAP": RECOVERY_MAP,
        "CHANGE_PLAN": CHANGE_PLAN,
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
print(f"{BOLD}         SAFETY — GRADER{RESET}")
print(f"{BOLD}         Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("Grading your safety_solution.py ...")
blank()

work_dir = tempfile.mkdtemp(prefix="safety_grade_")
ns = run_solution(work_dir)

if ns:
    exp_missing_fields = [field for field in REQUIRED_FIELDS if field not in CHANGE_REQUEST]
    exp_has_required_fields = len(exp_missing_fields) == 0
    exp_interface_is_allowed = CHANGE_REQUEST["interface"] in ALLOWED_INTERFACES
    exp_validation_report = {
        "valid": exp_has_required_fields and exp_interface_is_allowed,
        "missing_fields": exp_missing_fields,
        "interface_is_allowed": exp_interface_is_allowed,
    }
    exp_safe_error_summary = {
        "method": REQUEST_CONTEXT["method"],
        "url": REQUEST_CONTEXT["url"],
        "status_code": ERROR_RESPONSE["status_code"],
        "error": ERROR_RESPONSE["body"]["error"],
        "detail": ERROR_RESPONSE["body"]["detail"],
    }
    exp_recovery_action = RECOVERY_MAP[ERROR_RESPONSE["status_code"]]
    exp_rollback_plan = {
        "device": CHANGE_PLAN["device"],
        "interface": CHANGE_PLAN["interface"],
        "restore_description": CHANGE_PLAN["previous_description"],
    }
    exp_safety_summary = {
        "validation_passed": exp_validation_report["valid"],
        "status_code": exp_safe_error_summary["status_code"],
        "recovery_action": exp_recovery_action,
        "rollback_available": bool(exp_rollback_plan),
    }
    exp_safety_summary_json = json.dumps(exp_safety_summary, indent=2, sort_keys=True)

    ways = {
        "required": [("required field check", ["missing_fields = [field for field in REQUIRED_FIELDS if field not in CHANGE_REQUEST]", "has_required_fields = len(missing_fields) == 0"])],
        "allowed": [("allowed interface validation", ["interface_is_allowed = CHANGE_REQUEST['interface'] in ALLOWED_INTERFACES", "validation_report = {'valid': has_required_fields and interface_is_allowed, 'missing_fields': missing_fields, 'interface_is_allowed': interface_is_allowed}"])],
        "error": [("safe error summary", ["safe_error_summary = {'method': REQUEST_CONTEXT['method'], 'url': REQUEST_CONTEXT['url'], 'status_code': ERROR_RESPONSE['status_code'], 'error': ERROR_RESPONSE['body']['error'], 'detail': ERROR_RESPONSE['body']['detail']}"])],
        "recovery": [("recovery action and rollback", ["recovery_action = RECOVERY_MAP[ERROR_RESPONSE['status_code']]", "rollback_plan = {'device': CHANGE_PLAN['device'], 'interface': CHANGE_PLAN['interface'], 'restore_description': CHANGE_PLAN['previous_description']}"])],
        "summary": [("build and serialize safety summary", ["safety_summary = {'validation_passed': validation_report['valid'], 'status_code': safe_error_summary['status_code'], 'recovery_action': recovery_action, 'rollback_available': bool(rollback_plan)}", "safety_summary_json = json.dumps(safety_summary, indent=2, sort_keys=True)"])],
    }

    grade([
        ("Task 1", "missing_fields and has_required_fields — required validation", (ns.get("missing_fields"), ns.get("has_required_fields")), (exp_missing_fields, exp_has_required_fields), "Check each REQUIRED_FIELDS item against CHANGE_REQUEST.", ways["required"], "(missing_fields, has_required_fields)"),
        ("Task 2", "interface_is_allowed and validation_report — value validation", (ns.get("interface_is_allowed"), ns.get("validation_report")), (exp_interface_is_allowed, exp_validation_report), "Check the interface against ALLOWED_INTERFACES and build validation_report.", ways["allowed"], "(interface_is_allowed, validation_report)"),
        ("Task 3", "safe_error_summary — sanitized error report", ns.get("safe_error_summary"), exp_safe_error_summary, "Build the error summary without including request headers.", ways["error"], "safe_error_summary"),
        ("Task 4", "recovery_action and rollback_plan — recovery data", (ns.get("recovery_action"), ns.get("rollback_plan")), (exp_recovery_action, exp_rollback_plan), "Use RECOVERY_MAP and CHANGE_PLAN to build recovery details.", ways["recovery"], "(recovery_action, rollback_plan)"),
        ("Task 5", "safety_summary and JSON — final report", (ns.get("safety_summary"), ns.get("safety_summary_json")), (exp_safety_summary, exp_safety_summary_json), "Build the summary dictionary and serialize it with json.dumps(...).", ways["summary"], "(safety_summary, safety_summary_json)"),
    ])

shutil.rmtree(work_dir, ignore_errors=True)
pause()
