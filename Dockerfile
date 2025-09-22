# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY healthcheck.py .

# Make the script executable
RUN chmod +x healthcheck.py

# Set the entrypoint to run your script
# This allows you to pass arguments like --url when you run the container
ENTRYPOINT ["python", "./healthcheck.py"]