# n8n Streaming Webhook Guide

이 가이드는 n8n AI Agent의 스트리밍 응답을 처리하는 방법을 설명합니다.

## 파일 구조

- `streaming_webhook.py` - 스트리밍 웹훅 핸들러
- `stream_parser.py` - n8n 스트림 파서
- `test_webhook.py` - 업데이트된 테스트 스크립트 (스트리밍 지원)
- `streaming_examples.py` - 다양한 스트리밍 처리 예제

## 기본 사용법

### 1. 기본 스트리밍 테스트

```bash
python test_webhook.py --mode streaming
```

### 2. 파서와 함께 테스트

```bash
python test_webhook.py --mode parser
```

### 3. 모든 예제 실행

```bash
python streaming_examples.py
```

### 4. 샘플 데이터로 데모

```bash
python streaming_examples.py demo
```

## 코드 예제

### 기본 스트리밍 처리

```python
from streaming_webhook import StreamingWebhookHandler
from env_config import get_auth_credentials, get_webhook_url

# 설정 가져오기
webhook_url = get_webhook_url()
username, password = get_auth_credentials()

# 핸들러 생성
handler = StreamingWebhookHandler(webhook_url, username, password)

# 테스트 데이터
test_data = {
    "sessionId": "test-123",
    "chatInput": "안녕하세요!",
    "user": "test_user"
}

# 스트림 처리
def on_chunk(chunk, content):
    print(f"📝 {content}", end='', flush=True)

def on_complete(content, metadata):
    print(f"\n✅ 완료: {content}")

handler.process_stream(test_data, on_chunk=on_chunk, on_complete=on_complete)
```

### 파서 사용

```python
from stream_parser import N8nStreamParser

parser = N8nStreamParser()

# 스트림 라인 파싱
for line in stream_lines:
    chunk = parser.parse_line(line)
    if chunk and chunk.type == 'item':
        print(f"내용: {chunk.content}")

# 통계 정보
stats = parser.get_stream_stats()
print(f"총 청크: {stats['total_chunks']}")
print(f"완전한 내용: {parser.get_complete_content()}")
```

## 스트리밍 데이터 형식

n8n AI Agent는 다음과 같은 JSON 형식으로 스트리밍합니다:

```json
{"type":"start","metadata":{"nodeId":"...","nodeName":"AI Agent",...}}
{"type":"item","content":"안녕하세요! ","metadata":{"nodeId":"...",...}}
{"type":"item","content":"업무를 도","metadata":{"nodeId":"...",...}}
{"type":"end","metadata":{"nodeId":"...",...}}
```

## 주요 기능

### StreamingWebhookHandler
- 실시간 스트리밍 응답 처리
- 자동 재연결 및 오류 처리
- 커스텀 콜백 지원

### N8nStreamParser
- n8n 스트림 형식 파싱
- 청크 필터링 및 분석
- 통계 정보 제공

### 다양한 처리 패턴
1. **실시간 처리** - 각 청크를 즉시 처리
2. **누적 처리** - 내용을 모아서 배치 처리
3. **필터링** - 특정 조건의 내용만 처리
4. **오류 처리** - 견고한 오류 복구
5. **커스텀 콜백** - 사용자 정의 처리 로직

## 환경 설정

`env_config.py` 파일에서 다음 환경 변수를 설정하세요:

- `WEBHOOK_URL` - n8n 웹훅 URL
- `WEBHOOK_USERNAME` - 인증 사용자명
- `WEBHOOK_PASSWORD` - 인증 비밀번호

## 문제 해결

### 연결 오류
- 웹훅 URL과 인증 정보 확인
- 네트워크 연결 상태 확인

### 파싱 오류
- JSON 형식 확인
- 스트림 데이터 무결성 확인

### 성능 문제
- 청크 처리 로직 최적화
- 메모리 사용량 모니터링
