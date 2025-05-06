#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Create test database if it doesn't exist
echo "Preparing test database..."
PGPASSWORD=${POSTGRES_PASSWORD} psql -h db -U ${POSTGRES_USER} -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'licitacao_hub'" | grep -q 1 || \
PGPASSWORD=${POSTGRES_PASSWORD} psql -h db -U ${POSTGRES_USER} -d postgres -c "CREATE DATABASE licitacao_hub"
echo "Test database ready!"

# Run migrations on test database
echo "Running migrations on test database..."
alembic upgrade head

# Run tests
exec "$@"