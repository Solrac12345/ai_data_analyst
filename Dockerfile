# EN: Multi-stage build for production-grade image / FR: Build multi-étapes pour une image de production

# --- Stage 1: Builder (for testing & development) ---
FROM python:3.11-slim AS builder

WORKDIR /app

# EN: Install system dependencies needed for building Python packages / FR: Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# EN: Copy dependency file first to leverage Docker cache / FR: Copier uniquement le fichier de dépendances pour le cache
COPY pyproject.toml .

# EN: Install all dependencies (including dev) for testing / FR: Installer toutes les dépendances (y compris dev) pour les tests
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ".[dev]"

# EN: Copy source code so tests can import modules / FR: Copier le code source pour que les tests puissent importer les modules
COPY src/ ./src/
COPY config/ ./config/
COPY test/ ./test/

# --- Stage 2: Runtime (production) ---
FROM python:3.11-slim AS runtime

# EN: Copy the installed packages from builder / FR: Copier les packages installés
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

# EN: Create a non-root user for security / FR: Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# EN: Copy application code / FR: Copier le code de l'application
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser config/ ./config/

# EN: Switch to non-root user / FR: Basculer vers l'utilisateur non-root
USER appuser

# EN: Set environment variables / FR: Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# EN: Default entrypoint to the CLI / FR: Point d'entrée par défaut vers le CLI
ENTRYPOINT ["python", "-m", "src.cli.main"]
CMD ["--help"]