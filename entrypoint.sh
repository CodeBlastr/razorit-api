#!/bin/sh

# Load environment variables from the ECS Task Definition
if [ -f /app/.env ]; then
    echo "🔍 Loading environment variables from .env file"
    export $(cat /app/.env | xargs)
fi

echo "🔹 Environment Variables:"
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_NAME: $DB_NAME"
echo "DB_USER: $DB_USER"

# Check if DB_HOST is missing
if [ -z "$DB_HOST" ]; then
  echo "❌ ERROR: DB_HOST is not set! Exiting..."
  exit 1
fi

echo "⏳ Waiting for database to be ready..."
until nc -z -v -w30 "$DB_HOST" "$DB_PORT"; do
  echo "⌛ Waiting for database connection..."
  sleep 5
done

echo "✅ Database is ready! Running migrations and seeds..."
alembic upgrade head || { echo "❌ Migration failed!"; exit 1; }
python seed.py || { echo "❌ Seeding failed!"; exit 1; }

echo "🚀 Starting API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
