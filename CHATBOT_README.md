# n8n AI Chatbot

FastAPI 기반의 실시간 스트리밍 챗봇 애플리케이션입니다.

## 🚀 기능

- **실시간 스트리밍**: n8n AI Agent의 스트리밍 응답을 실시간으로 처리
- **WebSocket 지원**: 실시간 양방향 통신
- **모던 UI**: 반응형 웹 인터페이스
- **세션 관리**: 사용자별 세션 추적
- **REST API**: 프로그래밍 방식 접근 지원

## 📁 파일 구조

```
n8n-agent/
├── chatbot_app.py          # FastAPI 메인 애플리케이션
├── run_chatbot.py          # 실행 스크립트
├── requirements.txt        # Python 의존성
├── templates/
│   └── chat.html          # 웹 인터페이스
├── streaming_webhook.py    # 스트리밍 웹훅 핸들러
├── stream_parser.py        # 스트림 파서
├── env_config.py          # 환경 설정
└── .env                   # 환경 변수 (생성 필요)
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# New format (recommended)
WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-webhook-id
WEBHOOK_USERNAME=your-username
WEBHOOK_PASSWORD=your-password

# Old format (still supported for backward compatibility)
# N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/your-webhook-id
# N8N_USERNAME=your-username
# N8N_PASSWORD=your-password
```

**참고**: `python-dotenv`가 자동으로 `.env` 파일을 로드합니다. 환경 변수 이름은 새로운 형식(`WEBHOOK_*`)을 권장하지만, 기존 형식(`N8N_*`)도 지원합니다.

### 3. 애플리케이션 실행

```bash
python run_chatbot.py
```

또는 직접 실행:

```bash
python chatbot_app.py
```

### 4. 웹 브라우저에서 접속

- **챗봇 인터페이스**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **헬스 체크**: http://localhost:8000/api/health

## 🔧 API 엔드포인트

### WebSocket
- `ws://localhost:8000/ws/{session_id}` - 실시간 채팅

### REST API
- `GET /` - 챗봇 웹 인터페이스
- `POST /api/chat` - 채팅 메시지 전송 (비스트리밍)
- `GET /api/health` - 헬스 체크
- `GET /api/sessions` - 활성 세션 목록

## 💬 사용법

### 웹 인터페이스
1. 브라우저에서 http://localhost:8000 접속
2. 사용자명 입력 (선택사항)
3. 메시지 입력 후 전송
4. 실시간으로 AI 응답 확인

### API 사용 예제

```python
import requests

# REST API로 채팅
response = requests.post("http://localhost:8000/api/chat", json={
    "message": "안녕하세요!",
    "user": "test_user",
    "session_id": "test-session"
})

print(response.json())
```

### WebSocket 사용 예제

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/my-session');

ws.onopen = () => {
    ws.send(JSON.stringify({
        message: "안녕하세요!",
        user: "test_user"
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

## 🎨 UI 기능

- **실시간 스트리밍**: AI 응답이 실시간으로 표시
- **연결 상태 표시**: WebSocket 연결 상태 시각적 표시
- **타이핑 인디케이터**: AI가 응답을 생성 중임을 표시
- **반응형 디자인**: 모바일 및 데스크톱 지원
- **세션 관리**: 사용자별 세션 추적
- **오류 처리**: 연결 오류 및 기타 문제 표시

## 🔍 디버깅

### 로그 확인
애플리케이션 실행 시 콘솔에서 다음 정보를 확인할 수 있습니다:
- WebSocket 연결 상태
- 메시지 처리 로그
- 오류 메시지

### 환경 변수 확인
```bash
python -c "from env_config import *; print('Webhook URL:', get_webhook_url())"
```

## 🚨 문제 해결

### 연결 오류
1. `.env` 파일의 웹훅 URL과 인증 정보 확인
2. n8n 인스턴스가 실행 중인지 확인
3. 방화벽 설정 확인

### WebSocket 연결 실패
1. 브라우저 개발자 도구에서 네트워크 탭 확인
2. 서버 로그에서 오류 메시지 확인
3. 포트 8000이 사용 가능한지 확인

### 스트리밍 응답 없음
1. n8n 워크플로우가 스트리밍을 지원하는지 확인
2. 웹훅 설정이 올바른지 확인
3. 서버 로그에서 요청/응답 확인

## 🔧 커스터마이징

### UI 수정
`templates/chat.html` 파일을 편집하여 UI를 커스터마이징할 수 있습니다.

### API 확장
`chatbot_app.py`에 새로운 엔드포인트를 추가할 수 있습니다.

### 스트리밍 로직 수정
`streaming_webhook.py`와 `stream_parser.py`를 수정하여 스트리밍 처리 로직을 변경할 수 있습니다.

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
