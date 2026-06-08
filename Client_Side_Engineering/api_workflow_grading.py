# API Workflow Fundamentals — Grader
# Cisco API Perspective

import os, sys, json, shutil, tempfile, traceback
RESET="\033[0m"; CYAN="\033[96m"; GREEN="\033[92m"; YELLOW="\033[93m"; WHITE="\033[97m"; RED="\033[91m"; BOLD="\033[1m"; DIM="\033[2m"
def pause(): input(f"\n{DIM}  [ Press ENTER to continue ]{RESET} "); print()
def fail(text): print(f"    {RED}✘  {text}{RESET}")
def hint(text): print(f"    {YELLOW}💡 Hint: {text}{RESET}")
def explain(text): print(f"  {WHITE}{text}{RESET}")
def blank(): print()
def pretty(value): return value if isinstance(value,str) else repr(value)
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
def run_solution(work_dir):
    filename="api_workflow_solution.py"; solution_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
    if not os.path.exists(solution_path): blank(); fail(f"File '{filename}' not found."); blank(); explain(f"Create '{filename}' in the same folder as this grader."); blank(); sys.exit(1)
    namespace={"json":json,"os":os,"API_CONFIG":API_CONFIG,"NEW_DEVICE":NEW_DEVICE,"RAW_DEVICE_RESPONSE":RAW_DEVICE_RESPONSE,"API_RESPONSES":API_RESPONSES}
    try:
        with open(solution_path) as f: code=f.read()
        import textwrap; code=textwrap.dedent(code); old_cwd=os.getcwd(); os.chdir(work_dir)
        try: exec(compile(code,filename,"exec"),namespace)
        finally: os.chdir(old_cwd)
        return namespace
    except Exception:
        blank(); fail("Your script raised an error:"); print(); traceback.print_exc(); blank(); return None

def show_task_review(task_label,label,passed,actual,expected,hint_text,ways,var_name):
    status=f"{GREEN}✔  PASSED{RESET}" if passed else f"{RED}✘  FAILED{RESET}"
    print(f"{BOLD}{'─'*62}{RESET}"); print(f"{BOLD}  {task_label}: {label}{RESET}"); print(f"  {status}"); print(f"{BOLD}{'─'*62}{RESET}"); blank()
    if not passed:
        hint(hint_text); blank(); print(f"    {YELLOW}What your code produced:{RESET}"); print(f"    {CYAN}>>> print({var_name}){RESET}"); print(f"    {RED}{pretty(actual)}{RESET}"); blank()
    print(f"    {YELLOW}Ways to write the solution:{RESET}")
    for way_label, code in ways:
        print(f"    {YELLOW}  ▸ {way_label}{RESET}")
        for line in code: print(f"    {CYAN}    {line}{RESET}")
        blank()
    print(f"    {YELLOW}Correct output:{RESET}"); print(f"    {CYAN}>>> print({var_name}){RESET}"); print(f"    {GREEN}{pretty(expected)}{RESET}"); blank()

def grade(checks):
    total=len(checks); passed=0; results=[]
    for task_label,label,actual,expected,hint_text,ways,var_name in checks:
        ok=actual==expected; passed += 1 if ok else 0; results.append((task_label,label,ok,actual,expected,hint_text,ways,var_name))
    blank(); bar="█"*62; score_color=GREEN if passed>=4 else YELLOW if passed>=3 else RED
    print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print(); print(f"{BOLD}  YOUR SCORE:  {score_color}{passed} / {total}{RESET}"); print()
    for task_label,label,ok,*_ in results:
        mark=f"{GREEN}✔{RESET}" if ok else f"{RED}✘{RESET}"; print(f"    {mark}  {task_label}: {label}")
    print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank(); explain("Press ENTER to review each task — solutions are shown for all tasks.")
    for result in results: pause(); show_task_review(*result)
    blank(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print()
    if passed==total: print(f"{BOLD}{GREEN}  ✔  PERFECT SCORE! You scored {passed}/{total}.{RESET}")
    elif passed>=4: print(f"{BOLD}{GREEN}  ✔  GOOD JOB! You scored {passed}/{total}.{RESET}")
    else: print(f"{BOLD}{YELLOW}  You scored {passed}/{total}. Review, fix, and re-run.{RESET}")
    print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}")
