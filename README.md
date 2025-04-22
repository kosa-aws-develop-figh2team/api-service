# 💬 api-service

> **질문 등록 및 응답 생성 API 서비스**  
> 유저의 질문을 수신하고 내부 RAG 시스템과 연동하여 응답을 생성하는 FastAPI 기반 API 서버입니다.

## ✅ 개요
이 서비스는 RAG 기반 시스템의 API Gateway 또는 BFF 역할을 수행하며, 단일 통합 API를 제공합니다:

- **Endpoint**: `POST /chat/question`  
- **기능 순서**:  
  1. 질문 임베딩 생성  
  2. 관련 문서 검색  
  3. 응답 생성  
- **Request 예시**:
  ```json
  {
    "question_text": "질문 내용",
    "session_id": "세션ID"
  }
  ```
- **Response 예시**:
  ```json
  {
    "message_id": "msg-xxxx",
    "response_text": "응답 내용",
    "session_id": "세션ID"
  }
  ```

## ⏳ 처리 흐름 요약
```text
[사용자 질문 수신]
         ↓
[RAG 서비스에 질문 임베딩 요청]
         ↓
[임베딩 결과 기반 유사 문서 검색 요청]
         ↓
[질문 + 문서 기반 응답 생성 요청]
         ↓
[message_id와 함께 응답 반환]
```

## 🧩 API 명세

### 🔹 질문 등록 + 응답 생성 API
- **Endpoint**: `POST /chat/question`
- **Request 예시**:
  ```json
  {
    "question_text": "서울시 청년 정책 알려줘",
    "session_id": "abc123"
  }
  ```
- **Response 예시**:
  ```json
  {
    "message_id": "msg-abc123-001",
    "response_text": "서울시 청년 정책은 청년수당, 역세권 청년주택 등이 있습니다."
  }
  ```
- **Status Codes**:
  - `200 OK`: 응답 생성 성공  
  - `400 Bad Request`: 입력 오류  
  - `500 Internal Server Error`: 내부 처리 오류  

## 🚀 로컬 실행 방법
```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행
uvicorn main:app --reload --port 5200
```

## 🐳 Docker로 빌드 & 실행
```bash
# 1. 이미지 빌드
docker build -t api-service .

# 2. 컨테이너 실행
docker run --env-file .env -p 5200:5200 api-service
```

## 📦 .env 예시
```env
EMBED_API_HOST=embed-service
EMBED_API_PORT=5001
RAG_API_HOST=rag-service
RAG_API_PORT=5201
```

## ⚙️ CI/CD (ECR 배포 - CD 구현 전)
GitHub Actions를 통해 `main` 브랜치에 push 시 AWS ECR로 자동 배포됩니다:
- **ECR Repository**: `api-service`
- **Tag**: Git SHA 또는 `latest`  
- **참고**: `.github/workflows/deploy.yml`

## 🛠️ TODO
- 멀티턴 챗봇 기능 확장 (세션 기반 맥락 유지)  

## 📁 디렉토리 구조
(작성 중)