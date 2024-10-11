#!/bin/sh

echo "Cleaning Docker environment..."
docker system prune -af --volumes || echo "Error cleaning Docker environment."
echo "Docker environment cleaned."