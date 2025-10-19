#!/usr/bin/env python3
"""
Examples of different streaming processing patterns for n8n webhooks
"""
import json
import time
import asyncio
from typing import List, Dict, Any, Callable
from streaming_webhook import StreamingWebhookHandler
from stream_parser import N8nStreamParser, StreamingContentProcessor
from env_config import get_auth_credentials, get_webhook_url


class StreamingExamples:
    """Collection of streaming processing examples"""
    
    def __init__(self):
        webhook_url = get_webhook_url()
        username, password = get_auth_credentials()
        self.handler = StreamingWebhookHandler(webhook_url, username, password)
    
    def example_1_basic_streaming(self):
        """Example 1: Basic streaming with real-time output"""
        print("📝 Example 1: Basic Streaming")
        print("=" * 50)
        
        test_data = {
            "sessionId": "example-1",
            "chatInput": "안녕하세요! 간단한 인사말을 해주세요.",
            "user": "example_user"
        }
        
        def on_chunk(chunk, content):
            print(f"📦 Chunk: {content}", end='', flush=True)
        
        def on_complete(content, metadata):
            print(f"\n✅ Complete: {content}")
        
        self.handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
    
    def example_2_accumulated_processing(self):
        """Example 2: Accumulate content and process in batches"""
        print("\n📚 Example 2: Accumulated Processing")
        print("=" * 50)
        
        test_data = {
            "sessionId": "example-2",
            "chatInput": "데이터베이스에 대해 설명해주세요.",
            "user": "example_user"
        }
        
        accumulated_chunks = []
        
        def on_chunk(chunk, content):
            accumulated_chunks.append({
                'content': chunk.get('content', ''),
                'timestamp': chunk.get('metadata', {}).get('timestamp'),
                'node_id': chunk.get('metadata', {}).get('nodeId')
            })
            print(f"📊 Accumulated {len(accumulated_chunks)} chunks")
        
        def on_complete(content, metadata):
            print(f"\n🔍 Final Analysis:")
            print(f"   - Total chunks: {len(accumulated_chunks)}")
            print(f"   - Content length: {len(content)}")
            print(f"   - Word count: {len(content.split())}")
            
            # Process accumulated data
            for i, chunk in enumerate(accumulated_chunks):
                print(f"   - Chunk {i+1}: {chunk['content'][:20]}...")
        
        self.handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
    
    def example_3_parser_integration(self):
        """Example 3: Using stream parser for advanced processing"""
        print("\n🔍 Example 3: Parser Integration")
        print("=" * 50)
        
        test_data = {
            "sessionId": "example-3",
            "chatInput": "프로그래밍 언어에 대해 알려주세요.",
            "user": "example_user"
        }
        
        parser = N8nStreamParser()
        processor = StreamingContentProcessor(parser)
        
        def on_chunk(chunk, content):
            # Parse and process each chunk
            parsed_chunk = parser.parse_line(json.dumps(chunk))
            if parsed_chunk:
                processor.process_realtime(parsed_chunk)
                print(f"🔧 Processed: {parsed_chunk.content}", end='', flush=True)
        
        def on_complete(content, metadata):
            print(f"\n📊 Parser Statistics:")
            stats = parser.get_stream_stats()
            for key, value in stats.items():
                print(f"   - {key}: {value}")
            
            print(f"\n📝 Final processed content: {processor.get_processed_content()}")
        
        self.handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
    
    def example_4_content_filtering(self):
        """Example 4: Filter and process specific content types"""
        print("\n🎯 Example 4: Content Filtering")
        print("=" * 50)
        
        test_data = {
            "sessionId": "example-4",
            "chatInput": "여러 가지 주제에 대해 이야기해주세요.",
            "user": "example_user"
        }
        
        important_content = []
        
        def on_chunk(chunk, content):
            chunk_content = chunk.get('content', '')
            
            # Filter for important content (example: content with specific keywords)
            if any(keyword in chunk_content.lower() for keyword in ['데이터', '프로그래밍', '기술']):
                important_content.append(chunk_content)
                print(f"⭐ Important: {chunk_content}")
            else:
                print(f"📝 Regular: {chunk_content}", end='', flush=True)
        
        def on_complete(content, metadata):
            print(f"\n🎯 Important content found: {len(important_content)} chunks")
            for i, imp_content in enumerate(important_content):
                print(f"   {i+1}. {imp_content}")
        
        self.handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
    
    def example_5_error_handling(self):
        """Example 5: Robust error handling and recovery"""
        print("\n🛡️ Example 5: Error Handling")
        print("=" * 50)
        
        test_data = {
            "sessionId": "example-5",
            "chatInput": "에러 처리를 테스트해보세요.",
            "user": "example_user"
        }
        
        error_count = 0
        processed_chunks = 0
        
        def on_chunk(chunk, content):
            nonlocal error_count, processed_chunks
            
            try:
                # Simulate potential processing errors
                if processed_chunks % 5 == 0:  # Simulate error every 5th chunk
                    raise ValueError("Simulated processing error")
                
                print(f"✅ Processed: {content}", end='', flush=True)
                processed_chunks += 1
                
            except Exception as e:
                error_count += 1
                print(f"⚠️ Error processing chunk: {e}")
                # Continue processing despite error
        
        def on_complete(content, metadata):
            print(f"\n📊 Processing Summary:")
            print(f"   - Successfully processed: {processed_chunks} chunks")
            print(f"   - Errors encountered: {error_count}")
            print(f"   - Success rate: {(processed_chunks/(processed_chunks+error_count)*100):.1f}%")
        
        self.handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
    
    def example_6_custom_callbacks(self):
        """Example 6: Custom callback system"""
        print("\n🔧 Example 6: Custom Callbacks")
        print("=" * 50)
        
        test_data = {
            "sessionId": "example-6",
            "chatInput": "콜백 시스템을 테스트해보세요.",
            "user": "example_user"
        }
        
        # Custom callback functions
        def log_callback(chunk, content):
            print(f"📝 LOG: {content}", end='', flush=True)
        
        def analytics_callback(chunk, content):
            # Simulate analytics processing
            if len(content) > 10:
                print(f"📊 ANALYTICS: Long content detected ({len(content)} chars)")
        
        def security_callback(chunk, content):
            # Simulate security check
            if any(word in content.lower() for word in ['password', 'secret', 'key']):
                print(f"🔒 SECURITY: Sensitive content detected!")
        
        # Combine callbacks
        def combined_callback(chunk, content):
            log_callback(chunk, content)
            analytics_callback(chunk, content)
            security_callback(chunk, content)
        
        def on_complete(content, metadata):
            print(f"\n✅ All callbacks executed successfully")
        
        self.handler.process_stream(test_data, on_chunk=combined_callback, on_complete=on_complete)
    
    def run_all_examples(self):
        """Run all streaming examples"""
        print("🚀 Running All Streaming Examples")
        print("=" * 60)
        
        examples = [
            self.example_1_basic_streaming,
            self.example_2_accumulated_processing,
            self.example_3_parser_integration,
            self.example_4_content_filtering,
            self.example_5_error_handling,
            self.example_6_custom_callbacks
        ]
        
        for i, example in enumerate(examples, 1):
            try:
                example()
                print(f"\n✅ Example {i} completed successfully")
            except Exception as e:
                print(f"\n❌ Example {i} failed: {e}")
            
            if i < len(examples):
                print("\n" + "="*60)
                time.sleep(1)  # Brief pause between examples


