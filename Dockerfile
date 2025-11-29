FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Copy the Django project and install dependencies
COPY requirements.txt /app/

# Run this command to install all dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Schedule health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 CMD ["curl", "--silent", "--fail", "http://localhost:8000/health/"]

# Run server
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
CMD ["--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
