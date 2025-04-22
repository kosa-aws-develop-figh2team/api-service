# 🐍 1. Python 슬림 이미지 기반
FROM python:3.11-slim

# 🛠️ 2. 시스템 패키지 설치 (옵션: SSL, 압축 등)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 🗂️ 3. 작업 디렉토리 설정
WORKDIR /app

# 📦 4. 소스 복사
COPY main.py /app
COPY requirements.txt /app

# 📦 5. 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 🔓 6. 포트 개방
EXPOSE 5200

# 🚀 7. FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5200"]