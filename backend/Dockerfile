FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY backend /app/backend
COPY agents /app/agents
COPY rag /app/rag
COPY kafka /app/kafka
COPY ingestion /app/ingestion
COPY scripts /app/scripts

RUN groupadd --system app && useradd --system --gid app --create-home app \
    && mkdir -p /app/data /app/data_source \
    && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
