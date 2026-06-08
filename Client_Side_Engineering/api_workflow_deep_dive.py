
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
print(f"{BOLD}         Client Side Engineering{RESET}")
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
section("2.1 — You want to add a device to Catalyst Center")
explain("Scenario: You want Cisco Catalyst Center to add a new device.")
blank()
new_device={"hostname":"sfo-rtr-01","platform":"IOS-XE","mgmt_ip":"10.3.0.1"}
cmd("new_device")
show_json(new_device)
blank()
explain("Python understands dictionaries.")
explain("Catalyst Center cannot understand Python dictionaries because they only exist inside Python.")
explain("APIs communicate using JSON text, so Python must convert the dictionary into JSON before sending it.")
blank()
cmd("payload_json = json.dumps(new_device, indent=2, sort_keys=True)")
payload_json=json.dumps(new_device,indent=2,sort_keys=True)
cmd("print(payload_json)")
for line in payload_json.splitlines(): out(line)
blank()
cmd("print(type(payload_json))")
out(type(payload_json))
blank()
explain("Think of it like this:")
block("""Python Dict
      ↓
 json.dumps()
      ↓
JSON Text
      ↓
Sent to Catalyst Center""")
blank()
explain("Why do we do this? APIs communicate using JSON text, not Python objects.")
pause()

section("2.2 — Catalyst Center sends a response back")
explain("Scenario: Catalyst Center responds with information about the device.")
blank()
raw_json_response="""{
  "hostname": "sfo-rtr-01",
  "status": "reachable",
  "id": "device-101"
}"""
cmd("raw_json_response")
block(raw_json_response)
blank()
explain("What arrives over the network is just text.")
explain("To work with it in Python, we convert it into a dictionary.")
blank()
cmd("device = json.loads(raw_json_response)")
device=json.loads(raw_json_response)
cmd("print(device['status'])")
out(device["status"])
cmd("print(type(device))")
out(type(device))
blank()
explain("Think of it like this:")
block("""JSON Text from Catalyst Center
              ↓
         json.loads()
              ↓
         Python Dict
              ↓
      Easy to use in code""")
blank()
explain("Why do we do this? Automation works with Python objects, not raw text.")
pause()

section("2.3 — What response.json() is really doing")
explain("Scenario: Your automation sends a request to Catalyst Center.")
blank()
cmd("response = requests.get(url, headers=headers)")
blank()
explain("Catalyst Center returns JSON.")
explain("The requests library gives you a shortcut:")
blank()
cmd("device = response.json()")
blank()
explain("Now you can immediately work with the data.")
cmd("print(device['hostname'])")
out("sfo-rtr-01")
blank()
explain("Behind the scenes:")
block("""Catalyst Center Response
            ↓
         JSON Text
            ↓
      response.json()
            ↓
       Python Dict""")
blank()
explain("Why do engineers use it? It automatically converts JSON into Python data.")
pause()

chapter(3,"Handling Responses")
section("3.1 — Did Catalyst Center accept your request?")
explain("Scenario: Your automation just tried to add a new device to Catalyst Center.")
blank()
response_example={
  "request":"POST /api/v1/devices",
  "status_code":201,
  "body":'{"id": "device-999", "message": "created"}'
}
cmd("response_example")
show_json(response_example)
blank()
explain("Before trusting the response body, always check the status code.")
blank()
cmd("status_code = response_example['status_code']")
status_code=response_example["status_code"]
cmd("print(status_code)")
out(status_code)
blank()
explain("2xx means the request succeeded.")
explain("4xx means the request had a client-side problem, such as bad input or bad authentication.")
explain("5xx means the server had a problem.")
blank()
cmd("if 200 <= status_code < 300:")
cmd("    print('Request succeeded')")
cmd("else:")
cmd("    print('Request failed')")
if 200 <= status_code < 300:
    out("Request succeeded")
else:
    out("Request failed")
blank()
explain("Why do we do this? If Catalyst Center returns an error, your automation should not blindly trust the body.")
pause()

section("3.2 — Handle success and failure differently")
explain("Scenario: Your automation tried to add several devices.")
explain("Some requests succeeded, but one device failed.")
blank()
api_responses=[
 {"hostname":"sfo-rtr-01","method":"POST","path":"/devices","status_code":201,"body":'{"id": "device-101"}'},
 {"hostname":"nyc-rtr-01","method":"POST","path":"/devices","status_code":201,"body":'{"id": "device-102"}'},
 {"hostname":"dal-rtr-01","method":"POST","path":"/devices","status_code":400,"body":'{"error": "missing management IP"}'},
 {"hostname":"chi-rtr-01","method":"POST","path":"/devices","status_code":500,"body":'{"error": "server error"}'},
]
cmd("api_responses")
show_json(api_responses)
blank()
cmd("successful = [r for r in api_responses if 200 <= r['status_code'] < 300]")
successful=[r for r in api_responses if 200 <= r["status_code"] < 300]
cmd("failed = [r for r in api_responses if r['status_code'] >= 400]")
failed=[r for r in api_responses if r["status_code"] >= 400]
blank()
cmd("print('Successful devices:', [r['hostname'] for r in successful])")
out(f"Successful devices: {[r['hostname'] for r in successful]}")
cmd("print('Failed devices:', [r['hostname'] for r in failed])")
out(f"Failed devices: {[r['hostname'] for r in failed]}")
blank()
explain("Why do we do this? Successful devices can continue through the workflow.")
explain("Failed devices may need logging, troubleshooting, retries, or alerts.")
pause()

section("3.3 — Build a report for the operator")
explain("Scenario: At the end of the automation, the operator needs a clean result.")
explain("They do not want to read every raw API response.")
blank()
summary={
 "total_devices":len(api_responses),
 "successful_count":len(successful),
 "failed_count":len(failed),
 "successful_devices":[r["hostname"] for r in successful],
 "failed_devices":[
   {"hostname":r["hostname"],"status_code":r["status_code"],"body":r["body"]}
   for r in failed
 ]
}
cmd("summary")
show_json(summary)
blank()
cmd("summary_json = json.dumps(summary, indent=2, sort_keys=True)")
summary_json=json.dumps(summary,indent=2,sort_keys=True)
cmd("print(summary_json)")
for line in summary_json.splitlines(): out(line)
blank()
explain("Why do we do this? Automation is not finished when the API call returns.")
explain("Automation is finished when a human can quickly understand what happened.")
pause()

print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print(); print(f"{BOLD}   SUMMARY — Client Side Engineering{RESET}"); print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank()
print(f"  {BOLD}Ch 1{RESET}   Build request dictionaries with method, URL, headers, body")
print(f"  {BOLD}Ch 2{RESET}   Serialize with json.dumps(), deserialize with json.loads()")
print(f"  {BOLD}Ch 3{RESET}   Check status codes, parse bodies, summarize results")
blank(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}   Tutorial complete.{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
