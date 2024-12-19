# Use the latest Ubuntu image
FROM ubuntu:latest

# Install Python and necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    openssl \
    wget

# Create a working directory
WORKDIR /app

# Copy the server, client, and HTML files into the container
COPY server.py /app/server.py
COPY client.py /app/client.py
COPY index.html /app/index.html

# Install Python packages
RUN pip3 install cryptography

# Generate self-signed SSL certificates
RUN mkdir /app/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /app/certs/server.key -out /app/certs/server.crt -subj "/CN=localhost"

# Run the server
CMD ["python3", "/app/server.py"]