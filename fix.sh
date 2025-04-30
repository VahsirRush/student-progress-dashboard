#!/bin/bash

# Kill any existing Streamlit processes
echo "Killing any existing Streamlit processes..."
pkill -f streamlit

# Stop and remove ALL existing containers
echo "Stopping and removing ALL existing containers..."
docker stop $(docker ps -a -q) 2>/dev/null || true
docker rm $(docker ps -a -q) 2>/dev/null || true

# Remove ALL existing images
echo "Removing ALL existing images..."
docker rmi $(docker images -q) -f 2>/dev/null || true

# Build new image
echo "Building new image..."
docker build -t student-dashboard .

# Run new container
echo "Running new container..."
docker run -d -p 8501:8501 --name student-dashboard student-dashboard

# Check if container is running
echo "Checking container status..."
docker ps | grep student-dashboard

echo "Done! The application should be available at http://localhost:8501" 