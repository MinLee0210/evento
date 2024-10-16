#!/bin/bash


# Check if keyframes.csv exists, skip download if found
if [ ! -f "keyframes.csv" ]; then
  echo "Downloading and extracting files .... "

  # Load the JSON file
  JSON_FILE="kaggle.json"
  if [ ! -f "$JSON_FILE" ]; then
    echo "Error: kaggle.json not found."
    exit 1
  fi

  # Load the JSON data and set the environment variables
  
  KAGGLE_USERNAME=$(jq -r '.username' "$JSON_FILE")
  KAGGLE_KEY=$(jq -r '.key' "$JSON_FILE")

  echo $KAGGLE_USERNAME
  echo $KAGGLE_KEY

  # Install `kaggle` Python SDK
  python -m pip install kaggle || {
    echo "Error installing kaggle SDK. Check your pip installation."
    exit 1
  }

  read -p "Please enter Kaggle's dataset path" data_path
  # Download dataset
  kaggle datasets download $data_path --path ./ --unzip || {
    echo "Error downloading dataset. Check your kaggle credentials and network connection."
    exit 1
  }

  # Find all files ending with .zip
  zip_files=$(find . -name "*.zip")

  # Loop through the found zip files and remove them.  Crucially, handle the case where no zip files are found.
  if [[ -n "$zip_files" ]]; then
    for file in $zip_files; do
      rm "$file"
    done
  else
    echo "No .zip files found in the current directory." >&2  # Use >&2 for error output
  fi

  # Uninstall kaggle SDK
  python -m pip uninstall kaggle || {
    echo "Error uninstalling kaggle SDK. Check your pip installation."
    exit 1
  }
fi