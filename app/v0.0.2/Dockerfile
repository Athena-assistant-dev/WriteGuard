# WriteGuard v0.0.2 Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask python-dotenv pyyaml redbaron jsonpatch pillow python-docx python-pptx openpyxl ruamel.yaml

EXPOSE 5050

CMD ["python", "writeguard_api.py"]