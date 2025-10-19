#!/usr/bin/env python3
"""
Simple test with minimal data
"""
import requests
from env_config import get_auth_credentials, get_webhook_url

def simple_test():
    # Get configuration from environment variables
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    
    print("Testing with minimal GET request...")
    try:
        response = requests.get(webhook_url, auth=(username, password), timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting with minimal POST request...")
    try:
        response = requests.post(webhook_url, json={"sessionId": "test-session-12345", "chatInput": "Hello!"}, auth=(username, password), timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simple_test()
