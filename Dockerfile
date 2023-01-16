# Use an official Python runtime as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /shadow-app

# Copy the requirements file into the container
COPY requirements.txt *.py.

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port for the application to run on
EXPOSE 5000

# Run the command to start the application
CMD ["python", "shadow_api.py"]
