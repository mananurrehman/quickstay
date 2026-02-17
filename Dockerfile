# ==================== STAGE 1: BUILDER ====================
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==================== STAGE 2: PRODUCTION ====================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN groupadd -r quickstay && useradd -r -g quickstay -d /app quickstay

COPY . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

RUN mkdir -p /app/app/static/images/rooms/uploads \
    && chown -R quickstay:quickstay /app

USER quickstay

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Use entrypoint instead of CMD
ENTRYPOINT ["/app/entrypoint.sh"]