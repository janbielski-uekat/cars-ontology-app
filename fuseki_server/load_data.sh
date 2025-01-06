#!/bin/sh

# Start Fuseki server in the background
java -jar fuseki-server.jar &

# Capture the PID of the background process
FUSEKI_PID=$!

# Delete any existing dataset
 curl -X DELETE http://localhost:3030/$/datasets/cars-ontology

# Create a new dataset
curl -X POST --header "Content-Type: application/x-www-form-urlencoded" \
     --data "dbName=cars-ontology&dbType=tdb" \
     http://localhost:3030/$/datasets

# Load the ontology data into the new dataset
curl -X POST --data-binary @/fuseki/cars_ont.ttl \
     --header "Content-Type: text/turtle" \
     http://localhost:3030/cars-ontology/data

# Wait for the Fuseki server process to complete
wait $FUSEKI_PID