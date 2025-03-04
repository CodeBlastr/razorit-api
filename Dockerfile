FROM python:3.11

# Set the working directory
WORKDIR /app

# Install netcat-openbsd for DB connection check
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application files
COPY . .

# Explicitly copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Expose port 8000
EXPOSE 8000

# Use environment variables from ECS at runtime
CMD ["sh", "-c", "alembic upgrade head && python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
