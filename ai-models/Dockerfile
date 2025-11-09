FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directories
RUN mkdir -p data/input data/output

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "measurement_model.api:app", "--host", "0.0.0.0", "--port", "8000"]
