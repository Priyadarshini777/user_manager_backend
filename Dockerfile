# Stage 1: build/install dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# system deps for some packages (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Install into a target directory to keep runtime image lean
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: final runtime image
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r app && useradd -r -g app app \
 && mkdir -p /app && chown app:app /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy app source
COPY ./app ./app
COPY ./tests ./tests
COPY ./requirements.txt ./

# Expose port and run as non-root user
EXPOSE 8000
USER app

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
