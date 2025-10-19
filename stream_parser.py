#!/usr/bin/env python3
"""
Stream parser for n8n AI Agent streaming responses
"""
import json
import re
from typing import Dict, Any, List, Optional, Iterator
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StreamChunk:
    """Represents a single chunk in the stream"""
    type: str
    content: str
    metadata: Dict[str, Any]
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.metadata.get('timestamp'):
            try:
                # Convert timestamp to datetime if it's a number
                ts = self.metadata['timestamp']
                if isinstance(ts, (int, float)):
                    self.timestamp = datetime.fromtimestamp(ts / 1000)  # Convert from milliseconds
            except (ValueError, TypeError):
                self.timestamp = None


class N8nStreamParser:
    """Parser for n8n AI Agent streaming format"""
    
    def __init__(self):
        self.buffer = ""
        self.current_session = None
        self.chunks: List[StreamChunk] = []
    
    def parse_line(self, line: str) -> Optional[StreamChunk]:
        """
        Parse a single line from the stream
        
        Args:
            line: Raw line from stream
            
        Returns:
            StreamChunk if valid, None otherwise
        """
        line = line.strip()
        if not line:
            return None
        
        try:
            data = json.loads(line)
            
            chunk_type = data.get('type', 'unknown')
            content = data.get('content', '')
            metadata = data.get('metadata', {})
            
            chunk = StreamChunk(
                type=chunk_type,
                content=content,
                metadata=metadata
            )
            
            self.chunks.append(chunk)
            return chunk
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse line: {line}")
            print(f"Error: {e}")
            return None
    
    def parse_stream(self, stream_lines: Iterator[str]) -> Iterator[StreamChunk]:
        """
        Parse a stream of lines
        
        Args:
            stream_lines: Iterator of lines from stream
            
        Yields:
            StreamChunk objects
        """
        for line in stream_lines:
            chunk = self.parse_line(line)
            if chunk:
                yield chunk
    
    def get_complete_content(self) -> str:
        """Get the complete assembled content from all chunks"""
        content_parts = []
        for chunk in self.chunks:
            if chunk.type == 'item' and chunk.content:
                content_parts.append(chunk.content)
        return ''.join(content_parts)
    
    def get_session_info(self) -> Dict[str, Any]:
        """Extract session information from chunks"""
        session_info = {}
        
        for chunk in self.chunks:
            if chunk.type == 'start':
                session_info.update(chunk.metadata)
            elif chunk.type == 'end':
                session_info['end_metadata'] = chunk.metadata
        
        return session_info
    
    def get_stream_stats(self) -> Dict[str, Any]:
        """Get statistics about the stream"""
        stats = {
            'total_chunks': len(self.chunks),
            'content_chunks': len([c for c in self.chunks if c.type == 'item']),
            'start_chunks': len([c for c in self.chunks if c.type == 'start']),
            'end_chunks': len([c for c in self.chunks if c.type == 'end']),
            'total_content_length': len(self.get_complete_content()),
            'has_start': any(c.type == 'start' for c in self.chunks),
            'has_end': any(c.type == 'end' for c in self.chunks)
        }
        
        # Add timing info if available
        timestamps = [c.timestamp for c in self.chunks if c.timestamp]
        if len(timestamps) >= 2:
            stats['duration_seconds'] = (max(timestamps) - min(timestamps)).total_seconds()
        
        return stats
    
    def filter_by_type(self, chunk_type: str) -> List[StreamChunk]:
        """Filter chunks by type"""
        return [c for c in self.chunks if c.type == chunk_type]
    
    def filter_by_node(self, node_id: str) -> List[StreamChunk]:
        """Filter chunks by node ID"""
        return [c for c in self.chunks if c.metadata.get('nodeId') == node_id]
    
    def get_content_by_node(self, node_id: str) -> str:
        """Get complete content from a specific node"""
        content_parts = []
        for chunk in self.chunks:
            if (chunk.type == 'item' and 
                chunk.metadata.get('nodeId') == node_id and 
                chunk.content):
                content_parts.append(chunk.content)
        return ''.join(content_parts)


class StreamingContentProcessor:
    """Process streaming content with various strategies"""
    
    def __init__(self, parser: N8nStreamParser):
        self.parser = parser
        self.processed_content = ""
        self.processing_callbacks = []
    
    def add_callback(self, callback: callable):
        """Add a callback to be called on each content chunk"""
        self.processed_callbacks.append(callback)
    
    def process_realtime(self, chunk: StreamChunk):
        """Process chunk in real-time"""
        if chunk.type == 'item' and chunk.content:
            self.processed_content += chunk.content
            
            # Call all registered callbacks
            for callback in self.processing_callbacks:
                try:
                    callback(chunk, self.processed_content)
                except Exception as e:
                    print(f"⚠️ Callback error: {e}")
    
    def process_batch(self, chunks: List[StreamChunk]):
        """Process multiple chunks in batch"""
        for chunk in chunks:
            self.process_realtime(chunk)
    
    def get_processed_content(self) -> str:
        """Get the final processed content"""
        return self.processed_content


def demo_parser():
    """Demonstrate the stream parser with sample data"""
    
    # Sample streaming data (like what you showed)
    sample_stream = [
        '{"type":"start","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894373809}}',
        '{"type":"item","content":"안녕하세요! ","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894373897}}',
        '{"type":"item","content":"업무를 도","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894373897}}',
        '{"type":"item","content":"와드","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374001}}',
        '{"type":"item","content":"릴 수 ","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374001}}',
        '{"type":"item","content":"있습니다.","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374085}}',
        '{"type":"end","metadata":{"nodeId":"c81832f0-cde4-4fda-8dae-0f7b124923fd","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1760894374325}}'
    ]
    
    print("🧪 Stream Parser Demo")
    print("=" * 50)
    
    # Create parser
    parser = N8nStreamParser()
    
    # Parse the stream
    print("📥 Parsing stream...")
    for line in sample_stream:
        chunk = parser.parse_line(line)
        if chunk:
            print(f"✅ {chunk.type}: {chunk.content}")
    
    # Get results
    print("\n📊 Stream Analysis:")
    print("-" * 30)
    
    complete_content = parser.get_complete_content()
    print(f"Complete content: '{complete_content}'")
    
    stats = parser.get_stream_stats()
    print(f"Statistics: {json.dumps(stats, indent=2)}")
    
    session_info = parser.get_session_info()
    print(f"Session info: {json.dumps(session_info, indent=2, ensure_ascii=False)}")
    
    # Demonstrate filtering
    print("\n🔍 Filtering Examples:")
    print("-" * 30)
    
    content_chunks = parser.filter_by_type('item')
    print(f"Content chunks: {len(content_chunks)}")
    
    node_chunks = parser.filter_by_node('c81832f0-cde4-4fda-8dae-0f7b124923fd')
    print(f"Node chunks: {len(node_chunks)}")


if __name__ == "__main__":
    demo_parser()
