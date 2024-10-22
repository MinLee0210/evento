#!/bin/sh

# Update environment
apt-get update

apt-get install unzip

# Install virtual environment
apt install python3.10-venv
python3 -m venv evento_be
source evento_be/bin/activate

# Move to db 
cd db/
python3 -m pip install -U pip
python3 -m pip install gdown
bash download_file_from_gdrive.sh
echo "Finish setting up db" 
cd ../


# Run backend
echo "Moving to backend and install requirements"
python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
python3 -m pip install -r requirements.txt

echo "Moving to app and run the app"
pwd
cd ./app
# Assuming uvicorn requires typing_extensions (modify if not)
if [ -n "$VIRTUAL_ENV" ]; then
  # Use uvicorn within virtual environment (if activated)
  uvicorn main:app --host=0.0.0.0 --port=8080 --reload
else
  # Use uvicorn outside virtual environment
  python3 -m uvicorn main:app --host=0.0.0.0 --port=8080 --reload --workers=4
fi

