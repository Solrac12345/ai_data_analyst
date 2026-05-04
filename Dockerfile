# EN: Multi-stage build for production-grade image / FR: Build multi-étapes pour une image de production

# --- Stage 1: Builder (for testing & development) ---
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir ".[dev]"

COPY src/ ./src/
COPY config/ ./config/
COPY test/ ./test/

# --- Stage 2: Runtime (production) ---
FROM python:3.11-slim AS runtime

WORKDIR /app

# EN: Create non-root user explicitly / FR: Créer l'utilisateur non-root de manière explicite
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# EN: Copy dependencies & application code / FR: Copier les dépendances et le code applicatif
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser config/ ./config/

# EN: Ensure correct ownership / FR: Assurer la propriété correcte
RUN chown -R appuser:appuser /app

# EN: Switch to non-root user / FR: Basculer vers l'utilisateur non-root
USER appuser

ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app
ENTRYPOINT ["python", "-m", "src.cli.main"]
CMD ["--help"]