# Use a full base image (not slim) to reduce dependency issues
FROM python:3.11-bullseye

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y \
        curl \
        gnupg2 \
        unixodbc \
        unixodbc-dev \
        gcc \
        g++ \
        apt-transport-https \
        ca-certificates \
        libssl1.1 || true

# Add Microsoft package signing key and repository
RUN curl -sSL https://packages.microsoft.com/config/debian/11/prod.list -o /etc/apt/sources.list.d/mssql-release.list && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg

# Install the ODBC driver
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]



