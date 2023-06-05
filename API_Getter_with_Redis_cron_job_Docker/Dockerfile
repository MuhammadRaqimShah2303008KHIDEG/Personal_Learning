# # Use a base image with Python pre-installed
# FROM python:3.9

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements.txt file to the container
# COPY requirements.txt .
# COPY log_file.log .

# # Install the required packages
# RUN pip install --no-cache-dir -r requirements.txt

# # Install cron
# RUN apt-get update && apt-get install cron -y

# # Copy the application code to the container
# COPY . /app

# # Expose the port used by the FastAPI application
# EXPOSE 8000

# # Add the cron job command
# RUN echo "* * * * * python3 /app/main.py >> /log_file.log 2>&1" >> /etc/crontab

# # Give execution rights to the cron job
# RUN chmod 0644 /etc/cron.d/myapi-cron
# # Apply the cron job
# RUN crontab /etc/cron.d/myapi-cron

# # Run the cron daemon and the FastAPI application
# CMD (cron -f &) && uvicorn main:app --host 0.0.0.0 --port 8000

# Use a base image with Python pre-installed
FROM python:3.9
# Set the working directory in the container
WORKDIR /app
# Copy the requirements.txt file to the container
COPY requirements.txt .
# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code to the container
COPY . /app
RUN apt-get update && apt-get install -y cron
# Add the cron job command
RUN echo "* * * * * python3 /app/main.py >> /log_file.log 2>&1" > /etc/cron.d/myapi-cron
# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/myapi-cron
# Apply the cron job
RUN crontab /etc/cron.d/myapi-cron
# Expose the port used by the FastAPI application
EXPOSE 8000
# Run the cron daemon and the FastAPI application
CMD cron && uvicorn main:app --host 0.0.0.0 --port 8000