print(); bar="█"*62
print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); print(); print(f"{BOLD}         Client Side Engineering — GRADER{RESET}"); print(f"{BOLD}         Cisco API Perspective{RESET}"); print(); print(f"{BOLD}{bar}{RESET}"); print(f"{BOLD}{bar}{RESET}"); blank(); explain("Grading your api_workflow_solution.py ..."); blank()
work_dir=tempfile.mkdtemp(prefix="api_workflow_grade_"); ns=run_solution(work_dir)
if ns:
    exp_get={"method":"GET","url":API_CONFIG["base_url"]+API_CONFIG["devices_path"],"headers":{"Accept":API_CONFIG["accept"],"X-Auth-Token":API_CONFIG["token"]},"body":None}
    exp_json=json.dumps(NEW_DEVICE,indent=2,sort_keys=True)
    exp_post={"method":"POST","url":API_CONFIG["base_url"]+API_CONFIG["devices_path"],"headers":{"Accept":API_CONFIG["accept"],"Content-Type":"application/json","X-Auth-Token":API_CONFIG["token"]},"body":exp_json}
    exp_parsed=json.loads(RAW_DEVICE_RESPONSE); exp_host=exp_parsed["hostname"]; exp_status=exp_parsed["status"]
    exp_success=[r for r in API_RESPONSES if 200<=r["status_code"]<300]; exp_failed=[r for r in API_RESPONSES if r["status_code"]>=400]
    exp_summary={"total":len(API_RESPONSES),"success_count":len(exp_success),"failure_count":len(exp_failed),"failed_paths":[r["path"] for r in exp_failed]}
    exp_summary_json=json.dumps(exp_summary,indent=2,sort_keys=True)
    ways={
      "get":[("request dictionary",["get_devices_request = {'method': 'GET', 'url': API_CONFIG['base_url'] + API_CONFIG['devices_path'], 'headers': {'Accept': API_CONFIG['accept'], 'X-Auth-Token': API_CONFIG['token']}, 'body': None}"])],
      "post":[("serialize body and build POST request",["new_device_json = json.dumps(NEW_DEVICE, indent=2, sort_keys=True)","post_device_request = {'method': 'POST', 'url': API_CONFIG['base_url'] + API_CONFIG['devices_path'], 'headers': {'Accept': API_CONFIG['accept'], 'Content-Type': 'application/json', 'X-Auth-Token': API_CONFIG['token']}, 'body': new_device_json}"])],
      "parse":[("json.loads",["parsed_device_response = json.loads(RAW_DEVICE_RESPONSE)","response_hostname = parsed_device_response['hostname']","response_status = parsed_device_response['status']"])],
      "status":[("status code filters",["successful_responses = [r for r in API_RESPONSES if 200 <= r['status_code'] < 300]","failed_responses = [r for r in API_RESPONSES if r['status_code'] >= 400]"])],
      "summary":[("build and serialize summary",["api_summary = {'total': len(API_RESPONSES), 'success_count': len(successful_responses), 'failure_count': len(failed_responses), 'failed_paths': [r['path'] for r in failed_responses]}","api_summary_json = json.dumps(api_summary, indent=2, sort_keys=True)"])],
    }
    grade([
      ("Task 1","get_devices_request — GET request dictionary",ns.get("get_devices_request"),exp_get,"Build the GET request using API_CONFIG values.",ways["get"],"get_devices_request"),
      ("Task 2","post_device_request and new_device_json — serialized POST body",(ns.get("post_device_request"),ns.get("new_device_json")),(exp_post,exp_json),"Serialize NEW_DEVICE with json.dumps and use it as the POST body.",ways["post"],"(post_device_request, new_device_json)"),
      ("Task 3","parsed_device_response, response_hostname, response_status — deserialized response",(ns.get("parsed_device_response"),ns.get("response_hostname"),ns.get("response_status")),(exp_parsed,exp_host,exp_status),"Use json.loads(RAW_DEVICE_RESPONSE), then extract hostname and status.",ways["parse"],"(parsed_device_response, response_hostname, response_status)"),
      ("Task 4","successful_responses and failed_responses — response handling",(ns.get("successful_responses"),ns.get("failed_responses")),(exp_success,exp_failed),"Separate 2xx successes from >=400 failures.",ways["status"],"(successful_responses, failed_responses)"),
      ("Task 5","api_summary and api_summary_json — final JSON report",(ns.get("api_summary"),ns.get("api_summary_json")),(exp_summary,exp_summary_json),"Build the summary dictionary and serialize it with json.dumps(...).",ways["summary"],"(api_summary, api_summary_json)"),
    ])
shutil.rmtree(work_dir, ignore_errors=True); pause()
