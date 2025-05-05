# =====================================
# Estágio de construção
# Build stage
# =====================================
FROM python:3.12-slim AS builder

# Configurar variáveis de ambiente para Python
# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Instalar poetry
# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Configurar diretório de trabalho
# Set working directory
WORKDIR /app

# Copiar arquivos de configuração do Poetry
# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Instalar dependências sem desenvolvimento
# Install dependencies without development
RUN poetry install --no-dev --no-root

# =====================================
# Estágio final
# Final stage
# =====================================
FROM python:3.12-slim

# Configurar variáveis de ambiente para Python
# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Criar usuário não-root
# Create non-root user
RUN addgroup --system app && \
    adduser --system --group app

# Configurar diretório de trabalho
# Set working directory
WORKDIR /app

# Criar e configurar diretórios de upload
# Create and configure upload directories
RUN mkdir -p /app/uploads && \
    chown -R app:app /app/uploads

# Copiar dependências do estágio de construção
# Copy dependencies from build stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
# Copy application code
COPY --chown=app:app ./app /app/app
COPY --chown=app:app ./alembic /app/alembic
COPY --chown=app:app ./alembic.ini /app/

# Definir usuário não-root
# Set non-root user
USER app

# Expor porta
# Expose port
EXPOSE 8000

# Comando para executar a aplicação
# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]