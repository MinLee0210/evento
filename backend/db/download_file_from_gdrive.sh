#!/bin/sh

# Check if keyframes.csv exists, skip download if found
if [ ! -f "keyframes.csv" ]; then
  echo "Start downloading and extracting files .... "

  # Download dataset from Google Drive
  gdown --id 1uldiawgriu5JplvHn5Z1iXpNV_YHVG6p --output ./dataset.zip

  # Check if download was successful
  if [ $? -eq 0 ]; then
    # Extract dataset
    unzip ./dataset.zip
    
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

    echo "Done!"
  else
    echo "Download failed!"
    exit 1
  fi
else
  echo "Found keyframes.csv, skipping download."
fi