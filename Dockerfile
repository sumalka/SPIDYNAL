# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy your project files
COPY . .

# Install dependencies
RUN pip install pygame colorama termcolor speedtest-cli psutil

# Command to run your script with inputs
ENTRYPOINT ["python", "spidy.py"]
