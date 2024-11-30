# Use a Python base image
FROM python:3.9-slim

# Install dependencies
RUN pip install requests

# Copy the script into the image
COPY poller.py /app/poller.py

# Set the working directory
WORKDIR /app

# Set the entrypoint
ENTRYPOINT ["python", "poller.py"]