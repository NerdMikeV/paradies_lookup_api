# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system packages
RUN apt-get update && \
    apt-get install -y \
        curl \
        gnupg \
        gnupg2 \
        unixodbc \
        unixodbc-dev \
        gcc \
        g++ \
        apt-transport-https \
        ca-certificates && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl -sSL https://packages.microsoft.com/config/debian/11/prod.list -o /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run the app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]


