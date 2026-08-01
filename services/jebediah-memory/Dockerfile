FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv==0.11.32

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN uv sync --frozen --no-dev --group service --no-editable

ENV PATH="/app/.venv/bin:$PATH"

COPY services/jebediah-memory/app/main.py ./main.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
