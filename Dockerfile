# Build stage
FROM python:3.11-slim AS build

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# copy only files needed for pip install first for caching
COPY pyproject.toml requirements.txt ./

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential git curl \
  && pip install --upgrade pip setuptools wheel \
  && pip install -r requirements.txt \
  && apt-get purge -y --auto-remove build-essential

# Copy the rest of the source
COPY . .

# Production stage
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# create a non-root user
RUN useradd --create-home appuser
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app

RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Use uvicorn as the entrypoint
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
