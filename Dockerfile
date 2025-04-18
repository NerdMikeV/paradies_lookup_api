FROM python:3.11-buster

ENV ACCEPT_EULA=Y

# Install Microsoft SQL Server ODBC driver and build dependencies
RUN apt-get update && \
    apt-get install -y \
        curl \
        gnupg \
        unixodbc \
        unixodbc-dev \
        gcc \
        g++ \
        apt-transport-https \
        ca-certificates && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
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

# Expose and launch
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]






