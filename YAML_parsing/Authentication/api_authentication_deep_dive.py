# API Authentication — 3-Chapter Deep Dive
# Cisco API Perspective
# Press ENTER to advance through each step

import base64
import json

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
print(f"{BOLD}         API AUTHENTICATION FOR NETWORK AUTOMATION{RESET}")
print(f"{BOLD}         3-Chapter Deep Dive — Cisco API Perspective{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
explain("This deep dive explains how API authentication works before")
explain("you build the Cisco Sandbox challenge tasks.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — Why Authentication Exists
# ═════════════════════════════════════════════════════════════════════════════
chapter(1, "Why API Authentication Exists")

section("1.1 — The basic problem")
explain("An API is an entry point into a system.")
explain("For network automation, that system might be a router, switch, firewall,")
explain("controller, or cloud service.")
blank()
explain("Because APIs can expose real inventory and configuration, the API must")
explain("know who is making the request before it allows access.")
blank()
note("Authentication means: prove who you are.")
note("Authorization means: decide what you are allowed to do.")
blank()

real_world = {
    "you": "Python script or automation tool",
    "api": "Cisco device or controller",
    "credential": "password, token, or OAuth access token",
    "goal": "prove identity before reading or changing data",
}
cmd("real_world")
show_json(real_world)
pause()

section("1.2 — Where authentication appears in HTTP")
explain("Most API authentication is sent inside HTTP headers.")
explain("A header is extra metadata that travels with the request.")
blank()
explain("The API reads the header before deciding whether the request is allowed.")
blank()

raw_request = """\
GET /restconf/data/ietf-interfaces:interfaces HTTP/1.1
Host: sandbox-iosxe-latest-1.cisco.com
Accept: application/yang-data+json
Authorization: Basic ZGV2bmV0dXNlcjpDaXNjbzEyMyE=
"""
cmd("Raw HTTP request")
block(raw_request.rstrip())
blank()
explain("In this example:")
explain("  • GET is the HTTP method.")
explain("  • /restconf/data/... is the API path.")
explain("  • Accept tells the API what response format we want.")
explain("  • Authorization proves who we are.")
pause()

section("1.3 — Why we do not put secrets in the URL")
explain("A URL is often logged by browsers, proxies, servers, and tools.")
explain("Putting passwords or tokens in the URL is risky.")
blank()
warn("Bad idea:")
block("https://api.example.com/devices?password=Cisco123!")
blank()
out("Better idea:")
block("""GET /devices HTTP/1.1
Authorization: Basic <encoded-credential>""")
blank()
explain("Headers are still sensitive, but they are the correct place to send")
explain("authentication data in normal API workflows.")
pause()

section("1.4 — Keep secrets safe")
explain("Training labs often show sample credentials so students can practice.")
explain("Production code should treat credentials as secrets.")
blank()
safe_practices = [
    "do not commit real passwords or tokens to Git",
    "use environment variables for credentials",
    "use HTTPS",
    "rotate credentials if they are exposed",
    "give tokens only the permissions they need",
]
cmd("safe_practices")
show_json(safe_practices)
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Basic Auth and Token Auth
# ═════════════════════════════════════════════════════════════════════════════
chapter(2, "Basic Auth and Token Auth")

section("2.1 — Basic Auth in plain English")
explain("Basic authentication uses a username and password.")
explain("The client combines them in this format:")
blank()
block("username:password")
blank()
explain("Then the client Base64-encodes that text.")
explain("Base64 is not encryption. It is just an encoding format.")
blank()
note("Important: Basic Auth must be sent over HTTPS.")
pause()

section("2.2 — Build a Basic Auth header step by step")
username = "devnetuser"
password = "Cisco123!"
cmd("username = 'devnetuser'")
cmd("password = 'Cisco123!'")
blank()

credential = f"{username}:{password}"
cmd("credential = f'{username}:{password}'")
cmd("print(credential)")
out(credential)
blank()
explain("The credential string is the username, a colon, and the password.")
pause()

encoded = base64.b64encode(credential.encode()).decode()
cmd("encoded = base64.b64encode(credential.encode()).decode()")
cmd("print(encoded)")
out(encoded)
blank()
explain("Now the credential is Base64 encoded.")
explain("Again, this is not secret by itself; HTTPS protects it in transit.")
pause()

basic_header = "Basic " + encoded
cmd("basic_auth_header = 'Basic ' + encoded")
cmd("print(basic_auth_header)")
out(basic_header)
blank()
explain("The final Authorization header value starts with the word Basic,")
explain("then a space, then the encoded credential.")
pause()

section("2.3 — Cisco IOS XE Sandbox Basic Auth example")
explain("Cisco IOS XE RESTCONF sandbox examples commonly use Basic Auth.")
blank()
explain("The Python request needs:")
explain("  • URL")
explain("  • Accept header")
explain("  • Authorization header")
blank()

iosxe_request = {
    "method": "GET",
    "url": "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/ietf-interfaces:interfaces",
    "headers": {
        "Accept": "application/yang-data+json",
        "Authorization": basic_header,
    },
}
cmd("iosxe_request")
show_json(iosxe_request)
blank()
explain("This dictionary is not sending the request yet.")
explain("It is just the structure your code could pass into requests.get().")
pause()

section("2.4 — Token Auth in plain English")
explain("Token authentication uses a token instead of sending a username and")
explain("password on every API call.")
blank()
explain("Common flow:")
explain("  1. Authenticate once.")
explain("  2. Receive a token.")
explain("  3. Send that token in later API requests.")
blank()
note("A token is like a temporary badge for API access.")
pause()

section("2.5 — Bearer token style")
token = "abc123sandbox-token"
cmd("token = 'abc123sandbox-token'")
bearer = "Bearer " + token
cmd("authorization = 'Bearer ' + token")
cmd("print(authorization)")
out(bearer)
blank()
explain("Some APIs expect the token in the Authorization header like this:")
block("Authorization: Bearer abc123sandbox-token")
pause()

section("2.6 — Cisco Catalyst Center X-Auth-Token style")
explain("Cisco Catalyst Center commonly uses a slightly different pattern.")
explain("After you request a token, later API calls send that token as X-Auth-Token.")
blank()

catalyst_flow = {
    "step_1": {
        "method": "POST",
        "url": "https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token",
        "purpose": "get a token using username and password",
    },
    "step_2": {
        "method": "GET",
        "url": "https://sandboxdnac.cisco.com/dna/intent/api/v1/network-device",
        "header": "X-Auth-Token: <token>",
        "purpose": "use token to read devices",
    },
}
cmd("catalyst_flow")
show_json(catalyst_flow)
blank()
explain("This is still token-based authentication.")
explain("The difference is the header name: X-Auth-Token instead of Authorization.")
pause()

# ═════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — OAuth Fundamentals
# ═════════════════════════════════════════════════════════════════════════════
chapter(3, "OAuth Fundamentals")

section("3.1 — Why OAuth exists")
explain("OAuth is used when one application needs delegated access to another")
explain("system without sharing a user's password with that application.")
blank()
explain("Think of OAuth as a controlled token-issuing process.")
blank()
explain("Instead of giving the app your password, the app receives an access token.")
explain("That token can have limited permissions and an expiration time.")
pause()

section("3.2 — OAuth roles")
oauth_roles = {
    "resource_owner": "the user or system that owns the data",
    "client": "the application requesting access",
    "authorization_server": "the system that issues tokens",
    "resource_server": "the API that accepts tokens",
    "access_token": "the credential sent to the API",
    "scope": "what the token is allowed to do",
}
cmd("oauth_roles")
show_json(oauth_roles)
blank()
explain("For beginner API automation, the most important idea is:")
note("OAuth usually gives your script a token, and your script sends that token to the API.")
pause()

section("3.3 — OAuth token response")
token_response = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "network-device:read",
}
cmd("token_response")
show_json(token_response)
blank()
cmd("auth_header = token_response['token_type'] + ' ' + token_response['access_token']")
auth_header = token_response["token_type"] + " " + token_response["access_token"]
cmd("print(auth_header[:40])")
out(auth_header[:40])
blank()
explain("The token_type tells you how to send the token.")
explain("Here it says Bearer, so the header starts with Authorization: Bearer.")
pause()

section("3.4 — Simple comparison")
comparison = {
    "Basic Auth": {
        "what_you_send": "Base64 username:password",
        "common_header": "Authorization",
        "beginner_takeaway": "simple, but protect with HTTPS",
    },
    "Token Auth": {
        "what_you_send": "token value",
        "common_header": "Authorization or X-Auth-Token",
        "beginner_takeaway": "send token after login or token generation",
    },
    "OAuth": {
        "what_you_send": "access token issued by authorization server",
        "common_header": "Authorization: Bearer <token>",
        "beginner_takeaway": "delegated, scoped, often expiring access",
    },
}
cmd("comparison")
show_json(comparison)
pause()

bar = "█" * 62
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
print(f"{BOLD}   SUMMARY — API AUTHENTICATION{RESET}")
print()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}{bar}{RESET}")
blank()
print(f"  {BOLD}Ch 1{RESET}   Why APIs need authentication and where headers fit")
print(f"  {BOLD}Ch 2{RESET}   Basic Auth, token auth, and Cisco Sandbox examples")
print(f"  {BOLD}Ch 3{RESET}   OAuth fundamentals and how access tokens work")
blank()
print(f"  {WHITE}The main skill is knowing what credential the API expects,")
print(f"  which header carries it, and how your Python code builds that")
print(f"  header safely before making the request.{RESET}")
blank()
print(f"{BOLD}{bar}{RESET}")
print(f"{BOLD}   Tutorial complete.{RESET}")
print(f"{BOLD}{bar}{RESET}")
print()
