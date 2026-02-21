FROM python:3.12-slim-trixie

WORKDIR /app

COPY . . 

CMD ["uvicorn", "main:app", "--reload", "--host"," 0.0.0.0", "--port", "8000"]
