#!/bin/bash

# Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker ps -a | grep streamlit-app | awk '{print $1}' | xargs -r docker stop
docker ps -a | grep streamlit-app | awk '{print $1}' | xargs -r docker rm

# Remove existing image
echo "Removing existing image..."
docker rmi -f streamlit-app

# Clean up any unused images and volumes
echo "Cleaning up unused resources..."
docker system prune -f
docker volume prune -f

# Build new image with no cache
echo "Building new image..."
docker build --no-cache -t streamlit-app .

# Run new container with proper volume mounting
echo "Running new container..."
docker run -d \
    -p 8501:8501 \
    --name streamlit-app \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/.streamlit:/app/.streamlit \
    --restart unless-stopped \
    streamlit-app

# Check if container is running
echo "Checking container status..."
docker ps | grep streamlit-app

# Display logs
echo "Container logs:"
docker logs streamlit-app

echo "Done! The application should be available at http://localhost:8501" 