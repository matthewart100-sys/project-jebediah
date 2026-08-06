FROM python:3.12-slim

WORKDIR /app

COPY services/jebediah-interaction/requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY services/jebediah-interaction/app ./app

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
