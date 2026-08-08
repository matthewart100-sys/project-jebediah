FROM python:3.12-slim

WORKDIR /app

# Scanned PDFs are first-class organizational evidence. OCR remains entirely
# local to the governed interaction container.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY services/jebediah-interaction/requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY services/jebediah-interaction/app ./app

EXPOSE 8001

CMD ["python", "-m", "app.ocr_server"]
