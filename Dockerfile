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

# Ensure shell scripts are executable
RUN chmod +x /app/healthcheck.sh /app/entrypoint.sh

# Run the server
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 CMD [ "/app/healthcheck.sh" ]
ENTRYPOINT ["./entrypoint.sh"]
