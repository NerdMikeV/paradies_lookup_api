# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies for pyodbc and SQL Server ODBC driver
RUN apt-get update && \
    apt-get install -y curl gnupg unixodbc unixodbc-dev gcc g++ && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the app port
EXPOSE 8080

# Run the app with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
