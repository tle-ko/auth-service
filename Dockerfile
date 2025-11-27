FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project and install dependencies
COPY requirements.txt /app/

# Run this command to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Schedule health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 CMD ["curl", "--silent", "http://localhost:8000/health/"]

# Run server
RUN /app/manage.py migrate --no-input
ENTRYPOINT ["gunicorn", "app.wsgi:application"]
CMD ["--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
