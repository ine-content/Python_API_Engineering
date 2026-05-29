# CAT8K API CALL Workflow - Grader

import base64
import importlib.util
import json
import os
import sys
import traceback

from inventory import DEVICES, ENDPOINTS

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RED = "\033[91m"
BOLD = "\033[1m"

TODO_FILENAME = "cat8k_todo.py"
OUTPUT_FILENAME = "cat8k_parsed_output.json"

SAMPLE_INTERFACES = {
    "ietf-interfaces:interfaces": {
        "interface": [
            {"name": "GigabitEthernet1", "enabled": True},
            {"name": "Loopback0", "enabled": True},
        ]
    }
}


def blank():
    print()


def explain(text):
    print(f"  {WHITE}{text}{RESET}")


def pretty(value):
    if isinstance(value, str):
        return value
    return repr(value)


def fail_banner(label):
    print(f"{BOLD}{'─' * 62}{RESET}")
    print(f"{BOLD}  {label}{RESET}")
    print(f"  {RED}✘ FAILED{RESET}")
    print(f"{BOLD}{'─' * 62}{RESET}")


def pass_line(label):
    print(f"{BOLD}{'─' * 62}{RESET}")
    print(f"{BOLD}  {label}{RESET}")
    print(f"  {GREEN}✔ PASSED{RESET}")
    print(f"{BOLD}{'─' * 62}{RESET}")
    blank()


def show_solution_and_exit(label, actual, expected, hint_text, solution_lines):
    fail_banner(label)
    blank()
    print(f"    {YELLOW}Hint:{RESET} {hint_text}")
    blank()
    print(f"    {YELLOW}Your value:{RESET}   {RED}{pretty(actual)}{RESET}")
    print(f"    {YELLOW}Expected:{RESET}     {GREEN}{pretty(expected)}{RESET}")
    blank()
    print(f"    {CYAN}Solution for this TODO:{RESET}")
    for line in solution_lines:
        print(f"    {GREEN}{line}{RESET}")
    blank()
    print(f"{BOLD}{YELLOW}  Fix {TODO_FILENAME}, then run this grader again.{RESET}")
    blank()
    raise SystemExit(1)


def load_student_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    todo_path = os.path.join(base_dir, TODO_FILENAME)

    if not os.path.exists(todo_path):
        print(f"{RED}Could not find {TODO_FILENAME} in this folder.{RESET}")
        return None

    try:
        spec = importlib.util.spec_from_file_location("cat8k_student_todo", todo_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception:
        blank()
        print(f"{RED}Your {TODO_FILENAME} file raised an error:{RESET}")
        print()
        traceback.print_exc()
        blank()
        print(f"{BOLD}{YELLOW}  Fix the Python error above, then run this grader again.{RESET}")
        blank()
        return None


def parse_interfaces(response_json):
    interfaces = response_json.get("ietf-interfaces:interfaces", {}).get("interface", [])
    return [item.get("name") for item in interfaces]


def write_json_output(payload):
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_FILENAME)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return output_path


def run_live_tests(requests_by_device):
    print(f"{BOLD}{CYAN}  Running live CAT8K RESTCONF tests...{RESET}")
    blank()

    try:
        import requests
    except ImportError:
        print(f"{RED}  requests is not installed. Run: pip install requests{RESET}")
        return 1

    results = {}
    for device_name, request_data in requests_by_device.items():
        device = DEVICES[device_name]
        try:
            response = requests.request(
                method=request_data["method"],
                url=request_data["url"],
                headers=request_data["headers"],
                timeout=30,
                verify=device.get("verify_ssl", False),
            )
            response.raise_for_status()
            parsed = parse_interfaces(response.json())
            results[device_name] = {
                "source": "live_device",
                "host": device["host"],
                "status_code": response.status_code,
                "parsed_interfaces": parsed,
            }
            print(f"{GREEN}  {device_name}: live request successful. HTTP {response.status_code}{RESET}")
        except Exception as exc:
            results[device_name] = {
                "source": "live_device",
                "host": device["host"],
                "error": str(exc),
            }
            print(f"{RED}  {device_name}: live request failed. {exc}{RESET}")

    output_path = write_json_output({"mode": "live", "devices": results})
    blank()
    print(f"{CYAN}  Live output saved to: {output_path}{RESET}")
    return 0


def build_expected_values(username, password):
    expected_username_password = f"{username}:{password}"
    expected_encoded = base64.b64encode(expected_username_password.encode("utf-8")).decode("ascii")
    expected_auth_header = f"Basic {expected_encoded}"

    expected_requests = {}
    for device_name, device in DEVICES.items():
        expected_requests[device_name] = {
            "method": "GET",
            "url": f"https://{device['host']}{ENDPOINTS['interfaces']}",
            "headers": {
                "Accept": "application/yang-data+json",
                "Authorization": expected_auth_header,
            },
        }

    return expected_username_password, expected_encoded, expected_auth_header, expected_requests


