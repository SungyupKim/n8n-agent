#!/usr/bin/env python3
"""
FastAPI Chatbot Application with n8n streaming support
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from streaming_webhook import StreamingWebhookHandler
from stream_parser import N8nStreamParser
from env_config import get_auth_credentials, get_webhook_url


# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: str = None
    user: str = "anonymous"


class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: str
    status: str


# FastAPI app
app = FastAPI(title="n8n Chatbot", description="Streaming chatbot with n8n AI Agent")

# Templates
templates = Jinja2Templates(directory="templates")

# Global variables
active_connections: Dict[str, WebSocket] = {}
webhook_handler = None
parser = N8nStreamParser()


@app.on_event("startup")
async def startup_event():
    """Initialize webhook handler on startup"""
    global webhook_handler
    webhook_url = get_webhook_url()
    username, password = get_auth_credentials()
    webhook_handler = StreamingWebhookHandler(webhook_url, username, password)
    print("🚀 Chatbot application started!")


@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    """Serve the main chat page"""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process the message
            await process_chat_message(websocket, session_id, message_data)
            
    except WebSocketDisconnect:
        if session_id in active_connections:
            del active_connections[session_id]
        print(f"Client {session_id} disconnected")


async def process_chat_message(websocket: WebSocket, session_id: str, message_data: Dict[str, Any]):
    """Process incoming chat message and stream response"""
    user_message = message_data.get("message", "")
    user_name = message_data.get("user", "anonymous")
    
    print(f"📨 Received message from {user_name}: {user_message}")
    
    # Send acknowledgment
    await websocket.send_text(json.dumps({
        "type": "ack",
        "message": "Processing your message...",
        "timestamp": datetime.now().isoformat()
    }))
    
    # Prepare data for webhook
    test_data = {
        "sessionId": session_id,
        "chatInput": user_message,
        "message": user_message,
        "user": user_name,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # Process streaming response
        complete_response = await process_streaming_response(websocket, test_data)
        
        # Send final completion message if not already sent
        if complete_response:
            await websocket.send_text(json.dumps({
                "type": "complete",
                "message": complete_response,
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id
            }))
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Error processing message: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }))


async def process_streaming_response(websocket: WebSocket, test_data: Dict[str, Any]) -> str:
    """Process streaming response from n8n webhook"""
    import queue
    import threading
    
    # Queue to store chunks for async processing
    chunk_queue = queue.Queue()
    content_parts = []
    
    def on_chunk(chunk, content):
        """Handle each streaming chunk - add to queue for async processing"""
        if content:
            content_parts.append(content)
            chunk_queue.put({
                "type": "chunk",
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
    
    def on_complete(content, metadata):
        """Handle stream completion"""
        print(f"✅ Stream completed: {content}")
        chunk_queue.put({
            "type": "complete",
            "message": content,
            "timestamp": datetime.now().isoformat()
        })
    
    # Start streaming in a separate thread
    def stream_worker():
        webhook_handler.process_stream(test_data, on_chunk, on_complete)
    
    stream_thread = threading.Thread(target=stream_worker)
    stream_thread.start()
    
    # Process chunks as they arrive
    complete_response = ""
    while stream_thread.is_alive() or not chunk_queue.empty():
        try:
            # Wait for chunks with timeout
            chunk_data = chunk_queue.get(timeout=0.1)
            
            if chunk_data["type"] == "chunk":
                await websocket.send_text(json.dumps(chunk_data))
            elif chunk_data["type"] == "complete":
                complete_response = chunk_data["message"]
                break
                
        except queue.Empty:
            # No chunks available, continue waiting
            await asyncio.sleep(0.01)
            continue
    
    # Wait for thread to complete
    stream_thread.join()
    
    return complete_response


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """REST API endpoint for chat (non-streaming)"""
    session_id = chat_message.session_id or str(uuid.uuid4())
    
    test_data = {
        "sessionId": session_id,
        "chatInput": chat_message.message,
        "message": chat_message.message,
        "user": chat_message.user,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # Process streaming response
        complete_response = webhook_handler.process_stream(test_data)
        
        return ChatResponse(
            message=complete_response,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            status="success"
        )
        
    except Exception as e:
        return ChatResponse(
            message=f"Error: {str(e)}",
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            status="error"
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/sessions")
async def get_active_sessions():
    """Get list of active sessions"""
    return {
        "active_sessions": list(active_connections.keys()),
        "count": len(active_connections)
    }


if __name__ == "__main__":
    uvicorn.run(
        "chatbot_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
