#!/usr/bin/env python3
"""
Chatbot 실행 스크립트
"""
import uvicorn
import sys
import os

def main():
    """챗봇 애플리케이션 실행"""
    print("🚀 n8n AI Chatbot을 시작합니다...")
    print("=" * 50)
    
    # 환경 변수 확인 (dotenv가 자동으로 로드됨)
    from env_config import get_webhook_url, get_auth_credentials
    
    try:
        webhook_url = get_webhook_url()
        username, password = get_auth_credentials()
        print(f"✅ Webhook URL: {webhook_url}")
        print(f"✅ Username: {username}")
        print(f"✅ Password: {'*' * len(password)}")
    except ValueError as e:
        print(f"❌ 환경 변수 설정 오류: {e}")
        print("\n.env 파일을 생성하고 다음 변수들을 설정해주세요:")
        print("   - WEBHOOK_URL (또는 N8N_WEBHOOK_URL)")
        print("   - WEBHOOK_USERNAME (또는 N8N_USERNAME)")
        print("   - WEBHOOK_PASSWORD (또는 N8N_PASSWORD)")
        sys.exit(1)
    
    print("✅ 환경 변수 확인 완료")
    print("🌐 웹 인터페이스: http://localhost:8000")
    print("📡 WebSocket: ws://localhost:8000/ws/{session_id}")
    print("🔧 API 문서: http://localhost:8000/docs")
    print("=" * 50)
    
    # FastAPI 애플리케이션 실행
    uvicorn.run(
        "chatbot_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
