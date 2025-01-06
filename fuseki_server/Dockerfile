# Dockerfile for Fuseki server
FROM openjdk:17-slim

# Set work directory
WORKDIR /fuseki

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy Fuseki server files
COPY . /fuseki/

# Copy the ontology file and the load script
COPY ./cars_ont.ttl /fuseki/cars_ont.ttl
COPY load_data.sh /fuseki/load_data.sh

# Make the script executable
RUN chmod +x /fuseki/load_data.sh

# Expose port
EXPOSE 3030

# Run the load script
CMD ["/fuseki/load_data.sh"]