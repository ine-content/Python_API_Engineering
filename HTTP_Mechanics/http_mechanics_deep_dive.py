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
explain("The source-of-truth should describe the device.")
explain("Automation uses that data to build the HTTP request.")
blank()

device_inventory_json = """{
  "device_name": "nyc-rtr-01",
  "device_ip": "10.10.10.1",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

explain("Contents of device_inventory.json:")
blank()
block(device_inventory_json)
blank()

explain("The real automation code would open device_inventory.json like this:")
blank()
cmd("with open('device_inventory.json') as file:")
cmd("    device_inventory = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("device_inventory = json.loads(device_inventory_json)")
device_inventory = json.loads(device_inventory_json)
blank()

cmd("print(device_inventory)")
out(device_inventory)
blank()

explain("Now build the HTTP request from the inventory data.")
blank()
cmd("request = {")
cmd("    'method': 'GET',")
cmd("    'path': f\"{device_inventory['api_base_path']}/{device_inventory['device_name']}\",")
cmd("    'headers': {")
cmd("        'Host': device_inventory['api_host'],")
cmd("        'Accept': 'application/json',")
cmd("        'Authorization': f\"Bearer {device_inventory['auth_token']}\"")
cmd("    },")
cmd("    'body': None")
cmd("}")

request = {
    "method": "GET",
    "path": f"{device_inventory['api_base_path']}/{device_inventory['device_name']}",
    "headers": {
        "Host": device_inventory["api_host"],
        "Accept": "application/json",
        "Authorization": f"Bearer {device_inventory['auth_token']}",
    },
    "body": None,
}
blank()

cmd("print(request)")
out(request)
blank()

cmd("print(request['method'])")
out(request["method"])
cmd("print(request['path'])")
out(request["path"])
blank()

pause()

section("1.2 — HTTP verbs: GET and POST")
explain("The HTTP method tells the API what kind of action you want.")
blank()
explain("GET usually reads data. POST usually creates or triggers something.")
blank()
explain("The source-of-truth should describe the intent.")
explain("Automation chooses the HTTP method and builds the request.")
blank()

device_read_intent_json = """{
  "action": "read_device",
  "device_name": "nyc-rtr-01",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

device_create_intent_json = """{
  "action": "create_device",
  "device_name": "sfo-rtr-01",
  "platform": "IOS-XE",
  "mgmt_ip": "10.3.0.1",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

explain("Contents of device_read_intent.json:")
blank()
block(device_read_intent_json)
blank()

explain("Contents of device_create_intent.json:")
blank()
block(device_create_intent_json)
blank()

explain("The real automation code would open the intent files like this:")
blank()
cmd("with open('device_read_intent.json') as file:")
cmd("    read_intent = json.load(file)")
cmd("with open('device_create_intent.json') as file:")
cmd("    create_intent = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("read_intent = json.loads(device_read_intent_json)")
read_intent = json.loads(device_read_intent_json)
cmd("create_intent = json.loads(device_create_intent_json)")
create_intent = json.loads(device_create_intent_json)
blank()

cmd("print(read_intent)")
out(read_intent)
blank()
cmd("print(create_intent)")
out(create_intent)
blank()

explain("Build a GET request from the read intent.")
blank()
cmd("get_request = {")
cmd("    'method': 'GET',")
cmd("    'path': f\"{read_intent['api_base_path']}/{read_intent['device_name']}\",")
cmd("    'headers': {")
cmd("        'Host': read_intent['api_host'],")
cmd("        'Accept': 'application/json',")
cmd("        'Authorization': f\"Bearer {read_intent['auth_token']}\"")
cmd("    },")
cmd("    'body': None")
cmd("}")

get_request = {
    "method": "GET",
    "path": f"{read_intent['api_base_path']}/{read_intent['device_name']}",
    "headers": {
        "Host": read_intent["api_host"],
        "Accept": "application/json",
        "Authorization": f"Bearer {read_intent['auth_token']}",
    },
    "body": None,
}
blank()

explain("Build a POST request from the create intent.")
blank()
cmd("post_request = {")
cmd("    'method': 'POST',")
cmd("    'path': create_intent['api_base_path'],")
cmd("    'headers': {")
cmd("        'Host': create_intent['api_host'],")
cmd("        'Content-Type': 'application/json',")
cmd("        'Accept': 'application/json',")
cmd("        'Authorization': f\"Bearer {create_intent['auth_token']}\"")
cmd("    },")
cmd("    'body': {")
cmd("        'hostname': create_intent['device_name'],")
cmd("        'platform': create_intent['platform'],")
cmd("        'mgmt_ip': create_intent['mgmt_ip']")
cmd("    }")
cmd("}")

post_request = {
    "method": "POST",
    "path": create_intent["api_base_path"],
    "headers": {
        "Host": create_intent["api_host"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {create_intent['auth_token']}",
    },
    "body": {
        "hostname": create_intent["device_name"],
        "platform": create_intent["platform"],
        "mgmt_ip": create_intent["mgmt_ip"],
    },
}
blank()

cmd("print(get_request)")
out(get_request)
blank()
cmd("print(post_request)")
out(post_request)
blank()

cmd("print(get_request['method'])")
out(get_request["method"])
cmd("print(post_request['method'])")
out(post_request["method"])
blank()

explain("GET is used to read information from an API.")
explain("POST is used to create a resource or trigger an action.")
pause()

section("1.3 — HTTP verbs: PUT, PATCH, DELETE")
explain("PUT, PATCH, and DELETE are common when managing network resources.")
blank()
explain("PUT usually replaces a resource.")
explain("PATCH usually updates part of a resource.")
explain("DELETE removes a resource.")
blank()
explain("The source-of-truth should describe the desired operation.")
explain("Automation builds the correct HTTP request from that intent.")
blank()

device_replace_intent_json = """{
  "action": "replace_device",
  "device_name": "nyc-rtr-01",
  "description": "Updated by automation",
  "location": "New York",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

device_patch_intent_json = """{
  "action": "update_description",
  "device_name": "nyc-rtr-01",
  "description": "Updated by automation",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

device_delete_intent_json = """{
  "action": "remove_device",
  "device_name": "lab-rtr-99",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

explain("Contents of device_replace_intent.json:")
blank()
block(device_replace_intent_json)
blank()

explain("Contents of device_patch_intent.json:")
blank()
block(device_patch_intent_json)
blank()

explain("Contents of device_delete_intent.json:")
blank()
block(device_delete_intent_json)
blank()

explain("The real automation code would open the intent files like this:")
blank()
cmd("with open('device_replace_intent.json') as file:")
cmd("    replace_intent = json.load(file)")
cmd("with open('device_patch_intent.json') as file:")
cmd("    patch_intent = json.load(file)")
cmd("with open('device_delete_intent.json') as file:")
cmd("    delete_intent = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("replace_intent = json.loads(device_replace_intent_json)")
replace_intent = json.loads(device_replace_intent_json)
cmd("patch_intent = json.loads(device_patch_intent_json)")
patch_intent = json.loads(device_patch_intent_json)
cmd("delete_intent = json.loads(device_delete_intent_json)")
delete_intent = json.loads(device_delete_intent_json)
blank()

explain("Build a PUT request from the replace intent.")
blank()
put_request = {
    "method": "PUT",
    "path": f"{replace_intent['api_base_path']}/{replace_intent['device_name']}",
    "headers": {
        "Host": replace_intent["api_host"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {replace_intent['auth_token']}",
    },
    "body": {
        "hostname": replace_intent["device_name"],
        "description": replace_intent["description"],
        "location": replace_intent["location"],
    },
}
cmd("print(put_request)")
out(put_request)
blank()

explain("Build a PATCH request from the update intent.")
blank()
patch_request = {
    "method": "PATCH",
    "path": f"{patch_intent['api_base_path']}/{patch_intent['device_name']}",
    "headers": {
        "Host": patch_intent["api_host"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {patch_intent['auth_token']}",
    },
    "body": {
        "description": patch_intent["description"],
    },
}
cmd("print(patch_request)")
out(patch_request)
blank()

explain("Build a DELETE request from the remove intent.")
blank()
delete_request = {
    "method": "DELETE",
    "path": f"{delete_intent['api_base_path']}/{delete_intent['device_name']}",
    "headers": {
        "Host": delete_intent["api_host"],
        "Accept": "application/json",
        "Authorization": f"Bearer {delete_intent['auth_token']}",
    },
    "body": None,
}
cmd("print(delete_request)")
out(delete_request)
blank()

cmd("print(put_request['method'])")
out(put_request["method"])
cmd("print(patch_request['method'])")
out(patch_request["method"])
cmd("print(delete_request['method'])")
out(delete_request["method"])
blank()

explain("PUT replaces an entire resource.")
explain("PATCH updates only selected fields.")
explain("DELETE removes a resource.")
pause()

section("1.4 — Example API Call Flow")

explain("Let's walk through a complete API workflow.")
blank()
explain("Our goal is to change the hostname of a Cisco router.")
explain("The router management IP is 10.10.10.1.")
explain("We want to change its hostname to nyc-rtr-01.")
blank()
explain("The source-of-truth file should contain inventory and intent data,")
explain("not a fully built PATCH request.")
blank()

hostname_inventory_json = """{
  "device_name": "edge-router-temp",
  "device_ip": "10.10.10.1",
  "desired_hostname": "nyc-rtr-01",
  "platform": "IOS-XE",
  "site": "New York",
  "api_base_path": "/api/v1/devices",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

explain("Contents of hostname_inventory.json:")
blank()
block(hostname_inventory_json)
blank()

explain("The real automation code would open hostname_inventory.json like this:")
blank()
cmd("with open('hostname_inventory.json') as file:")
cmd("    device = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("device = json.loads(hostname_inventory_json)")
device = json.loads(hostname_inventory_json)
blank()

cmd("print(device)")
out(device)
blank()

explain("Extract the inventory and intent values from the Python dictionary.")
blank()
cmd("device_ip = device['device_ip']")
device_ip = device["device_ip"]
cmd("desired_hostname = device['desired_hostname']")
desired_hostname = device["desired_hostname"]
cmd("print(device_ip)")
out(device_ip)
cmd("print(desired_hostname)")
out(desired_hostname)
blank()

explain("Now build the PATCH request from the source-of-truth data.")
blank()
cmd("hostname_update_request = {")
cmd("    'method': 'PATCH',")
cmd("    'path': f\"{device['api_base_path']}/{device_ip}\",")
cmd("    'headers': {")
cmd("        'Host': device['api_host'],")
cmd("        'Content-Type': 'application/json',")
cmd("        'Accept': 'application/json',")
cmd("        'Authorization': f\"Bearer {device['auth_token']}\"")
cmd("    },")
cmd("    'body': {")
cmd("        'hostname': desired_hostname")
cmd("    }")
cmd("}")

hostname_update_request = {
    "method": "PATCH",
    "path": f"{device['api_base_path']}/{device_ip}",
    "headers": {
        "Host": device["api_host"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {device['auth_token']}",
    },
    "body": {
        "hostname": desired_hostname,
    },
}
blank()

cmd("print(hostname_update_request)")
out(hostname_update_request)
blank()

explain("Next, automation builds the URL that will be used for the API call.")
blank()

cmd("base_url = f\"https://{device_ip}\"")
base_url = f"https://{device_ip}"

cmd("url = f\"{base_url}{hostname_update_request['path']}\"")
url = f"{base_url}{hostname_update_request['path']}"

blank()

cmd("print(url)")
out(url)

blank()

explain("The API client would send the PATCH request to this URL.")
blank()

cmd("print(f\"Updating {device_ip} hostname to {desired_hostname}\")")
out(f"Updating {device_ip} hostname to {desired_hostname}")
blank()

explain("The API request would conceptually be sent as:")
blank()
cmd("PATCH /api/v1/devices/10.10.10.1")
cmd("Content-Type: application/json")
cmd("Authorization: Bearer XYZ123")
cmd("")
cmd("{")
cmd("    'hostname': 'nyc-rtr-01'")
cmd("}")
blank()

explain("If the API returns HTTP 200 OK,")
explain("the hostname change was successful.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — HTTP Responses
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "HTTP Responses")

section("2.1 — What an HTTP response looks like")
explain("After a request, the server sends a response.")
explain("The response includes a status code, headers, and often a body.")
blank()
explain("Response JSON comes from the API after automation sends a request.")
explain("Automation converts that response JSON into Python data.")
blank()

response_json = """{
  "status_code": 200,
  "reason": "OK",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "hostname": "nyc-rtr-01",
    "status": "up",
    "mgmt_ip": "10.0.0.1"
  }
}"""

explain("Contents of response.json:")
blank()
block(response_json)
blank()

explain("The API returned this JSON response.")
explain("Automation converts the response JSON into Python data.")
blank()

cmd("response = json.loads(response_json)")
response = json.loads(response_json)
blank()

cmd("print(response)")
out(response)
blank()
cmd("print(response['status_code'])")
out(response["status_code"])
cmd("print(response['body']['hostname'])")
out(response["body"]["hostname"])
pause()

section("2.2 — Status code families")
explain("Status codes are grouped by their first digit.")
blank()
explain("Reference data can also come from JSON.")
explain("Automation loads the reference data, then uses it for decisions.")
blank()

status_families_json = """{
  "200": "success",
  "201": "success",
  "204": "success with no response body",
  "400": "client error",
  "401": "authentication error",
  "403": "authorization error",
  "404": "not found",
  "409": "conflict",
  "500": "server error"
}"""

explain("Contents of status_families.json:")
blank()
block(status_families_json)
blank()

explain("The real automation code would open status_families.json like this:")
blank()
cmd("with open('status_families.json') as file:")
cmd("    status_families = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("status_families = json.loads(status_families_json)")
status_families = json.loads(status_families_json)
blank()

cmd("print(status_families)")
out(status_families)
blank()
cmd("print(status_families['404'])")
out(status_families["404"])
cmd("print(status_families['500'])")
out(status_families["500"])
pause()

section("2.3 — Deciding success or failure")
explain("Most automation treats any 2xx code as success.")
explain("4xx codes usually mean the request was wrong or not allowed.")
explain("5xx codes usually mean the server failed.")
blank()
explain("API result data can be stored as JSON after several calls.")
blank()

api_responses_json = """[
  {
    "method": "GET",
    "path": "/api/v1/devices/nyc-rtr-01",
    "status_code": 200
  },
  {
    "method": "POST",
    "path": "/api/v1/devices",
    "status_code": 201
  },
  {
    "method": "DELETE",
    "path": "/api/v1/devices/lab-rtr-99",
    "status_code": 204
  },
  {
    "method": "GET",
    "path": "/api/v1/devices/missing-rtr",
    "status_code": 404
  }
]"""

explain("Contents of api_responses.json:")
blank()
block(api_responses_json)
blank()

explain("The real automation code would open api_responses.json like this:")
blank()
cmd("with open('api_responses.json') as file:")
cmd("    responses = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("responses = json.loads(api_responses_json)")
responses = json.loads(api_responses_json)
blank()

cmd("print(responses)")
out(responses)
blank()
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
explain("Chapter 3 now follows one complete workflow from start to finish.")
blank()
explain("Goal: retrieve the interface status of a device from a Cisco-style API.")
blank()
explain("Before automation builds a request, it must choose the correct HTTP verb.")
explain("Because this workflow reads existing information, the correct verb is GET.")
blank()

interface_status_intent_json = """{
  "workflow": "retrieve_interface_status",
  "device_name": "nyc-access-01",
  "device_id": "device-101",
  "site": "New York",
  "api_base_path": "/dna/intent/api/v1/network-device",
  "api_host": "yourdomain.com",
  "auth_token": "XYZ123"
}"""

explain("Contents of interface_status_intent.json:")
blank()
block(interface_status_intent_json)
blank()

explain("The real automation code would open interface_status_intent.json like this:")
blank()
cmd("with open('interface_status_intent.json') as file:")
cmd("    interface_status_intent = json.load(file)")
blank()

explain("For this standalone deep dive, we convert the same JSON text directly.")
blank()
cmd("interface_status_intent = json.loads(interface_status_intent_json)")
interface_status_intent = json.loads(interface_status_intent_json)
blank()

cmd("print(interface_status_intent)")
out(interface_status_intent)
blank()

explain("Map the workflow intent to an HTTP method.")
blank()

intent_to_method_json = """{
  "retrieve_interface_status": "GET",
  "create_device": "POST",
  "replace_device": "PUT",
  "update_interface_description": "PATCH",
  "remove_device": "DELETE"
}"""

explain("Contents of intent_to_method.json:")
blank()
block(intent_to_method_json)
blank()

cmd("intent_to_method = json.loads(intent_to_method_json)")
intent_to_method = json.loads(intent_to_method_json)
blank()

cmd("method = intent_to_method[interface_status_intent['workflow']]")
method = intent_to_method[interface_status_intent["workflow"]]
blank()

cmd("print(method)")
out(method)
blank()

explain("GET is correct because the workflow is retrieving status data.")
explain("Nothing is being created, replaced, updated, or deleted.")
pause()

section("3.2 — Building the interface-status request")
explain("Now automation can build the actual HTTP request dictionary.")
blank()
explain("The request needs a method, path, headers, and body.")
explain("Because this is a GET request, there is no JSON body to send.")
blank()
explain("The source-of-truth gave us the device ID and API base path.")
explain("Automation uses those values to build the endpoint.")
blank()

cmd("device_id = interface_status_intent['device_id']")
device_id = interface_status_intent["device_id"]
cmd("base_path = interface_status_intent['api_base_path']")
base_path = interface_status_intent["api_base_path"]
blank()

cmd("path = f\"{base_path}/{device_id}/interfaces/status\"")
path = f"{base_path}/{device_id}/interfaces/status"
blank()

cmd("print(path)")
out(path)
blank()

explain("Now build the request dictionary that an API client could send.")
blank()

cmd("interface_status_request = {")
cmd("    'method': method,")
cmd("    'path': path,")
cmd("    'headers': {")
cmd("        'Host': interface_status_intent['api_host'],")
cmd("        'Accept': 'application/json',")
cmd("        'Authorization': f\"Bearer {interface_status_intent['auth_token']}\"")
cmd("    },")
cmd("    'body': None")
cmd("}")

interface_status_request = {
    "method": method,
    "path": path,
    "headers": {
        "Host": interface_status_intent["api_host"],
        "Accept": "application/json",
        "Authorization": f"Bearer {interface_status_intent['auth_token']}",
    },
    "body": None,
}
blank()

cmd("print(interface_status_request)")
out(interface_status_request)
blank()

cmd("print(interface_status_request['method'])")
out(interface_status_request["method"])
cmd("print(interface_status_request['path'])")
out(interface_status_request["path"])
cmd("print(interface_status_request['body'])")
out(interface_status_request["body"])
blank()

explain("Conceptually, the API client would send this HTTP request:")
blank()
cmd("GET /dna/intent/api/v1/network-device/device-101/interfaces/status")
cmd("Accept: application/json")
cmd("Authorization: Bearer XYZ123")
blank()

explain("The important point is that the request was built from source-of-truth data.")
explain("The workflow intent chose GET, and the device data built the path.")
pause()

section("3.3 — Reading and summarizing the interface-status response")
explain("After the GET request is sent, the API returns an HTTP response.")
blank()
explain("The response includes a status code and a JSON body with interface data.")
explain("Automation should inspect both before deciding what to do next.")
blank()

interface_status_response_json = """{
  "status_code": 200,
  "reason": "OK",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "device_name": "nyc-access-01",
    "device_id": "device-101",
    "interfaces": [
      {
        "name": "GigabitEthernet1",
        "admin_status": "up",
        "oper_status": "up",
        "vlan": 10
      },
      {
        "name": "GigabitEthernet2",
        "admin_status": "up",
        "oper_status": "down",
        "vlan": 20
      },
      {
        "name": "GigabitEthernet3",
        "admin_status": "down",
        "oper_status": "down",
        "vlan": 30
      }
    ]
  }
}"""

explain("Contents of interface_status_response.json:")
blank()
block(interface_status_response_json)
blank()

explain("The real API client would receive this JSON response from the controller.")
explain("Automation converts the response JSON into Python data.")
blank()

cmd("response = json.loads(interface_status_response_json)")
response = json.loads(interface_status_response_json)
blank()

cmd("print(response['status_code'])")
out(response["status_code"])
cmd("print(response['reason'])")
out(response["reason"])
blank()

explain("First, confirm that the HTTP request succeeded.")
blank()

cmd("request_succeeded = 200 <= response['status_code'] < 300")
request_succeeded = 200 <= response["status_code"] < 300
cmd("print(request_succeeded)")
out(request_succeeded)
blank()

explain("Now inspect the interface data in the response body.")
blank()

cmd("interfaces = response['body']['interfaces']")
interfaces = response["body"]["interfaces"]
blank()

cmd("up_interfaces = [i['name'] for i in interfaces if i['oper_status'] == 'up']")
up_interfaces = [i["name"] for i in interfaces if i["oper_status"] == "up"]
cmd("down_interfaces = [i['name'] for i in interfaces if i['oper_status'] == 'down']")
down_interfaces = [i["name"] for i in interfaces if i["oper_status"] == "down"]
cmd("unexpected_down = [i['name'] for i in interfaces if i['admin_status'] == 'up' and i['oper_status'] == 'down']")
unexpected_down = [
    i["name"]
    for i in interfaces
    if i["admin_status"] == "up" and i["oper_status"] == "down"
]
blank()

cmd("print(up_interfaces)")
out(up_interfaces)
cmd("print(down_interfaces)")
out(down_interfaces)
cmd("print(unexpected_down)")
out(unexpected_down)
blank()

explain("An interface that is administratively up but operationally down may need attention.")
blank()

summary = {
    "device_name": response["body"]["device_name"],
    "request_succeeded": request_succeeded,
    "total_interfaces": len(interfaces),
    "oper_up_count": len(up_interfaces),
    "oper_down_count": len(down_interfaces),
    "unexpected_down_interfaces": unexpected_down,
}

cmd("summary")
show_json(summary)
blank()

explain("This completes the flow:")
explain("choose GET, build the request, read the response, and summarize status.")
explain("That is the core HTTP loop used in API-driven network automation.")
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
print(f"  {BOLD}Ch 3{RESET}   Complete flow: retrieve and summarize interface status")
blank()
print(f"  {WHITE}HTTP mechanics are the grammar of API automation: choose the")
print(f"  right verb, send the right path and payload, then interpret the")
print(f"  status code before your workflow decides what to do next.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
