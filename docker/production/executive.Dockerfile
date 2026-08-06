FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv==0.11.32

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY apps ./apps
COPY docker/production/executive_server.py ./docker/production/executive_server.py

RUN uv sync --frozen --no-dev --no-editable

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:/app/src"
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "docker/production/executive_server.py"]
