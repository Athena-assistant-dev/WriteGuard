# WriteGuard v0.0.2 Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install --no-cache-dir flask python-dotenv pyyaml redbaron jsonpatch pillow python-docx python-pptx openpyxl ruamel.yaml pytz pytesseract prance fpdf beautifulsoup4 toml PyMuPDF openapi-schema-validator psycopg2-binary SQLAlchemy pgvector sentence-transformers

EXPOSE 5050

CMD ["python", "writeguard_api.py"]