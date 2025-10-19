#!/usr/bin/env python3
"""
Test script for n8n chat webhook with different HTTP methods
"""
import requests
import json

def test_webhook_methods():
    webhook_url = "https://sungyup.app.n8n.cloud/webhook/ddf4ea5b-94fc-4fbf-b856-95d39a04eb59/chat"
    
    # Basic Auth credentials
    username = "sungyupv@gmail.com"
    password = "159753/*sk"
    
    test_data = {
        "sessionId": "test-session-12345",
        "chatInput": "Hello from test script!",
        "message": "Hello from test script!",
        "user": "test_user"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "n8n-webhook-tester/1.0"
    }
    
    methods_to_test = [
        ("GET", None),
        ("POST", test_data),
        ("PUT", test_data),
        ("PATCH", test_data)
    ]
    
    for method, data in methods_to_test:
        print(f"\n{'='*60}")
        print(f"Testing {method} method")
        print(f"{'='*60}")
        
        try:
            if method == "GET":
                response = requests.get(webhook_url, headers=headers, auth=(username, password), timeout=10)
            elif method == "POST":
                response = requests.post(webhook_url, json=data, headers=headers, auth=(username, password), timeout=10)
            elif method == "PUT":
                response = requests.put(webhook_url, json=data, headers=headers, auth=(username, password), timeout=10)
            elif method == "PATCH":
                response = requests.patch(webhook_url, json=data, headers=headers, auth=(username, password), timeout=10)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.text:
                try:
                    response_json = response.json()
                    print(f"Response Body (JSON): {json.dumps(response_json, indent=2)}")
                except json.JSONDecodeError:
                    print(f"Response Body (Text): {response.text}")
            else:
                print("Response Body: (empty)")
                
            if response.status_code == 200:
                print(f"✅ {method} method successful!")
            elif response.status_code == 404:
                print(f"❌ {method} method - 404 Not Found")
            elif response.status_code == 405:
                print(f"❌ {method} method - 405 Method Not Allowed")
            else:
                print(f"⚠️  {method} method - Status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"❌ {method} method - Request timed out")
        except requests.exceptions.RequestException as e:
            print(f"❌ {method} method - Request failed: {e}")

if __name__ == "__main__":
    test_webhook_methods()