def main():
    print()
    bar = "█" * 62
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    print()
    print(f"{BOLD}         CAT8K API CALL WORKFLOW - GRADER{RESET}")
    print()
    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    blank()

    username = os.environ.get("DEVICE_USERNAME")
    password = os.environ.get("DEVICE_PASSWORD")
    if not username or not password:
        print(f"{RED}DEVICE_USERNAME and DEVICE_PASSWORD must be set.{RESET}")
        print("Example:")
        print("  export DEVICE_USERNAME=admin")
        print("  export DEVICE_PASSWORD='C1sc0123!'")
        return 1

    explain(f"Grading {TODO_FILENAME} for all CAT8K devices in inventory.py ...")
    blank()

    student = load_student_file()
    if student is None:
        return 1

    expected_username_password, expected_encoded, expected_auth_header, expected_requests = build_expected_values(username, password)

    checks = [
        {
            "label": "TODO 1 - Build cat8k_username_password",
            "actual": getattr(student, "cat8k_username_password", None),
            "expected": expected_username_password,
            "hint": "Combine DEVICE_USERNAME and DEVICE_PASSWORD as username:password.",
            "solution": [
                "cat8k_username_password = f\"{DEVICE_USERNAME}:{DEVICE_PASSWORD}\"",
            ],
        },
        {
            "label": "TODO 2 - Build cat8k_encoded_credentials",
            "actual": getattr(student, "cat8k_encoded_credentials", None),
            "expected": expected_encoded,
            "hint": "Base64 encode cat8k_username_password and decode the result to ascii.",
            "solution": [
                "cat8k_encoded_credentials = base64.b64encode(",
                "    cat8k_username_password.encode(\"utf-8\")",
                ").decode(\"ascii\")",
            ],
        },
        {
            "label": "TODO 3 - Build cat8k_authorization_header",
            "actual": getattr(student, "cat8k_authorization_header", None),
            "expected": expected_auth_header,
            "hint": "Prefix cat8k_encoded_credentials with 'Basic '.",
            "solution": [
                "cat8k_authorization_header = f\"Basic {cat8k_encoded_credentials}\"",
            ],
        },
        {
            "label": "TODO 4 - Build cat8k_requests",
            "actual": getattr(student, "cat8k_requests", None),
            "expected": expected_requests,
            "hint": "Build one GET RESTCONF request for every device in DEVICES.",
            "solution": [
                "cat8k_requests = {}",
                "for device_name, device in DEVICES.items():",
                "    cat8k_requests[device_name] = {",
                "        \"method\": \"GET\",",
                "        \"url\": f\"https://{device['host']}{ENDPOINTS['interfaces']}\",",
                "        \"headers\": {",
                "            \"Accept\": \"application/yang-data+json\",",
                "            \"Authorization\": cat8k_authorization_header,",
                "        },",
                "    }",
            ],
        },
        {
            "label": "TODO 5 - Build interfaces_requests",
            "actual": getattr(student, "interfaces_requests", None),
            "expected": expected_requests,
            "hint": "Set interfaces_requests to the completed cat8k_requests dictionary.",
            "solution": [
                "interfaces_requests = cat8k_requests",
            ],
        },
    ]

    passed = 0
    for check in checks:
        if check["actual"] == check["expected"]:
            passed += 1
            pass_line(check["label"])
        else:
            print(f"{BOLD}{bar}{RESET}")
            print(f"{BOLD}  YOUR SCORE BEFORE STOPPING: {YELLOW}{passed} / {len(checks)}{RESET}")
            print(f"{BOLD}{bar}{RESET}")
            blank()
            show_solution_and_exit(
                check["label"],
                check["actual"],
                check["expected"],
                check["hint"],
                check["solution"],
            )

    print(f"{BOLD}{bar}{RESET}")
    print(f"{BOLD}  YOUR SCORE: {GREEN}{passed} / {len(checks)}{RESET}")
    print(f"{BOLD}{bar}{RESET}")
    blank()

    sample_payload = {
        "mode": "sample",
        "devices": {
            device_name: {
                "source": "sample_inventory",
                "host": device["host"],
                "parsed_interfaces": parse_interfaces(SAMPLE_INTERFACES),
            }
            for device_name, device in DEVICES.items()
        },
    }
    output_path = write_json_output(sample_payload)
    print(f"{BOLD}{GREEN}  Good Job! All deterministic checks passed.{RESET}")
    print(f"{GREEN}  Sample parsed output saved to: {output_path}{RESET}")
    blank()

    answer = input(f"{CYAN}  Run live CAT8K tests for all devices now? (y/n): {RESET}").strip().lower()
    if answer in {"y", "yes"}:
        blank()
        return run_live_tests(getattr(student, "interfaces_requests", expected_requests))

    explain("Skipped live CAT8K tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
