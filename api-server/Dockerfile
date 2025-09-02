# ベース
FROM python:3.11-slim

WORKDIR /app

# 依存を先に入れる（キャッシュを効かせる）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY app ./app

# FastAPI を起動（本番はgunicorn/uvicorn worker構成でもOK）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
