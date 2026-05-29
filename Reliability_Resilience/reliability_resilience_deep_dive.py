# Reliability & Resilience — 3-Chapter Deep Dive
# Cisco API Perspective
# Press ENTER to advance through each step

import json
import time

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
print(f"{BOLD}         RELIABILITY & RESILIENCE FOR API AUTOMATION{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("This deep dive teaches how API automation survives slow networks,")
explain("temporary failures, and repeated requests without creating damage.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — Timeouts
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "Timeouts")

section("1.1 — Why timeouts matter")
explain("A network API call can hang for many reasons:")
explain("  • the controller is overloaded")
explain("  • the device is slow")
explain("  • DNS or routing is broken")
explain("  • the server accepted the connection but never responds")
blank()
explain("If your code waits forever, the automation job can freeze.")
blank()
note("A timeout is a limit: how long your script is willing to wait.")
pause()

section("1.2 — Timeout values in request plans")
explain("In Python requests, timeout is often passed as a number of seconds.")
explain("For training, we can model that in a request dictionary.")
blank()

request_plan = {
    "method": "GET",
    "url": "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device",
    "headers": {"Accept": "application/json", "X-Auth-Token": "abc123sandbox-token"},
    "timeout": 10,
}
cmd("request_plan")
show_json(request_plan)
blank()
explain("This means: if the API does not respond within 10 seconds,")
explain("the script should stop waiting and treat the call as failed.")
pause()

section("1.3 — Connect timeout vs read timeout")
explain("Some libraries let you use two timeout values:")
explain("  • connect timeout — time allowed to establish a connection")
explain("  • read timeout — time allowed to wait for the response body")
blank()

timeout_plan = {
    "connect_timeout": 3,
    "read_timeout": 10,
    "requests_timeout_argument": (3, 10),
}
cmd("timeout_plan")
show_json(timeout_plan)
blank()
explain("This is useful because connecting should usually be quick,")
explain("but some API operations may take longer to return data.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Retries and Exponential Backoff
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "Retries and Exponential Backoff")

section("2.1 — Why retries exist")
explain("Not every API failure is permanent.")
blank()
explain("A request may fail temporarily because:")
explain("  • the controller is busy")
explain("  • the device is rebooting")
explain("  • the API rate-limited the client")
explain("  • the network briefly dropped a packet")
blank()
note("Retries give temporary failures another chance.")
pause()

section("2.2 — Which status codes are retryable?")
explain("Do not retry every failure.")
blank()
explain("For example, 401 Unauthorized usually means credentials are wrong.")
explain("Retrying the same bad password will not help.")
blank()
explain("Common retryable status codes include:")
retryable_status_codes = [408, 429, 500, 502, 503, 504]
cmd("retryable_status_codes")
out(retryable_status_codes)
blank()
explain("These often mean timeout, rate limit, or temporary server failure.")
pause()

section("2.3 — Exponential backoff")
explain("If a request fails temporarily, retrying immediately can make things worse.")
explain("Exponential backoff waits longer between each retry.")
blank()
explain("Example formula:")
block("delay = base_delay * (2 ** attempt_number)")
blank()

base_delay = 1
max_attempts = 4
backoff_delays = [base_delay * (2 ** attempt) for attempt in range(max_attempts)]
cmd("backoff_delays = [base_delay * (2 ** attempt) for attempt in range(max_attempts)]")
cmd("print(backoff_delays)")
out(backoff_delays)
blank()
explain("The delays grow like this: 1, 2, 4, 8 seconds.")
pause()

section("2.4 — Retry decision example")
responses = [
    {"attempt": 1, "status_code": 503},
    {"attempt": 2, "status_code": 503},
    {"attempt": 3, "status_code": 200},
]
cmd("responses")
show_json(responses)
blank()
cmd("final_status = responses[-1]['status_code']")
final_status = responses[-1]["status_code"]
cmd("print(final_status)")
out(final_status)
blank()
explain("This simulated workflow failed twice, then succeeded.")
explain("A resilient script can record each attempt and report the final result.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — Idempotent Request Design
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "Idempotent Request Design")

section("3.1 — What idempotent means")
explain("Idempotent means repeating the same operation has the same final effect.")
blank()
explain("This matters because retries can send the same request more than once.")
blank()
note("Safe retry design asks: what happens if this request runs twice?")
pause()

section("3.2 — Common idempotency patterns")
patterns = {
    "GET": "safe to retry because it reads data",
    "PUT": "usually idempotent because it replaces with the same desired state",
    "DELETE": "often idempotent if deleting an already-missing resource is acceptable",
    "POST": "often not idempotent because it may create duplicates",
    "PATCH": "depends on whether the patch sets values or increments/changes relative state",
}
cmd("patterns")
show_json(patterns)
pause()

section("3.3 — Idempotency key for create requests")
explain("POST can create duplicate resources if retried after a timeout.")
blank()
explain("One solution is an idempotency key: a unique client-generated value")
explain("that tells the server repeated requests are the same operation.")
blank()

create_request = {
    "method": "POST",
    "url": "https://controller.example.local/api/v1/jobs",
    "headers": {
        "Content-Type": "application/json",
        "Idempotency-Key": "create-backup-job-nyc-rtr-01-2024-01-15",
    },
    "body": {
        "device": "nyc-rtr-01",
        "operation": "backup",
    },
}
cmd("create_request")
show_json(create_request)
blank()
explain("If the client retries this request, the server can recognize the")
explain("same Idempotency-Key and avoid creating duplicate jobs.")
pause()

section("3.4 — Putting it together")
workflow_policy = {
    "timeout": 10,
    "max_attempts": 4,
    "retryable_status_codes": [408, 429, 500, 502, 503, 504],
    "backoff_delays": [1, 2, 4, 8],
    "idempotency_key_required_for_post": True,
}
cmd("workflow_policy")
show_json(workflow_policy)
blank()
explain("A resilient API workflow should define these rules before it runs.")
pause()

bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — RELIABILITY & RESILIENCE{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   Timeouts prevent API calls from hanging forever")
print(f"  {BOLD}Ch 2{RESET}   Retries with exponential backoff handle temporary failures")
print(f"  {BOLD}Ch 3{RESET}   Idempotent design makes retries safer")
blank()
print(f"  {WHITE}Reliable automation is not just about succeeding when everything")
print(f"  works. It is about behaving safely when APIs are slow, overloaded,")
print(f"  unavailable, or uncertain.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
