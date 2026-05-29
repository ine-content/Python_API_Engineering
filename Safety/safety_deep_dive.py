# Safety — 3-Chapter Deep Dive
# Cisco API Perspective
# Press ENTER to advance through each step

import json

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

def note(text):
    print(f"  {YELLOW}{text}{RESET}")

def blank():
    print()

def block(text):
    for line in text.splitlines():
        print(f"    {CYAN}{line}{RESET}")

def show_json(value):
    for line in json.dumps(value, indent=2, sort_keys=True).splitlines():
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

bar = "█" * 62
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         SAFETY FOR API AUTOMATION{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("This deep dive teaches how to make API automation safer before,")
explain("during, and after requests.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — Validation Before Requests
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "Validation Before Requests")

section("1.1 — Why validation matters")
explain("Before sending an API request, your script should check that the")
explain("payload is complete and safe.")
blank()
explain("Without validation, automation can send bad data to a controller or device.")
blank()
warn("Bad input can become a bad network change.")
blank()
note("Validate before you request.")
pause()

section("1.2 — Required field validation")
explain("A simple safety check is verifying that required fields exist.")
blank()

change_request = {
    "hostname": "nyc-rtr-01",
    "interface": "GigabitEthernet1",
    "description": "WAN uplink",
}
required_fields = ["hostname", "interface", "description"]

cmd("change_request")
show_json(change_request)
blank()
cmd("required_fields = ['hostname', 'interface', 'description']")
cmd("missing_fields = [field for field in required_fields if field not in change_request]")
missing_fields = [field for field in required_fields if field not in change_request]
cmd("print(missing_fields)")
out(missing_fields)
blank()
if not missing_fields:
    out("payload has all required fields")
pause()

section("1.3 — Value validation")
explain("Field presence is not enough.")
explain("You should also check whether the values are acceptable.")
blank()

allowed_interfaces = ["GigabitEthernet1", "GigabitEthernet2", "Loopback0"]
cmd("allowed_interfaces = ['GigabitEthernet1', 'GigabitEthernet2', 'Loopback0']")
cmd("interface_is_allowed = change_request['interface'] in allowed_interfaces")
interface_is_allowed = change_request["interface"] in allowed_interfaces
cmd("print(interface_is_allowed)")
out(interface_is_allowed)
blank()
explain("This prevents the script from changing an unexpected interface.")
pause()

section("1.4 — Build a validation report")
explain("A validation report is useful because it tells the operator why")
explain("a request is allowed or blocked.")
blank()

validation_report = {
    "valid": not missing_fields and interface_is_allowed,
    "missing_fields": missing_fields,
    "interface_is_allowed": interface_is_allowed,
}
cmd("validation_report")
show_json(validation_report)
blank()
explain("If valid is False, your script should not send the API request.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Safe Error Handling
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "Safe Error Handling")

section("2.1 — Errors are expected")
explain("APIs fail sometimes.")
blank()
explain("Common errors include:")
explain("  • 400 Bad Request — your payload is wrong")
explain("  • 401 Unauthorized — credentials are wrong or expired")
explain("  • 403 Forbidden — you are authenticated but not allowed")
explain("  • 404 Not Found — the target resource does not exist")
explain("  • 500 Server Error — the server failed")
blank()
note("Safe automation handles errors without crashing blindly.")
pause()

section("2.2 — Error response example")
error_response = {
    "status_code": 400,
    "body": {
        "error": "invalid interface",
        "detail": "Interface GigabitEthernet99 does not exist",
    },
}
cmd("error_response")
show_json(error_response)
blank()
cmd("error_message = error_response['body'].get('error', 'unknown error')")
error_message = error_response["body"].get("error", "unknown error")
cmd("print(error_message)")
out(error_message)
pause()

section("2.3 — Safe error summary")
explain("A safe error summary should help troubleshooting but avoid exposing")
explain("secrets such as tokens, passwords, or full Authorization headers.")
blank()

request_context = {
    "method": "PATCH",
    "url": "https://controller.example.local/api/v1/interfaces/GigabitEthernet99",
    "headers": {
        "Accept": "application/json",
        "Authorization": "Bearer secret-token-value",
    },
}
cmd("request_context")
show_json(request_context)
blank()

safe_error = {
    "method": request_context["method"],
    "url": request_context["url"],
    "status_code": error_response["status_code"],
    "error": error_message,
}
cmd("safe_error")
show_json(safe_error)
blank()
explain("Notice the token is not included in the error summary.")
pause()

section("2.4 — Decide whether to continue")
explain("Some errors should stop the workflow immediately.")
explain("For example, authentication errors should not continue to later steps.")
blank()

status_code = 401
cmd("status_code = 401")
cmd("should_continue = status_code not in [401, 403]")
should_continue = status_code not in [401, 403]
cmd("print(should_continue)")
out(should_continue)
blank()
explain("If credentials are wrong or permissions are missing, continuing could")
explain("create confusing downstream failures.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — Failure Recovery
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "Failure Recovery")

section("3.1 — What failure recovery means")
explain("Failure recovery means deciding what to do after something goes wrong.")
blank()
explain("Recovery might mean:")
explain("  • stop safely")
explain("  • retry later")
explain("  • roll back a change")
explain("  • mark the device as skipped")
explain("  • alert a human operator")
pause()

section("3.2 — Recovery actions by status code")
recovery_map = {
    400: "stop_and_fix_payload",
    401: "stop_and_refresh_credentials",
    403: "stop_and_check_permissions",
    404: "skip_missing_resource",
    409: "stop_and_review_conflict",
    500: "retry_or_escalate",
    503: "retry_with_backoff",
}
cmd("recovery_map")
show_json(recovery_map)
blank()
cmd("print(recovery_map[503])")
out(recovery_map[503])
pause()

section("3.3 — Rollback planning")
explain("For risky changes, capture enough information to undo the change.")
blank()

change_plan = {
    "device": "nyc-rtr-01",
    "interface": "GigabitEthernet1",
    "new_description": "WAN uplink",
    "previous_description": "old description",
}
cmd("change_plan")
show_json(change_plan)
blank()

rollback_plan = {
    "device": change_plan["device"],
    "interface": change_plan["interface"],
    "restore_description": change_plan["previous_description"],
}
cmd("rollback_plan")
show_json(rollback_plan)
blank()
explain("The rollback plan uses the previous known-good value.")
pause()

section("3.4 — Safety summary")
safety_summary = {
    "validation_required": True,
    "safe_error_handling": True,
    "recovery_action": recovery_map[503],
    "rollback_available": True,
}
cmd("safety_summary")
show_json(safety_summary)
blank()
explain("Safe automation is not only about sending the correct API request.")
explain("It is also about preventing bad requests and recovering safely from failure.")
pause()

bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — SAFETY{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   Validate required fields and allowed values before requests")
print(f"  {BOLD}Ch 2{RESET}   Handle errors safely without leaking secrets")
print(f"  {BOLD}Ch 3{RESET}   Recover from failures with stop, skip, retry, or rollback")
blank()
print(f"  {WHITE}Safe automation checks before acting, handles failure clearly,")
print(f"  and preserves enough context to recover when something goes wrong.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
