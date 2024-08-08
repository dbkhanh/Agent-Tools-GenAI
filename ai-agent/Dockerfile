# Dockerfile for Uvicorn with FastAPI
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000"]
