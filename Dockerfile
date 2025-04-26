FROM python:3.11-slim

WORKDIR /app

# 1️⃣ сначала зависимости – кэш слоёв
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2️⃣ теперь весь исходный код
COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
