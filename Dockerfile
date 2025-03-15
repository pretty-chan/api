FROM python:3.12.2-slim-bookworm AS builder

# Set environment variables for better performance and error visibility
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.4

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    libffi-dev \
    build-essential \
    pkg-config \
    libssl-dev \
    libc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy dependency files before installation
COPY poetry.lock pyproject.toml /app/

# Use the correct Poetry install syntax (since --no-dev is deprecated)
RUN poetry install --only main --no-interaction --no-ansi

# Start building the final production image
FROM python:3.12.2-slim-bookworm

# Set runtime environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

# Install runtime dependencies (minimal install for production)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy built dependencies from builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Copy application source code
COPY . /app

# Set entry point
CMD ["python", "-m", "app"]