FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API logic
COPY main.py .

# Expose the port Uvicorn runs on
EXPOSE 8000

# Boot the engine
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
