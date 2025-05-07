#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Preparing test database..."
# First connect to default postgres database to create the test database
psql -h db -U postgres -c "DROP DATABASE IF EXISTS test_db;"
psql -h db -U postgres -c "CREATE DATABASE test_db OWNER postgres;"
echo "Test database ready!"

echo "Running migrations on test database..."
alembic upgrade heads

# Run the tests
pytest "$@"

# Optionally clean up after tests
# psql -h db -U postgres -c "DROP DATABASE test_db;"