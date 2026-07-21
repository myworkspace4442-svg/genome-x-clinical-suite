# Multi-stage Dockerfile
FROM python:3.10-slim AS builder

# BWA & SAMtools + dependencies သွင်းခြင်း
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    bwa \
    samtools \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x pipeline.sh

EXPOSE 8501
CMD ["streamlit", "run", "app/main_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]