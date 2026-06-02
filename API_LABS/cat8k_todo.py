
import os
import base64

from inventory import DEVICES, ENDPOINTS

DEVICE_USERNAME = os.environ.get("DEVICE_USERNAME")
DEVICE_PASSWORD = os.environ.get("DEVICE_PASSWORD")

# ==========================================================
# TODO 1 - Build username_password
# Combine username and password as username:password
# ==========================================================

cat8k_username_password = None 

# ==========================================================
# TODO 2 - Build encoded_credentials
# Base64 encode cat8k_username_password
# ==========================================================

cat8k_encoded_credentials = None

# ==========================================================
# TODO 3 - Build authorization_header
# Format: Basic <encoded_credentials>
# ==========================================================

cat8k_authorization_header = None

# ==========================================================
# TODO 4 - Build cat8k_requests
# Build one RESTCONF GET request for every CAT8K in DEVICES
# ==========================================================

cat8k_requests = {}

# Your code here

# ==========================================================
# TODO 5 - Build interfaces_requests
# Reuse the completed cat8k_requests dictionary
# ==========================================================

interfaces_requests = None



