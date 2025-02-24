#!/bin/sh

echo "Waiting for database to be ready..."
until nc -z -v -w30 $DB_HOST $DB_PORT
do
  echo "Waiting for database connection..."
  sleep 5
done

echo "Database is ready! Running migrations and seeds..."
alembic upgrade head
python seed.py

echo "Starting API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
