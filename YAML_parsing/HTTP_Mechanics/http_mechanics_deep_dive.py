# HTTP Mechanics — 3-Chapter Deep Dive
# Cisco API Perspective
# Press ENTER to advance through each step

import json
import shutil
import tempfile

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
print(f"{BOLD}         HTTP MECHANICS FOR NETWORK AUTOMATION{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — HTTP Requests
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "HTTP Requests")

section("1.1 — What an HTTP request looks like")
explain("Network APIs use HTTP requests to ask a controller, firewall, router,")
explain("or cloud service to do something.")
blank()
explain("A request usually has a method, a path, headers, and sometimes a body.")
blank()

raw_get_request = """\
GET /api/v1/devices/nyc-rtr-01 HTTP/1.1
Host: controller.example.local
Accept: application/json
Authorization: Bearer TOKEN
"""
cmd("raw_get_request")
block(raw_get_request.rstrip())
blank()

request = {
    "method": "GET",
    "path": "/api/v1/devices/nyc-rtr-01",
    "headers": {
        "Host": "controller.example.local",
        "Accept": "application/json",
        "Authorization": "Bearer TOKEN",
    },
    "body": None,
}
cmd("request = {'method': 'GET', 'path': '/api/v1/devices/nyc-rtr-01', ...}")
cmd("print(request['method'])")
out(request["method"])
cmd("print(request['path'])")
out(request["path"])
blank()
explain("In Python training labs, representing HTTP messages as dictionaries")
explain("lets you inspect the same parts that real HTTP libraries send.")
pause()

section("1.2 — HTTP verbs: GET and POST")
explain("The HTTP method tells the API what kind of action you want.")
blank()
explain("GET usually reads data. POST usually creates or triggers something.")
blank()

raw_post_request = """\
POST /api/v1/devices HTTP/1.1
Host: controller.example.local
Content-Type: application/json
Accept: application/json

{
  "hostname": "sfo-rtr-01",
  "platform": "IOS-XE",
  "mgmt_ip": "10.3.0.1"
}
"""
cmd("raw_post_request")
block(raw_post_request.rstrip())
blank()

verb_purpose = {
    "GET": "read an existing resource",
    "POST": "create a new resource or trigger an action",
}
cmd("verb_purpose = {'GET': 'read an existing resource', 'POST': 'create a new resource or trigger an action'}")
cmd("print(verb_purpose['GET'])")
out(verb_purpose["GET"])
cmd("print(verb_purpose['POST'])")
out(verb_purpose["POST"])
pause()

section("1.3 — HTTP verbs: PUT, PATCH, DELETE")
explain("PUT, PATCH, and DELETE are common when managing network resources.")
blank()
explain("PUT usually replaces a resource.")
explain("PATCH usually updates part of a resource.")
explain("DELETE removes a resource.")
blank()

examples = [
    {
        "method": "PUT",
        "path": "/api/v1/devices/nyc-rtr-01",
        "purpose": "replace the full device record",
    },
    {
        "method": "PATCH",
        "path": "/api/v1/devices/nyc-rtr-01",
        "purpose": "update only selected fields",
    },
    {
        "method": "DELETE",
        "path": "/api/v1/devices/lab-rtr-99",
        "purpose": "remove a device record",
    },
]
cmd("examples")
show_json(examples)
blank()
cmd("for item in examples:")
cmd("    print(item['method'], item['purpose'])")
for item in examples:
    out(f"{item['method']} {item['purpose']}")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — HTTP Responses
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "HTTP Responses")

section("2.1 — What an HTTP response looks like")
explain("After a request, the server sends a response.")
explain("The response includes a status code, headers, and often a body.")
blank()

raw_response = """\
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hostname": "nyc-rtr-01",
  "status": "up",
  "mgmt_ip": "10.0.0.1"
}
"""
cmd("raw_response")
block(raw_response.rstrip())
blank()

response = {
    "status_code": 200,
    "reason": "OK",
    "headers": {"Content-Type": "application/json"},
    "body": {
        "hostname": "nyc-rtr-01",
        "status": "up",
        "mgmt_ip": "10.0.0.1",
    },
}
cmd("print(response['status_code'])")
out(response["status_code"])
cmd("print(response['body']['hostname'])")
out(response["body"]["hostname"])
pause()