def demo_with_sample_data():
    """Demo using the sample streaming data you provided"""
    print("🎭 Demo with Sample Data")
    print("=" * 50)
    
    # Your sample streaming data
    sample_data = [
        '{"type":"start","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894373809}}',
        '{"type":"item","content":"안녕하세요! ","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894373897}}',
        '{"type":"item","content":"업무를 도","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894373897}}',
        '{"type":"item","content":"와드","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374001}}',
        '{"type":"item","content":"릴 수 ","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374001}}',
        '{"type":"item","content":"있습니다.","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374085}}',
        '{"type":"end","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374325}}'
    ]
    
    parser = N8nStreamParser()
    
    print("📥 Processing sample stream...")
    for line in sample_data:
        chunk = parser.parse_line(line)
        if chunk:
            if chunk.type == 'item':
                print(f"📝 {chunk.content}", end='', flush=True)
            elif chunk.type == 'start':
                print("🔄 Stream started")
            elif chunk.type == 'end':
                print("\n✅ Stream ended")
    
    print(f"\n📊 Analysis:")
    stats = parser.get_stream_stats()
    print(f"   - Complete content: '{parser.get_complete_content()}'")
    print(f"   - Total chunks: {stats['total_chunks']}")
    print(f"   - Duration: {stats.get('duration_seconds', 'N/A')} seconds")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_with_sample_data()
    else:
        examples = StreamingExamples()
        examples.run_all_examples()
