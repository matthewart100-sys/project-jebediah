FROM python:3.12-slim

WORKDIR /app

# Scanned PDFs are first-class organizational evidence.  Keep OCR local to the
# governed interaction container so document contents never leave the homelab.
# Poppler rasterizes PDF pages and Tesseract performs OCR.  --no-install-recommends
# keeps the production image bounded.
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

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
