from pydantic import BaseModel
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session
from fastapi import APIRouter

router = APIRouter()


"""
INSERT INTO users (username, password, full_name, phone, role)
VALUES ('admin', '$2b$12$U321LLHDaTqJZ6HNeIJaA.uhto64DHvPlEr7nvW7dHXp.fyZbaUZO', 'Admin', '+998942305333', 'admin');

"""

import requests

# Base API url, your Gateway API token and a phone number
BASE_URL = 'https://gatewayapi.telegram.org/'
TOKEN = 'AAGOHgAArUykoCJFlDCo_IxydAtlONEe2gs_7nw8JLdQWQ'
PHONE = '+998942305333'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# Function to query the API
def post_request_status(endpoint, json_body):
    url = f"{BASE_URL}{endpoint}"
    resp = requests.post(url, headers=HEADERS, json=json_body, verify=False)
    if resp.ok:
        return resp.json()
    else:
        print(f"Failed to get request status: HTTP {resp.status_code}")
        print(resp.text)
        return None


endpoint = 'sendVerificationMessage'

json_body = {
    'phone_number': PHONE,
    'code_length': 5,
    'ttl': 60,
    'payload': 42355,
}
resp = post_request_status(endpoint, json_body)
print(resp)


