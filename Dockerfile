FROM python:3.12.12 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.12.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Run the API using uvicorn on port 8000
CMD ["/app/.venv/bin/uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
