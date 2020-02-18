FROM python:3

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api/
COPY app.py ./
COPY worker.py ./

