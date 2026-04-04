FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install CPU-only PyTorch first (much smaller image, avoids CUDA download)
RUN pip install --no-cache-dir \
    torch>=2.1.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and model source
COPY backend/ ./backend/
COPY model/ ./model/

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
