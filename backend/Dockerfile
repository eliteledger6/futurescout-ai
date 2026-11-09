# FUTURESCOUT AI backend (FastAPI). Build from the repo root:  docker build -f backend/Dockerfile -t futurescout-api backend
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml README.md* ./
COPY app ./app
COPY config ./config
COPY scripts ./scripts
COPY migrations ./migrations
COPY alembic.ini ./
COPY samples ./samples
RUN pip install --no-cache-dir -e .
# Keys come from the environment (docker compose reads ../.env); never bake them into the image.
EXPOSE 8000
CMD ["python", "scripts/serve.py", "--host", "0.0.0.0", "--port", "8000"]
