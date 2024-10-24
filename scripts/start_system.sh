#!/bin/bash

# Check if backend directory exists. Exit with an error if not.
if [ ! -d "./backend" ]; then
  echo "Error: Backend directory './backend' not found."
  exit 1
fi

# Check if frontend directory exists. Exit with an error if not.
if [ ! -d "./frontend" ]; then
  echo "Error: Frontend directory './frontend' not found."
  exit 1
fi

# Check if requirements.txt exists in backend
if [ ! -f "./backend/requirements.txt" ]; then
  echo "Error: 'requirements.txt' not found in './backend'."
  exit 1
fi


echo "Checking backend requirements..."

# Check if the package 'uvicorn' is installed (example). Adjust as needed.
if ! pip3 show uvicorn > /dev/null 2>&1; then
    echo "Installing backend requirements..."
    cd ./backend
    pip3 install -r requirements.txt
    cd ..
else
    echo "Backend requirements already installed."
fi


echo "Starting backend server..."
cd ./backend/app
bash start_be.sh

# Go back to root
cd ../../


echo "Starting frontend server..."
cd ./frontend

# Check if requirements.txt exists in frontend
if [ ! -f "./frontend/requirements.txt" ]; then
  echo "Error: 'requirements.txt' not found in './frontend'."
  exit 1
fi


bash start_be.sh
cd ../

echo "Backend and frontend servers started successfully."