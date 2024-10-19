#!/bin/sh

# Update environment
apt-get update
apt install python3.10-venv

# Install virtual environment
python3 -m venv evento_fe
source evento_fe/bin/activate

echo "Moving to frontend and install requirements"
python3 -m pip install -r requirements.txt

echo "Moving to app and run the app"
# Assuming uvicorn requires typing_extensions (modify if not)
if [ -n "$VIRTUAL_ENV" ]; then
  # Use streamlit within virtual environment (if activated)
  streamlit run app.py
else
  # Use streamlit outside virtual environment
  python -m streamlit run app.py
fi