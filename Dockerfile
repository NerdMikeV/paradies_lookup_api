FROM python:3.11-slim

# Environment for Microsoft EULA
ENV ACCEPT_EULA=Y

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gnupg2 \
        ca-certificates \
        apt-transport-https \
        unixodbc \
        unixodbc-dev \
        gcc \
        g++ \
        libgssapi-krb5-2 && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null && \
    curl -sSL https://packages.microsoft.com/config/debian/11/prod.list -o /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files and install Python packages
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask app
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]





