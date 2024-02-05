FROM python:3.10-slim

WORKDIR /app-backend

ENV PYTHONUNBUFFERED=1 \
		PYTHONDOWNTWRITEBYTECODE=1

COPY requirements.prod.txt /app-backend/

RUN apt-get update && \
    apt-get clean && \
		pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.prod.txt && \
		apt-get remove -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY . /app-backend/
