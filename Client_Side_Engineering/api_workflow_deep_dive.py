# API Workflow Fundamentals — 3-Chapter Deep Dive
# Cisco API Perspective
# Press ENTER to advance through each step

import json

RESET="\033[0m"; CYAN="\033[96m"; GREEN="\033[92m"; YELLOW="\033[93m"; WHITE="\033[97m"; RED="\033[91m"; BOLD="\033[1m"; DIM="\033[2m"
def pause(): input(f"\n{DIM}  [ Press ENTER to continue ]{RESET} "); print()
def cmd(command): print(f"    {CYAN}>>> {command}{RESET}")
def out(value): print(f"    {GREEN}{value}{RESET}")
def explain(text): print(f"  {WHITE}{text}{RESET}")
def blank(): print()
def block(text):
    for line in text.splitlines(): print(f"    {CYAN}{line}{RESET}")
def show_json(value):
    for line in json.dumps(value, indent=2, sort_keys=True).splitlines(): out(line)
def section(title):
    print(f"{BOLD}{'─'*62}{RESET}"); print(f"{BOLD}  {title}{RESET}"); print(f"{BOLD}{'─'*62}{RESET}"); blank()
def chapter(num,title):
    bar="█"*62; print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print(); print(f"{BOLD}   CHAPTER {num}{RESET}"); print(f"{BOLD}   {title}{RESET}"); print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank()

bar="█"*62
print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
print(f"{BOLD}         API WORKFLOW FUNDAMENTALS{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco API Perspective{RESET}")
print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank()
explain("This deep dive focuses on the full API workflow:")
explain("build a request, serialize data, handle the response,")
explain("deserialize JSON, and summarize results.")
pause()

chapter(1,"Building Requests")
section("1.1 — What a request needs")
explain("Before Python can call an API, your code must know what request to send.")
blank(); explain("A request usually needs method, URL, headers, and sometimes a body.")
blank()
request={"method":"GET","url":"https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device","headers":{"Accept":"application/json","X-Auth-Token":"abc123sandbox-token"},"body":None}
cmd("request")
show_json(request)
blank(); explain("This dictionary is a plan for an API call. It does not contact the API yet.")
pause()

section("1.2 — Building a GET request")
explain("GET is used to read data. A GET request usually does not have a JSON body.")
blank()
base_url="https://sandboxdnac.cisco.com"; path="/dna/intent/api/v1/network-device"; token="abc123sandbox-token"
cmd("url = base_url + path")
url=base_url+path
cmd("headers = {'Accept': 'application/json', 'X-Auth-Token': token}")
headers={"Accept":"application/json","X-Auth-Token":token}
cmd("get_request = {'method': 'GET', 'url': url, 'headers': headers, 'body': None}")
get_request={"method":"GET","url":url,"headers":headers,"body":None}
show_json(get_request)
pause()

section("1.3 — Building a POST request with a JSON body")
explain("POST is often used to create something or trigger an action.")
explain("When an API expects JSON input, your request needs Content-Type and a body.")
blank()
new_device={"hostname":"sfo-rtr-01","platform":"IOS-XE","mgmt_ip":"10.3.0.1"}
cmd("new_device")
show_json(new_device)
post_request={"method":"POST","url":"https://controller.example.local/api/v1/devices","headers":{"Accept":"application/json","Content-Type":"application/json"},"body":new_device}
cmd("post_request")
show_json(post_request)
blank(); explain("The body is still a Python dict here. Before sending it, it may need to become JSON text.")
pause()

chapter(2,"Serialization and Deserialization")
section("2.1 — Python dict to JSON string with json.dumps()")
explain("Serialization means converting Python data into a string format that can be sent or stored.")
blank(); cmd("payload_json = json.dumps(new_device, indent=2, sort_keys=True)")
payload_json=json.dumps(new_device,indent=2,sort_keys=True)
cmd("print(payload_json)")
for line in payload_json.splitlines(): out(line)
cmd("print(type(payload_json))"); out(type(payload_json))
pause()

section("2.2 — JSON string to Python dict with json.loads()")
explain("Deserialization means converting JSON text back into Python data.")
blank()
raw_json_response='''{
  "hostname": "nyc-rtr-01",
  "id": "device-101",
  "status": "reachable"
}'''
cmd("raw_json_response")
block(raw_json_response)
cmd("device = json.loads(raw_json_response)")
device=json.loads(raw_json_response)
cmd("print(device['hostname'])"); out(device['hostname'])
cmd("print(type(device))"); out(type(device))
pause()

section("2.3 — response.json() concept")
explain("The requests library often gives you a response object. response.json() parses JSON response body text into Python data.")
blank()
response_example={"status_code":200,"body_text":'{"hostname": "nyc-rtr-01", "status": "reachable"}'}
cmd("response_example")
show_json(response_example)
cmd("parsed_body = json.loads(response_example['body_text'])")
parsed_body=json.loads(response_example['body_text'])
cmd("print(parsed_body['status'])"); out(parsed_body['status'])
pause()

chapter(3,"Handling Responses")
section("3.1 — Status codes decide what happens next")
explain("Automation should check the status code before trusting the body.")
blank(); explain("2xx means success. 4xx means a client/request problem. 5xx means a server problem.")
blank()
api_responses=[
 {"method":"GET","path":"/devices","status_code":200,"body":'{"count": 2}'},
 {"method":"POST","path":"/devices","status_code":201,"body":'{"id": "device-999"}'},
 {"method":"GET","path":"/devices/missing","status_code":404,"body":'{"error": "not found"}'},
 {"method":"PATCH","path":"/devices/nyc-rtr-01","status_code":500,"body":'{"error": "server error"}'},
]
cmd("api_responses")
show_json(api_responses)
pause()

section("3.2 — Separate successful and failed responses")
cmd("successful = [r for r in api_responses if 200 <= r['status_code'] < 300]")
successful=[r for r in api_responses if 200 <= r['status_code'] < 300]
cmd("failed = [r for r in api_responses if r['status_code'] >= 400]")
failed=[r for r in api_responses if r['status_code'] >= 400]
cmd("print(len(successful), len(failed))"); out(f"{len(successful)} {len(failed)}")
blank(); explain("This lets your automation continue on good responses and handle errors separately.")
pause()

section("3.3 — Build a clean summary")
summary={"total":len(api_responses),"success_count":len(successful),"failure_count":len(failed),"failed_paths":[r['path'] for r in failed]}
cmd("summary")
show_json(summary)
cmd("summary_json = json.dumps(summary, indent=2, sort_keys=True)")
summary_json=json.dumps(summary,indent=2,sort_keys=True)
cmd("print(summary_json)")
for line in summary_json.splitlines(): out(line)
blank(); explain("This is a common final step: summarize an API workflow in JSON.")
pause()

print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print(); print(f"{BOLD}   SUMMARY — API WORKFLOW FUNDAMENTALS{RESET}"); print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank()
print(f"  {BOLD}Ch 1{RESET}   Build request dictionaries with method, URL, headers, body")
print(f"  {BOLD}Ch 2{RESET}   Serialize with json.dumps(), deserialize with json.loads()")
print(f"  {BOLD}Ch 3{RESET}   Check status codes, parse bodies, summarize results")
blank(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}   Tutorial complete.{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
