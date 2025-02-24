FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script separately before the rest
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the FastAPI application
COPY . .

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Expose port 8000
EXPOSE 8000

# Command to run migrations before starting the app
CMD ["sh", "-c", "alembic upgrade head && python seed.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