section("2.2 — Status code families")
explain("Status codes are grouped by their first digit.")
blank()
status_families = {
    200: "success",
    201: "success",
    204: "success with no response body",
    400: "client error",
    401: "authentication error",
    403: "authorization error",
    404: "not found",
    409: "conflict",
    500: "server error",
}
cmd("status_families")
show_json(status_families)
blank()
cmd("print(status_families[404])")
out(status_families[404])
cmd("print(status_families[500])")
out(status_families[500])
pause()

section("2.3 — Deciding success or failure")
explain("Most automation treats any 2xx code as success.")
explain("4xx codes usually mean the request was wrong or not allowed.")
explain("5xx codes usually mean the server failed.")
blank()

responses = [
    {"method": "GET", "path": "/api/v1/devices/nyc-rtr-01", "status_code": 200},
    {"method": "POST", "path": "/api/v1/devices", "status_code": 201},
    {"method": "DELETE", "path": "/api/v1/devices/lab-rtr-99", "status_code": 204},
    {"method": "GET", "path": "/api/v1/devices/missing-rtr", "status_code": 404},
]
cmd("success_codes = [r['status_code'] for r in responses if 200 <= r['status_code'] < 300]")
success_codes = [r["status_code"] for r in responses if 200 <= r["status_code"] < 300]
cmd("print(success_codes)")
out(success_codes)
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — HTTP Mechanics in Automation
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "HTTP Mechanics in Automation")

section("3.1 — Choosing the right verb")
explain("Automation often starts by choosing the correct HTTP verb.")
blank()

intent_to_method = {
    "read_device": "GET",
    "create_device": "POST",
    "replace_device": "PUT",
    "update_description": "PATCH",
    "remove_device": "DELETE",
}
cmd("intent_to_method")
show_json(intent_to_method)
blank()
cmd("print(intent_to_method['update_description'])")
out(intent_to_method["update_description"])
pause()

section("3.2 — Building request dictionaries")
explain("A request dictionary is a simple way to model what your API call will send.")
blank()

request_body = {
    "description": "Updated by automation",
}
patch_request = {
    "method": "PATCH",
    "path": "/api/v1/devices/nyc-rtr-01",
    "headers": {"Content-Type": "application/json", "Accept": "application/json"},
    "body": request_body,
}
cmd("patch_request")
show_json(patch_request)
blank()
explain("This mirrors a real API call: method, endpoint, headers, and JSON body.")
pause()

section("3.3 — Summarizing API call results")
explain("After several API calls, automation should summarize what happened.")
blank()

api_results = [
    {"action": "read_device", "method": "GET", "status_code": 200},
    {"action": "create_device", "method": "POST", "status_code": 201},
    {"action": "update_description", "method": "PATCH", "status_code": 200},
    {"action": "remove_lab_device", "method": "DELETE", "status_code": 204},
    {"action": "read_missing_device", "method": "GET", "status_code": 404},
]
cmd("success_count = sum(1 for r in api_results if 200 <= r['status_code'] < 300)")
success_count = sum(1 for r in api_results if 200 <= r["status_code"] < 300)
cmd("failed_actions = [r['action'] for r in api_results if r['status_code'] >= 400]")
failed_actions = [r["action"] for r in api_results if r["status_code"] >= 400]
cmd("print(success_count)")
out(success_count)
cmd("print(failed_actions)")
out(failed_actions)
blank()
summary = {"success_count": success_count, "failed_actions": failed_actions}
show_json(summary)
pause()

bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — HTTP MECHANICS{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   HTTP requests and verbs: GET, POST, PUT, PATCH, DELETE")
print(f"  {BOLD}Ch 2{RESET}   HTTP responses and status code meaning")
print(f"  {BOLD}Ch 3{RESET}   Choosing verbs, building requests, summarizing results")
blank()
print(f"  {WHITE}HTTP mechanics are the grammar of API automation: choose the")
print(f"  right verb, send the right path and payload, then interpret the")
print(f"  status code before your workflow decides what to do next.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
