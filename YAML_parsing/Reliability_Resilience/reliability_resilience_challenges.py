# Reliability & Resilience — Student Challenges
# Cisco API Perspective
# Scenario-based tasks mapped directly to reliability_resilience_deep_dive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: reliability_resilience_solution.py
# 3. Run: python3 reliability_resilience_grading.py

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
    explain("Available in reliability_resilience_solution.py:")
    for name in names:
        explain(f"  • {name}")
    blank()

def output_intro():
    explain("Once you complete this task, your solution must produce the following output:")
    blank()

# DATA — same data shapes used in the deep dive examples
# -----------------------------------------------------------------------------

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

# ═════════════════════════════════════════════════════════════════════════════
# INTRO
# ═════════════════════════════════════════════════════════════════════════════
print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         RELIABILITY & RESILIENCE — CHALLENGES{RESET}")
print(f"{BOLD}         Cisco API Scenario Practice{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("5 scenario-based tasks mapped directly to the DeepDive examples.")
explain("You will add timeouts, build retry backoff delays, identify")
explain("retryable responses, and make a POST request safer to retry.")
blank()
explain("Write answers in: reliability_resilience_solution.py")
explain("Then run: python3 reliability_resilience_grading.py")

pause()

# ── Task 1 ────────────────────────────────────────────────────────────────────
task_section(1, "Add timeout settings to an API request", "Easy")
explain("Scenario: Your automation calls a Cisco controller API. To avoid")
explain("waiting forever if the API hangs, add timeout settings to the request.")
blank()
available("API_REQUEST")
explain("Your task: Create request_with_timeout.")
explain("It must contain the same method, url, and headers as API_REQUEST.")
explain("Add a timeout key with the value 10.")
blank()
hint("Refer DeepDive Chapter 1.2 — Timeout values in request plans.")
blank()
output_intro()
header(">>> print(request_with_timeout['timeout'])")
header("10")
header(">>> print(request_with_timeout['method'])")
header("GET")
blank()

pause()

# ── Task 2 ────────────────────────────────────────────────────────────────────
task_section(2, "Build exponential backoff delays", "Easy")
explain("Scenario: A temporary API failure should not be retried immediately.")
explain("Build the delay schedule your script will use between retry attempts.")
blank()
available("RETRY_POLICY")
explain("Your task: Create backoff_delays.")
explain("Use base_delay * (2 ** attempt) for each attempt number.")
explain("Use attempt numbers from 0 up to max_attempts - 1.")
blank()
hint("Refer DeepDive Chapter 2.3 — Exponential backoff.")
blank()
output_intro()
header(">>> print(backoff_delays)")
header("[1, 2, 4, 8]")
blank()

pause()

# ── Task 3 ────────────────────────────────────────────────────────────────────
task_section(3, "Identify retryable responses", "Medium")
explain("Scenario: Your API call failed twice with temporary server errors,")
explain("then succeeded. Identify which simulated responses were retryable.")
blank()
available("RETRY_POLICY", "SIMULATED_RESPONSES")
explain("Your task: Create retryable_responses and final_status_code.")
explain("retryable_responses must include responses with status codes in")
explain("RETRY_POLICY['retryable_status_codes'].")
explain("final_status_code must be the status code from the last response.")
blank()
hint("Refer DeepDive Chapter 2.2 and 2.4 — Retryable status codes.")
blank()
output_intro()
header(">>> print(len(retryable_responses))")
header("2")
header(">>> print(final_status_code)")
header("200")
blank()

pause()

# ── Task 4 ────────────────────────────────────────────────────────────────────
task_section(4, "Add an idempotency key to a POST request", "Medium")
explain("Scenario: A POST request creates a backup job. If the request times")
explain("out and your script retries it, the API might create duplicate jobs.")
explain("Add an idempotency key so the repeated request can be recognized.")
blank()
available("CREATE_JOB_REQUEST")
explain("Your task: Create idempotent_create_request.")
explain("It must include method, url, body, and headers.")
explain("Headers must include Content-Type: application/json and")
explain("Idempotency-Key: backup-nyc-rtr-01.")
blank()
hint("Refer DeepDive Chapter 3.3 — Idempotency key for create requests.")
blank()
output_intro()
header(">>> print(idempotent_create_request['headers']['Idempotency-Key'])")
header("backup-nyc-rtr-01")
blank()

pause()

# ── Task 5 ────────────────────────────────────────────────────────────────────
task_section(5, "Build a resilience summary JSON string", "Medium")
explain("Scenario: At the end of the workflow, your automation should report")
explain("the timeout, retry policy, retryable attempts, and final status.")
blank()
available("request_with_timeout  (created in Task 1)", "backoff_delays  (created in Task 2)", "retryable_responses  (created in Task 3)", "final_status_code  (created in Task 3)")
explain("Your task: Create resilience_summary and resilience_summary_json.")
explain("resilience_summary must include timeout, max_attempts, backoff_delays,")
explain("retryable_attempts, and final_status_code.")
explain("resilience_summary_json must use json.dumps(..., indent=2, sort_keys=True).")
blank()
hint("Refer DeepDive Chapter 3.4 — Putting it together.")
blank()
output_intro()
header(">>> print(resilience_summary['timeout'], resilience_summary['max_attempts'])")
header("10 4")
header(">>> print(resilience_summary['retryable_attempts'])")
header("[1, 2]")
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
print(f"{BOLD}{CYAN}    reliability_resilience_solution.py{RESET}")
print()
print(f"{BOLD}  Then check them with:{RESET}")
print()
print(f"{BOLD}{CYAN}    python3 reliability_resilience_grading.py{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
