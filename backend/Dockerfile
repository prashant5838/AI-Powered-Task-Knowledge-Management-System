FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc \
    && pip install --upgrade pip wheel setuptools \
    && pip install -r requirements.txt \
    && apt-get remove -y build-essential gcc && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
COPY . /app
ENV PYTHONPATH=/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
