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

# Check if 'requirements.txt' already exists in backend, and install if needed
if [[ ! -f "./backend/requirements.txt" ]]; then
    echo "Error: requirements.txt not found in backend folder."
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
# Use uvicorn within virtual environment (if activated). This is crucial.
if [ -n "$VIRTUAL_ENV" ]; then
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi

# Go back to root
cd ../../


echo "Starting frontend server..."
cd ./frontend

# Check for package.json
if [ ! -f ./package.json ]; then
    echo "Error: 'package.json' not found in frontend folder. Cannot start frontend."
    exit 1
fi

# Check node version
node_version=$(node -v 2>/dev/null)  # Suppress stderr, get version
if [[ "$node_version" == "" ]]; then
    echo "Error: Node.js is not installed or not in your PATH."
    exit 1
fi


# Check if the node version is greater than 18
node_version_parts=($(/usr/bin/node -p "process.versions.node"))
if [[ "${node_version_parts[0]}" -lt 18 ]]; then
    echo "Error: Node.js version must be 18 or greater. Your current version is ${node_version}."
    exit 1
fi


echo "Installing frontend dependencies..."
npm install || exit 1

echo "Starting frontend development server..."
npm run dev || exit 1  # Start frontend server (with error handling).


cd ..
echo "Backend and frontend servers started successfully."