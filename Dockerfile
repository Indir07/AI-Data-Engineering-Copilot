# syntax=docker/dockerfile:1
# ---------------------------------------------------------------------------
# Single image used by both the API and the UI services (they differ only by
# the command they run). Kept simple and reproducible; the same image is what a
# cluster would run (ADR-0006).
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps: build tools for wheels, curl for healthchecks.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better layer caching.
COPY requirements/base.txt requirements/base.txt
RUN pip install --upgrade pip && pip install -r requirements/base.txt

# Install the application package.
COPY pyproject.toml README.md ./
COPY src ./src
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini
RUN pip install -e .

# Entrypoint runs DB migrations (when RUN_MIGRATIONS=1) then execs the command.
COPY deploy/docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create writable data dir for chroma / uploads / sqlite.
RUN mkdir -p /app/data/chroma /app/data/uploads

EXPOSE 8000 8501

ENTRYPOINT ["entrypoint.sh"]
# Default command = API. The UI service overrides this in docker-compose.yml.
CMD ["uvicorn", "copilot.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
