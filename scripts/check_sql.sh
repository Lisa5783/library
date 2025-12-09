#!/bin/bash
set -e

echo "Running SQL security & lint check via Docker..."

# Текущая директория — это корень репозитория (TeamCity так и делает)
# Монтируем её внутрь контейнера в /app
docker run --rm \
  -v "$PWD":/app \
  python:3.11-slim \
  bash -c "pip install --no-cache-dir sqlfluff && \
           sqlfluff lint /app/db_schema/*.sql"
