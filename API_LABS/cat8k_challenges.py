# CAT8K RESTCONF Workflow - Student Challenge
# Build Basic Auth and GET interface requests for all CAT8K devices in inventory.

RESET = "\033[0m"
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"


def pause():
    input("\n" + DIM + "  [ Press ENTER to continue ] " + RESET)
    print()


def explain(text):
    print(f"  {WHITE}{text}{RESET}")


def header(text):
    print(f"    {CYAN}{text}{RESET}")


def blank():
    print()


print()
bar = "█" * 70
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}         CAT8K API CALL WORKFLOW - STUDENT CHALLENGE{RESET}")
print(f"{BOLD}         Build Basic Auth and Interface Requests for All Devices{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("In this lab, you will build RESTCONF request dictionaries for every CAT8K")
explain("device listed in inventory.py.")
blank()
explain("Before starting, update inventory.py with your CAT8K device IPs or FQDNs.")
blank()
explain("Then set credentials with environment variables:")
header("export DEVICE_USERNAME=admin")
header("export DEVICE_PASSWORD='C1sc0123!'")
blank()
explain("Complete your work in:")
header("cat8k_todo.py")
blank()
explain("Then run:")
header("python3 cat8k_grading.py")
blank()
pause()

print(f"{BOLD}{'─' * 70}{RESET}")
print(f"{BOLD}  Task 01 - Build CAT8K Basic Auth and Requests for All Devices{RESET}")
print(f"{BOLD}{'─' * 70}{RESET}")
blank()
explain("Complete these variables in cat8k_todo.py:")
explain("  - cat8k_username_password")
explain("  - cat8k_encoded_credentials")
explain("  - cat8k_authorization_header")
explain("  - cat8k_requests")
explain("  - interfaces_requests")
blank()
explain("Requirements:")
explain("  - Read DEVICE_USERNAME and DEVICE_PASSWORD from environment variables.")
explain("  - Combine username and password as username:password.")
explain("  - Base64 encode that credential.")
explain("  - Prefix the encoded value with 'Basic '.")
explain("  - Build one GET RESTCONF request for every device in inventory.py.")
explain("  - Each request must include method, url, and headers.")
explain("  - Headers must include Accept and Authorization.")
explain("  - interfaces_requests must reuse the completed cat8k_requests dictionary.")
blank()
explain("RESTCONF path used in this lab:")
header("/restconf/data/ietf-interfaces:interfaces")
blank()
