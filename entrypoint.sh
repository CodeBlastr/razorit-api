#!/bin/sh

# Load environment variables from the ECS Task Definition
if [ -f /app/.env ]; then
    echo "Loading environment variables from .env file"
    export $(cat /app/.env | xargs)
fi

echo "Environment Variables Loaded:"
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"

# Ensure critical environment variables are set
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
  echo "ERROR: Database environment variables are not set! Exiting..."
  exit 1
fi

echo "Waiting for database to be ready..."
until nc -z -v -w30 "$DB_HOST" "$DB_PORT"; do
  echo "⌛ Waiting for database connection..."
  sleep 5
done

echo "Database is ready! Running migrations..."
alembic upgrade head || { echo "Migration failed!"; exit 1; }

echo "🚀 Starting API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
