# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 (Flask's default port)
EXPOSE 5000

# Set the APP_VERSION environment variable (can be overridden at runtime)
ENV APP_VERSION=1.0.0

# Run the application using Gunicorn
# 0.0.0.0 makes the server accessible from outside the container
# --timeout 120 (optional) can be added if requests are expected to take longer
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
