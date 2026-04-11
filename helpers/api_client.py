import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def get(endpoint):
    return requests.get(f"{BASE_URL}{endpoint}")

def post(endpoint, payload):
    return requests.post(f"{BASE_URL}{endpoint}", json=payload)

def put(endpoint, payload):
    return requests.put(f"{BASE_URL}{endpoint}", json=payload)

def delete(endpoint):
    return requests.delete(f"{BASE_URL}{endpoint}")