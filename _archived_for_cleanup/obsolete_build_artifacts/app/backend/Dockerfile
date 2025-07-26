FROM python:3.11-slim

# Educational AI metadata
LABEL name="SIRAJ Educational AI Backend"
LABEL version="8.1.0"
LABEL description="Multi-perspective AI tutoring system powered by Gemma 3n"
LABEL maintainer="SIRAJ Educational AI Team"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/education \
             /app/logs/education \
             /app/sessions \
             /app/static \
             /app/uploads

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV SIRAJ_MODE=educational
ENV SIRAJ_VERSION=8.1.0

# Create non-root user for security
RUN groupadd -r siraj && useradd -r -g siraj siraj
RUN chown -R siraj:siraj /app
USER siraj

# Health check for educational services
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose educational API port
EXPOSE 8000

# Run educational AI backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]