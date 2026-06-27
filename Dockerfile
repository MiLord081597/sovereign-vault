# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the headless daemon script into the container
COPY baxter_daemon.py .

# Command to execute when the container spins up
CMD ["python", "baxter_daemon.py"]
