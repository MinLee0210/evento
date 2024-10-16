#!/bin/sh


# Run backend
echo "Moving to backend and install requirements"
# python3 -m pip install -r requirements.txt --no-cache-dir
# cd ../

echo "Moving to app and run the app"
# cd ./backend/app
pwd
cd ./app
# Assuming uvicorn requires typing_extensions (modify if not)
if [ -n "$VIRTUAL_ENV" ]; then
  # Use uvicorn within virtual environment (if activated)
  uvicorn main:app --host=0.0.0.0 --port=8080 --reload
else
  # Use uvicorn outside virtual environment
  python -m uvicorn main:app --host=0.0.0.0 --port=8080 --reload
fi