#!/usr/bin/env python3
"""
Test script for n8n chat webhook
"""
import requests
import json
import sys
import base64

def test_webhook():
    webhook_url = "https://sungyup.app.n8n.cloud/webhook/ddf4ea5b-94fc-4fbf-b856-95d39a04eb59/chat"
    
    # Basic Auth credentials
    username = "sungyupv@gmail.com"
    password = "159753/*sk"
    
    # Test data - you can modify this based on what your webhook expects
    test_data = {
        "sessionId": "test-session-12345",
        "chatInput": "Hello from test script!",
        "message": "Hello from test script!",
        "user": "test_user",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "n8n-webhook-tester/1.0"
    }
    
    try:
        print(f"Testing webhook: {webhook_url}")
        print(f"Sending data: {json.dumps(test_data, indent=2)}")
        print("-" * 50)
        
        # Make the request with basic auth
        response = requests.post(
            webhook_url,
            json=test_data,
            headers=headers,
            auth=(username, password),
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("-" * 50)
        
        # Try to parse JSON response
        try:
            response_json = response.json()
            print(f"Response Body (JSON): {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Body (Text): {response.text}")
        
        # Check if request was successful
        if response.status_code == 200:
            print("\n✅ Webhook test successful!")
        else:
            print(f"\n❌ Webhook test failed with status code: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check your internet connection")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_webhook()
