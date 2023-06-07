# Use an official Python runtime as the base image
FROM python:3.9
# Set the working directory in the container
WORKDIR /app
# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk-headless && \
    apt-get clean
# Set the Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# Install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the code files to the working directory
COPY . .
# Expose the port used by your application (if applicable)
# EXPOSE 6379
# Run the Python script when the container starts
CMD ["python", "spark.py"]