FROM python:3.12-slim

# Setting environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV ALEMBIC_CONFIG=/app/alembic.ini
ENV PATH="/app/.venv/bin:$PATH"

# Installing dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN python -m pip install --upgrade pip && \
    pip install uv

# Copy dependency files
COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

# Selecting a working directory
WORKDIR /app

# Install dependencies with uv
RUN uv sync --frozen --no-dev

# Copy the source code
COPY ./src /app/src
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

# Copy commands
COPY ./commands /commands

# Ensure Unix-style line endings for scripts
RUN dos2unix /commands/*.sh

# Add execute bit to commands files
RUN chmod +x /commands/*.sh
