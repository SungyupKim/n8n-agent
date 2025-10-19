#!/usr/bin/env python3
"""
Test script for n8n chat webhook with streaming support
"""
import requests
import json
import sys
import argparse
from env_config import get_auth_credentials, get_webhook_url
from streaming_webhook import StreamingWebhookHandler
from stream_parser import N8nStreamParser

def test_webhook():
    # Get configuration from environment variables
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    
    # Test data - you can modify this based on what your webhook expects
    test_data = {
        "sessionId": "test-session-12345",
        "chatInput": "test데이터베이스의 테이블 목록 알려줘",
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

def test_streaming_webhook():
    """Test streaming webhook functionality"""
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    
    # Create streaming handler
    handler = StreamingWebhookHandler(webhook_url, username, password)
    
    # Test data
    test_data = {
        "sessionId": "streaming-test-12345",
        "chatInput": "데이터베이스의 테이블 목록을 알려주세요",
        "message": "Hello from streaming test!",
        "user": "streaming_test_user",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    print("🧪 Testing Streaming Webhook")
    print("=" * 60)
    
    # Process the stream
    try:
        complete_response = handler.process_stream(test_data)
        print(f"\n🎉 Streaming test completed!")
        print(f"📝 Complete response: {complete_response}")
        return complete_response
    except Exception as e:
        print(f"\n❌ Streaming test failed: {e}")
        return None


def test_with_parser():
    """Test webhook with stream parser"""
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    
    handler = StreamingWebhookHandler(webhook_url, username, password)
    parser = N8nStreamParser()
    
    test_data = {
        "sessionId": "parser-test-12345",
        "chatInput": "간단한 인사말을 해주세요",
        "user": "parser_test_user"
    }
    
    print("🔍 Testing with Stream Parser")
    print("=" * 60)
    
    def on_chunk(chunk, content):
        # Parse each chunk
        parsed_chunk = parser.parse_line(json.dumps(chunk))
        if parsed_chunk:
            print(f"📦 Parsed: {parsed_chunk.type} - {parsed_chunk.content}")
    
    def on_complete(content, metadata):
        print(f"\n📊 Stream Analysis:")
        stats = parser.get_stream_stats()
        print(f"   - Total chunks: {stats['total_chunks']}")
        print(f"   - Content chunks: {stats['content_chunks']}")
        print(f"   - Complete content: '{parser.get_complete_content()}'")
    
    try:
        handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
        print("\n✅ Parser test completed!")
    except Exception as e:
        print(f"\n❌ Parser test failed: {e}")


def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Test n8n webhook with streaming support')
    parser.add_argument('--mode', choices=['basic', 'streaming', 'parser'], 
                       default='streaming', help='Test mode to run')
    parser.add_argument('--input', type=str, 
                       help='Custom input message for testing')
    
    args = parser.parse_args()
    
    if args.mode == 'basic':
        test_webhook()
    elif args.mode == 'streaming':
        test_streaming_webhook()
    elif args.mode == 'parser':
        test_with_parser()


if __name__ == "__main__":
    main()
