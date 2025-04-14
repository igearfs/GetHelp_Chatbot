FROM python:3.11-slim

# Environment hardening
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    OLLAMA_MODELS=/root/.ollama/models

WORKDIR /project

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    build-essential \
    gcc \
    g++ \
    git \
    poppler-utils \
    libreoffice \
    unzip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    screen \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy necessary files and folders
COPY app.py .
COPY llm_indexer.py .
COPY llm_loader.py .
COPY requirements.txt .
COPY data ./data
COPY docs ./docs
COPY sql ./sql

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Ollama CLI and pull the mistral model
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose Streamlit port
EXPOSE 8501

# Define entrypoint script and make it executable
COPY ./docker/start.sh ./start.sh
RUN chmod +x ./start.sh

# CMD to start the app
CMD ["./start.sh"]
