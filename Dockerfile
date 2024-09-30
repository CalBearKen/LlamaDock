# Use an official Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl ca-certificates build-essential libssl-dev libffi-dev python3 python3-pip supervisor

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies (Flask and requests)
RUN pip3 install Flask requests

# Expose the necessary ports (Ollama and Flask API)
EXPOSE 11434
EXPOSE 5001

# Copy the Python API files and startup script
COPY start-ollama.sh /app/start-ollama.sh
COPY API.py /app/API.py

# Make the startup script executable
RUN chmod +x /app/start-ollama.sh

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord to start both the Ollama server and the Flask API
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
