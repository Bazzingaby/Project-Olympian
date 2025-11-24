FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies for OpenCV and MoviePy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Start Celery worker
CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]
