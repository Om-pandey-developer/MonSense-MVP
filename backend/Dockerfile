# MonSense Backend Dockerfile
# — Ananya Deshmukh (DevOps & Cloud Infrastructure Engineer)

FROM python:3.11-slim

WORKDIR /app

# System dependencies for geospatial libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
