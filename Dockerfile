# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the contents of the local app directory into the container at /app
COPY ./app/ .

# Install the requests library, which is needed for the HTTP GET request
RUN pip install requests

# Run healthcheck.py when the container launches
CMD ["python", "healthcheck.py"]