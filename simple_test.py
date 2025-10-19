#!/usr/bin/env python3
"""
Simple test with minimal data
"""
import requests

def simple_test():
    webhook_url = "https://sungyup.app.n8n.cloud/webhook/ddf4ea5b-94fc-4fbf-b856-95d39a04eb59/chat"
    
    # Basic Auth credentials
    username = "sungyupv@gmail.com"
    password = "159753/*sk"
    
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
