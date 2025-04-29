from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging
import requests
import uuid
import os
import dotenv

dotenv.load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

# 모델 정의
class QuestionRequest(BaseModel):
    question_text: str
    session_id: str

class ChatResponse(BaseModel):
    message_id: str
    response_text: str
    service_ids: list

# 환경 변수에서 API 주소 불러오기
RAG_API_HOST = os.getenv("RAG_API_HOST", "rag-service.backend.svc.cluster.local")
RAG_API_PORT = os.getenv("RAG_API_PORT", "5201")  # rag-service가 포트 5201에서 실행 중

# 질문 등록 + 응답 생성 통합 API
@app.post("/chat/question", response_model=ChatResponse)
def submit_and_respond(request: QuestionRequest):
    try:
        logger.info(f"질문 수신 및 응답 생성 시작: session_id={request.session_id}, text='{request.question_text}'")

        # ✅ message_id 생성
        message_id = f"msg-{uuid.uuid4()}"

        generate_url = f"http://{RAG_API_HOST}:{RAG_API_PORT}/rag/answer"
        generate_response = requests.post(generate_url, json={
            "question_text": request.question_text,
        })
        if generate_response.status_code != 200:
            raise HTTPException(status_code=500, detail="응답 생성 실패")
        response_text = generate_response.json().get("response_text")
        raw_service_ids = generate_response.json().get("service_ids")
        service_ids = list(set(raw_service_ids))

        logger.info(f"응답 생성 완료: message_id={message_id}")
        return {"message_id": message_id, "response_text": response_text, "session_id": request.session_id, "service_ids": service_ids}

    except Exception as e:
        logger.error(f"질문-응답 처리 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="질문 응답 처리 중 오류 발생")