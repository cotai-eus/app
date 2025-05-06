#!/bin/bash
set -e

# Create and set permissions for poetry cache
mkdir -p /tmp/poetry_cache
chmod -R 777 /tmp/poetry_cache
mkdir -p /app/.venv
chmod -R 777 /app/.venv

exec "$@"