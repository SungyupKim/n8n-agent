#!/usr/bin/env python3
"""
Streaming webhook handler for n8n AI Agent responses
"""
import requests
import json
import sys
import time
from typing import Iterator, Dict, Any, Optional
from env_config import get_auth_credentials, get_webhook_url


class StreamingWebhookHandler:
    """Handle streaming responses from n8n webhook"""
    
    def __init__(self, webhook_url: str, username: str, password: str):
        self.webhook_url = webhook_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "n8n-streaming-client/1.0"
        })
    
    def send_streaming_request(self, data: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """
        Send request and yield streaming responses
        
        Args:
            data: Request payload
            
        Yields:
            Dict containing parsed streaming data
        """
        try:
            print(f"🚀 Sending streaming request to: {self.webhook_url}")
            print(f"📤 Payload: {json.dumps(data, indent=2, ensure_ascii=False)}")
            print("-" * 60)
            
            response = self.session.post(
                self.webhook_url,
                json=data,
                stream=True,
                timeout=60
            )
            
            if response.status_code != 200:
                print(f"❌ Request failed with status: {response.status_code}")
                print(f"Response: {response.text}")
                return
            
            print("✅ Streaming response started")
            print("-" * 60)
            
            # Process streaming response
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        # Parse each line as JSON
                        chunk = json.loads(line)
                        yield chunk
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Failed to parse chunk: {line}")
                        print(f"Error: {e}")
                        continue
                        
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def process_stream(self, data: Dict[str, Any], 
                      on_chunk: Optional[callable] = None,
                      on_complete: Optional[callable] = None) -> str:
        """
        Process streaming response and return complete content
        
        Args:
            data: Request payload
            on_chunk: Optional callback for each chunk
            on_complete: Optional callback when stream completes
            
        Returns:
            Complete assembled content
        """
        content_parts = []
        metadata = {}
        
        for chunk in self.send_streaming_request(data):
            chunk_type = chunk.get('type', 'unknown')
            
            if chunk_type == 'item':
                # Extract content from streaming item
                content = chunk.get('content', '')
                if content:
                    content_parts.append(content)
                    print(f"📝 Content: {content}", end='', flush=True)
                    
                    # Call custom chunk handler if provided
                    if on_chunk:
                        on_chunk(chunk, content)
            
            elif chunk_type == 'start':
                print("🔄 Stream started")
                metadata['start'] = chunk.get('metadata', {})
                
            elif chunk_type == 'end':
                print("\n✅ Stream completed")
                metadata['end'] = chunk.get('metadata', {})
                break
            
            else:
                print(f"📊 {chunk_type}: {chunk}")
        
        # Assemble complete content
        complete_content = ''.join(content_parts)
        
        # Call completion handler if provided
        if on_complete:
            on_complete(complete_content, metadata)
        
        return complete_content


def test_streaming_webhook():
    """Test the streaming webhook functionality"""
    
    # Get configuration
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    
    # Create handler
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
    
    # Define custom handlers
    def on_chunk(chunk, content):
        """Handle each streaming chunk"""
        # You can add custom processing here
        pass
    
    def on_complete(content, metadata):
        """Handle stream completion"""
        print(f"\n📋 Complete Response:")
        print(f"Length: {len(content)} characters")
        print(f"Content: {content}")
        print(f"Metadata: {json.dumps(metadata, indent=2, ensure_ascii=False)}")
    
    # Process the stream
    try:
        complete_response = handler.process_stream(
            test_data,
            on_chunk=on_chunk,
            on_complete=on_complete
        )
        
        print("\n🎉 Streaming test completed successfully!")
        return complete_response
        
    except Exception as e:
        print(f"\n❌ Streaming test failed: {e}")
        return None


def demo_streaming_processing():
    """Demonstrate different streaming processing patterns"""
    
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    handler = StreamingWebhookHandler(webhook_url, username, password)
    
    test_data = {
        "sessionId": "demo-12345",
        "chatInput": "간단한 인사말을 해주세요",
        "user": "demo_user"
    }
    
    print("🎭 Streaming Processing Demo")
    print("=" * 60)
    
    # Pattern 1: Real-time processing
    print("\n1️⃣ Real-time Processing:")
    print("-" * 30)
    
    def realtime_handler(chunk, content):
        # Process each chunk as it arrives
        if content.strip():
            print(f"⚡ Real-time: '{content}'")
    
    handler.process_stream(test_data, on_chunk=realtime_handler)
    
    # Pattern 2: Accumulate and process
    print("\n2️⃣ Accumulate and Process:")
    print("-" * 30)
    
    accumulated = []
    
    def accumulate_handler(chunk, content):
        accumulated.append(content)
        print(f"📦 Accumulated {len(accumulated)} chunks")
    
    def final_process(content, metadata):
        print(f"🔍 Final analysis:")
        print(f"   - Total chunks: {len(accumulated)}")
        print(f"   - Total length: {len(content)}")
        print(f"   - Word count: {len(content.split())}")
    
    handler.process_stream(
        test_data, 
        on_chunk=accumulate_handler,
        on_complete=final_process
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_streaming_processing()
    else:
        test_streaming_webhook()
