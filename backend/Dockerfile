FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend
COPY agents /app/agents
COPY rag /app/rag
COPY kafka /app/kafka
COPY ingestion /app/ingestion
COPY scripts /app/scripts
COPY conftest.py /app/conftest.py

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
