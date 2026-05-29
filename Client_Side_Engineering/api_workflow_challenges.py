# API Workflow Fundamentals — Student Challenges
# Cisco API Perspective
# Scenario-based tasks mapped directly to api_workflow_deep_dive.py
#
# HOW IT WORKS:
# 1. Read each scenario carefully
# 2. Write your solution in: api_workflow_solution.py
# 3. Run: python3 api_workflow_grading.py

import json
import os

RESET="\033[0m"; CYAN="\033[96m"; GREEN="\033[92m"; YELLOW="\033[93m"; WHITE="\033[97m"; RED="\033[91m"; BOLD="\033[1m"; DIM="\033[2m"
def pause(): input(f"\n{DIM}  [ Press ENTER to continue ]{RESET} "); print()
def header(text): print(f"    {CYAN}{text}{RESET}")
def explain(text): print(f"  {WHITE}{text}{RESET}")
def hint(text): print(f"  {YELLOW}Hint: {text}{RESET}")
def blank(): print()
def task_section(num,title,difficulty):
    stars={"Easy":"★☆☆","Medium":"★★☆","Hard":"★★★"}; label=f"Task {num:02d} — {title}  |  {difficulty} {stars[difficulty]}"
    print(f"{BOLD}{'─'*70}{RESET}"); print(f"{BOLD}  {label}{RESET}"); print(f"{BOLD}{'─'*70}{RESET}"); blank()
def available(*names):
    explain("Available in api_workflow_solution.py:")
    for name in names: explain(f"  • {name}")
    blank()
def output_intro(): explain("Once you complete this task, your solution must produce the following output:"); blank()

API_CONFIG={"base_url":"https://sandboxdnac.cisco.com","devices_path":"/dna/intent/api/v1/network-device","token":"abc123sandbox-token","accept":"application/json"}
NEW_DEVICE={"hostname":"sfo-rtr-01","platform":"IOS-XE","mgmt_ip":"10.3.0.1"}
RAW_DEVICE_RESPONSE="""\
{
  "hostname": "nyc-rtr-01",
  "id": "device-101",
  "status": "reachable"
}
"""
API_RESPONSES=[
 {"method":"GET","path":"/devices","status_code":200,"body":'{"count": 2}'},
 {"method":"POST","path":"/devices","status_code":201,"body":'{"id": "device-999"}'},
 {"method":"GET","path":"/devices/missing","status_code":404,"body":'{"error": "not found"}'},
 {"method":"PATCH","path":"/devices/nyc-rtr-01","status_code":500,"body":'{"error": "server error"}'},
]

print(); bar="█"*70
print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
print(f"{BOLD}         API WORKFLOW FUNDAMENTALS — CHALLENGES{RESET}")
print(f"{BOLD}         Cisco API Scenario Practice{RESET}")
print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank()
explain("5 scenario-based tasks mapped directly to the DeepDive examples.")
explain("You will build requests, serialize JSON, deserialize JSON,")
explain("handle response status codes, and create a summary.")
blank(); explain("Write answers in: api_workflow_solution.py"); explain("Then run: python3 api_workflow_grading.py")
blank(); explain("These tasks use Cisco Sandbox-style URLs and realistic raw data,"); explain("but the grader does not require live internet access.")
pause()

task_section(1,"Build a GET request dictionary","Easy")
explain("Scenario: You are preparing to read network devices from a Cisco controller API.")
explain("Before sending the call, build a request dictionary that contains method, URL, headers, and body.")
blank(); available("API_CONFIG")
explain("Your task: Create get_devices_request.")
explain("It must use method GET, combine base_url and devices_path for the URL,")
explain("include Accept and X-Auth-Token headers, and use body=None.")
blank(); hint("Refer DeepDive Chapter 1.2 — Building a GET request."); blank(); output_intro()
header(">>> print(get_devices_request['method'])"); header("GET")
header(">>> print(get_devices_request['headers']['X-Auth-Token'])"); header("abc123sandbox-token")
blank(); pause()

task_section(2,"Build a POST request and serialize the body","Easy")
explain("Scenario: Your automation needs to create a new device record.")
explain("The API expects a JSON body, so the Python dictionary must be serialized into a JSON string.")
blank(); available("NEW_DEVICE")
explain("Your task: Create post_device_request and new_device_json.")
explain("new_device_json must use json.dumps(NEW_DEVICE, indent=2, sort_keys=True).")
explain("post_device_request must include method POST, headers, and body=new_device_json.")
blank(); hint("Refer DeepDive Chapter 1.3 and 2.1 — POST request and json.dumps()."); blank(); output_intro()
header(">>> print(post_device_request['method'])"); header("POST")
header(">>> print(type(new_device_json))"); header("<class 'str'>")
blank(); pause()

task_section(3,"Deserialize a raw JSON response","Easy")
explain("Scenario: The API returned JSON text for one device.")
explain("Your code cannot access fields until the JSON string becomes a Python dictionary.")
blank(); available("RAW_DEVICE_RESPONSE")
explain("Your task: Create parsed_device_response, response_hostname, and response_status.")
explain("Use json.loads(RAW_DEVICE_RESPONSE).")
blank(); hint("Refer DeepDive Chapter 2.2 — JSON string to Python dict with json.loads()."); blank(); output_intro()
header(">>> print(response_hostname, response_status)"); header("nyc-rtr-01 reachable")
blank(); pause()

task_section(4,"Separate successful and failed API responses","Medium")
explain("Scenario: Your script collected several API responses.")
explain("Separate successful responses from failed responses using status codes.")
blank(); available("API_RESPONSES")
explain("Your task: Create successful_responses and failed_responses.")
explain("successful_responses must include responses where 200 <= status_code < 300.")
explain("failed_responses must include responses where status_code >= 400.")
blank(); hint("Refer DeepDive Chapter 3.1 and 3.2 — Handling response status codes."); blank(); output_intro()
header(">>> print(len(successful_responses), len(failed_responses))"); header("2 2")
blank(); pause()

task_section(5,"Build a JSON API run summary","Medium")
explain("Scenario: At the end of the workflow, you need a JSON report summarizing the run.")
blank(); available("API_RESPONSES","successful_responses  (created in Task 4)","failed_responses  (created in Task 4)")
explain("Your task: Create api_summary and api_summary_json.")
explain("api_summary must include total, success_count, failure_count, and failed_paths.")
explain("api_summary_json must use json.dumps(api_summary, indent=2, sort_keys=True).")
blank(); hint("Refer DeepDive Chapter 3.3 — Build a clean summary."); blank(); output_intro()
header(">>> print(api_summary['total'], api_summary['success_count'], api_summary['failure_count'])"); header("4 2 2")
header(">>> print(api_summary['failed_paths'])"); header("['/devices/missing', '/devices/nyc-rtr-01']")
blank(); pause()

print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
print(f"{BOLD}  All tasks read. Write your answers in:{RESET}"); print(); print(f"{BOLD}{CYAN}    api_workflow_solution.py{RESET}"); print()
print(f"{BOLD}  Then check them with:{RESET}"); print(); print(f"{BOLD}{CYAN}    python3 api_workflow_grading.py{RESET}"); print()
print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
